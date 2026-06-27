# Tag Preview Image — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add preview image display and one-click ComfyUI-powered image generation to tag management cards.

**Architecture:** Add `image_path`/`image_status` columns to `tag_tags` table. New backend modules: `tag_image_manager.py` (CRUD), `comfyui_workflow.py` (workflow builder + executor), `tag_image_queue.py` (asyncio queue + worker). Five new API routes on prompt_server.py. New frontend `GenerateImageDialog.vue` component. Modify `tag_index.vue` template to show thumbnails with hover overlay.

**Tech Stack:** Python (asyncio, aiohttp, PIL/Pillow), Vue 3 (Composition API), SQLite (aiosqlite)

---

## File Structure

**New files:**
- `app/server/prompt_api/tag_image_manager.py` — tag image CRUD functions
- `app/server/prompt_api/comfyui_workflow.py` — build workflow JSON, submit, poll, download result
- `app/server/prompt_api/tag_image_queue.py` — asyncio.Queue + single worker coroutine
- `src/src/view/tag_manager/components/GenerateImageDialog.vue` — generation config dialog

**Modified files:**
- `app/server/dao/dao.py` — schema migration v4: add `image_path`, `image_status` to `tag_tags`
- `app/server/prompt_api/tags_manager.py` — include `image_path`/`image_status`/`t_uuid` in `get_tag_tags` query
- `app/server/prompt_server.py` — add 5 new routes + static file serving for images/thumbs
- `src/src/view/tag_manager/tag_index.vue` — thumbnail area, hover overlay, generate button, status UI
- `src/src/api/tags.js` — add `generateTagImage`, `getTagImageStatus`, `getTagImageStatusByUuid`, `getGenerationOptions` methods

---

### Task 1: Database migration — add image columns to tag_tags

**Files:**
- Modify: `app/server/dao/dao.py`

- [ ] **Step 1: Add version 4 migration code**

In `dao.py`, find the `migrate_db` function. After the version 3 migration block (around line 478), add a version 4 migration block. Also update `create_tables` to include the new columns.

In `create_tables`, modify the `tag_tags` CREATE TABLE to add the new columns. Since SQLite's `CREATE TABLE IF NOT EXISTS` won't add columns to existing tables, we must use the migration for existing DBs and ALTER TABLE in the migration. For new DBs, add the columns in CREATE TABLE.

Find the `tag_tags` CREATE TABLE in `create_tables` (around line 213):

```python
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tag_tags (
        id_index INTEGER PRIMARY KEY AUTOINCREMENT,
        subgroup_id INTEGER,
        text TEXT,
        desc TEXT,
        color TEXT,
        create_time INTEGER,
        t_uuid TEXT(128),
        g_uuid TEXT(128)
    )
"""
)
```

Replace with:

```python
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS tag_tags (
        id_index INTEGER PRIMARY KEY AUTOINCREMENT,
        subgroup_id INTEGER,
        text TEXT,
        desc TEXT,
        color TEXT,
        create_time INTEGER,
        t_uuid TEXT(128),
        g_uuid TEXT(128),
        image_path TEXT,
        image_status TEXT
    )
"""
)
```

After the version 3 migration block (after `print("升级完成")` around line 478), add a version 4 migration block:

```python
# 添加版本4的迁移
if current_version < 4:
    print("检测到数据库版本变动 版本V4 正在升级中...")
    conn = sqlite3.connect(tags_db_path)
    cursor = conn.cursor()

    # 添加 image_path 和 image_status 列
    def add_column_if_not_exists(table, column, column_type):
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [info[1] for info in cursor.fetchall()]
        if column not in columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")

    add_column_if_not_exists("tag_tags", "image_path", "TEXT")
    add_column_if_not_exists("tag_tags", "image_status", "TEXT")

    update_version("tags", 4)
    conn.commit()
    conn.close()
    print("升级完成 V4")
```

Also update `get_current_version` to return 0 if no tags DB exists yet (it already does this via the try/except). The migration relies on `update_version` and `get_current_version` already being defined.

- [ ] **Step 2: Verify the migration**

Run a quick Python check to verify the schema:

```bash
cd "D:\game\SD_ComfyUI\ComfyUI-aki-v2\ComfyUI\custom_nodes\WeiLin-Comfyui-Tools" && python -c "
import sqlite3, os
tags_db = os.path.join('app', 'server', '..', '..', '..', 'user_data', 'userdatas_default_tags.db')
tags_db = os.path.normpath(os.path.join('app', 'server', 'dao', tags_db))
# Instead, call create_tables + migrate_db
from app.server.dao.dao import create_tables, migrate_db
create_tables()
migrate_db()
# Verify columns
conn = sqlite3.connect('user_data/userdatas_default_tags.db')
cursor = conn.cursor()
cursor.execute('PRAGMA table_info(tag_tags)')
cols = [c[1] for c in cursor.fetchall()]
print('Columns:', cols)
assert 'image_path' in cols
assert 'image_status' in cols
print('Migration V4 successful')
conn.close()
"
```

