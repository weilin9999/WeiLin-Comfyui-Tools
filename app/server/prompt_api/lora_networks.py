# -*- coding: UTF-8 -*-
import os
import folder_paths
from PIL import Image
import base64
from io import BytesIO
import requests
import asyncio
import concurrent.futures
from tqdm import tqdm

from .lora_info import get_model_info

filters = [
    # 'filename',
    # 'description',
    'search_term',
    'local_preview',
    'metadata',
]

def download_image(url, filename, directory):
    _, ext = os.path.splitext(url)
    filename, _ = os.path.splitext(filename)
    filepath = os.path.join(directory, f"{filename}{ext}")
    try:
        resp = requests.get(url, stream=True)
        resp.raise_for_status()
        with open(filepath, 'wb') as f:
             for chunk in resp.iter_content(chunk_size=4096):
                 f.write(chunk)
    except Exception as e:
        print(e)
        if os.path.exists(filepath):
            os.remove(filepath)

def prepare_lora_item_data(item_path, auto_fetch=False):
    lora_path = folder_paths.get_full_path("loras", item_path)
    [model_name, model_extension] = os.path.splitext(item_path)
    file_name = os.path.basename(item_path)
    info_data = asyncio.run(get_model_info(item_path, light=True))
    if auto_fetch:
        if len(info_data['images']) == 0: # 无数据
            info_data = asyncio.run(get_model_info(item_path, maybe_fetch_civitai=True, maybe_fetch_metadata=True, light=False))
        if len(info_data['images']) != 0 and item_path not in info_data['images'][0]['url']: # 未设置封面
            url = next(filter(lambda x: x['type'] == 'image', info_data['images']), {}).get('url')
            download_image(url=url, filename=file_name, directory=os.path.dirname(lora_path))

    item = {
            "basename": item_path,
            "name": item_path,
            "dirname": os.path.dirname(lora_path),
            "file_path": lora_path,
            "preview":preview_file(lora_path),
            "model_name": model_name,
            "model_filename": file_name,
        }
    item["local_info"] = info_data
    # item["search_terms"] = ["Lora\\"+item_path]
    return item

async def get_extra_networks(auto_fetch=False):
    loras_path  = folder_paths.get_filename_list("loras")
    return_response= {"path": "", "loras": []}
    return_response["path"] = loras_path
    items = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()*2) as executor:
        futures = [executor.submit(prepare_lora_item_data, item_path, auto_fetch) for item_path in loras_path]
        for future in tqdm(futures):
            items.append(future.result())
    return_response["loras"] = items
    return return_response

def preview_file(filename: str):
    preview_exts = [".jpg", ".png", ".jpeg", ".gif"]
    preview_exts = [*preview_exts, *[".preview" + x for x in preview_exts]]
    for ext in preview_exts:
        try:
            pathStr = os.path.splitext(filename)[0] + ext
            if os.path.exists(pathStr):
                # because ComfyUI has extra model path feature
                # the path might not be relative to the ComfyUI root
                # so instead of returning the path, we return the image data directly, to avoid security issues
                # print(pathStr)
                bytes = get_thumbnail_for_image_file(pathStr)
                # Get the base64 string
                img_base64 = base64.b64encode(bytes).decode()
                # Return the base64 string
                return f"data:image/jpeg;base64, {img_base64}"
        except Exception as e:
            print(f"读取封面出错: {e}")
            return None


MAX_IMAGE_SIZE = 250

def get_thumbnail_for_image_file(file_path):
    try:
        with Image.open(file_path) as img:
            # If the image is too large, resize it
            if img.width > MAX_IMAGE_SIZE and img.height > MAX_IMAGE_SIZE:
                # Calculate new width to maintain aspect ratio
                width = int(img.width * MAX_IMAGE_SIZE / img.height)
                # Resize the image
                img = img.resize((width, MAX_IMAGE_SIZE))
            img = img.convert("RGB")
            # Save the image to a BytesIO object
            buffer = BytesIO()
            img.save(buffer, format="JPEG", quality=85)
            return buffer.getvalue()
    except Exception as e:
        print(f"打开封面出错: {e}")
        return None
