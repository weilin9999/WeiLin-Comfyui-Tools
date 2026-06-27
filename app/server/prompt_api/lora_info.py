import hashlib
import json
import os
import re
from datetime import datetime

import folder_paths
import requests

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
USERDATA = os.path.join(THIS_DIR, "../../../", "lora_userdatas")

# code from rgthree-comfy thanks


def image_upload(post, image_save_function=None):
    image = post.get("image")
    path = post.get("path")
    fileName = post.get("fileName")

    lora_path = folder_paths.get_full_path("loras", path)
    if not path_exists(lora_path):
        lora_path = os.path.abspath(lora_path)

    for ext in ["jpg", "png", "jpeg", "gif", "webp"]:
        try_path = f"{os.path.splitext(lora_path)[0]}.{ext}"
        if path_exists(try_path):
            os.remove(try_path)  # 删除已经存在的图片

    file_name_with_extension = os.path.basename(lora_path)
    file_namea, _ = os.path.splitext(file_name_with_extension)
    model = file_namea

    upload_dir = os.path.dirname(os.path.abspath(lora_path))

    api_response = {"status": 200}

    if image and image.file:
        file_name, file_extension = os.path.splitext(fileName)

        filepath = os.path.join(upload_dir, model + file_extension)

        with open(filepath, "wb") as f:
            f.write(image.file.read())

        api_response["res"] = "success"
        return api_response
    else:
        api_response["status"] = "404"
        return api_response


def get_param(request, param, default=None):
    """Gets a param from a request."""
    # return request.rel_url.query[param] if param in request.rel_url.query else default
    if param in request.rel_url.query:
        value = request.rel_url.query[param]
        try:
            # 尝试URL解码特殊字符
            import urllib.parse

            return urllib.parse.unquote(value)
        except:
            return value
    return default


def is_param_falsy(request, param):
    """Determines if a param is explicitly 0 or false."""
    val = get_param(request, param)
    return val is not None and (val == "0" or val.upper() == "FALSE")


def path_exists(path):
    """Checks if a path exists, accepting None type."""
    if path is not None:
        return os.path.exists(path)
    return False


def get_folder_path(file: str, model_type="loras"):
    """Gets the file path ensuring it exists."""
    try:
        import urllib.parse

        file = urllib.parse.unquote(file)
    except:
        pass
    file_path = folder_paths.get_full_path(model_type, file)
    if file_path and not path_exists(file_path):
        file_path = os.path.abspath(file_path)
    if not path_exists(file_path):
        file_path = None
    return file_path


async def get_loras_info_response(
    request, maybe_fetch_civitai=False, maybe_fetch_metadata=False
):
    """Gets lora info for all or a single lora"""
    api_response = {"status": 200}
    lora_file = get_param(request, "file")

    if get_param(request, "light") is not None:
        light = is_param_falsy(request, "light")
    else:
        light = False
    if lora_file is not None:
        if light:
            info_data = await get_model_info(
                lora_file,
                maybe_fetch_civitai=maybe_fetch_civitai,
                maybe_fetch_metadata=maybe_fetch_metadata,
                light=light,
            )
        else:
            info_data = await get_model_info(
                lora_file,
                force_fetch_civitai=maybe_fetch_civitai,
                force_fetch_metadata=maybe_fetch_metadata,
                light=light,
            )
        if info_data is None:
            api_response["status"] = "404"
            api_response["error"] = "No Lora found at path"
        else:
            api_response["data"] = info_data
    else:
        api_response["data"] = []
        lora_files = folder_paths.get_filename_list("loras")
        for lora_file in lora_files:
            info_data = await get_model_info(
                lora_file,
                maybe_fetch_civitai=maybe_fetch_civitai,
                maybe_fetch_metadata=maybe_fetch_metadata,
                light=light,
            )
            api_response["data"].append(info_data)
    return api_response


def load_json_file(file: str, default=None):
    """Reads a json file and returns the json dict, stripping out "//" comments first."""
    if path_exists(file):
        with open(file, encoding="UTF-8") as file:
            config = file.read()
            try:
                return json.loads(config)
            except json.decoder.JSONDecodeError:
                try:
                    config = re.sub(r"^\s*//\s.*", "", config, flags=re.MULTILINE)
                    return json.loads(config)
                except json.decoder.JSONDecodeError:
                    try:
                        config = re.sub(r"(?:^|\s)//.*", "", config, flags=re.MULTILINE)
                        return json.loads(config)
                    except json.decoder.JSONDecodeError:
                        pass
    return default


