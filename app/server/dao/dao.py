import os
import sqlite3
import locale
import datetime
import shutil
import requests
from ..user_init.user_init import read_init_file

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
                translate TEXT
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
    conn = sqlite3.connect(db_map[db_type])
    cursor = conn.cursor()
    cursor.execute('INSERT INTO schema_version (version) VALUES (?)', (version,))
    conn.commit()
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
                
                # 迁移tag_groups
                old_cursor.execute("SELECT * FROM tag_groups")
                tags_cursor.executemany("INSERT INTO tag_groups (name, color, create_time) VALUES (?, ?, ?)", 
                                     [(row[1], row[2], row[3]) for row in old_cursor.fetchall()])
                
                # 迁移tag_subgroups
                old_cursor.execute("SELECT * FROM tag_subgroups")
                tags_cursor.executemany("INSERT INTO tag_subgroups (group_id, name, color, create_time) VALUES (?, ?, ?, ?)", 
                                      [(row[1], row[2], row[3], row[4]) for row in old_cursor.fetchall()])
                
                # 迁移tag_tags
                old_cursor.execute("SELECT * FROM tag_tags")
                tags_cursor.executemany("INSERT INTO tag_tags (subgroup_id, text, desc, color, create_time) VALUES (?, ?, ?, ?, ?)", 
                                      [(row[1], row[2], row[3], row[4], row[5]) for row in old_cursor.fetchall()])
                
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

            # 迁移danbooru表
            old_cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='danbooru_tag'")
            if old_cursor.fetchone():
                if not os.path.exists(danbooru_db_path):
                    open(danbooru_db_path, 'a').close()
                
                danbooru_conn = sqlite3.connect(danbooru_db_path)
                danbooru_cursor = danbooru_conn.cursor()
                
                # 迁移danbooru_tag
                old_cursor.execute("SELECT * FROM danbooru_tag")
                danbooru_cursor.executemany("INSERT INTO danbooru_tag (tag, color_id, translate) VALUES (?, ?, ?)", 
                                          [(row[1], row[2], row[3]) for row in old_cursor.fetchall()])
                
                danbooru_conn.commit()
                danbooru_conn.close()

            old_conn.close()

            # 迁移完成后将旧数据库移动到old_db_path
            # 获取绝对路径
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

# 拉去远程数据库
def check_and_initialize_db(db_type):
    db_map = {
        'tags': {
            'path': tags_db_path,
            'url': 'https://github.com/weilin9999/WeiLin-Comfyui-Tools-Prompt/tree/master/tags/2025_03_031'
        },
        'danbooru': {
            'path': danbooru_db_path,
            'url': 'https://github.com/weilin9999/WeiLin-Comfyui-Tools-Prompt/tree/master/danbooru/2025_03_31'
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
            api_url = db_info['url'].replace('https://github.com', 'https://api.github.com/repos').replace('/tree/master/', '/contents/')
            print(api_url)
            response = requests.get(api_url)
            response.raise_for_status()
            
            files = response.json()
            print(f"获取到 {len(files)} 个文件")
            for file in files:
                if file['name'].endswith('.sql'):
                    file_url = file['download_url']
                    print(f"正在处理文件: {file['name']}")
                    file_response = requests.get(file_url)
                    file_response.raise_for_status()
                    sql_content = file_response.text
                    cursor.executescript(sql_content)
            
            conn.commit()
            print(f"{db_type} 数据库已成功初始化")
    except sqlite3.OperationalError as e:
        print(f"执行SQL脚本时出错: {e}")
    except requests.RequestException as e:
        print(f"从GitHub获取 {db_type} SQL文件失败: {e}")
    finally:
        conn.close()

def execute_query(db_type, query, params=()):
    db_map = {
        'tags': tags_db_path,
        'history': history_db_path,
        'danbooru': danbooru_db_path
    }
    conn = sqlite3.connect(db_map[db_type])
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    conn.close()

def fetch_all(db_type, query, params=()):
    db_map = {
        'tags': tags_db_path,
        'history': history_db_path,
        'danbooru': danbooru_db_path
    }
    conn = sqlite3.connect(db_map[db_type])
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.close()
    return results

def fetch_one(db_type, query, params=()):
    db_map = {
        'tags': tags_db_path,
        'history': history_db_path,
        'danbooru': danbooru_db_path
    }
    conn = sqlite3.connect(db_map[db_type])
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchone()
    conn.close()
    return result

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