- [ ] **Step 3: Commit**

```bash
git add app/server/dao/dao.py
git commit -m "feat: add image_path and image_status columns to tag_tags (DB migration V4)"
```

---

### Task 2: Tag image CRUD functions

**Files:**
- Create: `app/server/prompt_api/tag_image_manager.py`

- [ ] **Step 1: Create the file with all CRUD functions**

```python
import os
from ..dao.dao import execute_query, fetch_one, fetch_all, tags_db_path


# Get the project root (ComfyUI-aki-v2/ComfyUI/custom_nodes/WeiLin-Comfyui-Tools)
def _get_user_data_dir():
    return os.path.normpath(os.path.join(os.path.dirname(tags_db_path), "."))


def _image_dir():
    d = os.path.join(_get_user_data_dir(), "tag_images")
    os.makedirs(d, exist_ok=True)
    return d


def _thumb_dir():
    d = os.path.join(_get_user_data_dir(), "tag_thumbs")
    os.makedirs(d, exist_ok=True)
    return d


async def update_tag_image_path(t_uuid, image_path):
    query = """
        UPDATE tag_tags
        SET image_path = ?, image_status = ?
        WHERE t_uuid = ?
    """
    await execute_query("tags", query, (image_path, "ready", t_uuid))


async def update_tag_image_status(t_uuid, status, image_path=None):
    if image_path is not None:
        query = """
            UPDATE tag_tags
            SET image_status = ?, image_path = ?
            WHERE t_uuid = ?
        """
        await execute_query("tags", query, (status, image_path, t_uuid))
    else:
        query = """
            UPDATE tag_tags
            SET image_status = ?
            WHERE t_uuid = ?
        """
        await execute_query("tags", query, (status, t_uuid))


async def get_tag_image_info(t_uuid):
    query = """
        SELECT image_path, image_status
        FROM tag_tags
        WHERE t_uuid = ?
    """
    row = await fetch_one("tags", query, (t_uuid,))
    if row:
        return {"image_path": row[0], "image_status": row[1]}
    return None


async def reset_pending_statuses():
    """Reset all pending/generating statuses to NULL on startup."""
    query = """
        UPDATE tag_tags
        SET image_status = NULL
        WHERE image_status IN ('pending', 'generating')
    """
    await execute_query("tags", query, ())
```

- [ ] **Step 2: Commit**

```bash
git add app/server/prompt_api/tag_image_manager.py
git commit -m "feat: add tag image CRUD functions"
```

---

### Task 3: ComfyUI workflow builder and executor

**Files:**
- Create: `app/server/prompt_api/comfyui_workflow.py`

- [ ] **Step 1: Create the ComfyUI workflow module**

```python
import json
import time
import uuid
import aiohttp
import os
from io import BytesIO
from PIL import Image

from .tag_image_manager import _image_dir, _thumb_dir, update_tag_image_path

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
                    await _sleep(POLL_INTERVAL)
                    continue
                data = await resp.json()
                if prompt_id in data:
                    return data[prompt_id]
            await _sleep(POLL_INTERVAL)
    raise TimeoutError(f"Generation timed out after {timeout}s")


async def _sleep(seconds):
    import asyncio
    await asyncio.sleep(seconds)


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
    image_dir = _image_dir()
    ext = os.path.splitext(filename)[1] or ".png"
    saved_name = f"{t_uuid}{ext}"
    saved_path = os.path.join(image_dir, saved_name)
    with open(saved_path, "wb") as f:
        f.write(img_bytes)

    # Generate thumbnail
    img = Image.open(BytesIO(img_bytes))
    img = img.convert("RGB")
    img.thumbnail(THUMB_SIZE, Image.LANCZOS)
    thumb_dir = _thumb_dir()
    thumb_name = f"{t_uuid}.webp"
    thumb_path = os.path.join(thumb_dir, thumb_name)
    img.save(thumb_path, "WEBP", quality=80)

    # Update database with relative path
    rel_path = f"tag_images/{saved_name}"
    await update_tag_image_path(t_uuid, rel_path)

    return rel_path
```

- [ ] **Step 2: Commit**

```bash
git add app/server/prompt_api/comfyui_workflow.py
git commit -m "feat: add ComfyUI workflow builder and executor for tag image generation"
```

