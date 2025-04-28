import folder_paths
import os
import json
import re
import hashlib
import requests
from datetime import datetime

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
USERDATA = os.path.join(THIS_DIR, '../../../', 'lora_userdatas')

# code from rgthree-comfy thanks

def image_upload(post, image_save_function=None):
  image = post.get("image")
  path = post.get("path")
  fileName = post.get("fileName")

  lora_path = folder_paths.get_full_path("loras", path)
  if not path_exists(lora_path):
    lora_path = os.path.abspath(lora_path)

  for ext in ['jpg', 'png', 'jpeg', 'gif']:
    try_path = f'{os.path.splitext(lora_path)[0]}.{ext}'
    if path_exists(try_path):
      os.remove(try_path) #删除已经存在的图片
  
  file_name_with_extension = os.path.basename(lora_path)
  file_namea, _ = os.path.splitext(file_name_with_extension)
  model = file_namea

  upload_dir = os.path.dirname(os.path.abspath(lora_path))

  api_response = {'status': 200}
  
  if image and image.file:
      
      file_name, file_extension = os.path.splitext(fileName)
      
      filepath = os.path.join(upload_dir, model+file_extension)

      with open(filepath, "wb") as f:
        f.write(image.file.read())
      
      api_response['res'] = 'success'
      return api_response
  else:
      api_response['status'] = '404'
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


async def get_loras_info_response(request, maybe_fetch_civitai=False, maybe_fetch_metadata=False):
  """Gets lora info for all or a single lora"""
  api_response = {'status': 200}
  lora_file = get_param(request, 'file')

  if get_param(request, 'light') is not None:
    light = is_param_falsy(request, 'light')
  else:
    light = False
  if lora_file is not None:
    if light:
      info_data = await get_model_info(lora_file,
                                       maybe_fetch_civitai=maybe_fetch_civitai,
                                       maybe_fetch_metadata=maybe_fetch_metadata,
                                       light=light)
    else:
      info_data = await get_model_info(lora_file,
                                       force_fetch_civitai=maybe_fetch_civitai,
                                       force_fetch_metadata=maybe_fetch_metadata,
                                       light=light)
    if info_data is None:
      api_response['status'] = '404'
      api_response['error'] = 'No Lora found at path'
    else:
      api_response['data'] = info_data
  else:
    api_response['data'] = []
    lora_files = folder_paths.get_filename_list("loras")
    for lora_file in lora_files:
      info_data = await get_model_info(lora_file,
                                       maybe_fetch_civitai=maybe_fetch_civitai,
                                       maybe_fetch_metadata=maybe_fetch_metadata,
                                       light=light)
      api_response['data'].append(info_data)
  return api_response



def load_json_file(file: str, default=None):
  """Reads a json file and returns the json dict, stripping out "//" comments first."""
  if path_exists(file):
    with open(file, 'r', encoding='UTF-8') as file:
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
  if 'triggerWords' in info_data and len(info_data['triggerWords']) > 0:
    civitai_words = ','.join((get_dict_value(info_data, 'raw.civitai.triggerWords', default=[]) +
                              get_dict_value(info_data, 'raw.civitai.trainedWords', default=[])))
    if 'trainedWords' not in info_data:
      info_data['trainedWords'] = []
    for trigger_word in info_data['triggerWords']:
      word_data = next((data for data in info_data['trainedWords'] if data['word'] == trigger_word),
                       None)
      if word_data is None:
        word_data = {'word': trigger_word}
        info_data['trainedWords'].append(word_data)
      if trigger_word in civitai_words:
        word_data['civitai'] = True
      else:
        word_data['user'] = True

    del info_data['triggerWords']
    should_save = True
  return should_save

