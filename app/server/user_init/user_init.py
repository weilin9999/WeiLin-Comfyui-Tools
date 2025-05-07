import os
import json
import locale

current_dir = os.path.dirname(os.path.abspath(__file__))
init_file_path = os.path.join(current_dir, '../../../init.json')

# 检测系统语言
localLan = locale.getdefaultlocale()[0]
localLan = "zh_CN"
if localLan != "zh_CN":
    localLan = "en_US"

default_settings = {
    "user_lang": localLan,
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
    ],
    "translate_setting": "network",
    "translate_service": "alibaba",
    "translate_source_lang": "en",
    "translate_target_lang": "zh",
    "show_auto_limit": 25,
    "random_template": "",
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
    from ..dao.dao import set_language

    """修改 init.json 文件中的 user_lang 设置"""
    data = read_init_file() or {}
    
    data['user_lang'] = lang
    
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    # 修改 DAO 中的语言设置
    set_language(lang)

    
def get_translate_setting():
    """获取translate_setting参数，如果不存在则添加默认值"""
    data = read_init_file() or {}
    
    # 如果不存在translate_setting参数，则添加默认值
    if 'translate_setting' not in data:
        data['translate_setting'] = 'network'
        with open(init_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return data['translate_setting']

def update_translate_setting(new_setting):
    """更新translate_setting参数"""
    data = read_init_file() or {}
    data['translate_setting'] = new_setting
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True

def get_translate_settings():
    """获取翻译相关参数，如果不存在则添加默认值"""
    data = read_init_file() or {}
    
    # 如果不存在相关参数，则添加默认值
    if 'translate_service' not in data:
        data['translate_service'] = 'alibaba'
    if 'translate_source_lang' not in data:
        data['translate_source_lang'] = 'en'
    if 'translate_target_lang' not in data:
        data['translate_target_lang'] = 'zh'
        
    # 如果有新增参数，则保存到文件
    if any(key not in data for key in ['translate_service', 'translate_source_lang', 'translate_target_lang']):
        with open(init_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return {
        'translate_service': data['translate_service'],
        'translate_source_lang': data['translate_source_lang'],
        'translate_target_lang': data['translate_target_lang']
    }

def update_translate_settings(service=None, source_lang=None, target_lang=None):
    """更新翻译相关参数"""
    data = read_init_file() or {}
    
    if service is not None:
        data['translate_service'] = service
    if source_lang is not None:
        data['translate_source_lang'] = source_lang
    if target_lang is not None:
        data['translate_target_lang'] = target_lang
        
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True

def get_auto_limit_setting():
    """获取show_auto_limit参数，如果不存在则添加默认值"""
    data = read_init_file() or {}
    
    # 如果不存在show_auto_limit参数，则添加默认值
    if 'show_auto_limit' not in data:
        data['show_auto_limit'] = 25
        with open(init_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return data['show_auto_limit']

def update_auto_limit_setting(new_setting: int):
    """更新show_auto_limit参数"""
    data = read_init_file() or {}
    data['show_auto_limit'] = new_setting
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True



def get_random_template_setting():
    """获取random_template参数，如果不存在则添加默认值"""
    data = read_init_file() or {}
    
    # 如果不存在random_template参数，则添加默认值
    if 'random_template' not in data:
        data['random_template'] = ""
        with open(init_file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    return data['random_template']

def update_random_template_setting(new_setting):
    """更新random_template参数"""
    data = read_init_file() or {}
    data['random_template'] = new_setting
    with open(init_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True