def _update_data(info_data: dict) -> bool:
    """Ports old data to new data if necessary."""
    should_save = False
    # If we have "triggerWords" then move them over to "trainedWords"
    if "triggerWords" in info_data and len(info_data["triggerWords"]) > 0:
        civitai_words = ",".join(
            get_dict_value(info_data, "raw.civitai.triggerWords", default=[])
            + get_dict_value(info_data, "raw.civitai.trainedWords", default=[])
        )
        if "trainedWords" not in info_data:
            info_data["trainedWords"] = []
        for trigger_word in info_data["triggerWords"]:
            word_data = next(
                (
                    data
                    for data in info_data["trainedWords"]
                    if data["word"] == trigger_word
                ),
                None,
            )
            if word_data is None:
                word_data = {"word": trigger_word}
                info_data["trainedWords"].append(word_data)
            if trigger_word in civitai_words:
                word_data["civitai"] = True
            else:
                word_data["user"] = True

        del info_data["triggerWords"]
        should_save = True

    # 自动关联 trainedWords 到 loraWorks（解决触发词自动填充问题）
    # 处理 loraWorks 不存在、为空、或包含多个词的情况
    should_update_loraWorks = False
    
    if "loraWorks" not in info_data or not info_data["loraWorks"]:
        # loraWorks不存在或为空
        should_update_loraWorks = True
    elif isinstance(info_data["loraWorks"], str) and "," in info_data["loraWorks"]:
        # loraWorks包含多个词（用逗号分隔），需要更新为只取第一个
        should_update_loraWorks = True
    
    if should_update_loraWorks:
        # 从 trainedWords 中提取第一个训练词作为默认触发词
        if (
            "trainedWords" in info_data
            and isinstance(info_data["trainedWords"], list)
            and len(info_data["trainedWords"]) > 0
        ):
            first_word = info_data["trainedWords"][0]
            # 兼容 {"word": "xxx"} 格式和直接字符串格式
            if isinstance(first_word, dict) and "word" in first_word:
                info_data["loraWorks"] = first_word["word"].strip()
            elif isinstance(first_word, str) and first_word.strip():
                info_data["loraWorks"] = first_word.strip()
            should_save = True

    return should_save