---

### Task 4: Task queue for image generation

**Files:**
- Create: `app/server/prompt_api/tag_image_queue.py`

- [ ] **Step 1: Create the async task queue module**

```python
import asyncio
import traceback
from .tag_image_manager import update_tag_image_status, reset_pending_statuses
from .comfyui_workflow import build_workflow, submit_workflow, poll_history, download_and_save_result


# In-memory task registry
_tasks: dict[str, dict] = {}
_queue = asyncio.Queue(maxsize=100)
_worker_task = None


def _generate_task_id():
    import uuid
    return str(uuid.uuid4())


async def start_worker():
    """Start the background worker coroutine. Call once on plugin init."""
    global _worker_task
    await reset_pending_statuses()
    _worker_task = asyncio.create_task(_worker_loop())
    print("[TagImageQueue] Worker started")


async def stop_worker():
    """Stop the worker. Call on plugin shutdown."""
    global _worker_task
    if _worker_task:
        _worker_task.cancel()
        try:
            await _worker_task
        except asyncio.CancelledError:
            pass
        _worker_task = None


async def _worker_loop():
    """Single worker that processes generation tasks sequentially."""
    while True:
        task = await _queue.get()
        task_id = task["task_id"]
        t_uuid = task["t_uuid"]
        params = task["params"]

        try:
            # Set status to generating
            _tasks[task_id]["status"] = "generating"
            await update_tag_image_status(t_uuid, "generating")

            # Build and submit workflow
            workflow = build_workflow(
                checkpoint=params["checkpoint"],
                width=params["width"],
                height=params["height"],
                sampler_name=params["sampler_name"],
                steps=params["steps"],
                cfg=params["cfg"],
                seed=params["seed"],
                positive=params["positive"],
                negative=params["negative"],
            )
            prompt_id = await submit_workflow(workflow)
            _tasks[task_id]["prompt_id"] = prompt_id

            # Poll for result
            history = await poll_history(prompt_id)

            # Download and save
            image_path = await download_and_save_result(history, t_uuid)

            # Mark ready
            _tasks[task_id]["status"] = "ready"
            _tasks[task_id]["image_path"] = image_path

        except Exception as e:
            error_msg = str(e)
            traceback.print_exc()
            _tasks[task_id]["status"] = "failed"
            _tasks[task_id]["error_msg"] = error_msg
            await update_tag_image_status(t_uuid, "failed")

        finally:
            _queue.task_done()


async def enqueue_generation(t_uuid, params):
    """Enqueue a generation task. Returns task_id. Raises RuntimeError if already in progress."""
    # Check if tag already has a task in progress
    for tid, t in _tasks.items():
        if t["t_uuid"] == t_uuid and t["status"] in ("pending", "generating"):
            raise RuntimeError("已有生成任务进行中")

    task_id = _generate_task_id()
    _tasks[task_id] = {
        "task_id": task_id,
        "t_uuid": t_uuid,
        "status": "pending",
        "prompt_id": None,
        "image_path": None,
        "error_msg": None,
    }

    # Update DB status
    await update_tag_image_status(t_uuid, "pending")

    # Enqueue
    await _queue.put({
        "task_id": task_id,
        "t_uuid": t_uuid,
        "params": params,
    })

    return task_id


def get_task_status(task_id):
    """Get task status by task_id."""
    return _tasks.get(task_id)


def get_task_status_by_tuuid(t_uuid):
    """Find the latest task for a given t_uuid."""
    for tid, t in _tasks.items():
        if t["t_uuid"] == t_uuid:
            return t
    return None
```

- [ ] **Step 2: Commit**

```bash
git add app/server/prompt_api/tag_image_queue.py
git commit -m "feat: add async task queue for tag image generation"
```

---

### Task 5: Update tags_manager.py to include image fields

**Files:**
- Modify: `app/server/prompt_api/tags_manager.py:608-625`

- [ ] **Step 1: Update get_tag_tags query to include image fields and t_uuid**

In `tags_manager.py`, find the `get_tag_tags` function (around line 605). Change the SELECT to include `t_uuid`, `image_path`, `image_status`:

```python
async def get_tag_tags(g_uuid):
    """根据g_uuid获取标签"""
    query = """
        SELECT
            id_index, text, desc, color, create_time, g_uuid, t_uuid, image_path, image_status
        FROM tag_tags
        WHERE g_uuid = ?
        ORDER BY create_time DESC
    """
    data = await fetch_all("tags", query, (g_uuid,))
    return [
        {
            "id_index": row[0],
            "text": row[1],
            "desc": row[2],
            "color": row[3],
            "create_time": row[4],
            "g_uuid": row[5],
            "t_uuid": row[6],
            "image_path": row[7],
            "image_status": row[8],
        }
        for row in data
    ]
```

