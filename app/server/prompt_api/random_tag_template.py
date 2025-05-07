import json
import os
import datetime
import random
from typing import List
from ..dao.dao import tags_db_path
import sqlite3

current_dir = os.path.dirname(os.path.abspath(__file__))
init_file_path = os.path.join(current_dir, '../../../random_tag')
def save_template(data):
    """
    保存模板到random_tag文件夹
    
    参数:
        name: 文件名前缀(可选)
        data: 要保存的字典数据
    """
    try:
        # 检查random_tag文件夹是否存在，不存在则创建
        if not os.path.exists(init_file_path):
            os.makedirs(init_file_path)
            
        # 生成时间戳文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_name = timestamp
        file_path = os.path.join(init_file_path, f"{file_name}.json")
        
        # 检查文件是否已存在
        if os.path.exists(file_path):
            print("文件已存在")
            raise Exception("文件已存在")
            
        # 写入JSON文件
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return {"code": 200, "path_name": str(file_name)}
        
    except Exception as e:
        print(str(e))
        raise Exception(str(e))


def update_template(name: str, data):
    """
    更新random_tag文件夹中的模板文件
    
    参数:
        name: 文件名(不带.json后缀)
        data: 要更新的字典数据
    """
    try:
        # 构建完整文件路径
        file_path = os.path.join(init_file_path, f"{name}.json")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise Exception("文件不存在")
            
        # 写入JSON文件(覆盖更新)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        return {"code": 200, "path_name": str(name)}
        
    except Exception as e:
        raise Exception(str(e))



def delete_template(name: str):
    """
    删除random_tag文件夹中的模板文件
    
    参数:
        name: 文件名(不带.json后缀)
    """
    try:
        # 构建完整文件路径
        file_path = os.path.join(init_file_path, f"{name}.json")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise Exception("文件不存在")
            
        # 删除文件
        os.remove(file_path)
        
        return {"code": 200, "message": "文件删除成功", "path_name": str(name)}
        
    except Exception as e:
        raise Exception(str(e))


def get_template_list():
    """
    获取random_tag文件夹中的JSON文件列表
    返回格式: [{"file_name": "", "path_name": ""}]
    """
    try:
        # 检查random_tag文件夹是否存在
        if not os.path.exists(init_file_path):
            return {"code": 200, "data": []}
            
        # 获取所有JSON文件
        file_list = []
        for filename in os.listdir(init_file_path):
            if filename.endswith('.json'):
                file_path = os.path.join(init_file_path, filename)
                try:
                    # 读取JSON文件获取file_name字段
                    with open(file_path, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        file_name = data.get('file_name', '')
                except:
                    file_name = ''
                
                file_list.append({
                    "file_name": file_name,
                    "path_name": filename.replace('.json', '')
                })
        
        return {"code": 200, "data": file_list}
        
    except Exception as e:
        raise Exception(str(e))

def get_template_data(name: str):
    """
    获取指定模板文件的JSON数据
    
    参数:
        name: 文件名(不带.json后缀)
    返回:
        包含文件数据的字典，如果文件不存在或读取失败则返回错误信息
    """
    try:
        # 构建完整文件路径
        file_path = os.path.join(init_file_path, f"{name}.json")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise Exception("文件不存在")
            
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return {"code": 200, "data": data, "path_name": str(name)}
        
    except Exception as e:
        raise Exception(str(e))


def get_random_tags_by_group(p_uuid: str) -> List[str]:
    """根据group的p_uuid获取随机标签"""
    conn = sqlite3.connect(tags_db_path)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.text FROM tag_tags t
        JOIN tag_subgroups sg ON t.subgroup_id = sg.id_index
        WHERE sg.p_uuid = ?
    ''', (p_uuid,))
    results = cursor.fetchall()
    return [row[0] for row in results]

def get_random_tags_by_subgroup(g_uuid: str) -> List[str]:
    """根据subgroup的g_uuid获取随机标签"""
    conn = sqlite3.connect(tags_db_path)
    cursor =  conn.cursor()
    cursor.execute('''
        SELECT text FROM tag_tags WHERE g_uuid = ?
    ''', (g_uuid,))
    results = cursor.fetchall()
    return [row[0] for row in results]

def shuffle_and_select(tags: List[str], count: int) -> List[str]:
    """随机打乱并选择指定数量的标签"""
    random.shuffle(tags)
    return tags[:count]

def generate_random_tags(data: dict) -> str:
    """生成随机标签字符串"""
    result = []
    
    for rule in data['rules']:
        min_count = rule['range']['min']
        max_count = rule['range']['max']
        count = max_count - min_count + 1
        
        if rule['type'] == 'category':
            tags = []
            for group in rule['tagGroupList']:
                if group['sub']:
                    tags.extend(get_random_tags_by_subgroup(group['sub']['g_uuid']))
                else:
                    tags.extend(get_random_tags_by_group(group['group']['p_uuid']))
            selected_tags = shuffle_and_select(tags, count)
            result.extend(selected_tags)
            
        elif rule['type'] == 'specific':
            tags = rule['specificTags']
            selected_tags = shuffle_and_select(tags, min(count, len(tags)))
            result.extend(selected_tags)
    
    return ','.join(result) + ','


def go_radom_template(name: str):
    try:
        # 构建完整文件路径
        file_path = os.path.join(init_file_path, f"{name}.json")
        
        # 检查文件是否存在
        if not os.path.exists(file_path):
            raise Exception("文件不存在")
            
        # 读取JSON文件
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # 生成随机标签
        random_tags = generate_random_tags(data)
        
        return {"code": 200, "random_tags": random_tags, "path_name": str(name)}
        
    except Exception as e:
        raise Exception(str(e))