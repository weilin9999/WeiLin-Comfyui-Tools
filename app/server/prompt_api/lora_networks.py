# -*- coding: UTF-8 -*-
import os
import folder_paths
from PIL import Image
import base64
from io import BytesIO
import asyncio
import concurrent.futures
from tqdm import tqdm

from .lora_info import get_model_info

loading_status = {
    "isLoading": False,
    "progress": 0,
    "total": 0,
    "current": 0
}

filters = [
    # 'filename',
    # 'description',
    'search_term',
    'local_preview',
    'metadata',
]


def prepare_lora_item_data(item_path, auto_fetch=False):
    lora_path = folder_paths.get_full_path("loras", item_path)
    try:
        # 安全处理文件名，避免特殊字符问题
        item_path = item_path.encode('utf-8', 'ignore').decode('utf-8')
        [model_name, model_extension] = os.path.splitext(item_path)
        file_name = os.path.basename(item_path)
    except Exception as e:
        print(f"文件名处理错误: {e}")
        model_name = os.path.splitext(os.path.basename(item_path))[0]
        model_extension = os.path.splitext(item_path)[1]
        file_name = os.path.basename(item_path)

    info_data = asyncio.run(get_model_info(item_path, light=True))
    if auto_fetch:
        if len(info_data['images']) == 0: # 无数据
            info_data = asyncio.run(get_model_info(item_path, maybe_fetch_civitai=True, maybe_fetch_metadata=True, light=False))
        # if len(info_data['images']) != 0 and item_path not in info_data['images'][0]['url']: # 未设置封面
        #     url = next(filter(lambda x: x['type'] == 'image', info_data['images']), {}).get('url')
        #     download_image(url=url, filename=file_name, directory=os.path.dirname(lora_path))

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

def get_lora_folder():
    """
    获取Lora文件夹结构，以层次化结构返回，包含每个目录下的文件和子目录
    
    返回:
        包含目录结构的字典:
        - "/": 根目录
          - "/": 根目录下的文件列表
        - "一级目录名": 该一级目录下的子目录和文件
          - "/": 该目录下的文件列表
          - "子目录名": 子目录下的文件列表
          - "all": 该目录下所有文件的列表
    """
    all_files = folder_paths.get_filename_list("loras")
    
    # 初始化结果字典
    result = {
        "all": all_files,
        "/": {
            "/": {},  # 根目录下的文件
            "all": []  # 根目录下所有文件
        }
    }
    
    # 处理所有文件路径
    for file_path in all_files:
        parts = file_path.replace('\\', '/').split('/')
        
        if len(parts) == 1:
            # 根目录文件
            result["/"]["/"][parts[0]] = file_path
            result["/"]["all"].append(file_path)
        else:
            # 一级目录
            level1_dir = parts[0]
            
            # 确保一级目录在结果字典中
            if level1_dir not in result:
                result[level1_dir] = {
                    "all": [],  # 该目录下所有文件
                    "/": {}  # 该目录下的文件
                }
            
            if len(parts) == 2:
                # 一级目录下的文件
                result[level1_dir]["/"][parts[1]] = file_path
                result[level1_dir]["all"].append(file_path)
            else:
                # 二级及以下目录
                subdir = "\\".join(parts[1:-1])  # 排除文件名
                
                # 确保子目录在一级目录下
                if subdir not in result[level1_dir]:
                    result[level1_dir][subdir] = {
                        "all": [],  # 子目录下所有文件
                        "/": {}  # 子目录下的文件
                    }
                
                # 添加文件到子目录，使用完整路径
                result[level1_dir][subdir][parts[-1]] = file_path
                result[level1_dir][subdir]["all"].append(file_path)
                result[level1_dir]["all"].append(file_path)
    
    return result

async def search_lora_files(query):
    """
    模糊搜索Lora文件，根据文件名进行匹配
    
    参数:
        query: 搜索关键词
    
    返回:
        匹配的文件路径列表
    """
    all_files = folder_paths.get_filename_list("loras")
    results = []
    
    # 转换查询字符串为小写，用于不区分大小写的搜索
    query = query.lower()
    
    for file_path in all_files:
        # 获取文件名（不含路径）
        file_name = os.path.basename(file_path)
        
        # 如果文件名包含查询字符串，则添加到结果中
        if query in file_name.lower():
            results.append(file_path)
    
    return results

async def get_rang_for_extra_networks(arr=[]):
    return_response= {"loras": []}
    if len(arr) > 0:
        items = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()*2) as executor:
            futures = [executor.submit(prepare_lora_item_data, item_path, False) for item_path in arr]
            for future in tqdm(futures):
                items.append(future.result())
        return_response["loras"] = items
    return return_response

async def get_extra_networks(auto_fetch=False):
    global loading_status
    loras_path  = folder_paths.get_filename_list("loras")
    return_response= {"path": "", "loras": []}
    return_response["path"] = loras_path
    items = []
    
    loading_status["isLoading"] = True
    loading_status["total"] = len(loras_path)
    loading_status["current"] = 0
    loading_status["progress"] = 0
    
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()*2) as executor:
            futures = [executor.submit(prepare_lora_item_data, item_path, auto_fetch) for item_path in loras_path]
            for future in tqdm(futures):
                items.append(future.result())
                loading_status["current"] += 1
                loading_status["progress"] = int((loading_status["current"] / loading_status["total"]) * 100)
    finally:
        loading_status["isLoading"] = False
        
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