async def get_model_info(file: str,
                         model_type="loras",
                         default=None,
                         maybe_fetch_civitai=False,
                         force_fetch_civitai=False,
                         maybe_fetch_metadata=False,
                         force_fetch_metadata=False,
                         light=False):
  """Compiles a model info given a stored file next to the model, and/or metadata/civitai."""

  file_path = get_folder_path(file, model_type)
  if file_path is None:
    return default

  info_data = {}
  should_save = False
  # Try to load a weilin-info.json file next to the file.
  try_info_path = f'{file_path}.weilin-info.json'
  if path_exists(try_info_path):
    info_data = load_json_file(try_info_path)

  if 'file' not in info_data:
    info_data['file'] = file
    should_save = True
  if 'path' not in info_data:
    info_data['path'] = file_path
    should_save = True

  # Check if we have an image next to the file and, if so, add it to the front of the images
  # (if it isn't already).
  img_next_to_file = None
  for ext in ['jpg', 'png', 'jpeg']:
    try_path = f'{os.path.splitext(file_path)[0]}.{ext}'
    if path_exists(try_path):
      img_next_to_file = try_path
      break

  if 'images' not in info_data:
    info_data['images'] = []
    should_save = True

  if img_next_to_file:
    img_next_to_file_url = f'/weilin/prompt_ui/api/lorainfo/api/loras/img?file={file}'
    if len(info_data['images']) == 0 or info_data['images'][0]['url'] != img_next_to_file_url:
      info_data['images'].insert(0, {'url': img_next_to_file_url})
      should_save = True

  # If we just want light data then bail now with just existing data, plus file, path and img if
  # next to the file.
  if light and not maybe_fetch_metadata and not force_fetch_metadata and not maybe_fetch_civitai and not force_fetch_civitai:
    return info_data

  if 'raw' not in info_data:
    info_data['raw'] = {}
    should_save = True

  should_save = _update_data(info_data) or should_save

  should_fetch_civitai = force_fetch_civitai is True or (maybe_fetch_civitai is True and
                                                         ('civitai' not in info_data['raw'] or len(info_data['raw']['civitai']) == 0))
  should_fetch_metadata = force_fetch_metadata is True or (maybe_fetch_metadata is True and
                                                           ('metadata' not in info_data['raw'] or len(info_data['raw']['metadata']) == 0))

  if should_fetch_metadata:
    data_meta = _get_model_metadata(file,
                                    model_type=model_type,
                                    default={},
                                    refresh=force_fetch_metadata)
    should_save = _merge_metadata(info_data, data_meta) or should_save

  if should_fetch_civitai:
    data_civitai = _get_model_civitai_data(file,
                                           model_type=model_type,
                                           default={},
                                           refresh=force_fetch_civitai)
    should_save = _merge_civitai_data(info_data, data_civitai) or should_save

  if 'sha256' not in info_data:
    file_hash = _get_sha256_hash(file_path)
    if file_hash is not None:
      info_data['sha256'] = file_hash
      should_save = True

  if should_save:
    if 'trainedWords' in info_data:
      # Sort by count; if it doesn't exist, then assume it's a top item from civitai or elsewhere.
      info_data['trainedWords'] = sorted(info_data['trainedWords'],
                                         key=lambda w: w['count'] if 'count' in w else 99999,
                                         reverse=True)
    save_model_info(file, info_data, model_type=model_type)

    # If we're saving, then the UI is likely waiting to see if the refreshed data is coming in.
    # await PromptServer.instance.send("weilin-refreshed-lora-info", {"data": info_data})

  return info_data


def _merge_metadata(info_data: dict, data_meta: dict) -> bool:
  """Returns true if data was saved."""
  should_save = False

  base_model_file = get_dict_value(data_meta, 'ss_sd_model_name', None)
  if base_model_file:
    info_data['baseModelFile'] = base_model_file

  # Loop over metadata tags
  trained_words = {}
  if 'ss_tag_frequency' in data_meta and isinstance(data_meta['ss_tag_frequency'], dict):
    for bucket_value in data_meta['ss_tag_frequency'].values():
      if isinstance(bucket_value, dict):
        for tag, count in bucket_value.items():
          if tag not in trained_words:
            trained_words[tag] = {'word': tag, 'count': 0, 'metadata': True}
          trained_words[tag]['count'] = trained_words[tag]['count'] + count

  if 'trainedWords' not in info_data:
    info_data['trainedWords'] = list(trained_words.values())
    should_save = True
  else:
    # We can't merge, because the list may have other data, like it's part of civitaidata.
    merged_dict = {}
    for existing_word_data in info_data['trainedWords']:
      merged_dict[existing_word_data['word']] = existing_word_data
    for new_key, new_word_data in trained_words.items():
      if new_key not in merged_dict:
        merged_dict[new_key] = {}
      merged_dict[new_key] = {**merged_dict[new_key], **new_word_data}
    info_data['trainedWords'] = list(merged_dict.values())
    should_save = True

  # trained_words = list(trained_words.values())
  # info_data['meta_trained_words'] = trained_words
  info_data['raw']['metadata'] = data_meta
  should_save = True

  if 'sha256' not in info_data and '_sha256' in data_meta:
    info_data['sha256'] = data_meta['_sha256']
    should_save = True

  return should_save