- [ ] **Step 2: Commit**

```bash
git add app/server/prompt_api/tags_manager.py
git commit -m "feat: include image_path, image_status and t_uuid in get_tag_tags response"
```

---

### Task 6: Add new API routes to prompt_server.py

**Files:**
- Modify: `app/server/prompt_server.py` (append new routes before the labels section)

- [ ] **Step 1: Add imports at the top of prompt_server.py**

Add after the existing imports (around line 30):

```python
from .prompt_api.tag_image_manager import get_tag_image_info, update_tag_image_status, _image_dir, _thumb_dir
from .prompt_api.comfyui_workflow import get_generation_options
from .prompt_api.tag_image_queue import enqueue_generation, get_task_status, get_task_status_by_tuuid, start_worker
```

- [ ] **Step 2: Add routes before labels section**

Find the comment `# ============================================ 标签数据管理 ============================================` (around line 1217) and insert the new routes before it:

```python
# ============================================ 标签图片管理 ============================================


@PromptServer.instance.routes.post(baseUrl + "tag_image/options")
async def _get_tag_image_options(request):
    return web.json_response({"data": get_generation_options()})


@PromptServer.instance.routes.post(baseUrl + "tag_image/generate")
async def _generate_tag_image(request):
    data = await request.json()
    t_uuid = data.get("t_uuid")
    params = data.get("params", {})

    if not t_uuid:
        return web.json_response({"error": "t_uuid is required"}, status=400)

    # Validate required params
    required = ["checkpoint", "width", "height", "sampler_name", "steps", "cfg", "seed", "positive", "negative"]
    for key in required:
        if key not in params:
            return web.json_response({"error": f"Missing required param: {key}"}, status=400)

    try:
        task_id = await enqueue_generation(t_uuid, params)
        return web.json_response({"data": {"task_id": task_id}})
    except RuntimeError as e:
        return web.json_response({"error": str(e)}, status=409)
    except Exception as e:
        print(f"Error enqueuing generation: {e}")
        return web.Response(status=500)


@PromptServer.instance.routes.post(baseUrl + "tag_image/status")
async def _get_tag_image_status_by_task(request):
    data = await request.json()
    task_id = data.get("task_id")

    if not task_id:
        return web.json_response({"error": "task_id is required"}, status=400)

    task = get_task_status(task_id)
    if not task:
        return web.json_response({"error": "task not found"}, status=404)

    return web.json_response({"data": {
        "task_id": task["task_id"],
        "status": task["status"],
        "error_msg": task.get("error_msg"),
        "image_path": task.get("image_path"),
    }})


@PromptServer.instance.routes.get(baseUrl + "tag_image/status/{t_uuid}")
async def _get_tag_image_status_by_uuid(request):
    t_uuid = request.match_info.get("t_uuid")

    if not t_uuid:
        return web.json_response({"error": "t_uuid is required"}, status=400)

    # Check DB first
    db_info = await get_tag_image_info(t_uuid)
    status = db_info["image_status"] if db_info else None
    image_path = db_info["image_path"] if db_info else None

    # Check if there's a running task
    task = get_task_status_by_tuuid(t_uuid)
    task_id = task["task_id"] if task else None
    if task and task["status"] in ("pending", "generating"):
        status = task["status"]

    return web.json_response({"data": {
        "status": status,
        "task_id": task_id,
        "image_url": f"/weilin/prompt_ui/api/tag_image/{t_uuid}" if status == "ready" else None,
        "thumb_url": f"/weilin/prompt_ui/api/tag_thumb/{t_uuid}" if status == "ready" else None,
        "error_msg": task.get("error_msg") if task else None,
    }})


@PromptServer.instance.routes.get(baseUrl + "tag_image/{t_uuid}")
async def _serve_tag_image(request):
    t_uuid = request.match_info.get("t_uuid")
    image_dir = _image_dir()
    # Try common extensions
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        path = os.path.join(image_dir, f"{t_uuid}{ext}")
        if os.path.isfile(path):
            return web.FileResponse(path)
    return web.Response(status=404, text="Image not found")


@PromptServer.instance.routes.get(baseUrl + "tag_thumb/{t_uuid}")
async def _serve_tag_thumb(request):
    t_uuid = request.match_info.get("t_uuid")
    thumb_dir = _thumb_dir()
    path = os.path.join(thumb_dir, f"{t_uuid}.webp")
    if os.path.isfile(path):
        return web.FileResponse(path)
    return web.Response(status=404, text="Thumbnail not found")


# ============================================ 标签图片管理 End ============================================
```

