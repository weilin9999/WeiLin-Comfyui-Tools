from ..dao.dao import execute_query, fetch_all, fetch_one, db_path
import sqlite3
import time
import uuid
import json

def generate_unique_timestamp():
    return int(time.time() * 1000) + uuid.uuid4().int % 1000

# 一级目录操作
def add_tag_group(name, color):
    query = 'INSERT INTO tag_groups (name, color, create_time) VALUES (?, ?, ?)'
    execute_query(query, (name, color, generate_unique_timestamp()))

def edit_tag_group(id_index, name, color):
    query = 'UPDATE tag_groups SET name = ?, color = ? WHERE id_index = ?'
    execute_query(query, (name, color, id_index))

def delete_tag_group(id_index):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('BEGIN')
        query = '''
            DELETE FROM tag_tags
            WHERE subgroup_id IN (
                SELECT id_index FROM tag_subgroups WHERE group_id = ?
            )
        '''
        cursor.execute(query, (id_index,))
        query = 'DELETE FROM tag_subgroups WHERE group_id = ?'
        cursor.execute(query, (id_index,))
        query = 'DELETE FROM tag_groups WHERE id_index = ?'
        cursor.execute(query, (id_index,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_tag_groups():
    query = 'SELECT * FROM tag_groups'
    result = fetch_all(query)
    json_result = []
    for row in result:
        json_result.append({
            'id_index': row[0],
            'name': row[1],
            'color': row[2],
            'create_time': row[3]
        })
    return json.dumps(json_result)

# 二级目录操作
def add_tag_subgroup(group_id, name, color):
    query = 'INSERT INTO tag_subgroups (group_id, name, color, create_time) VALUES (?, ?, ?, ?)'
    execute_query(query, (group_id, name, color, generate_unique_timestamp()))

def edit_tag_subgroup(id_index, name, color):
    query = 'UPDATE tag_subgroups SET name = ?, color = ? WHERE id_index = ?'
    execute_query(query, (name, color, id_index))

def delete_tag_subgroup(id_index):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute('BEGIN')
        query = 'DELETE FROM tag_tags WHERE subgroup_id = ?'
        cursor.execute(query, (id_index,))
        query = 'DELETE FROM tag_subgroups WHERE id_index = ?'
        cursor.execute(query, (id_index,))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

def get_tag_subgroups(group_id):
    query = 'SELECT * FROM tag_subgroups WHERE group_id = ?'
    result = fetch_all(query, (group_id,))
    json_result = []
    for row in result:
        json_result.append({
            'id_index': row[0],
            'group_id': row[1],
            'name': row[2],
            'color': row[3],
            'create_time': row[4]
        })
    return json.dumps(json_result)

# 标签操作
def add_tag(subgroup_id, text, desc, color):
    query = 'INSERT INTO tag_tags (subgroup_id, text, desc, color, create_time) VALUES (?, ?, ?, ?, ?)'
    execute_query(query, (subgroup_id, text, desc, color, generate_unique_timestamp()))

def edit_tag(id_index, text, desc, color):
    query = 'UPDATE tag_tags SET text = ?, desc = ?, color = ? WHERE id_index = ?'
    execute_query(query, (text, desc, color, id_index))

def delete_tag(id_index):
    query = 'DELETE FROM tag_tags WHERE id_index = ?'
    execute_query(query, (id_index,))

def get_tags(subgroup_id):
    query = 'SELECT * FROM tag_tags WHERE subgroup_id = ?'
    result = fetch_all(query, (subgroup_id,))
    json_result = []
    for row in result:
        json_result.append({
            'id_index': row[0],
            'subgroup_id': row[1],
            'text': row[2],
            'desc': row[3],
            'color': row[4],
            'create_time': row[5]
        })
    return json.dumps(json_result)

# 排序操作
def move_tag_group(id_index, reference_id_index, position='before'):
    query = 'SELECT create_time FROM tag_groups WHERE id_index = ?'
    reference_group = fetch_one(query, (reference_id_index,))
    if not reference_group:
        return {"info": "Reference group not found"}

    reference_create_time = reference_group[0]

    if position == 'after':
        new_create_time = reference_create_time - 1
    elif position == 'before':
        new_create_time = reference_create_time + 1
    else:
        return {"info": "Invalid position"}

    query = '''
        UPDATE tag_groups
        SET create_time = ?
        WHERE id_index = ?
    '''
    execute_query(query, (new_create_time, id_index))

    return {"info": "Group moved"}

def move_tag_subgroup(id_index, reference_id_index, position='before'):
    query = 'SELECT create_time FROM tag_subgroups WHERE id_index = ?'
    reference_subgroup = fetch_one(query, (reference_id_index,))
    if not reference_subgroup:
        return {"info": "Reference subgroup not found"}

    reference_create_time = reference_subgroup[0]

    if position == 'after':
        new_create_time = reference_create_time - 1
    elif position == 'before':
        new_create_time = reference_create_time + 1
    else:
        return {"info": "Invalid position"}

    query = '''
        UPDATE tag_subgroups
        SET create_time = ?
        WHERE id_index = ?
    '''
    execute_query(query, (new_create_time, id_index))

    return {"info": "Subgroup moved"}

def move_tag(id_index, reference_id_index, position='before'):
    query = 'SELECT create_time FROM tag_tags WHERE id_index = ?'
    reference_tag = fetch_one(query, (reference_id_index,))
    if not reference_tag:
        return {"info": "Reference tag not found"}

    reference_create_time = reference_tag[0]

    if position == 'after':
        new_create_time = reference_create_time - 1
    elif position == 'before':
        new_create_time = reference_create_time + 1
    else:
        return {"info": "Invalid position"}

    query = '''
        UPDATE tag_tags
        SET create_time = ?
        WHERE id_index = ?
    '''
    execute_query(query, (new_create_time, id_index))

    return {"info": "Tag moved"}