async def get_model_info(
    file: str,
    model_type="loras",
    default=None,
    maybe_fetch_civitai=False,
    force_fetch_civitai=False,
    maybe_fetch_metadata=False,
    force_fetch_metadata=False,
    light=False,
):
    """Compiles a model info given a stored file next to the model, and/or metadata/civitai."""

    file_path = get_folder_path(file, model_type)
    if file_path is None:
        return default

    info_data = {}
    should_save = False
    # Try to load a weilin-info.json file next to the file.
    try_info_path = f"{file_path}.weilin-info.json"
    if path_exists(try_info_path):
        info_data = load_json_file(try_info_path)

    if "file" not in info_data:
        info_data["file"] = file
        should_save = True
    if "path" not in info_data:
        info_data["path"] = file_path
        should_save = True

    # Check if we have an image next to the file and, if so, add it to the front of the images
    # (if it isn't already).
    img_next_to_file = None
    for ext in ["jpg", "png", "jpeg", "webp"]:
        try_path = f"{os.path.splitext(file_path)[0]}.{ext}"
        if path_exists(try_path):
            img_next_to_file = try_path
            break

    if "images" not in info_data:
        info_data["images"] = []
        should_save = True

    if img_next_to_file:
        img_next_to_file_url = (
            f"/weilin/prompt_ui/api/lorainfo/api/loras/img?file={file}"
        )
        if (
            len(info_data["images"]) == 0
            or info_data["images"][0]["url"] != img_next_to_file_url
        ):
            info_data["images"].insert(0, {"url": img_next_to_file_url})
            should_save = True

    # If we just want light data then bail now with just existing data, plus file, path and img if
    # next to the file.
    if (
        light
        and not maybe_fetch_metadata
        and not force_fetch_metadata
        and not maybe_fetch_civitai
        and not force_fetch_civitai
    ):
        return info_data

    if "raw" not in info_data:
        info_data["raw"] = {}
        should_save = True

    should_save = _update_data(info_data) or should_save

    should_fetch_civitai = force_fetch_civitai is True or (
        maybe_fetch_civitai is True
        and ("civitai" not in info_data["raw"] or len(info_data["raw"]["civitai"]) == 0)
    )
    should_fetch_metadata = force_fetch_metadata is True or (
        maybe_fetch_metadata is True
        and (
            "metadata" not in info_data["raw"] or len(info_data["raw"]["metadata"]) == 0
        )
    )

    if should_fetch_metadata:
        data_meta = _get_model_metadata(
            file, model_type=model_type, default={}, refresh=force_fetch_metadata
        )
        should_save = _merge_metadata(info_data, data_meta) or should_save

    if should_fetch_civitai:
        data_civitai = _get_model_civitai_data(
            file, model_type=model_type, default={}, refresh=force_fetch_civitai
        )
        should_save = _merge_civitai_data(info_data, data_civitai) or should_save

    if "sha256" not in info_data:
        file_hash = _get_sha256_hash(file_path)
        if file_hash is not None:
            info_data["sha256"] = file_hash
            should_save = True

    if (
        len(info_data["images"]) != 0 and file not in info_data["images"][0]["url"]
    ):  # 未设置封面
        file_name = os.path.basename(file)
        url = next(filter(lambda x: x["type"] == "image", info_data["images"]), {}).get(
            "url"
        )
        download_image(
            url=url, filename=file_name, directory=os.path.dirname(file_path)
        )

    if should_save:
        if "trainedWords" in info_data:
            # Sort by count; if it doesn't exist, then assume it's a top item from civitai or elsewhere.
            info_data["trainedWords"] = sorted(
                info_data["trainedWords"],
                key=lambda w: w["count"] if "count" in w else 99999,
                reverse=True,
            )
        save_model_info(file, info_data, model_type=model_type)

        # If we're saving, then the UI is likely waiting to see if the refreshed data is coming in.
        # await PromptServer.instance.send("weilin-refreshed-lora-info", {"data": info_data})

    return info_data


def download_image(url, filename, directory):
    try:
        # 安全处理文件名
        filename = filename.encode("utf-8", "ignore").decode("utf-8")
        _, ext = os.path.splitext(url)
        filename, _ = os.path.splitext(filename)
        filepath = os.path.join(directory, f"{filename}{ext}")

        try:
            resp = requests.get(url, stream=True)
            resp.raise_for_status()
            with open(filepath, "wb") as f:
                for chunk in resp.iter_content(chunk_size=4096):
                    f.write(chunk)
        except Exception as e:
            print(e)
            if os.path.exists(filepath):
                os.remove(filepath)

    except Exception as e:
        print(f"文件名处理错误: {e}")