- [ ] **Step 3: Start the worker on plugin init**

Find where the plugin initializes. In `prompt_server.py`, the routes are registered at module import time. Add worker startup at the bottom of the file or in a suitable init hook. Add after the existing `atexit` handler if one exists, or at the end of the file:

```python
# Start the tag image generation worker
import asyncio as _asyncio
try:
    _loop = _asyncio.get_event_loop()
    if _loop.is_running():
        _asyncio.ensure_future(start_worker())
    else:
        _loop.run_until_complete(start_worker())
except Exception:
    pass
```

- [ ] **Step 4: Commit**

```bash
git add app/server/prompt_server.py
git commit -m "feat: add tag image generation API routes and static file serving"
```

---

### Task 7: Frontend API methods

**Files:**
- Modify: `src/src/api/tags.js`

- [ ] **Step 1: Add new API methods to tags.js**

Append to the `tagsApi` export object, before the closing `}`:

```javascript
  // 获取生成选项（checkpoint列表、采样器、尺寸预设）
  getGenerationOptions: () => {
    return request({
      url: '/tag_image/options',
      method: 'post'
    })
  },

  // 提交生成任务
  // eslint-disable-next-line camelcase
  generateTagImage: (t_uuid, params) => {
    return request({
      url: '/tag_image/generate',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { t_uuid, params }
    })
  },

  // 按 task_id 查询任务状态
  getTagImageStatus: (task_id) => {
    return request({
      url: '/tag_image/status',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { task_id }
    })
  },

  // 按 t_uuid 查询任务状态（页面刷新恢复用）
  // eslint-disable-next-line camelcase
  getTagImageStatusByUuid: (t_uuid) => {
    return request({
      url: `/tag_image/status/${t_uuid}`,
      method: 'get'
    })
  }
```

- [ ] **Step 2: Commit**

```bash
git add src/src/api/tags.js
git commit -m "feat: add tag image generation API methods to frontend"
```

---

### Task 8: GenerateImageDialog Vue component

**Files:**
- Create: `src/src/view/tag_manager/components/GenerateImageDialog.vue`

- [ ] **Step 1: Create the dialog component**

```vue
<template>
  <div v-if="visible" class="weilin-tools-dialog-overlay" @mousedown.self="onCancel">
    <div class="weilin-tools-dialog-content generate-image-dialog" @mousedown.stop>
      <div class="weilin-tools-dialog-header">
        <h2>生成标签预览图</h2>
        <button class="close-btn" @click="onCancel">×</button>
      </div>
      <div class="weilin-tools-dialog-body">
        <div class="form-group">
          <label>模型</label>
          <select v-model="form.checkpoint" class="form-select">
            <option v-for="cp in options.checkpoints" :key="cp.name" :value="cp.name">
              {{ cp.name }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>尺寸</label>
          <select v-model="form.sizeIndex" class="form-select">
            <option v-for="(s, i) in options.sizes" :key="i" :value="i">
              {{ s.label }}
            </option>
          </select>
        </div>

        <div class="form-group">
          <label>采样器</label>
          <select v-model="form.sampler_name" class="form-select">
            <option v-for="s in options.samplers" :key="s" :value="s">{{ s }}</option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group form-group-half">
            <label>步数: {{ form.steps }}</label>
            <input type="range" v-model.number="form.steps" min="1" max="50" class="form-range" />
          </div>
          <div class="form-group form-group-half">
            <label>CFG: {{ form.cfg }}</label>
            <input type="range" v-model.number="form.cfg" min="1" max="20" step="0.5" class="form-range" />
          </div>
        </div>

        <div class="form-group">
          <label>种子 (-1 为随机)</label>
          <input type="number" v-model.number="form.seed" class="form-input" />
        </div>

        <div class="form-group">
          <label>正向提示词</label>
          <textarea v-model="form.positive" class="form-textarea" rows="3"></textarea>
        </div>

        <div class="form-group">
          <label>负向提示词</label>
          <textarea v-model="form.negative" class="form-textarea" rows="2"></textarea>
        </div>
      </div>
      <div class="weilin-tools-dialog-footer">
        <button class="cancel-btn" @click="onCancel">取消</button>
        <button class="confirm-btn" @click="onGenerate" :disabled="generating">生成</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'
import { tagsApi } from '@/api/tags'

const props = defineProps({
  visible: { type: Boolean, default: false },
  tag: { type: Object, default: null },
  options: { type: Object, default: () => ({ checkpoints: [], samplers: [], sizes: [] }) }
})
const emit = defineEmits(['close', 'generated'])

const generating = ref(false)

const form = reactive({
  checkpoint: '',
  sizeIndex: 0,
  sampler_name: 'euler',
  steps: 20,
  cfg: 7.0,
  seed: -1,
  positive: '',
  negative: 'worst quality, low quality, nsfw'
})

watch(() => props.visible, (v) => {
  if (v && props.tag) {
    // Set defaults from tag
    form.positive = `${props.tag.text || ''}, masterpiece, best quality`
    form.negative = 'worst quality, low quality, nsfw'
    form.checkpoint = props.options.checkpoints?.[0]?.name || ''
    form.sampler_name = 'euler'
    form.steps = 20
    form.cfg = 7.0
    form.seed = -1
    form.sizeIndex = 0
    generating.value = false
  }
})

function onCancel() {
  if (!generating.value) {
    emit('close')
  }
}

async function onGenerate() {
  const size = props.options.sizes[form.sizeIndex] || props.options.sizes[0]
  generating.value = true
  try {
    const params = {
      checkpoint: form.checkpoint,
      width: size.width,
      height: size.height,
      sampler_name: form.sampler_name,
      steps: form.steps,
      cfg: form.cfg,
      seed: form.seed,
      positive: form.positive,
      negative: form.negative
    }
    const res = await tagsApi.generateTagImage(props.tag.t_uuid, params)
    emit('generated', { task_id: res.data.task_id, t_uuid: props.tag.t_uuid })
    emit('close')
  } catch (err) {
    if (err.response?.status === 409) {
      alert('已有生成任务进行中')
    } else {
      alert('生成失败: ' + (err.message || '未知错误'))
    }
  } finally {
    generating.value = false
  }
}
</script>

<style scoped>
.generate-image-dialog {
  width: 520px;
  max-width: 90vw;
}
.form-row {
  display: flex;
  gap: 16px;
}
.form-group-half {
  flex: 1;
}
.form-select, .form-input, .form-textarea {
  width: 100%;
  padding: 6px 10px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
}
.form-textarea {
  resize: vertical;
}
.form-range {
  width: 100%;
}
.confirm-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>
```

