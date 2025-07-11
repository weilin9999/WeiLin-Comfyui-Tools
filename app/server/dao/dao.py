import os
import sqlite3
import locale
import datetime
import shutil
import requests
from ..user_init.user_init import read_init_file

import aiosqlite
import asyncio
from typing import Optional, List, Tuple, Any
from ..cloud_warehouse.save_history import save_package_path
from uuid_extensions import uuid7

def getUUID():
    return str(uuid7())

# 修改连接池为异步版本
_connection_pool = {}
_connection_lock = asyncio.Lock()


current_dir = os.path.dirname(os.path.abspath(__file__))
db_prefix = 'userdatas_'
db_suffix = 'default'
localLang = locale.getdefaultlocale()[0]

# 读取配置文件中的语言设置来决定加载什么数据库文件
userSetting = read_init_file() or {}
# print(userSetting)
if userSetting == {}:
    # 根据系统语言设置数据库文件
    system_lang = locale.getdefaultlocale()[0]
    if system_lang.startswith('zh'):
        localLang = 'zh_CN'
    else:
        localLang = 'en_US'
else :
    localLang = userSetting['user_lang']


# 旧表数据
db_path = os.path.join(current_dir, f'../../../user_data/{db_prefix}{db_suffix}.db')

# 新增数据库路径定义
tags_db_path = os.path.join(current_dir, f'../../../user_data/{db_prefix}{db_suffix}_tags.db')
history_db_path = os.path.join(current_dir, f'../../../user_data/{db_prefix}{db_suffix}_history.db')
danbooru_db_path = os.path.join(current_dir, f'../../../user_data/{db_prefix}{db_suffix}_danbooru.db')
old_db_path = os.path.join(current_dir, f'../../../user_data_old/')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'application/json'
}


async def _get_connection(db_type: str) -> aiosqlite.Connection:
    """从连接池获取数据库连接"""
    async with _connection_lock:
        if db_type not in _connection_pool:
            db_map = {
                'tags': tags_db_path,
                'history': history_db_path,
                'danbooru': danbooru_db_path
            }
            conn = await aiosqlite.connect(db_map[db_type])
            # 设置连接池参数
            await conn.execute("PRAGMA journal_mode=WAL")
            await conn.execute("PRAGMA synchronous=NORMAL")
            await conn.execute("PRAGMA cache_size=-2000")
            _connection_pool[db_type] = conn
        return _connection_pool[db_type]


