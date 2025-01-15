import time
import uuid
from ruamel.yaml import YAML
import sqlite3
from ..dao.dao import get_db_path

def create_tables_for_json_util(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tag_groups (
            id_index INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            color TEXT,
            create_time INTEGER
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tag_subgroups (
            id_index INTEGER PRIMARY KEY AUTOINCREMENT,
            group_id INTEGER,
            name TEXT,
            color TEXT,
            create_time INTEGER,
            FOREIGN KEY (group_id) REFERENCES tag_groups (id_index)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tag_tags (
            id_index INTEGER PRIMARY KEY AUTOINCREMENT,
            subgroup_id INTEGER,
            text TEXT,
            desc TEXT,
            color TEXT,
            create_time INTEGER,
            FOREIGN KEY (subgroup_id) REFERENCES tag_subgroups (id_index)
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def fetch_last_insert_id_for_json_util(cursor):
    """获取最后插入的 id"""
    cursor.execute('SELECT last_insert_rowid()')
    result = cursor.fetchone()
    return result[0] if result else None

def get_current_timestamp_for_json_util():
    return int(time.time())

def get_or_insert_tag_group(db_path, group):
    """获取或插入 tag_group 数据"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = '''
        SELECT id_index FROM tag_groups WHERE name = ?
    '''
    cursor.execute(query, (group['name'],))
    result = cursor.fetchone()
    if result:
        group_id = result[0]
    else:
        query = '''
            INSERT INTO tag_groups (name, color, create_time)
            VALUES (?, ?, ?)
        '''
        cursor.execute(query, (group['name'], group['color'], get_current_timestamp_for_json_util()))
        group_id = fetch_last_insert_id_for_json_util(cursor)
    conn.commit()
    conn.close()
    return group_id

def get_or_insert_tag_subgroup(db_path, group_id, subgroup):
    """获取或插入 tag_subgroup 数据"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = '''
        SELECT id_index FROM tag_subgroups WHERE name = ? AND group_id = ?
    '''
    cursor.execute(query, (subgroup['name'], group_id))
    result = cursor.fetchone()
    if result:
        subgroup_id = result[0]
    else:
        query = '''
            INSERT INTO tag_subgroups (group_id, name, color, create_time)
            VALUES (?, ?, ?, ?)
        '''
        cursor.execute(query, (group_id, subgroup['name'], subgroup['color'], get_current_timestamp_for_json_util()))
        subgroup_id = fetch_last_insert_id_for_json_util(cursor)
    conn.commit()
    conn.close()
    return subgroup_id

def insert_tag_if_not_exists(db_path, subgroup_id, tag):
    """插入 tag 数据，如果 text 不存在"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query = '''
        SELECT id_index FROM tag_tags WHERE text = ? AND subgroup_id = ?
    '''
    cursor.execute(query, (tag['text'], subgroup_id))
    result = cursor.fetchone()
    if not result:
        query = '''
            INSERT INTO tag_tags (subgroup_id, text, desc, color, create_time)
            VALUES (?, ?, ?, ?, ?)
        '''
        cursor.execute(query, (subgroup_id, tag['text'], tag['desc'], tag['color'], get_current_timestamp_for_json_util()))
    conn.commit()
    conn.close()

def load_json_to_db(db_path, json_data):
    """将指定语言文件中的数据写入到数据库中"""
    create_tables_for_json_util(db_path)
    
    # 插入数据到数据库
    for group in json_data:
        group_id = get_or_insert_tag_group(db_path, group)
        for subgroup in group.get('groups', []):
            subgroup_id = get_or_insert_tag_subgroup(db_path, group_id, subgroup)
            for tag in subgroup.get('tags', []):
                insert_tag_if_not_exists(db_path, subgroup_id, tag)

def generate_unique_id():
    return str(uuid.uuid4())

def generate_unique_timestamp():
    return int(time.time() * 1000) + uuid.uuid4().int % 1000


def convert_yaml_to_json(yaml_file):
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.width = 100000  # 防止自动换行
    with open(yaml_file, 'r', encoding='utf8') as f:
        yaml_data = yaml.load(f)

    json_data = []
    for item in yaml_data:
        name = item.get('name')
        color = item.get('color', 'rgba(255, 123, 2, .4)')
        groups = item.get('groups', [])
        id_index = generate_unique_id()
        create_time = generate_unique_timestamp()
        
        new_groups = []
        for group in groups:
            group_name = group.get('name')
            group_color = group.get('color', 'rgba(255, 123, 2, .4)')
            group_color = color if group_color is None else group_color
            tags = group.get('tags', {})
            
            new_tags = []
            for text, desc in tags.items():
                new_tags.append({
                    "text": text,
                    "desc": desc,
                    "color": group_color,
                    "id_index": generate_unique_id(),
                    "create_time": generate_unique_timestamp()
                })
            
            new_groups.append({
                "name": group_name,
                "color": group_color,
                "tags": new_tags,
                "id_index": generate_unique_id(),
                "create_time": generate_unique_timestamp()
            })
        
        json_data.append({
            "name": name,
            "color": color,
            "groups": new_groups,
            "id_index": id_index,
            "create_time": create_time
        })
    return json_data

def mergerDataToDb(yaml_file):
    """
    将YAML文件数据合并到数据库
    :param yaml_file: YAML文件路径
    :return: 成功返回True，失败返回False
    """
    try:
        # 1. 转换YAML数据
        data = convert_yaml_to_json(yaml_file)
        if not data:
            raise ValueError("转换后的数据为空")
            
        # 2. 加载到数据库
        load_json_to_db(get_db_path(), data)
        
        # 3. 记录成功日志
        print(f"成功合并数据：{yaml_file}")
        return True
        
    except Exception as e:
        # 记录错误日志
        print(f"合并数据失败：{str(e)}")
        # 可以根据需要记录更详细的错误信息
        print(f"文件路径：{yaml_file}")
        print(f"错误类型：{type(e).__name__}")
        return False