def _merge_civitai_data(info_data: dict, data_civitai: dict) -> bool:
  """Returns true if data was saved."""
  should_save = False

  if 'name' not in info_data:
    info_data['name'] = get_dict_value(data_civitai, 'model.name', '')
    should_save = True
    version_name = get_dict_value(data_civitai, 'name')
    if version_name is not None:
      info_data['name'] += f' - {version_name}'

  if 'type' not in info_data:
    info_data['type'] = get_dict_value(data_civitai, 'model.type')
    should_save = True
  if 'baseModel' not in info_data:
    info_data['baseModel'] = get_dict_value(data_civitai, 'baseModel')
    should_save = True

  # We always want to merge triggerword.
  civitai_trigger = get_dict_value(data_civitai, 'triggerWords', default=[])
  civitai_trained = get_dict_value(data_civitai, 'trainedWords', default=[])
  civitai_words = ','.join(civitai_trigger + civitai_trained)
  if civitai_words:
    civitai_words = re.sub(r"\s*,\s*", ",", civitai_words)
    civitai_words = re.sub(r",+", ",", civitai_words)
    civitai_words = re.sub(r"^,", "", civitai_words)
    civitai_words = re.sub(r",$", "", civitai_words)
    if civitai_words:
      civitai_words = civitai_words.split(',')
      if 'trainedWords' not in info_data:
        info_data['trainedWords'] = []
      for trigger_word in civitai_words:
        word_data = next(
          (data for data in info_data['trainedWords'] if data['word'] == trigger_word), None)
        if word_data is None:
          word_data = {'word': trigger_word}
          info_data['trainedWords'].append(word_data)
        word_data['civitai'] = True

  if 'sha256' not in info_data:
    info_data['sha256'] = data_civitai['_sha256']
    should_save = True

  if 'modelId' in data_civitai:
    info_data['links'] = info_data['links'] if 'links' in info_data else []
    civitai_link = f'https://civitai.com/models/{get_dict_value(data_civitai, "modelId")}'
    if get_dict_value(data_civitai, "id"):
      civitai_link += f'?modelVersionId={get_dict_value(data_civitai, "id")}'
    info_data['links'].append(civitai_link)
    info_data['links'].append(data_civitai['_civitai_api'])
    should_save = True

  # Take images from civitai
  if 'images' in data_civitai:
    info_data_image_urls = list(map(lambda i: i['url']
                                    if 'url' in i else None, info_data['images']))
    for img in data_civitai['images']:
      img_url = get_dict_value(img, 'url')
      if img_url is not None and img_url not in info_data_image_urls:
        img_id = os.path.splitext(os.path.basename(img_url))[0] if img_url is not None else None
        img_data = {
          'url': img_url,
          'civitaiUrl': f'https://civitai.com/images/{img_id}' if img_id is not None else None,
          'width': get_dict_value(img, 'width'),
          'height': get_dict_value(img, 'height'),
          'type': get_dict_value(img, 'type'),
          'nsfwLevel': get_dict_value(img, 'nsfwLevel'),
          'seed': get_dict_value(img, 'meta.seed'),
          'positive': get_dict_value(img, 'meta.prompt'),
          'negative': get_dict_value(img, 'meta.negativePrompt'),
          'steps': get_dict_value(img, 'meta.steps'),
          'sampler': get_dict_value(img, 'meta.sampler'),
          'cfg': get_dict_value(img, 'meta.cfgScale'),
          'model': get_dict_value(img, 'meta.Model'),
          'resources': get_dict_value(img, 'meta.resources'),
        }
        info_data['images'].append(img_data)
        should_save = True

  # The raw data
  if 'civitai' not in info_data['raw']:
    info_data['raw']['civitai'] = data_civitai
    should_save = True

  return should_save


def _get_model_civitai_data(file: str, model_type="loras", default=None, refresh=False):
  """Gets the civitai data, either cached from the user directory, or from civitai api."""
  file_hash = _get_sha256_hash(get_folder_path(file, model_type))
  if file_hash is None:
    return None

  json_file_path = _get_info_cache_file(file_hash, 'civitai')

  api_url = f'https://civitai.com/api/v1/model-versions/by-hash/{file_hash}'
  file_data = read_userdata_json(json_file_path)
  if file_data is None or refresh is True:
    try:
      response = requests.get(api_url, timeout=5000)
      data = response.json()
      save_userdata_json(json_file_path, {
        'url': api_url,
        'timestamp': datetime.now().timestamp(),
        'response': data
      })
      file_data = read_userdata_json(json_file_path)
    except requests.exceptions.RequestException as e:  # This is the correct syntax
      print(e)
  response = file_data['response'] if file_data is not None and 'response' in file_data else None
  if response is not None:
    response['_sha256'] = file_hash
    response['_civitai_api'] = api_url
  return response if response is not None else default