def create_tables():
    try:
        # 创建tags数据库表
        conn = sqlite3.connect(tags_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag_groups (
                id_index INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                color TEXT,
                create_time INTEGER,
                p_uuid TEXT(128)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tag_subgroups (
                id_index INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER,
                name TEXT,
                color TEXT,
                create_time INTEGER,
                p_uuid TEXT(128),
                g_uuid TEXT(128)
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
                t_uuid TEXT(128),
                g_uuid TEXT(128)
            )
        ''')
         # 添加update_info表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS update_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                update_at INTEGER
            )
        ''')
        # 插入默认数据
        cursor.execute('''
            INSERT OR IGNORE INTO update_info (id, update_at) 
            VALUES (1, 1743405726)
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()
        conn.close()

        # 创建history数据库表
        conn = sqlite3.connect(history_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id_index INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                name TEXT,
                color TEXT,
                create_time INTEGER,
                is_deleted INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS collect_history (
                id_index INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                name TEXT,
                color TEXT,
                create_time INTEGER,
                is_deleted INTEGER DEFAULT 0
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()
        conn.close()

        # 创建danbooru数据库表
        conn = sqlite3.connect(danbooru_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS danbooru_tag (
                id_index INTEGER PRIMARY KEY AUTOINCREMENT,
                tag TEXT,
                color_id INTEGER,
                translate TEXT,
                hot INTEGER DEFAULT 0,
                aliases INTEGER DEFAULT 0
            )
        ''')
        # 添加update_info表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS update_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                update_at INTEGER
            )
        ''')
        # 插入默认数据
        cursor.execute('''
            INSERT OR IGNORE INTO update_info (id, update_at) 
            VALUES (1, 1743405726)
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        ''')
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"创建tags数据库表时出错: {e}")
        raise

def get_current_version(db_type):
    db_map = {
        'tags': tags_db_path,
        'history': history_db_path,
        'danbooru': danbooru_db_path
    }
    conn = sqlite3.connect(db_map[db_type])
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT version FROM schema_version ORDER BY version DESC LIMIT 1')
        result = cursor.fetchone()
        return result[0] if result else 0
    except sqlite3.OperationalError:
        # 如果schema_version表不存在，说明是旧版本
        return 0
    finally:
        conn.close()

def update_version(db_type, version):
    db_map = {
        'tags': tags_db_path,
        'history': history_db_path,
        'danbooru': danbooru_db_path
    }
    try:
        conn = sqlite3.connect(db_map[db_type])
        cursor = conn.cursor()
        cursor.execute('INSERT INTO schema_version (version) VALUES (?)', (version,))
        conn.commit()
    except sqlite3.Error as e:
        print(f"更新版本时出错: {e}")
        raise
    finally:
        if 'conn' in locals():
            conn.close()

def migrate_db():
    # tags数据库迁移
    current_version = get_current_version('tags')
    if current_version < 1:
        conn = sqlite3.connect(tags_db_path)
        cursor = conn.cursor()
        # 创建schema_version表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        ''')
        # 其他迁移操作
        update_version('tags', 1)
        conn.commit()
        conn.close()
    
    # 添加版本2的迁移
    if current_version < 2:
        conn = sqlite3.connect(tags_db_path)
        cursor = conn.cursor()

        # 检查并添加新字段
        def add_column_if_not_exists(table, column, column_type):
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in cursor.fetchall()]
            if column not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
        
        add_column_if_not_exists('tag_groups', 'p_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_subgroups', 'p_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_subgroups', 'g_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_tags', 't_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_tags', 'g_uuid', 'TEXT(128)')

         # 删除特定数据
        cursor.execute("DELETE FROM tag_groups WHERE id_index = 11")
        cursor.execute("DELETE FROM tag_subgroups WHERE id_index = 134")
        cursor.execute("DELETE FROM tag_tags WHERE subgroup_id = 137")

        # 更新所有UUID字段
        update_uuids(conn)
        update_version('tags', 2)
        conn.commit()
        conn.close()
    
    # 添加版本3的迁移
    if current_version < 3:
        print("检测到数据库版本变动 版本V3 正在升级中...")
        conn = sqlite3.connect(tags_db_path)
        cursor = conn.cursor()
        
        # 检查并添加新字段(如果不存在)
        def add_column_if_not_exists(table, column, column_type):
            cursor.execute(f"PRAGMA table_info({table})")
            columns = [info[1] for info in cursor.fetchall()]
            if column not in columns:
                cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {column_type}")
        
        # 确保所有表都有UUID字段
        add_column_if_not_exists('tag_groups', 'p_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_subgroups', 'p_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_subgroups', 'g_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_tags', 't_uuid', 'TEXT(128)')
        add_column_if_not_exists('tag_tags', 'g_uuid', 'TEXT(128)')
        
        # 更新所有UUID字段
        update_uuids_v3(conn)

        update_version('tags', 3)
        conn.commit()
        conn.close()
        print("升级完成")

    # history数据库迁移
    current_version = get_current_version('history')
    if current_version < 1:
        conn = sqlite3.connect(history_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        ''')
        update_version('history', 1)
        conn.commit()
        conn.close()

    # danbooru数据库迁移
    current_version = get_current_version('danbooru')
    if current_version < 1:
        conn = sqlite3.connect(danbooru_db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS schema_version (
                version INTEGER PRIMARY KEY
            )
        ''')
        update_version('danbooru', 1)
        conn.commit()
        conn.close()
    
    # 添加版本2的迁移
    if current_version < 2:
        conn = sqlite3.connect(danbooru_db_path)
        cursor = conn.cursor()
        # 检查hot列是否存在
        cursor.execute("PRAGMA table_info(danbooru_tag)")
        columns = [info[1] for info in cursor.fetchall()]
        if 'hot' not in columns:
            # 添加hot字段
            cursor.execute('''
                ALTER TABLE danbooru_tag ADD COLUMN hot INTEGER DEFAULT 0
            ''')
        if 'aliases' not in columns:
            # 添加hot字段
            cursor.execute('''
                ALTER TABLE danbooru_tag ADD COLUMN aliases INTEGER DEFAULT 0
            ''')
        update_version('danbooru', 2)
        conn.commit()
        conn.close()

