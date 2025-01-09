import os
import json
import uuid
import time

# 获取 collect_history_datas.json 文件的路径
current_dir = os.path.dirname(os.path.abspath(__file__))
collect_history_file_path = os.path.join(current_dir, '../../../history_userdatas/collect_history_datas.json')

def read_collect_history():
    """读取 collect_history_datas.json 文件并返回内容"""
    if os.path.exists(collect_history_file_path):
        with open(collect_history_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    else:
        return []

def add_collect_history(tag, name="", color=""):
    """添加新的历史记录到 collect_history_datas.json 文件"""
    data = read_collect_history()
    # 检查是否存在相同的 tag
    for entry in data:
        if entry['tag'] == tag:
            return {"code": 201}
    
    new_entry = {
        "name": name,
        "color": color,
        "id_index": str(uuid.uuid4()),
        "create_time": int(time.time()),
        "tag": tag
    }
    
    data = read_collect_history()
    data.append(new_entry)
    
    with open(collect_history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return new_entry

def delete_collect_history(id_index):
    """删除指定 id_index 的历史记录"""
    data = read_collect_history()
    data = [entry for entry in data if entry['id_index'] != id_index]
    
    with open(collect_history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return {"info": "Deleted"}

def batch_delete_collect_history(id_indices):
    """批量删除指定 id_index 的历史记录"""
    data = read_collect_history()
    data = [entry for entry in data if entry['id_index'] not in id_indices]
    
    with open(collect_history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return {"info": "Batch Deleted"}


def edit_collect_history(id_index, name=None, color=None, tag=None):
    """编辑指定 id_index 的历史记录"""
    data = read_collect_history()
    for entry in data:
        if entry['id_index'] == id_index:
            if name is not None:
                entry['name'] = name
            if color is not None:
                entry['color'] = color
            if tag is not None:
                entry['tag'] = tag
            break
    
    with open(collect_history_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    return {"info": "Edited"}