def _is_common_tag(tag: str) -> bool:
    """
    判断是否为常见通用标签（非触发词）
    
    这些标签通常出现在训练数据中，但不是真正的触发词
    """
    # 常见通用标签列表（小写）
    common_tags = {
        # 人物相关
        '1girl', '1boy', '2girls', '2boys', '3girls', '3boys', 'multiple girls', 'multiple boys',
        'solo', 'couple', 'group',
        # 身体特征
        'long hair', 'short hair', 'white hair', 'black hair', 'blonde hair', 'brown hair',
        'red hair', 'blue hair', 'green hair', 'pink hair', 'purple hair', 'silver hair',
        'gradient hair', 'multicolored hair', 'two-tone hair',
        'blue eyes', 'green eyes', 'brown eyes', 'red eyes', 'yellow eyes', 'purple eyes',
        'black eyes', 'white eyes', 'orange eyes', 'pink eyes',
        'small breasts', 'medium breasts', 'large breasts', 'huge breasts',
        # 服装相关
        'dress', 'white dress', 'black dress', 'red dress', 'blue dress', 'green dress',
        'school uniform', 'swimsuit', 'bikini', 'maid', 'nurse', 'waitress',
        'skirt', 'shorts', 'pants', 'jeans', 'shirt', 'blouse', 'jacket', 'coat',
        # 姿势相关
        'standing', 'sitting', 'lying', 'walking', 'running', 'jumping',
        'looking at viewer', 'looking away', 'from behind', 'from side', 'from above', 'from below',
        # 背景相关
        'simple background', 'white background', 'black background', 'grey background',
        'outdoors', 'indoors', 'sky', 'cloud', 'tree', 'flower', 'water', 'building',
        # 画面风格
        'highres', 'absurdres', 'best quality', 'high quality', 'normal quality', 'low quality',
        'masterpiece', 'great quality', 'good quality', 'average quality', 'bad quality',
        'worst quality', 'very bad quality',
        # 其他常见标签
        'smile', 'open mouth', 'closed mouth', 'blush', 'tears', 'sweat',
        'gloves', 'shoes', 'boots', 'socks', 'stockings', 'pantyhose',
        'hat', 'headwear', 'hair ornament', 'ribbon', 'bow', 'flower', 'jewelry',
        'bangs', 'ponytail', 'twintails', 'braid', 'ahoge', 'sidelocks',
        'pointy ears', 'animal ears', 'cat ears', 'dog ears', 'rabbit ears', 'fox ears',
        'tail', 'cat tail', 'dog tail', 'fox tail', 'rabbit tail',
        'wings', 'angel wings', 'demon wings', 'fairy wings',
        'no humans', 'scenery', 'landscape', 'cityscape', 'seascape',
    }
    
    tag_lower = tag.lower().strip()
    return tag_lower in common_tags


def _merge_metadata(info_data: dict, data_meta: dict) -> bool:
    """
    合并模型元数据到info_data
    
    优化版：按训练频率排序触发词，与 ComfyUI-Lora-Auto-Trigger-Words 保持一致
    
    Returns true if data was saved.
    """
    should_save = False

    base_model_file = get_dict_value(data_meta, "ss_sd_model_name", None)
    if base_model_file:
        info_data["baseModelFile"] = base_model_file

    # Loop over metadata tags
    trained_words = {}
    if "ss_tag_frequency" in data_meta:
        tag_freq_data = data_meta["ss_tag_frequency"]
        
        # 如果是字符串，需要解析JSON（某些模型存储为JSON字符串）
        if isinstance(tag_freq_data, str):
            try:
                tag_freq_data = json.loads(tag_freq_data)
            except json.JSONDecodeError:
                tag_freq_data = {}
        
        if isinstance(tag_freq_data, dict):
            for bucket_value in tag_freq_data.values():
                if isinstance(bucket_value, dict):
                    for tag, count in bucket_value.items():
                        tag = str(tag).strip()
                        if tag:
                            if tag not in trained_words:
                                trained_words[tag] = {"word": tag, "count": 0, "metadata": True}
                            trained_words[tag]["count"] = trained_words[tag]["count"] + count

    if "trainedWords" not in info_data:
        # 按训练次数降序排序（与 ComfyUI-Lora-Auto-Trigger-Words 保持一致）
        sorted_words = sorted(trained_words.values(), key=lambda x: x["count"], reverse=True)
        
        # 智能过滤：优先保留非通用标签
        # 如果前几个标签都是通用标签，尝试找到第一个非通用标签放在最前面
        filtered_words = []
        non_common_words = []
        
        for word_data in sorted_words:
            if not _is_common_tag(word_data["word"]):
                non_common_words.append(word_data)
            else:
                filtered_words.append(word_data)
        
        # 如果有非通用标签，将它们放在前面
        if non_common_words:
            info_data["trainedWords"] = non_common_words + filtered_words
        else:
            info_data["trainedWords"] = sorted_words
        
        should_save = True
    else:
        # We can't merge, because the list may have other data, like it's part of civitaidata.
        merged_dict = {}
        for existing_word_data in info_data["trainedWords"]:
            merged_dict[existing_word_data["word"]] = existing_word_data
        for new_key, new_word_data in trained_words.items():
            if new_key not in merged_dict:
                merged_dict[new_key] = {}
            merged_dict[new_key] = {**merged_dict[new_key], **new_word_data}
        
        # 按训练次数排序（有count的排前面，没有count的保持原顺序）
        merged_list = list(merged_dict.values())
        merged_list.sort(key=lambda x: x.get("count", 99999), reverse=True)
        
        # 智能过滤：优先保留非通用标签
        filtered_words = []
        non_common_words = []
        
        for word_data in merged_list:
            if not _is_common_tag(word_data.get("word", "")):
                non_common_words.append(word_data)
            else:
                filtered_words.append(word_data)
        
        # 如果有非通用标签，将它们放在前面
        if non_common_words:
            info_data["trainedWords"] = non_common_words + filtered_words
        else:
            info_data["trainedWords"] = merged_list
        
        should_save = True

    # trained_words = list(trained_words.values())
    # info_data['meta_trained_words'] = trained_words
    info_data["raw"]["metadata"] = data_meta
    should_save = True

    if "sha256" not in info_data and "_sha256" in data_meta:
        info_data["sha256"] = data_meta["_sha256"]
        should_save = True

    return should_save