def update_uuids(conn):
    """根据SQL文件中的固定UUID更新所有表的UUID字段"""
    cursor = conn.cursor()
    print("开始更新Tag数据...")
    try:
        
        # 从Gitee获取SQL文件内容
        # sql_url = "https://api.gitcode.com/api/v5/repos/qq_27627297/WeiLin-Comfyui-Tools-Prompt/raw/tags/2025_03_31/tags_2025_03_31.sql?access_token=y7S27_wDHXy1xaSQjupJk-Wy"
        sql_url = "https://raw.githubusercontent.com/weilin9999/WeiLin-Comfyui-Tools-Prompt/refs/heads/master/tags/2025_03_31/tags_2025_03_31.sql"
        response = requests.get(sql_url, headers=headers)
        response.raise_for_status()
        sql_content = response.text

        # 直接执行整个SQL文件
        cursor.executescript(sql_content)

        # 1. 先检查并更新tag_groups的p_uuid
        cursor.execute("SELECT id_index FROM tag_groups WHERE p_uuid IS NULL OR p_uuid = ''")
        empty_groups = cursor.fetchall()
        for group in empty_groups:
            group_id = group[0]
            new_uuid = getUUID()
            cursor.execute("UPDATE tag_groups SET p_uuid = ? WHERE id_index = ?", (new_uuid, group_id))
        
        # 2. 更新tag_subgroups的p_uuid和g_uuid
        cursor.execute('''
            SELECT sg.id_index, g.p_uuid 
            FROM tag_subgroups sg
            JOIN tag_groups g ON sg.group_id = g.id_index
            WHERE sg.p_uuid IS NULL OR sg.p_uuid = '' OR sg.g_uuid IS NULL OR sg.g_uuid = ''
        ''')
        subgroups = cursor.fetchall()
        for subgroup in subgroups:
            subgroup_id, group_p_uuid = subgroup
            new_g_uuid = getUUID()
            cursor.execute('''
                UPDATE tag_subgroups 
                SET p_uuid = ?, g_uuid = ?
                WHERE id_index = ?
            ''', (group_p_uuid, new_g_uuid, subgroup_id))
        
        # 3. 更新tag_tags的g_uuid和t_uuid
        cursor.execute('''
            SELECT t.id_index, sg.g_uuid 
            FROM tag_tags t
            JOIN tag_subgroups sg ON t.subgroup_id = sg.id_index
            WHERE t.g_uuid IS NULL OR t.g_uuid = '' OR t.t_uuid IS NULL OR t.t_uuid = ''
        ''')
        tags = cursor.fetchall()
        for tag in tags:
            tag_id, subgroup_g_uuid = tag
            new_t_uuid = getUUID()
            cursor.execute('''
                UPDATE tag_tags 
                SET g_uuid = ?, t_uuid = ?
                WHERE id_index = ?
            ''', (subgroup_g_uuid, new_t_uuid, tag_id))

        conn.commit()
        save_package_path("tags/2025_03_31/tags_2025_03_31.sql")
        print("Tag数据更新完成。")
    except Exception as e:
        print(f"更新UUID时出错: {e}")
        conn.rollback()
        raise