- [ ] **Step 2: Commit**

```bash
git add src/src/view/tag_manager/components/GenerateImageDialog.vue
git commit -m "feat: add GenerateImageDialog component for tag preview image generation"
```

---

### Task 9: Modify tag_index.vue — thumbnail display, hover overlay, generate button

**Files:**
- Modify: `src/src/view/tag_manager/tag_index.vue`

This is the core UI change. We modify the tag card template and add reactive state + methods.

- [ ] **Step 1: Import the GenerateImageDialog component**

Find the `<script setup>` section imports (search for `import` statements in the script block). Add:

```javascript
import GenerateImageDialog from './components/GenerateImageDialog.vue'
```

- [ ] **Step 2: Add reactive state variables**

Find where other refs are declared (around lines 500-520). Add:

```javascript
// --- Tag image preview state ---
const showGenerateDialog = ref(false)
const generateTargetTag = ref(null)
const generationOptions = ref({ checkpoints: [], samplers: [], sizes: [] })
const pollingTimers = ref({})  // { t_uuid: intervalId }
const hoverTimer = ref(null)
const hoveredTag = ref(null)
const hoverImageCache = ref({})  // { t_uuid: blobUrl }
```

- [ ] **Step 3: Modify the tag card template**

Find the tag grid section (around lines 202-232). Change the tag card from:

```html
<div class="tags-grid" v-if="selectedGroup">
  <div v-for="tag in currentTags" :key="'tag-grid-' + tag.id_index"
    :class="highlightedTagId === tag.id_index ? 'tag-wrapper highlight' : 'tag-wrapper'">
    <div class="tag-content" @click="handleTagClick(tag)">
      <div class="tag-main" :style="{ backgroundColor: tag.color || 'transparent' }">
        {{ tag.desc }}
        ...
```

To:

