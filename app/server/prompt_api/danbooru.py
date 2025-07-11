import aiosqlite
from typing import List, Dict, Optional, Any
from ..dao.dao import danbooru_db_path
import sqlite3

async def get_danbooru_tags(search: str = None, page: int = 1, page_size: int = 100) -> Dict[str, Any]:
    """获取标签列表，支持分页和通过tag或translate字段搜索
    Args:
        search: 搜索关键词
        page: 页码，从1开始
        page_size: 每页大小
    Returns:
        {
            "data": List[Dict],  # 标签数据
            "total": int,        # 总记录数
            "total_pages": int   # 总页数
        }
    """
    async with aiosqlite.connect(danbooru_db_path) as db:
        cursor = await db.cursor()
        
        # 获取总记录数
        if search:
            count_query = """
            SELECT COUNT(*) FROM danbooru_tag 
            WHERE tag LIKE ? OR translate LIKE ?
            """
            search_param = f"%{search}%"
            await cursor.execute(count_query, (search_param, search_param))
        else:
            await cursor.execute("SELECT COUNT(*) FROM danbooru_tag")
        
        total = (await cursor.fetchone())[0]
        total_pages = (total + page_size - 1) // page_size
        
        # 获取分页数据
        offset = (page - 1) * page_size
        if search:
            query = """
            SELECT * FROM danbooru_tag 
            WHERE tag LIKE ? OR translate LIKE ?
            ORDER BY hot DESC
            LIMIT ? OFFSET ?
            """
            await cursor.execute(query, (search_param, search_param, page_size, offset))
        else:
            query = """
            SELECT * FROM danbooru_tag 
            ORDER BY hot DESC
            LIMIT ? OFFSET ?
            """
            await cursor.execute(query, (page_size, offset))
        
        rows = await cursor.fetchall()
        columns = [column[0] for column in cursor.description]
        
        return {
            "data": [dict(zip(columns, row)) for row in rows],
            "total": total,
            "total_pages": total_pages
        }

async def add_danbooru_tag(tag_data: Dict) -> int:
    """添加新标签"""
    async with aiosqlite.connect(danbooru_db_path) as db:
        cursor = await db.cursor()
        query = """
        INSERT INTO danbooru_tag (tag, color_id, translate, hot, aliases)
        VALUES (?, ?, ?, ?, ?)
        """
        await cursor.execute(
            query,
            (
                tag_data["tag"],
                tag_data.get("color_id", 0),
                tag_data.get("translate", ""),
                tag_data.get("hot", 0),
                tag_data.get("aliases", 0)
            )
        )
        await db.commit()
        return cursor.lastrowid

async def update_danbooru_tag(tag_id: int, update_data: Dict) -> bool:
    """更新标签信息"""
    async with aiosqlite.connect(danbooru_db_path) as db:
        cursor = await db.cursor()
        
        set_clauses = []
        params = []
        
        for field, value in update_data.items():
            set_clauses.append(f"{field} = ?")
            params.append(value)
        
        if not set_clauses:
            return False
        
        query = f"UPDATE danbooru_tag SET {', '.join(set_clauses)} WHERE id_index = ?"
        params.append(tag_id)
        
        await cursor.execute(query, params)
        await db.commit()
        return cursor.rowcount > 0

async def delete_danbooru_tag(tag_id: int) -> bool:
    """删除标签"""
    async with aiosqlite.connect(danbooru_db_path) as db:
        cursor = await db.cursor()
        await cursor.execute("DELETE FROM danbooru_tag WHERE id_index = ?", (tag_id,))
        await db.commit()
        return cursor.rowcount > 0

async def get_danbooru_tag_by_id(tag_id: int) -> Optional[Dict]:
    """根据ID获取单个标签"""
    async with aiosqlite.connect(danbooru_db_path) as db:
        cursor = await db.cursor()
        await cursor.execute("SELECT * FROM danbooru_tag WHERE id_index = ?", (tag_id,))
        row = await cursor.fetchone()
        
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

async def delete_danbooru_tags_batch(tag_ids: List[int]) -> int:
    """批量删除标签
    Args:
        tag_ids: 要删除的标签ID列表
    Returns:
        int: 成功删除的记录数
    """
    if not tag_ids:
        return 0
    
    async with aiosqlite.connect(danbooru_db_path) as db:
        cursor = await db.cursor()
        
        # 开始事务
        await db.execute("BEGIN TRANSACTION")
        
        try:
            deleted_count = 0
            for tag_id in tag_ids:
                await cursor.execute("DELETE FROM danbooru_tag WHERE id_index = ?", (tag_id,))
                deleted_count += cursor.rowcount
            
            # 提交事务
            await db.commit()
            return deleted_count
            
        except Exception as e:
            # 回滚事务
            await db.rollback()
            raise e

def run_danbooru_sql_text(sql_array):
    conn = sqlite3.connect(danbooru_db_path)
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