def _merge_civitai_data(info_data: dict, data_civitai: dict) -> bool:
    """
    合并Civitai数据到info_data
    
    优化版：Civitai触发词作为最高优先级，放在trainedWords列表最前面
    
    Returns true if data was saved.
    """
    should_save = False

    if "name" not in info_data:
        info_data["name"] = get_dict_value(data_civitai, "model.name", "")
        should_save = True
        version_name = get_dict_value(data_civitai, "name")
        if version_name is not None:
            info_data["name"] += f" - {version_name}"

    if "type" not in info_data:
        info_data["type"] = get_dict_value(data_civitai, "model.type")
        should_save = True
    if "baseModel" not in info_data:
        info_data["baseModel"] = get_dict_value(data_civitai, "baseModel")
        should_save = True

    # We always want to merge triggerword.
    civitai_trigger = get_dict_value(data_civitai, "triggerWords", default=[])
    civitai_trained = get_dict_value(data_civitai, "trainedWords", default=[])
    civitai_words = ",".join(civitai_trigger + civitai_trained)
    if civitai_words:
        civitai_words = re.sub(r"\s*,\s*", ",", civitai_words)
        civitai_words = re.sub(r",+", ",", civitai_words)
        civitai_words = re.sub(r"^,", "", civitai_words)
        civitai_words = re.sub(r",$", "", civitai_words)
        if civitai_words:
            civitai_words_list = civitai_words.split(",")
            if "trainedWords" not in info_data:
                info_data["trainedWords"] = []
            
            # 创建一个有序字典来保持Civitai触发词的顺序
            existing_words = {data["word"]: data for data in info_data["trainedWords"]}
            
            # 将Civitai触发词插入到列表开头（最高优先级）
            civitai_word_data_list = []
            for trigger_word in civitai_words_list:
                trigger_word = trigger_word.strip()
                if not trigger_word:
                    continue
                if trigger_word in existing_words:
                    # 更新现有条目
                    existing_words[trigger_word]["civitai"] = True
                else:
                    # 创建新条目
                    civitai_word_data_list.append({"word": trigger_word, "civitai": True})
            
            # 合并：Civitai触发词在前，其他触发词在后
            non_civitai_words = [data for data in info_data["trainedWords"] if not data.get("civitai", False)]
            civitai_existing_words = [
                existing_words.get(data["word"], data) 
                for data in info_data["trainedWords"] 
                if data.get("civitai", False) and data["word"] not in {w["word"] for w in civitai_word_data_list}
            ]
            info_data["trainedWords"] = civitai_word_data_list + civitai_existing_words + non_civitai_words
            should_save = True

    if "sha256" not in info_data:
        info_data["sha256"] = data_civitai["_sha256"]
        should_save = True

    if "modelId" in data_civitai:
        info_data["links"] = info_data["links"] if "links" in info_data else []
        civitai_link = (
            f"https://civitai.com/models/{get_dict_value(data_civitai, 'modelId')}"
        )
        if get_dict_value(data_civitai, "id"):
            civitai_link += f"?modelVersionId={get_dict_value(data_civitai, 'id')}"
        info_data["links"].append(civitai_link)
        info_data["links"].append(data_civitai["_civitai_api"])
        should_save = True

    # Take images from civitai
    if "images" in data_civitai:
        info_data_image_urls = list(
            map(lambda i: i["url"] if "url" in i else None, info_data["images"])
        )
        for img in data_civitai["images"]:
            img_url = get_dict_value(img, "url")
            if img_url is not None and img_url not in info_data_image_urls:
                img_id = (
                    os.path.splitext(os.path.basename(img_url))[0]
                    if img_url is not None
                    else None
                )
                img_data = {
                    "url": img_url,
                    "civitaiUrl": (
                        f"https://civitai.com/images/{img_id}"
                        if img_id is not None
                        else None
                    ),
                    "width": get_dict_value(img, "width"),
                    "height": get_dict_value(img, "height"),
                    "type": get_dict_value(img, "type"),
                    "nsfwLevel": get_dict_value(img, "nsfwLevel"),
                    "seed": get_dict_value(img, "meta.seed"),
                    "positive": get_dict_value(img, "meta.prompt"),
                    "negative": get_dict_value(img, "meta.negativePrompt"),
                    "steps": get_dict_value(img, "meta.steps"),
                    "sampler": get_dict_value(img, "meta.sampler"),
                    "cfg": get_dict_value(img, "meta.cfgScale"),
                    "model": get_dict_value(img, "meta.Model"),
                    "resources": get_dict_value(img, "meta.resources"),
                }
                info_data["images"].append(img_data)
                should_save = True

    # The raw data
    if "civitai" not in info_data["raw"]:
        info_data["raw"]["civitai"] = data_civitai
        should_save = True

    return should_save


