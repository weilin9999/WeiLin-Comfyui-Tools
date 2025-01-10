import os
import glob
import json
import csv

# 获取文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
collect_history_file_path = os.path.join(
    current_dir, '../../../history_userdatas/collect_history_datas.json')


def _get_tags_filename(name):
    """获取 zh_CN.json 文件的路径"""
    file = os.path.join(
        current_dir, '../../../tags_userdatas/', name + '.json')
    return file


def read_collect_history():
    """读取 collect_history_datas.json 文件并返回内容"""
    if os.path.exists(collect_history_file_path):
        with open(collect_history_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    else:
        return []


def read_tag_json(lang):
    """读取 zh_CN.json 文件并返回内容"""
    zh_cn_file_path = _get_tags_filename(lang)
    if os.path.exists(zh_cn_file_path):
        with open(zh_cn_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            return data
    else:
        return []


def read_danbooru_csv(language):
    """读取 danbooru-0-zh_CN.csv 文件并返回内容"""
    csv_files = glob.glob(os.path.join(
        current_dir, '../../../translate_userdatas', '*-'+language+'.csv'))
    translations = {}
    for csv_file in csv_files:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 2:
                    tag, desc = row[0], row[1]
                    translations[tag] = desc
    return translations


def integrate_files(lang):
    """整合三个文件的内容"""
    collect_history = read_collect_history()
    zh_cn_data = read_tag_json(lang)
    danbooru_translations = read_danbooru_csv(lang)

    integrated_data = []

    # 整合 collect_history_datas.json
    for entry in collect_history:
        integrated_data.append({
            "tag": entry['tag'],
            "desc": entry['name'],
            "color": entry['color']
        })

    # 整合 zh_CN.json
    for group in zh_cn_data:
        for subgroup in group['groups']:
            for tag in subgroup['tags']:
                integrated_data.append({
                    "tag": tag['text'],
                    "desc": tag['desc'],
                    "color": tag['color']
                })

    # 整合 danbooru-0-zh_CN.csv
    for tag, desc in danbooru_translations.items():
        integrated_data.append({
            "tag": tag,
            "desc": desc,
            "color": ""
        })

    return integrated_data
