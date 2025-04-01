import os
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
JSON_FILE_PATH = os.path.join(current_dir, '../../../user_cloud_package.json')

def save_package_path(path: str) -> int:
    """
    保存package路径到JSON文件
    :param path: 要保存的路径字符串
    :return: 0表示保存成功，1表示路径已存在
    """
    # 如果文件不存在，创建空列表
    if not os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)

    # 读取现有数据
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 检查路径是否已存在
    if path in data:
        return 1

    # 添加新路径并保存
    data.append(path)
    with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return 0


def get_package_paths() -> list:
    """
    获取所有已保存的package路径
    :return: 包含所有路径的列表，如果文件不存在则创建并返回空列表
    """
    # 如果文件不存在，创建空列表
    if not os.path.exists(JSON_FILE_PATH):
        with open(JSON_FILE_PATH, 'w', encoding='utf-8') as f:
            json.dump([], f)
        return []

    # 读取并返回数据
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)