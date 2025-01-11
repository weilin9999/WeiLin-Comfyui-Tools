import json
import os
from aiohttp import web

# 默认配置
config = {
    "api_key": "",
    "api_base_url": "",
    "model": ""
}

init_file_path = os.path.join(os.path.dirname(
    os.path.abspath(__file__)), '../../../init.json')


def load_init_settings():
    """加载 init.json 文件中的设置"""
    with open(init_file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_init_settings(settings):
    """保存设置到 init.json 文件"""
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(settings, f, ensure_ascii=False, indent=4)


def update_openai_settings(index, api_key=None, base_url=None, model=None):
    """修改 openai_settings 内的参数"""
    settings = load_init_settings()
    if 0 <= index < len(settings['openai_settings']):
        if api_key:
            settings['openai_settings'][index]['api_key'] = api_key
        if base_url:
            settings['openai_settings'][index]['base_url'] = base_url
        if model:
            settings['openai_settings'][index]['model'] = model
        save_init_settings(settings)


def add_openai_setting(api_key, base_url, model):
    """新增 openai_settings 内的参数"""
    settings = load_init_settings()
    settings['openai_settings'].append({
        "api_key": api_key,
        "base_url": base_url,
        "model": model
    })
    save_init_settings(settings)


def delete_openai_setting(index):
    """删除 openai_settings 内的参数"""
    settings = load_init_settings()
    if 0 <= index < len(settings['openai_settings']):
        settings['openai_settings'].pop(index)
        save_init_settings(settings)


def set_select_openai(index):
    """设置 select_openai 的值并重新初始化 config"""
    settings = load_init_settings()
    if 0 <= index < len(settings['openai_settings']):
        settings['select_openai'] = index
        save_init_settings(settings)



def initialize_config():
    """初始化 config"""
    settings = load_init_settings()
    index = settings.get('select_openai', 0)
    if 0 <= index < len(settings['openai_settings']):
        return settings['openai_settings'][index]
    return config