def _get_model_civitai_data(file: str, model_type="loras", default=None, refresh=False):
    """Gets the civitai data, either cached from the user directory, or from civitai api."""
    file_hash = _get_sha256_hash(get_folder_path(file, model_type))
    if file_hash is None:
        return None

    json_file_path = _get_info_cache_file(file_hash, "civitai")

    api_url = f"https://civitai.com/api/v1/model-versions/by-hash/{file_hash}"
    file_data = read_userdata_json(json_file_path)
    if file_data is None or refresh is True:
        try:
            response = requests.get(api_url, timeout=5000)
            data = response.json()
            save_userdata_json(
                json_file_path,
                {
                    "url": api_url,
                    "timestamp": datetime.now().timestamp(),
                    "response": data,
                },
            )
            file_data = read_userdata_json(json_file_path)
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            print(e)
    response = (
        file_data["response"]
        if file_data is not None and "response" in file_data
        else None
    )
    if response is not None:
        response["_sha256"] = file_hash
        response["_civitai_api"] = api_url
    return response if response is not None else default


def _get_model_metadata(file: str, model_type="loras", default=None, refresh=False):
    """Gets the metadata from the file itself."""
    file_path = get_folder_path(file, model_type)
    file_hash = _get_sha256_hash(file_path)
    if file_hash is None:
        return default

    json_file_path = _get_info_cache_file(file_hash, "metadata")

    file_data = read_userdata_json(json_file_path)
    if file_data is None or refresh is True:
        data = _read_file_metadata_from_header(file_path)
        if data is not None:
            file_data = {
                "url": file,
                "timestamp": datetime.now().timestamp(),
                "response": data,
            }
            save_userdata_json(json_file_path, file_data)
    response = (
        file_data["response"]
        if file_data is not None and "response" in file_data
        else None
    )
    if response is not None:
        response["_sha256"] = file_hash
    return response if response is not None else default


def _read_file_metadata_from_header(file_path: str) -> dict:
    """Reads the file's header and returns a JSON dict metdata if available."""
    data = None
    try:
        if file_path.endswith(".safetensors"):
            with open(file_path, "rb") as file:
                # https://github.com/huggingface/safetensors#format
                # 8 bytes: N, an unsigned little-endian 64-bit integer, containing the size of the header
                header_size = int.from_bytes(file.read(8), "little", signed=False)

                if header_size <= 0:
                    raise BufferError("Invalid header size")

                header = file.read(header_size)
                if header is None:
                    raise BufferError("Invalid header")

                header_json = json.loads(header)
                data = (
                    header_json["__metadata__"]
                    if "__metadata__" in header_json
                    else None
                )

                if data is not None:
                    for key, value in data.items():
                        if (
                            isinstance(value, str)
                            and value.startswith("{")
                            and value.endswith("}")
                        ):
                            try:
                                value_as_json = json.loads(value)
                                data[key] = value_as_json
                            except Exception:
                                print(f"metdata for field {key} did not parse as json")
    except requests.exceptions.RequestException as e:
        print(e)
        data = None

    return data