```html
<div class="tags-grid" v-if="selectedGroup">
  <div v-for="tag in currentTags" :key="'tag-grid-' + tag.id_index"
    :class="highlightedTagId === tag.id_index ? 'tag-wrapper highlight' : 'tag-wrapper'">
    <!-- Thumbnail area -->
    <div class="tag-thumb-area"
      @mouseenter="onThumbHover(tag, $event)"
      @mouseleave="onThumbLeave">
      <!-- Ready: show thumbnail -->
      <img v-if="tag.image_status === 'ready' && tag.t_uuid"
        class="tag-thumb-img"
        :src="getThumbUrl(tag.t_uuid)"
        alt="preview"
        loading="lazy"
      />
      <!-- Pending/Generating: show loading -->
      <div v-else-if="tag.image_status === 'pending' || tag.image_status === 'generating'"
        class="tag-thumb-placeholder tag-thumb-loading">
        <div class="tag-thumb-spinner"></div>
        <span>{{ tag.image_status === 'pending' ? '排队中…' : '生成中…' }}</span>
      </div>
      <!-- Failed: show retry -->
      <div v-else-if="tag.image_status === 'failed'"
        class="tag-thumb-placeholder tag-thumb-failed"
        @click.stop="openGenerateDialog(tag)"
        title="生成失败，点击重试">
        <svg viewBox="0 0 24 24" width="24" height="24" fill="#ff6b6b">
          <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 15h-2v-2h2v2zm0-4h-2V7h2v6z"/>
        </svg>
        <span>重试</span>
      </div>
      <!-- NULL: show generate button -->
      <div v-else class="tag-thumb-placeholder tag-thumb-empty"
        @click.stop="openGenerateDialog(tag)"
        title="生成预览图">
        <svg viewBox="0 0 24 24" width="28" height="28" fill="currentColor" opacity="0.5">
          <path d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z"/>
        </svg>
        <span>生成</span>
      </div>
    </div>

    <!-- Hover overlay with full-size image -->
    <div v-if="hoveredTag === tag.id_index && hoverImageCache[tag.t_uuid]"
      class="tag-thumb-overlay"
      :style="hoverOverlayStyle">
      <img :src="hoverImageCache[tag.t_uuid]" class="tag-thumb-full" />
    </div>

    <div class="tag-content" @click="handleTagClick(tag)">
      <div class="tag-main" :style="{ backgroundColor: tag.color || 'transparent' }">
        {{ tag.desc }}
        <div class="tag-actions">
          ...
```

- [ ] **Step 4: Add methods for thumbnail handling**

Add these methods in the `<script setup>` block:

```javascript
// --- Tag image methods ---

function getThumbUrl(t_uuid) {
  return `/weilin/prompt_ui/api/tag_thumb/${t_uuid}`
}

function getImageUrl(t_uuid) {
  return `/weilin/prompt_ui/api/tag_image/${t_uuid}`
}

async function openGenerateDialog(tag) {
  if (!generationOptions.value.checkpoints.length) {
    try {
      const res = await tagsApi.getGenerationOptions()
      generationOptions.value = res.data || res || generationOptions.value
    } catch (e) {
      console.error('Failed to load generation options:', e)
    }
  }
  generateTargetTag.value = tag
  showGenerateDialog.value = true
}

function onGenerateDialogClose() {
  showGenerateDialog.value = false
  generateTargetTag.value = null
}

async function onImageGenerated({ task_id, t_uuid }) {
  // Update local tag status
  const tag = currentTags.value.find(t => t.t_uuid === t_uuid)
  if (tag) {
    tag.image_status = 'pending'
  }
  // Start polling
  startPolling(task_id, t_uuid)
}

function startPolling(task_id, t_uuid) {
  if (pollingTimers.value[t_uuid]) {
    clearInterval(pollingTimers.value[t_uuid])
  }
  const timer = setInterval(async () => {
    try {
      const res = await tagsApi.getTagImageStatus(task_id)
      const data = res.data || res
      if (data.status === 'ready' || data.status === 'failed') {
        clearInterval(timer)
        delete pollingTimers.value[t_uuid]
        // Refresh tag status from server
        await refreshSingleTagImageStatus(t_uuid)
      }
    } catch (e) {
      console.error('Polling error:', e)
    }
  }, 2000)
  pollingTimers.value[t_uuid] = timer
}

async function refreshSingleTagImageStatus(t_uuid) {
  try {
    const res = await tagsApi.getTagImageStatusByUuid(t_uuid)
    const data = res.data || res
    const tag = currentTags.value.find(t => t.t_uuid === t_uuid)
    if (tag) {
      tag.image_status = data.status
      if (data.status === 'ready' && data.thumb_url) {
        tag.image_path = data.image_url
      }
    }
    // If still pending/generating, resume polling if we have a task_id
    if ((data.status === 'pending' || data.status === 'generating') && data.task_id) {
      startPolling(data.task_id, t_uuid)
    }
    // Clear cache for updated image
    if (data.status === 'ready') {
      delete hoverImageCache.value[t_uuid]
    }
  } catch (e) {
    console.error('Failed to refresh tag image status:', e)
  }
}

// --- Hover overlay ---
const hoverOverlayStyle = ref({})

function onThumbHover(tag, event) {
  if (tag.image_status !== 'ready' || !tag.t_uuid) return

  hoverTimer.value = setTimeout(async () => {
    hoveredTag.value = tag.id_index
    // Load full image if not cached
    if (!hoverImageCache.value[tag.t_uuid]) {
      const imgUrl = getImageUrl(tag.t_uuid)
      hoverImageCache.value[tag.t_uuid] = imgUrl
    }
    // Position overlay near the thumbnail
    const rect = event.target.getBoundingClientRect()
    hoverOverlayStyle.value = {
      left: (rect.right + 12) + 'px',
      top: rect.top + 'px',
    }
  }, 200)
}

function onThumbLeave() {
  clearTimeout(hoverTimer.value)
  hoveredTag.value = null
}
```

