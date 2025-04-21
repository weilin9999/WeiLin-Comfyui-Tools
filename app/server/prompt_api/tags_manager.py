import time
from ..dao.dao import execute_query, fetch_all, fetch_one, tags_db_path
import uuid
import sqlite3
from uuid_extensions import uuid7

def generate_unique_timestamp():
    return int(time.time() * 1000) + uuid.uuid4().int % 1000

async def add_group_tag(text, desc, subgroup_id, color, g_uuid):
    query = '''
        INSERT INTO tag_tags (subgroup_id, text, desc, color, create_time, t_uuid, g_uuid)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    '''
    await execute_query('tags',query, (subgroup_id, text, desc, color, generate_unique_timestamp(), str(uuid7()), g_uuid ))

async def edit_group_tag(text, desc, id_index, color):
    query = '''
        UPDATE tag_tags
        SET text = ?, desc = ?, color = ?
        WHERE id_index = ?
    '''
    await execute_query('tags',query, (text, desc, color, id_index))

async def move_tag(id_index, reference_id_index, position='before'):
    query = 'SELECT create_time FROM tag_tags WHERE id_index = ?'
    reference_tag = await fetch_one('tags',query, (reference_id_index,))
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
    await execute_query('tags',query, (new_create_time, id_index))

    return {"info": "Tag moved"}

async def delete_group_tag(id_index):
    query = 'DELETE FROM tag_tags WHERE id_index = ?'
    await execute_query('tags',query, (id_index,))

async def batch_delete_group_tags(id_indices):
    query = "DELETE FROM tag_tags WHERE id_index IN ({seq})".format(
        seq=','.join(['?']*len(id_indices)))
    await execute_query('tags',query, id_indices)

async def add_new_node_group(key, color):
    # 检查 name 是否已经存在
    # query = 'SELECT COUNT(*) FROM tag_groups WHERE name = ?'
    # result = await fetch_one('tags',query, (key,))
    # if result == None:
    #     return {"code": 500}
    # if result[0] > 0:
    #     return {"code": 201}

    query = '''
        INSERT INTO tag_groups (name, color, create_time, p_uuid)
        VALUES (?, ?, ?, ?)
    '''
    await execute_query('tags',query, (key, color, generate_unique_timestamp(), str(uuid7()) ))
    return {"code": 200}

async def add_new_group(key, group_key, color, p_uuid):
    # 检查 name 是否已经存在
    # query = 'SELECT COUNT(*) FROM tag_subgroups WHERE name = ?'
    # result = await fetch_one('tags',query, (group_key,))
    # if result == None:
    #     return {"code": 500}
    # if result[0] > 0:
    #     return {"code": 201}

    query = '''
        INSERT INTO tag_subgroups (group_id, name, color, create_time, p_uuid, g_uuid)
        VALUES (?, ?, ?, ?, ?, ?)
    '''
    await execute_query('tags',query, (key, group_key, color, generate_unique_timestamp(), p_uuid, str(uuid7()) ))
    return {"code": 200}

async def edit_node_group(id_index, new_key, new_color):
    # 检查 name 是否已经存在
    # query = 'SELECT COUNT(*) FROM tag_groups WHERE name = ? AND id_index != ?'
    # result = await fetch_one('tags',query, (new_key, id_index))
    # if result == None:
    #     return {"code": 500}
    # if result[0] > 0:
    #     return {"code": 201}

    query = '''
        UPDATE tag_groups
        SET name = ?, color = ?
        WHERE id_index = ?
    '''
    await execute_query('tags',query, (new_key, new_color, id_index))
    return {"code": 200}

async def edit_child_node_group(id_index, new_key, new_color):
    # 检查 name 是否已经存在
    # query = 'SELECT COUNT(*) FROM tag_subgroups WHERE name = ? AND id_index != ?'
    # result = await fetch_one('tags',query, (new_key, id_index))
    # if result == None:
    #     return {"code": 500}
    # if result[0] > 0:
    #     return {"code": 201}

    query = '''
        UPDATE tag_subgroups
        SET name = ?, color = ?
        WHERE id_index = ?
    '''
    await execute_query('tags',query, (new_key, new_color, id_index))
    return {"code": 200}

def delete_node_group(p_uuid):
    conn = sqlite3.connect(tags_db_path)
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN')
        
        # 删除与该组关联的子组和标签
        query = '''
            DELETE FROM tag_tags
            WHERE g_uuid IN (
                SELECT g_uuid FROM tag_subgroups WHERE p_uuid = ?
            )
        '''
        cursor.execute(query, (p_uuid,))
        
        query = 'DELETE FROM tag_subgroups WHERE p_uuid = ?'
        cursor.execute(query, (p_uuid,))
        
        # 删除组
        query = 'DELETE FROM tag_groups WHERE p_uuid = ?'
        cursor.execute(query, (p_uuid,))
        
        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        raise e
    finally:
        conn.close()

