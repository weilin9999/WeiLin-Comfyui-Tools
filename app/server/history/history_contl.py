import time
from ..dao.dao import execute_query, fetch_all, fetch_one

def read_history():
    """读取历史记录"""
    query = "SELECT id_index, tag, name, color, create_time FROM history WHERE is_deleted = 0"
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

def add_history(tag, name="", color=""):
    """添加新的历史记录"""
    if not tag:
        return {"info": "Tag is required"}
    if len(tag) <= 0:
        return {"info": "Tag is required"}

    create_time = int(time.time())
    
    # 检查是否有可复用的 id_index
    query = "SELECT id_index FROM history WHERE is_deleted = 1 LIMIT 1"
    deleted_id = fetch_one(query)
    
    if deleted_id:
        id_index = deleted_id[0]
        # 更新复用的 id_index
        query = '''
            UPDATE history
            SET tag = ?, name = ?, color = ?, create_time = ?, is_deleted = 0
            WHERE id_index = ?
        '''
        execute_query(query, (tag, name, color, create_time, id_index))
    else:
        query = '''
            INSERT INTO history (tag, name, color, create_time)
            VALUES (?, ?, ?, ?)
        '''
        execute_query(query, (tag, name, color, create_time))
    
    return {"info": "Append"}

def delete_history(id_index):
    """删除指定 id_index 的历史记录"""
    query = "UPDATE history SET is_deleted = 1 WHERE id_index = ?"
    execute_query(query, (id_index,))
    return {"info": "Deleted"}

def batch_delete_history(id_indices):
    """批量删除指定 id_index 的历史记录"""
    query = "UPDATE history SET is_deleted = 1 WHERE id_index IN ({seq})".format(
        seq=','.join(['?']*len(id_indices)))
    execute_query(query, id_indices)
    return {"info": "Batch Deleted"}