- [ ] **Step 5: Add onMounted logic to restore polling after refresh**

Find the existing `onMounted` hook (if any) or add one. Add logic to iterate current tags and restore polling:

```javascript
onMounted(async () => {
  // Restore polling for any tags in pending/generating state
  await nextTick()
  for (const tag of currentTags.value) {
    if (tag.image_status === 'pending' || tag.image_status === 'generating') {
      await refreshSingleTagImageStatus(tag.t_uuid)
    }
  }
})
```

If `nextTick` is not already imported, add it to the Vue import.

- [ ] **Step 6: Add scoped CSS for thumbnails**

Add to the existing `<style scoped>` block:

```css
/* --- Tag thumbnail --- */
.tag-thumb-area {
  width: 120px;
  height: 120px;
  margin: 0 auto 6px auto;
  border-radius: 6px;
  overflow: hidden;
  position: relative;
}

.tag-thumb-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.tag-thumb-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.15s ease;
}

.tag-thumb-empty {
  border: 2px dashed var(--weilin-prompt-ui-border-color);
  border-radius: 6px;
  color: var(--weilin-prompt-ui-secondary-text);
}

.tag-thumb-empty:hover {
  border-color: var(--weilin-prompt-ui-primary-color);
  color: var(--weilin-prompt-ui-primary-color);
  background: color-mix(in srgb, var(--weilin-prompt-ui-primary-color) 8%, transparent);
}

.tag-thumb-loading {
  border: 2px solid var(--weilin-prompt-ui-border-color);
  border-radius: 6px;
  color: var(--weilin-prompt-ui-secondary-text);
}

.tag-thumb-failed {
  border: 2px dashed #ff6b6b;
  border-radius: 6px;
  color: #ff6b6b;
  gap: 2px;
}

.tag-thumb-failed:hover {
  background: color-mix(in srgb, #ff6b6b 8%, transparent);
}

.tag-thumb-spinner {
  width: 24px;
  height: 24px;
  border: 3px solid var(--weilin-prompt-ui-border-color);
  border-top-color: var(--weilin-prompt-ui-primary-color);
  border-radius: 50%;
  animation: thumb-spin 0.8s linear infinite;
}

@keyframes thumb-spin {
  to { transform: rotate(360deg); }
}

/* Hover overlay */
.tag-thumb-overlay {
  position: fixed;
  z-index: 9999;
  max-width: 400px;
  max-height: 500px;
  border-radius: 8px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
  overflow: hidden;
  background: #000;
  pointer-events: none;
}

.tag-thumb-full {
  width: 100%;
  height: 100%;
  object-fit: contain;
}
```

- [ ] **Step 7: Add GenerateImageDialog to template**

Add at the end of the template (just before the closing `</div>` of the root element):

```html
<!-- 生成预览图对话框 -->
<GenerateImageDialog
  :visible="showGenerateDialog"
  :tag="generateTargetTag"
  :options="generationOptions"
  @close="onGenerateDialogClose"
  @generated="onImageGenerated"
/>
```

- [ ] **Step 8: Commit**

```bash
git add src/src/view/tag_manager/tag_index.vue
git commit -m "feat: add tag preview image thumbnails, hover overlay, and generate button to tag cards"
```

---

### Task 10: Build and verify

**Files:**
- No new files, verify everything works together.

- [ ] **Step 1: Build the frontend**

```bash
cd "D:\game\SD_ComfyUI\ComfyUI-aki-v2\ComfyUI\custom_nodes\WeiLin-Comfyui-Tools\src" && npm run build
```

- [ ] **Step 2: Restart ComfyUI and verify**

Restart ComfyUI, open the tag manager UI, verify:
- Tags show thumbnail placeholder area
- Clicking "Generate" opens the dialog with all options
- Submitting queues a generation (check server logs)
- Hover shows full image (after generation completes)

- [ ] **Step 3: Commit build output**

```bash
git add dist/
git commit -m "build: update dist for tag preview image feature"
```
