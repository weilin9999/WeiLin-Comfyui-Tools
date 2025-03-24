import os
import sqlite3
import locale
import shutil
from ..user_init.user_init import read_init_file

current_dir = os.path.dirname(os.path.abspath(__file__))
db_prefix = 'userdatas_'
db_suffix = 'default'
db_path = os.path.join(current_dir, f'../../../user_data/{db_prefix}{db_suffix}.db')

def create_tables():
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
        CREATE TABLE IF NOT EXISTS danbooru_tag (
            id_index INTEGER PRIMARY KEY AUTOINCREMENT,
            tag TEXT,
            color_id INTEGER,
            translate TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
    ''')
    conn.commit()
    conn.close()

def get_current_version():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT version FROM schema_version ORDER BY version DESC LIMIT 1')
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0

def update_version(version):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schema_version (version) VALUES (?)', (version,))
    conn.commit()
    conn.close()

def migrate():
    current_version = get_current_version()
    if current_version < 1:
        # Migration to version 1: Add is_deleted column to history and collect_history tables
        update_version(1)

def execute_query(query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_one(query, params=()):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result

def set_language(lang):
    global db_path
    if lang == 'zh_CN':
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../user_data/userdatas_zh_CN.db')
        if not os.path.exists(db_path):
            template_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../tags_templete/userdatas_zh_CN.db')
            if os.path.exists(template_path):
                shutil.copy(template_path, db_path)
            else:
                raise FileNotFoundError(f"Template database not found at {template_path}")
    else:
        db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../user_data/userdatas_'+lang+'.db')
    create_tables()
    migrate()

def get_db_path():
    return db_path


# 读取配置文件中的语言设置来决定加载什么数据库文件
userSetting = read_init_file() or {}
# print(userSetting)
if userSetting == {}:
    # 根据系统语言设置数据库文件
    system_lang = locale.getdefaultlocale()[0]
    if system_lang.startswith('zh'):
        set_language('zh_CN')
    else:
        set_language('en_US')
else :
    set_language(userSetting['user_lang'])