def update_uuids_v3(conn):
    """根据SQL文件中的固定UUID更新所有表的UUID字段"""
    cursor = conn.cursor()
    print("开始更新Tag数据 V3...")
    try:
        # 1. 确保所有tag_groups都有p_uuid
        cursor.execute("SELECT id_index FROM tag_groups WHERE p_uuid IS NULL OR p_uuid = ''")
        empty_groups = cursor.fetchall()
        for group in empty_groups:
            group_id = group[0]
            new_uuid = getUUID()
            cursor.execute("UPDATE tag_groups SET p_uuid = ? WHERE id_index = ?", (new_uuid, group_id))
        
        # 2. 更新tag_subgroups的p_uuid和g_uuid
        cursor.execute('''
            SELECT sg.id_index, g.p_uuid 
            FROM tag_subgroups sg
            LEFT JOIN tag_groups g ON sg.group_id = g.id_index
            WHERE sg.p_uuid IS NULL OR sg.p_uuid = '' OR sg.g_uuid IS NULL OR sg.g_uuid = ''
        ''')
        subgroups = cursor.fetchall()
        for subgroup in subgroups:
            subgroup_id, group_p_uuid = subgroup
            new_g_uuid = getUUID()
            if group_p_uuid:  # 如果找到对应的group
                cursor.execute('''
                    UPDATE tag_subgroups 
                    SET p_uuid = ?, g_uuid = ?
                    WHERE id_index = ?
                ''', (group_p_uuid, new_g_uuid, subgroup_id))
            else:  # 如果没有对应的group，只设置g_uuid
                cursor.execute('''
                    UPDATE tag_subgroups 
                    SET g_uuid = ?
                    WHERE id_index = ?
                ''', (new_g_uuid, subgroup_id))
        
        # 3. 更新tag_tags的g_uuid和t_uuid
        cursor.execute('''
            SELECT t.id_index, sg.g_uuid 
            FROM tag_tags t
            LEFT JOIN tag_subgroups sg ON t.subgroup_id = sg.id_index
            WHERE t.g_uuid IS NULL OR t.g_uuid = '' OR t.t_uuid IS NULL OR t.t_uuid = ''
        ''')
        tags = cursor.fetchall()
        for tag in tags:
            tag_id, subgroup_g_uuid = tag
            new_t_uuid = getUUID()
            if subgroup_g_uuid:  # 如果找到对应的subgroup
                cursor.execute('''
                    UPDATE tag_tags 
                    SET g_uuid = ?, t_uuid = ?
                    WHERE id_index = ?
                ''', (subgroup_g_uuid, new_t_uuid, tag_id))
            else:  # 如果没有对应的subgroup，只设置t_uuid
                cursor.execute('''
                    UPDATE tag_tags 
                    SET t_uuid = ?
                    WHERE id_index = ?
                ''', (new_t_uuid, tag_id))

        
        
        # 删除空UUID的数据
        print("删除空UUID的数据...")
        cursor.execute("DELETE FROM tag_groups WHERE p_uuid IS NULL OR p_uuid = ''")
        cursor.execute("DELETE FROM tag_subgroups WHERE g_uuid IS NULL OR g_uuid = ''")
        cursor.execute("DELETE FROM tag_tags WHERE t_uuid IS NULL OR t_uuid = ''")

        
        # 处理重复的t_uuid值
        print("检查并修复重复的UUID...")
        cursor.execute('''
            SELECT t_uuid, COUNT(*) as count
            FROM tag_tags
            WHERE t_uuid IS NOT NULL
            GROUP BY t_uuid
            HAVING count > 1
        ''')
        
        duplicates = cursor.fetchall()
        for dup in duplicates:
            dup_uuid = dup[0]
            # 获取所有具有相同t_uuid的记录
            cursor.execute('SELECT id_index FROM tag_tags WHERE t_uuid = ? ORDER BY id_index', (dup_uuid,))
            records = cursor.fetchall()
            # 保留第一条记录，更新其余记录的t_uuid
            for record in records[1:]:
                new_uuid = getUUID()
                cursor.execute('UPDATE tag_tags SET t_uuid = ? WHERE id_index = ?', (new_uuid, record[0]))
        
        # 处理重复的p_uuid值（tag_groups表）
        cursor.execute('''
            SELECT p_uuid, COUNT(*) as count
            FROM tag_groups
            WHERE p_uuid IS NOT NULL
            GROUP BY p_uuid
            HAVING count > 1
        ''')
        
        duplicates = cursor.fetchall()
        for dup in duplicates:
            dup_uuid = dup[0]
            # 获取所有具有相同p_uuid的记录
            cursor.execute('SELECT id_index FROM tag_groups WHERE p_uuid = ? ORDER BY id_index', (dup_uuid,))
            records = cursor.fetchall()
            # 保留第一条记录，更新其余记录的p_uuid
            for record in records[1:]:
                new_uuid = getUUID()
                cursor.execute('UPDATE tag_groups SET p_uuid = ? WHERE id_index = ?', (new_uuid, record[0]))
        
        # 处理重复的g_uuid值（tag_subgroups表）
        cursor.execute('''
            SELECT g_uuid, COUNT(*) as count
            FROM tag_subgroups
            WHERE g_uuid IS NOT NULL
            GROUP BY g_uuid
            HAVING count > 1
        ''')
        
        duplicates = cursor.fetchall()
        for dup in duplicates:
            dup_uuid = dup[0]
            # 获取所有具有相同g_uuid的记录
            cursor.execute('SELECT id_index FROM tag_subgroups WHERE g_uuid = ? ORDER BY id_index', (dup_uuid,))
            records = cursor.fetchall()
            # 保留第一条记录，更新其余记录的g_uuid
            for record in records[1:]:
                new_uuid = getUUID()
                cursor.execute('UPDATE tag_subgroups SET g_uuid = ? WHERE id_index = ?', (new_uuid, record[0]))
        
        # 添加唯一索引
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_tag_groups_p_uuid ON tag_groups(p_uuid)')
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_tag_subgroups_g_uuid ON tag_subgroups(g_uuid)')
        cursor.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_tag_tags_t_uuid ON tag_tags(t_uuid)')

        
        conn.commit()
        print("Tag数据更新完成。")
    except Exception as e:
        print(f"更新UUID时出错: {e}")
        conn.rollback()
        raise

