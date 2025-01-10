import os
import json
import time
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))

def _get_tags_filename(name):
    file = os.path.join(current_dir, '../../../tags_userdatas/', name + '.json')
    return file

def get_group_tags(lang):
    tags_file = _get_tags_filename(lang)
    if not os.path.exists(tags_file):
        tags_file = _get_tags_filename('default')
    if not os.path.exists(tags_file):
        print(f"File {tags_file} does not exist.")
        return []

    try:
        with open(tags_file, 'r', encoding='utf8') as f:
            data = json.load(f)
        
        # 对每个子组的标签按创建时间进行排序
        for group in data:
            for subgroup in group['groups']:
                subgroup['tags'] = sorted(subgroup['tags'], key=lambda x: x['create_time'], reverse=True)
        
        return data
    except Exception as e:
        print(f"Error parsing JSON from file {tags_file}: {e}")
        return []

def generate_unique_id():
    return str(uuid.uuid4())

def generate_unique_timestamp():
    return int(time.time() * 1000) + uuid.uuid4().int % 1000

def add_group_tag(lang, text, desc, id_index, color):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    for group in data:
        for subgroup in group['groups']:
            if subgroup['id_index'] == id_index:
                new_tag = {
                    "text": text,
                    "desc": desc,
                    "color": color,
                    "id_index": generate_unique_id(),
                    "create_time": generate_unique_timestamp()
                }
                subgroup['tags'].append(new_tag)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def edit_group_tag(lang, text, desc, id_index, color):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    for group in data:
        for subgroup in group['groups']:
            for tag in subgroup['tags']:
                if tag['id_index'] == id_index:
                    tag['text'] = text
                    tag['desc'] = desc
                    tag['color'] = color

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def move_tag(lang, id_index, reference_id_index, position='before'):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    target_tag = None
    found_reference = False
    original_subgroup = None

    # 查找并移除目标标签
    for group in data:
        for subgroup in group['groups']:
            for tag in subgroup['tags']:
                if tag['id_index'] == id_index:
                    target_tag = tag
                    original_subgroup = subgroup
                    subgroup['tags'].remove(tag)
                    break

    if target_tag is None:
        return {"info": "Tag not found"}

    # 查找参考标签并调整创建时间
    for group in data:
        for subgroup in group['groups']:
            for tag in subgroup['tags']:
                if tag['id_index'] == reference_id_index:
                    found_reference = True
                    if position == 'before':
                        target_tag['create_time'] = tag['create_time'] + 1
                    elif position == 'after':
                        target_tag['create_time'] = tag['create_time'] - 1
                    else:
                        return {"info": "Invalid position"}
                    break

    if not found_reference:
        return {"info": "Reference tag not found"}

    # 将目标标签重新插入到原来的子组并排序
    if original_subgroup is not None:
        original_subgroup['tags'].append(target_tag)
        original_subgroup['tags'] = sorted(original_subgroup['tags'], key=lambda x: x['create_time'], reverse=True)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

    return {"info": "Tag moved"}

def delete_group_tag(lang, id_index):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    for group in data:
        for subgroup in group['groups']:
            subgroup['tags'] = [tag for tag in subgroup['tags'] if tag['id_index'] != id_index]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def batch_delete_group_tags(lang, id_indices):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    for id_index in id_indices:
        for group in data:
            for subgroup in group['groups']:
                subgroup['tags'] = [tag for tag in subgroup['tags'] if tag['id_index'] != id_index]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_new_node_group(lang, key, color):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    new_group = {
        'name': key,
        'color': color,
        'id_index': generate_unique_id(),
        "create_time": generate_unique_timestamp(),
        'groups': []
    }

    data.append(new_group)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def add_new_group(lang, key, group_key, color):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    new_subgroup = {
        'name': group_key,
        'color': color,
        'id_index': generate_unique_id(),
        "create_time": generate_unique_timestamp(),
        'tags': []
    }

    for group in data:
        if group['id_index'] == key:
            group['groups'].append(new_subgroup)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def edit_node_group(lang, id_index, new_key, new_color):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    if not data:
        return
    for group in data:
        if group['id_index'] == id_index:
            group['name'] = new_key
            group['color'] = new_color

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def edit_child_node_group(lang, id_index, new_key, new_color):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    for group in data:
        for subgroup in group['groups']:
            if subgroup['id_index'] == id_index:
                subgroup['name'] = new_key
                subgroup['color'] = new_color


    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def delete_node_group(lang, id_index):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    data = [group for group in data if group['id_index'] != id_index]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

def delete_child_node_group(lang, id_index):
    file_path = _get_tags_filename(lang)

    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
    else:
        data = []

    for group in data:
        group['groups'] = [subgroup for subgroup in group['groups'] if subgroup['id_index'] != id_index]

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

