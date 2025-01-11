import time
from ..dao.dao import execute_query, fetch_all, fetch_one, db_path
import uuid
import sqlite3

def generate_unique_timestamp():
    return int(time.time() * 1000) + uuid.uuid4().int % 1000

def add_group_tag(text, desc, subgroup_id, color):
    query = '''
        INSERT INTO tag_tags (subgroup_id, text, desc, color, create_time)
        VALUES (?, ?, ?, ?, ?)
    '''
    execute_query(query, (subgroup_id, text, desc, color, generate_unique_timestamp()))

def edit_group_tag(text, desc, id_index, color):
    query = '''
        UPDATE tag_tags
        SET text = ?, desc = ?, color = ?
        WHERE id_index = ?
    '''
    execute_query(query, (text, desc, color, id_index))

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

def delete_group_tag(id_index):
    query = 'DELETE FROM tag_tags WHERE id_index = ?'
    execute_query(query, (id_index,))

def batch_delete_group_tags(id_indices):
    query = "DELETE FROM tag_tags WHERE id_index IN ({seq})".format(
        seq=','.join(['?']*len(id_indices)))
    execute_query(query, id_indices)

def add_new_node_group(key, color):
    # 检查 name 是否已经存在
    query = 'SELECT COUNT(*) FROM tag_groups WHERE name = ?'
    result = fetch_one(query, (key,))
    if result[0] > 0:
        return {"info": "Group name already exists"}

    query = '''
        INSERT INTO tag_groups (name, color, create_time)
        VALUES (?, ?, ?)
    '''
    execute_query(query, (key, color, generate_unique_timestamp()))
    return {"info": "Group added"}

def add_new_group(key, group_key, color):
    # 检查 name 是否已经存在
    query = 'SELECT COUNT(*) FROM tag_subgroups WHERE name = ?'
    result = fetch_one(query, (group_key,))
    if result[0] > 0:
        return {"info": "Subgroup name already exists"}

    query = '''
        INSERT INTO tag_subgroups (group_id, name, color, create_time)
        VALUES (?, ?, ?, ?)
    '''
    execute_query(query, (key, group_key, color, generate_unique_timestamp()))
    return {"info": "Subgroup added"}

def edit_node_group(id_index, new_key, new_color):
    # 检查 name 是否已经存在
    query = 'SELECT COUNT(*) FROM tag_groups WHERE name = ? AND id_index != ?'
    result = fetch_one(query, (new_key, id_index))
    if result[0] > 0:
        return {"info": "Group name already exists"}

    query = '''
        UPDATE tag_groups
        SET name = ?, color = ?
        WHERE id_index = ?
    '''
    execute_query(query, (new_key, new_color, id_index))
    return {"info": "Group updated"}

def edit_child_node_group(id_index, new_key, new_color):
    # 检查 name 是否已经存在
    query = 'SELECT COUNT(*) FROM tag_subgroups WHERE name = ? AND id_index != ?'
    result = fetch_one(query, (new_key, id_index))
    if result[0] > 0:
        return {"info": "Subgroup name already exists"}

    query = '''
        UPDATE tag_subgroups
        SET name = ?, color = ?
        WHERE id_index = ?
    '''
    execute_query(query, (new_key, new_color, id_index))
    return {"info": "Subgroup updated"}

def delete_node_group(id_index):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN')
        
        # 删除与该组关联的子组和标签
        query = '''
            DELETE FROM tag_tags
            WHERE subgroup_id IN (
                SELECT id_index FROM tag_subgroups WHERE group_id = ?
            )
        '''
        cursor.execute(query, (id_index,))
        
        query = 'DELETE FROM tag_subgroups WHERE group_id = ?'
        cursor.execute(query, (id_index,))
        
        # 删除组
        query = 'DELETE FROM tag_groups WHERE id_index = ?'
        cursor.execute(query, (id_index,))
        
        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_child_node_group(id_index):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN')
        
        # 删除与该子组关联的标签
        query = 'DELETE FROM tag_tags WHERE subgroup_id = ?'
        cursor.execute(query, (id_index,))
        
        # 删除子组
        query = 'DELETE FROM tag_subgroups WHERE id_index = ?'
        cursor.execute(query, (id_index,))
        
        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        raise e
    finally:
        conn.close()


def get_group_tags():
    query = '''
        SELECT g.id_index as group_id, g.name as group_name, g.color as group_color, g.create_time as group_create_time,
               sg.id_index as subgroup_id, sg.name as subgroup_name, sg.color as subgroup_color, sg.create_time as subgroup_create_time,
               t.id_index as tag_id, t.text as tag_text, t.desc as tag_desc, t.color as tag_color, t.create_time as tag_create_time
        FROM tag_groups g
        LEFT JOIN tag_subgroups sg ON g.id_index = sg.group_id
        LEFT JOIN tag_tags t ON sg.id_index = t.subgroup_id
        ORDER BY g.create_time ASC, sg.create_time ASC, t.create_time DESC
    '''
    data = fetch_all(query)

    result = []
    group_map = {}
    subgroup_map = {}

    for row in data:
        group_id, group_name, group_color, group_create_time, subgroup_id, subgroup_name, subgroup_color, subgroup_create_time, tag_id, tag_text, tag_desc, tag_color, tag_create_time = row

        if group_id not in group_map:
            group_map[group_id] = {
                'id_index': group_id,
                'name': group_name,
                'color': group_color,
                'create_time': group_create_time,
                'groups': []
            }
            result.append(group_map[group_id])

        if subgroup_id and subgroup_id not in subgroup_map:
            subgroup_map[subgroup_id] = {
                'id_index': subgroup_id,
                'name': subgroup_name,
                'color': subgroup_color,
                'create_time': subgroup_create_time,
                'tags': []
            }
            group_map[group_id]['groups'].append(subgroup_map[subgroup_id])

        if tag_id:
            subgroup_map[subgroup_id]['tags'].append({
                'id_index': tag_id,
                'text': tag_text,
                'desc': tag_desc,
                'color': tag_color,
                'create_time': tag_create_time
            })

    return result