def migrate_old_db():
    if os.path.exists(db_path):
        try:
            print("检测到旧数据插件，开始数据库迁移...")
            # 确保目标目录存在
            os.makedirs(os.path.dirname(tags_db_path), exist_ok=True)
            
            # 先创建新表
            create_tables()
            
            # 连接旧数据库
            old_conn = sqlite3.connect(db_path)
            old_cursor = old_conn.cursor()
            
            # 迁移tag相关表
            old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tag_groups'")
            if old_cursor.fetchone():
                # 确保新数据库文件存在
                if not os.path.exists(tags_db_path):
                    open(tags_db_path, 'a').close()
                
                tags_conn = sqlite3.connect(tags_db_path)
                tags_cursor = tags_conn.cursor()
                
                # 迁移tag_groups，保留原始id_index
                old_cursor.execute("SELECT * FROM tag_groups")
                tags_cursor.executemany("INSERT INTO tag_groups (id_index, name, color, create_time) VALUES (?, ?, ?, ?)", 
                                     [(row[0], row[1], row[2], row[3]) for row in old_cursor.fetchall()])
                
                # 迁移tag_subgroups，保留原始id_index
                old_cursor.execute("SELECT * FROM tag_subgroups")
                tags_cursor.executemany("INSERT INTO tag_subgroups (id_index, group_id, name, color, create_time) VALUES (?, ?, ?, ?, ?)", 
                                      [(row[0], row[1], row[2], row[3], row[4]) for row in old_cursor.fetchall()])
                
                # 迁移tag_tags，保留原始id_index
                old_cursor.execute("SELECT * FROM tag_tags")
                tags_cursor.executemany("INSERT INTO tag_tags (id_index, subgroup_id, text, desc, color, create_time) VALUES (?, ?, ?, ?, ?, ?)", 
                                      [(row[0], row[1], row[2], row[3], row[4], row[5]) for row in old_cursor.fetchall()])
                
                # 更新SQLite序列计数器
                tags_cursor.execute("SELECT MAX(id_index) FROM tag_groups")
                max_id = tags_cursor.fetchone()[0] or 0
                tags_cursor.execute(f"UPDATE SQLITE_SEQUENCE SET seq = {max_id} WHERE name = 'tag_groups'")
                
                tags_cursor.execute("SELECT MAX(id_index) FROM tag_subgroups")
                max_id = tags_cursor.fetchone()[0] or 0
                tags_cursor.execute(f"UPDATE SQLITE_SEQUENCE SET seq = {max_id} WHERE name = 'tag_subgroups'")
                
                tags_cursor.execute("SELECT MAX(id_index) FROM tag_tags")
                max_id = tags_cursor.fetchone()[0] or 0
                tags_cursor.execute(f"UPDATE SQLITE_SEQUENCE SET seq = {max_id} WHERE name = 'tag_tags'")
                
                tags_conn.commit()
                tags_conn.close()

            # 迁移history相关表
            old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='history'")
            if old_cursor.fetchone():
                if not os.path.exists(history_db_path):
                    open(history_db_path, 'a').close()
                
                history_conn = sqlite3.connect(history_db_path)
                history_cursor = history_conn.cursor()
                
                # 迁移history
                old_cursor.execute("SELECT * FROM history")
                history_cursor.executemany("INSERT INTO history (tag, name, color, create_time, is_deleted) VALUES (?, ?, ?, ?, ?)", 
                                         [(row[1], row[2], row[3], row[4], row[5]) for row in old_cursor.fetchall()])
                
                # 迁移collect_history
                old_cursor.execute("SELECT * FROM collect_history")
                history_cursor.executemany("INSERT INTO collect_history (tag, name, color, create_time, is_deleted) VALUES (?, ?, ?, ?, ?)", 
                                         [(row[1], row[2], row[3], row[4], row[5]) for row in old_cursor.fetchall()])
                
                history_conn.commit()
                history_conn.close()

            # danbooru表不迁移
            
            old_conn.close()

            # 迁移完成后将旧数据库移动到old_db_path
            # 获取绝对路径
            os.makedirs(old_db_path, exist_ok=True)
            abs_db_path = os.path.abspath(db_path)
            abs_old_db_path = os.path.abspath(old_db_path)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            old_db_filename = os.path.basename(abs_db_path)
            new_db_path = os.path.join(abs_old_db_path, f"{timestamp}_{old_db_filename}")
            
            # 检查源文件是否存在
            if os.path.exists(abs_db_path):
                # 移动文件
                shutil.move(abs_db_path, new_db_path)
                print(f"数据迁移完成，旧数据库文件已移动到: {new_db_path}")
            else:
                print(f"警告：源文件 {abs_db_path} 不存在，无法移动")
            
        except sqlite3.Error as e:
            print(f"数据库迁移出错: {e}")
            raise
        except Exception as e:
            print(f"文件移动出错: {e}")
            raise

