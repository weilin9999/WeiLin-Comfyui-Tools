import time
from ..dao.dao import execute_query, fetch_all, fetch_one

def read_collect_history():
    """读取 collect_history 表并返回内容"""
    query = "SELECT id_index, tag, name, color, create_time FROM collect_history WHERE is_deleted = 0"
    data = fetch_all(query)
    
    # 将数据转换为 JSON 格式
    result = []
    for row in data:
        result.append({
            "id_index": row[0],
            "tag": row[1],
            "name": row[2],
            "color": row[3],
            "create_time": row[4]
        })
    
    return result

def add_collect_history(tag, name="", color=""):
    """添加新的历史记录到 collect_history 表"""
    create_time = int(time.time())
    
    # 检查是否有可复用的 id_index
    query = "SELECT id_index FROM collect_history WHERE is_deleted = 1 LIMIT 1"
    deleted_id = fetch_one(query)
    
    if deleted_id:
        id_index = deleted_id[0]
        # 更新复用的 id_index
        query = '''
            UPDATE collect_history
            SET tag = ?, name = ?, color = ?, create_time = ?, is_deleted = 0
            WHERE id_index = ?
        '''
        execute_query(query, (tag, name, color, create_time, id_index))
    else:
        query = '''
            INSERT INTO collect_history (tag, name, color, create_time)
            VALUES (?, ?, ?, ?)
        '''
        execute_query(query, (tag, name, color, create_time))
    
    return {"info": "Append"}

def delete_collect_history(id_index):
    """删除指定 id_index 的历史记录"""
    query = "UPDATE collect_history SET is_deleted = 1 WHERE id_index = ?"
    execute_query(query, (id_index,))
    return {"info": "Deleted"}

def batch_delete_collect_history(id_indices):
    """批量删除指定 id_index 的历史记录"""
    query = "UPDATE collect_history SET is_deleted = 1 WHERE id_index IN ({seq})".format(
        seq=','.join(['?']*len(id_indices)))
    execute_query(query, id_indices)
    return {"info": "Batch Deleted"}

def edit_collect_history(id_index, name=None, color=None, tag=None):
    """编辑指定 id_index 的历史记录"""
    query = "SELECT id_index, tag, name, color, create_time FROM collect_history WHERE id_index = ?"
    entry = fetch_one(query, (id_index,))
    if not entry:
        return {"info": "Record not found"}

    update_fields = []
    params = []

    if name is not None:
        update_fields.append("name = ?")
        params.append(name)
    if color is not None:
        update_fields.append("color = ?")
        params.append(color)
    if tag is not None:
        update_fields.append("tag = ?")
        params.append(tag)

    if update_fields:
        query = f"UPDATE collect_history SET {', '.join(update_fields)} WHERE id_index = ?"
        params.append(id_index)
        execute_query(query, params)

    return {"info": "Edited"}