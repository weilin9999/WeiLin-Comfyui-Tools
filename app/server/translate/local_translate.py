import os
import glob
import csv

# =================================离线翻译功能=================================

def read_csv_to_dict(file_path):
    translation_dict = {}
    try:
        with open(file_path, 'r', encoding='utf-8-sig') as file:  # 使用 utf-8-sig 来处理 BOM
            reader = csv.reader(file)
            for i, row in enumerate(reader, start=1):  # 使用 enumerate 记录行号
                if len(row) >= 2:
                    original, translated = row[0], row[1]
                    translation_dict[original] = translated
                else:
                    print(f"Warning: Row {i} in {file_path} does not have enough columns.")
    except Exception as e:
        print(f"Failed to read {file_path}: {e}")
    return translation_dict

def translate_text(text, language):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    csv_files = glob.glob(os.path.join(current_dir, '../../../translate_userdatas', '*-'+language+'.csv'))
    
    for csv_file in csv_files:
        translations = read_csv_to_dict(csv_file)
        if text in translations:
            return translations[text]
    
    return ""


# ==============================================================================