# 拉去远程数据库 y7S27_wDHXy1xaSQjupJk-Wy
def check_and_initialize_db(db_type):
    db_map = {
        'tags': {
            'path': tags_db_path,
            'url': 'https://api.github.com/repos/weilin9999/WeiLin-Comfyui-Tools-Prompt/contents/tags/2025_03_31'
        },
        'danbooru': {
            'path': danbooru_db_path,
            'url': 'https://api.github.com/repos/weilin9999/WeiLin-Comfyui-Tools-Prompt/contents/danbooru/2025_04_01'
        }
    }
    
    db_info = db_map[db_type]
    conn = sqlite3.connect(db_info['path'])
    cursor = conn.cursor()
    
    try:
        # 检查是否有数据
        if db_type == 'tags':
            cursor.execute("SELECT COUNT(*) FROM tag_groups")
        else:  # danbooru
            cursor.execute("SELECT COUNT(*) FROM danbooru_tag")
            
        count = cursor.fetchone()[0]
        if count == 0:
            print(f"{db_type} 数据库正在拉取中... 地址{db_info['url']}")
            print("大文件处理速度可能会需要点时间，请耐心等待...")
            
            # 获取目录下的所有SQL文件
            response = requests.get(db_info['url'], headers=headers)
            response.raise_for_status()
            
            files = response.json()
            print(f"获取到 {len(files)} 个文件")
            print("只获取前3个Danbooru文件，如果需要完整版请进入插件UI内获取完整版")
            i=0
            for file in files:
                if file['name'].endswith('.sql'):
                    i=i+1
                    if i>3:
                        break
                    print(f"正在处理文件: {file['name']}")

                    # 从GitCode获取SQL文件内容
                    sql_url = "https://raw.githubusercontent.com/weilin9999/WeiLin-Comfyui-Tools-Prompt/master/"+file['path']
                    response = requests.get(sql_url, headers=headers)
                    response.raise_for_status()
                    sql_content = response.text

                    cursor.executescript(sql_content)
                    save_package_path(file['path'])
            
            conn.commit()
            print(f"{db_type} 数据库已成功初始化")
    except sqlite3.OperationalError as e:
        print(f"执行SQL脚本时出错: {e}")
    except requests.RequestException as e:
        print(f"从GitCode获取 {db_type} SQL文件失败: {e}")
    finally:
        conn.close()


