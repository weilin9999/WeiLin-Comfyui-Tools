import json
import time
import os
import asyncio
from io import BytesIO
from PIL import Image
import aiohttp

from .tag_image_manager import image_dir, thumb_dir, update_tag_image_path

THUMB_SIZE = (120, 120)
TIMEOUT_TOTAL = 300  # 5 minutes
POLL_INTERVAL = 2  # seconds between polls


def _comfyui_url():
    """Get ComfyUI's base URL. The plugin runs inside ComfyUI, so we use localhost."""
    port = os.environ.get("COMFYUI_PORT", "8188")
    return f"http://127.0.0.1:{port}"


def _get_checkpoints():
    """Scan ComfyUI's checkpoint directory. Falls back to hardcoded defaults."""
    import glob as _glob
    base = os.path.normpath(os.path.join(os.path.dirname(__file__), "../../../../../../models/checkpoints"))
    if not os.path.isdir(base):
        base = "models/checkpoints"
    files = _glob.glob(os.path.join(base, "**/*.safetensors"), recursive=True)
    files += _glob.glob(os.path.join(base, "**/*.ckpt"), recursive=True)
    result = []
    for f in files:
        name = os.path.relpath(f, base)
        result.append({"name": name, "path": name})
    return result


def _get_samplers():
    """Return KSampler sampler_name options."""
    return [
        "euler", "euler_ancestral", "heun", "heunpp2",
        "dpm_2", "dpm_2_ancestral", "lms", "dpm_fast",
        "dpm_adaptive", "dpmpp_2s_ancestral", "dpmpp_sde",
        "dpmpp_sde_gpu", "dpmpp_2m", "dpmpp_2m_sde",
        "dpmpp_2m_sde_gpu", "dpmpp_3m_sde", "dpmpp_3m_sde_gpu",
        "ddpm", "lcm", "ddim", "uni_pc", "uni_pc_bh2",
    ]


def get_generation_options():
    return {
        "checkpoints": _get_checkpoints(),
        "samplers": _get_samplers(),
        "sizes": [
            {"label": "512×512", "width": 512, "height": 512},
            {"label": "768×512", "width": 768, "height": 512},
            {"label": "512×768", "width": 512, "height": 768},
            {"label": "768×768", "width": 768, "height": 768},
            {"label": "1024×1024", "width": 1024, "height": 1024},
        ],
    }


def build_workflow(checkpoint, width, height, sampler_name, steps, cfg, seed, positive, negative):
    """Build a minimal txt2img ComfyUI workflow JSON (API format)."""
    import random as _random
    if seed is None or seed < 0:
        seed = _random.randint(0, 2**31 - 1)
    workflow = {
        "1": {
            "inputs": {"ckpt_name": checkpoint},
            "class_type": "CheckpointLoaderSimple",
        },
        "2": {
            "inputs": {"width": width, "height": height, "batch_size": 1},
            "class_type": "EmptyLatentImage",
        },
        "3": {
            "inputs": {
                "text": positive,
                "clip": ["1", 1],
            },
            "class_type": "CLIPTextEncode",
        },
        "4": {
            "inputs": {
                "text": negative,
                "clip": ["1", 1],
            },
            "class_type": "CLIPTextEncode",
        },
        "5": {
            "inputs": {
                "seed": seed,
                "steps": steps,
                "cfg": cfg,
                "sampler_name": sampler_name,
                "scheduler": "normal",
                "denoise": 1.0,
                "model": ["1", 0],
                "positive": ["3", 0],
                "negative": ["4", 0],
                "latent_image": ["2", 0],
            },
            "class_type": "KSampler",
        },
        "6": {
            "inputs": {
                "samples": ["5", 0],
                "vae": ["1", 2],
            },
            "class_type": "VAEDecode",
        },
        "7": {
            "inputs": {
                "images": ["6", 0],
            },
            "class_type": "PreviewImage",
        },
    }
    return workflow


async def submit_workflow(workflow):
    """Submit workflow to ComfyUI /api/prompt. Returns prompt_id."""
    url = f"{_comfyui_url()}/prompt"
    payload = {"prompt": workflow}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                raise RuntimeError(f"ComfyUI prompt submission failed: HTTP {resp.status}")
            data = await resp.json()
            if "prompt_id" not in data:
                raise RuntimeError(f"ComfyUI prompt response missing prompt_id: {data}")
            return data["prompt_id"]


async def poll_history(prompt_id, timeout=TIMEOUT_TOTAL):
    """Poll /api/history/{prompt_id} until the result is ready. Returns the history entry."""
    url = f"{_comfyui_url()}/history/{prompt_id}"
    start = time.time()
    async with aiohttp.ClientSession() as session:
        while time.time() - start < timeout:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                if resp.status != 200:
                    await asyncio.sleep(POLL_INTERVAL)
                    continue
                data = await resp.json()
                if prompt_id in data:
                    return data[prompt_id]
            await asyncio.sleep(POLL_INTERVAL)
    raise TimeoutError(f"Generation timed out after {timeout}s")


async def download_and_save_result(history_entry, t_uuid):
    """Download generated images from ComfyUI and save original + thumbnail."""
    outputs = history_entry.get("outputs", {})
    if "7" not in outputs:
        raise RuntimeError("No PreviewImage output in workflow result")

    images = outputs["7"].get("images", [])
    if not images:
        raise RuntimeError("No images in PreviewImage output")

    img_info = images[0]
    filename = img_info["filename"]
    subfolder = img_info.get("subfolder", "")
    img_type = img_info.get("type", "output")

    # Download from ComfyUI's /view endpoint
    if subfolder:
        view_url = f"{_comfyui_url()}/view?filename={filename}&subfolder={subfolder}&type={img_type}"
    else:
        view_url = f"{_comfyui_url()}/view?filename={filename}&type={img_type}"

    async with aiohttp.ClientSession() as session:
        async with session.get(view_url, timeout=aiohttp.ClientTimeout(total=30)) as resp:
            if resp.status != 200:
                raise RuntimeError(f"Failed to download image: HTTP {resp.status}")
            img_bytes = await resp.read()

    # Save original
    img_dir = image_dir()
    ext = os.path.splitext(filename)[1] or ".png"
    saved_name = f"{t_uuid}{ext}"
    saved_path = os.path.join(img_dir, saved_name)
    with open(saved_path, "wb") as f:
        f.write(img_bytes)

    # Generate thumbnail
    img = Image.open(BytesIO(img_bytes))
    img = img.convert("RGB")
    img.thumbnail(THUMB_SIZE, Image.LANCZOS)
    t_dir = thumb_dir()
    thumb_name = f"{t_uuid}.webp"
    thumb_path = os.path.join(t_dir, thumb_name)
    img.save(thumb_path, "WEBP", quality=80)

    # Update database with relative path
    rel_path = f"tag_images/{saved_name}"
    await update_tag_image_path(t_uuid, rel_path)

    return rel_path