def _get_model_metadata(file: str, model_type="loras", default=None, refresh=False):
  """Gets the metadata from the file itself."""
  file_path = get_folder_path(file, model_type)
  file_hash = _get_sha256_hash(file_path)
  if file_hash is None:
    return default

  json_file_path = _get_info_cache_file(file_hash, 'metadata')

  file_data = read_userdata_json(json_file_path)
  if file_data is None or refresh is True:
    data = _read_file_metadata_from_header(file_path)
    if data is not None:
      file_data = {'url': file, 'timestamp': datetime.now().timestamp(), 'response': data}
      save_userdata_json(json_file_path, file_data)
  response = file_data['response'] if file_data is not None and 'response' in file_data else None
  if response is not None:
    response['_sha256'] = file_hash
  return response if response is not None else default


def _read_file_metadata_from_header(file_path: str) -> dict:
  """Reads the file's header and returns a JSON dict metdata if available."""
  data = None
  try:
    if file_path.endswith('.safetensors'):
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
        data = header_json["__metadata__"] if "__metadata__" in header_json else None

        if data is not None:
          for key, value in data.items():
            if isinstance(value, str) and value.startswith('{') and value.endswith('}'):
              try:
                value_as_json = json.loads(value)
                data[key] = value_as_json
              except Exception:
                print(f'metdata for field {key} did not parse as json')
  except requests.exceptions.RequestException as e:
    print(e)
    data = None

  return data


def get_folder_path(file: str, model_type="loras"):
  """Gets the file path ensuring it exists."""
  file_path = folder_paths.get_full_path(model_type, file)
  if file_path and not path_exists(file_path):
    file_path = os.path.abspath(file_path)
  if not path_exists(file_path):
    file_path = None
  return file_path


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
  try_info_path = f'{file_path}.weilin-info.json'
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
    
    if 'user_diy_fileds' not in info_data:  # 修正拼写错误
      return False

    if isinstance(fields_to_remove, str):
      fields_to_remove = [fields_to_remove]
    
    # print(fields_to_remove)
    removed = False
    for field in fields_to_remove:
      if field in info_data['user_diy_fileds']:
        # print(f'删除字段: {field}')
        del info_data['user_diy_fileds'][field]
        removed = True
    
    if removed:
      save_model_info(file, info_data, model_type=model_type)
    
    return removed


def get_dict_value(data: dict, dict_key: str, default=None):
  """ Gets a deeply nested value given a dot-delimited key."""
  keys = dict_key.split('.')
  key = keys.pop(0) if len(keys) > 0 else None
  found = data[key] if key in data else None
  if found is not None and len(keys) > 0:
    return get_dict_value(found, '.'.join(keys), default)
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
  paths = rel_path.split('/')
  for path in paths:
    cleaned = os.path.join(cleaned, path)
  return cleaned


def save_json_file(file_path: str, data: dict):
  """Saves a json file."""
  os.makedirs(os.path.dirname(file_path), exist_ok=True)
  with open(file_path, 'w+', encoding='UTF-8') as file:
    json.dump(data, file, sort_keys=False, indent=2, separators=(",", ": "))



def _get_info_cache_file(data_type: str, file_hash: str):
  return f'info/{file_hash}.{data_type}.json'


async def delete_model_info(file: str,
                            model_type="loras",
                            del_info=True,
                            del_metadata=True,
                            del_civitai=True):
  """Delete the info json, and the civitai & metadata caches."""
  file_path = get_folder_path(file, model_type)
  if file_path is None:
    return
  if del_info:
    try_info_path = f'{file_path}.weilin-info.json'
    if os.path.isfile(try_info_path):
      os.remove(try_info_path)
  if del_civitai or del_metadata:
    file_hash = _get_sha256_hash(file_path)
    if del_civitai:
      json_file_path = _get_info_cache_file(file_hash, 'civitai')
      delete_userdata_file(json_file_path)
    if del_metadata:
      json_file_path = _get_info_cache_file(file_hash, 'metadata')
      delete_userdata_file(json_file_path)


def delete_userdata_file(rel_path: str):
  """Deletes a file from the userdata directory."""
  file_path = clean_path(rel_path)
  if os.path.isfile(file_path):
    os.remove(file_path)