def delete_child_node_group(g_uuid):
    conn = sqlite3.connect(tags_db_path)
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN')
        
        # 删除与该子组关联的标签
        query = 'DELETE FROM tag_tags WHERE g_uuid = ?'
        cursor.execute(query, (g_uuid,))
        
        # 删除子组
        query = 'DELETE FROM tag_subgroups WHERE g_uuid = ?'
        cursor.execute(query, (g_uuid,))
        
        # 提交事务
        conn.commit()
    except Exception as e:
        # 回滚事务
        conn.rollback()
        raise e
    finally:
        conn.close()

async def get_group_tags():
    query = '''
        SELECT 
            g.id_index as group_id, g.name as group_name, g.color as group_color, 
            g.create_time as group_create_time, g.p_uuid as group_p_uuid,
            sg.id_index as subgroup_id, sg.name as subgroup_name, sg.color as subgroup_color,
            sg.create_time as subgroup_create_time, sg.g_uuid as subgroup_g_uuid, sg.p_uuid as subgroup_p_uuid,
            t.id_index as tag_id, t.text as tag_text, t.desc as tag_desc, 
            t.color as tag_color, t.create_time as tag_create_time, t.g_uuid as tag_g_uuid
        FROM tag_groups g
        LEFT JOIN tag_subgroups sg ON g.p_uuid = sg.p_uuid
        LEFT JOIN tag_tags t ON sg.g_uuid = t.g_uuid
        ORDER BY g.create_time ASC, sg.create_time ASC, t.create_time DESC
    '''
    data = await fetch_all('tags', query)
    
    # 使用字典存储结果，提高查找效率
    result = {}
    subgroups = {}
    
    for row in data:
        # 解包数据
        group_data = {
            'id_index': row[0],
            'name': row[1],
            'color': row[2],
            'create_time': row[3],
            'p_uuid': row[4],
            'groups': []
        }
        
        subgroup_data = {
            'id_index': row[5],
            'name': row[6],
            'color': row[7],
            'create_time': row[8],
            'g_uuid': row[9],
            'p_uuid': row[10],
            'tags': []
        }
        
        tag_data = {
            'id_index': row[11],
            'text': row[12],
            'desc': row[13],
            'color': row[14],
            'create_time': row[15],
            'g_uuid': row[16]
        } if row[11] else None
        
        # 处理组数据
        if group_data['p_uuid'] not in result:
            result[group_data['p_uuid']] = group_data
        
        # 处理子组数据
        if subgroup_data['g_uuid'] and subgroup_data['g_uuid'] not in subgroups:
            subgroups[subgroup_data['g_uuid']] = subgroup_data
            result[group_data['p_uuid']]['groups'].append(subgroup_data)
        
        # 处理标签数据
        if tag_data and tag_data['g_uuid'] in subgroups:
            subgroups[tag_data['g_uuid']]['tags'].append(tag_data)
    
    # 返回列表形式的结果
    return list(result.values())

async def get_groups_list():
    query = '''
        SELECT 
            g.id_index as group_id, g.name as group_name, g.color as group_color, 
            g.create_time as group_create_time, g.p_uuid as group_p_uuid,
            sg.id_index as subgroup_id, sg.name as subgroup_name, sg.color as subgroup_color,
            sg.create_time as subgroup_create_time, sg.g_uuid as subgroup_g_uuid, sg.p_uuid as subgroup_p_uuid
        FROM tag_groups g
        LEFT JOIN tag_subgroups sg ON g.p_uuid = sg.p_uuid
        ORDER BY g.create_time ASC, sg.create_time ASC
    '''
    data = await fetch_all('tags', query)
    
    # 使用字典存储结果，提高查找效率
    result = {}
    
    for row in data:
        # 解包数据
        group_data = {
            'id_index': row[0],
            'name': row[1],
            'color': row[2],
            'create_time': row[3],
            'p_uuid': row[4],
            'groups': []
        }
        
        subgroup_data = {
            'id_index': row[5],
            'name': row[6],
            'color': row[7],
            'create_time': row[8],
            'g_uuid': row[9],
            'p_uuid': row[10]
        }
        
        # 处理组数据
        if group_data['p_uuid'] not in result:
            result[group_data['p_uuid']] = group_data
        
        # 处理子组数据
        if subgroup_data['g_uuid']:
            result[group_data['p_uuid']]['groups'].append(subgroup_data)
    
    # 返回列表形式的结果
    return list(result.values())


def run_sql_text(sql_array):
    conn = sqlite3.connect(tags_db_path)
    cursor = conn.cursor()
    
    try:
        # 开始事务
        cursor.execute('BEGIN')
        # 执行所有SQL语句
        for sql in sql_array:
            cursor.execute(sql)
        # 提交事务
        conn.commit()
        print("SQL执行成功")
        return {"code": 200, "message": "SQL执行成功"}
    except Exception as e:
        # 回滚事务
        conn.rollback()
        print(f"SQL执行失败: {str(e)}")
        return {"code": 500, "message": f"SQL执行失败: {str(e)}"}
    finally:
        conn.close()