# 拉去远程数据库-安装
def install_cloud_file_db(db_type, paths):
    db_map = {
        'tags': {
            'path': tags_db_path,
        },
        'danbooru': {
            'path': danbooru_db_path,
        }
    }
    
    db_info = db_map[db_type]
    conn = sqlite3.connect(db_info['path'])
    cursor = conn.cursor()
    
    try:    
        if len(paths) > 0:
            print(f"从你的选择中获取到 {len(paths)} 个文件")
            for path_url in paths:
                if path_url.endswith('.sql'):
                    print(f"正在处理文件: {path_url}")

                    # 从GitCode获取SQL文件内容
                    sql_url = "https://raw.githubusercontent.com/weilin9999/WeiLin-Comfyui-Tools-Prompt/master/"+path_url
                    response = requests.get(sql_url, headers=headers)
                    response.raise_for_status()
                    sql_content = response.text

                    cursor.executescript(sql_content)
                    save_package_path(path_url)
            
            conn.commit()
            print(f"{db_type} 已完成数据安装。")
    except sqlite3.OperationalError as e:
        print(f"执行SQL脚本时出错: {e}")
    except requests.RequestException as e:
        print(f"从GitCode获取 {db_type} SQL文件失败: {e}")
    finally:
        conn.close()

async def execute_query(db_type: str, query: str, params: Tuple[Any, ...] = ()) -> None:
    """执行SQL查询"""
    conn = await _get_connection(db_type)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            await conn.commit()
    except aiosqlite.Error as e:
        print(f"执行查询时出错: {e}")
        raise

async def fetch_all(db_type: str, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
    """获取所有结果"""
    conn = await _get_connection(db_type)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchall()
    except aiosqlite.Error as e:
        print(f"获取数据时出错: {e}")
        raise

async def fetch_one(db_type: str, query: str, params: Tuple[Any, ...] = ()) -> Optional[Tuple[Any, ...]]:
    """获取单条结果"""
    conn = await _get_connection(db_type)
    try:
        async with conn.cursor() as cursor:
            await cursor.execute(query, params)
            return await cursor.fetchone()
    except aiosqlite.Error as e:
        print(f"获取数据时出错: {e}")
        raise

# 修改set_language函数
def set_language(lang):
    global db_path, tags_db_path, history_db_path, danbooru_db_path
    db_path = os.path.join(current_dir, f'../../../user_data/userdatas_{lang}.db')
    tags_db_path = os.path.join(current_dir, f'../../../user_data/userdatas_{lang}_tags.db')
    history_db_path = os.path.join(current_dir, f'../../../user_data/userdatas_{lang}_history.db')
    danbooru_db_path = os.path.join(current_dir, f'../../../user_data/userdatas_{lang}_danbooru.db')
    
    # 初始化数据库
    create_tables()
    migrate_old_db() # 迁移旧数据库
    migrate_db()  # 新增数据库迁移

    # 检查并初始化tags和danbooru数据库
    if lang == 'zh_CN':
        check_and_initialize_db('tags')
        check_and_initialize_db('danbooru')

# 获取数据库路径
def get_db_path(db_type):
    db_map = {
        'tags': tags_db_path,
        'history': history_db_path,
        'danbooru': danbooru_db_path
    }
    return db_map[db_type]

# 初始化数据库
set_language(localLang)


import atexit

@atexit.register
async def _close_connections() -> None:
    """关闭所有数据库连接"""
    for conn in _connection_pool.values():
        try:
            await conn.close()
        except:
            pass