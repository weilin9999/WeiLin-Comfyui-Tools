import os
import json
import uuid
import time

# 获取 history_datas.json 文件的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
history_file_path = os.path.join(
    current_dir, '../../../history_userdatas/history_datas.json')


def read_history():
    """读取 history_datas.json 文件并返回内容"""
    if os.path.exists(history_file_path):
        with open(history_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    else:
        return []


def add_history(tag, name="", color=""):
    """添加新的历史记录到 history_datas.json 文件"""
    new_entry = {
        "name": name,
        "color": color,
        "id_index": str(uuid.uuid4()),
        "create_time": int(time.time()),
        "tag": tag
    }

    data = read_history()
    data.append(new_entry)

    with open(history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return {"info": "Append"}


def delete_history(id_index):
    """删除指定 id_index 的历史记录"""
    data = read_history()
    data = [entry for entry in data if entry['id_index'] != id_index]

    with open(history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return {"info": "Deleted"}

def batch_delete_history(id_indices):
    """批量删除指定 id_index 的历史记录"""
    data = read_history()
    data = [entry for entry in data if entry['id_index'] not in id_indices]
    
    with open(history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return {"info": "Batch Deleted"}
