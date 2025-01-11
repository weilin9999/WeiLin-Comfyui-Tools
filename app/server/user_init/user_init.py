import os
import json
from ..dao.dao import set_language

current_dir = os.path.dirname(os.path.abspath(__file__))
init_file_path = os.path.join(current_dir, '../../../init.json')


default_settings = {
    "user_lang": "zh_CN",
    "select_openai": 0,
    "openai_settings": [
        {
            "api_key": "",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o"
        },
        {
            "api_key": "",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-4o-mini"
        },
        {
            "api_key": "",
            "base_url": "https://api.openai.com/v1",
            "model": "o1"
        },
        {
            "api_key": "",
            "base_url": "https://api.openai.com/v1",
            "model": "go1-mini"
        },
        {
            "api_key": "",
            "base_url": "https://api.openai.com/v1",
            "model": "gpt-3.5-turbo"
        },
        {
            "api_key": "",
            "base_url": "https://api.deepseek.com/v1",
            "model": "deepseek-chat"
        }
    ]
}

def read_init_file():
    """读取 init.json 文件中的所有设置"""
    if not os.path.exists(init_file_path):
        with open(init_file_path, 'w', encoding='utf-8') as f:
            json.dump(default_settings, f, ensure_ascii=False, indent=4)
        return default_settings
    
    with open(init_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data

def set_user_lang(lang):
    """修改 init.json 文件中的 user_lang 设置"""
    data = read_init_file() or {}
    
    data['user_lang'] = lang
    
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # 修改 DAO 中的语言设置
    set_language(lang)