def _get_sha256_hash(file_path: str):
    """Returns the hash for the file."""
    if not file_path or not path_exists(file_path):
        return None
    file_hash = None
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
        file_hash = sha256_hash.hexdigest()
    return file_hash


async def set_model_info_partial(file: str, info_data_partial, model_type="loras"):
    """Sets partial data into the existing model info data."""
    info_data = await get_model_info(file, model_type=model_type, default={})
    info_data = {**info_data, **info_data_partial}
    save_model_info(file, info_data, model_type=model_type)


def save_model_info(file: str, info_data, model_type="loras"):
    """Saves the model info alongside the model itself."""
    file_path = get_folder_path(file, model_type)
    if file_path is None:
        return
    try_info_path = f"{file_path}.weilin-info.json"
    save_json_file(try_info_path, info_data)


async def remove_user_diy_fields(file: str, fields_to_remove, model_type="loras"):
    """
    从模型的user_diy_fields中删除指定字段

    参数:
        file: 模型文件名
        fields_to_remove: 要删除的字段名，可以是字符串或字符串列表
        model_type: 模型类型，默认为"loras"
    """
    info_data = await get_model_info(file, model_type=model_type, default={})

    if "user_diy_fileds" not in info_data:  # 修正拼写错误
        return False

    if isinstance(fields_to_remove, str):
        fields_to_remove = [fields_to_remove]

    # print(fields_to_remove)
    removed = False
    for field in fields_to_remove:
        if field in info_data["user_diy_fileds"]:
            # print(f'删除字段: {field}')
            del info_data["user_diy_fileds"][field]
            removed = True

    if removed:
        save_model_info(file, info_data, model_type=model_type)

    return removed


def get_dict_value(data: dict, dict_key: str, default=None):
    """Gets a deeply nested value given a dot-delimited key."""
    keys = dict_key.split(".")
    key = keys.pop(0) if len(keys) > 0 else None
    found = data[key] if key in data else None
    if found is not None and len(keys) > 0:
        return get_dict_value(found, ".".join(keys), default)
    return found if found is not None else default


def read_userdata_json(rel_path: str):
    """Reads a json file from the userdata directory."""
    file_path = clean_path(rel_path)
    return load_json_file(file_path)


def save_userdata_json(rel_path: str, data: dict):
    """Saves a json file from the userdata directory."""
    file_path = clean_path(rel_path)
    return save_json_file(file_path, data)


def clean_path(rel_path: str):
    """Cleans a relative path by splitting on forward slash and os.path.joining."""
    cleaned = USERDATA
    paths = rel_path.split("/")
    for path in paths:
        cleaned = os.path.join(cleaned, path)
    return cleaned


def save_json_file(file_path: str, data: dict):
    """Saves a json file."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w+", encoding="UTF-8") as file:
        json.dump(data, file, sort_keys=False, indent=2, separators=(",", ": "))


def _get_info_cache_file(data_type: str, file_hash: str):
    return f"info/{file_hash}.{data_type}.json"


async def delete_model_info(
    file: str, model_type="loras", del_info=True, del_metadata=True, del_civitai=True
):
    """Delete the info json, and the civitai & metadata caches."""
    file_path = get_folder_path(file, model_type)
    if file_path is None:
        return
    if del_info:
        try_info_path = f"{file_path}.weilin-info.json"
        if os.path.isfile(try_info_path):
            os.remove(try_info_path)
    if del_civitai or del_metadata:
        file_hash = _get_sha256_hash(file_path)
        if del_civitai:
            json_file_path = _get_info_cache_file(file_hash, "civitai")
            delete_userdata_file(json_file_path)
        if del_metadata:
            json_file_path = _get_info_cache_file(file_hash, "metadata")
            delete_userdata_file(json_file_path)


def delete_userdata_file(rel_path: str):
    """Deletes a file from the userdata directory."""
    file_path = clean_path(rel_path)
    if os.path.isfile(file_path):
        os.remove(file_path)
