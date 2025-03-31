from ..dao.dao import fetch_one

def get_translation_from_tag_tags(word):
    """从 tag_tags 表中获取单词的翻译"""
    query = 'SELECT desc, color FROM tag_tags WHERE text = ?'
    result = fetch_one('tags',query, (word,))
    if result:
        return {"translate": result[0], "color": result[1], "color_id": -1}
    return None

def get_translation_from_danbooru_tag(word):
    """从 danbooru_tag 表中获取单词的翻译"""
    query = 'SELECT translate, color_id FROM danbooru_tag WHERE tag = ?'
    result = fetch_one('danbooru',query, (word,))
    if result:
        return {"translate": result[0], "color": None, "color_id": result[1]}
    return None

def get_translation(word):
    """从数据库中获取单词的翻译，优先从 tag_tags 表中获取"""
    translation = get_translation_from_tag_tags(word)
    if translation:
        return translation
    return get_translation_from_danbooru_tag(word)

def translate_phrase(phrase):
    """翻译整个词组"""
    words = phrase.split()
    translated_dict = {"translate": "", "color": None, "color_id": None}
    i = 0

    while i < len(words):
        found_translation = False
        for j in range(len(words), i, -1):
            sub_phrase = ' '.join(words[i:j])
            translation = get_translation(sub_phrase)
            if translation:
                translated_dict["translate"] += translation["translate"] + " "
                if translation["color"] is not None:
                    translated_dict["color"] = translation["color"]
                if translation["color_id"] is not None:
                    translated_dict["color_id"] = translation["color_id"]
                i = j
                found_translation = True
                break
        if not found_translation:
            translated_dict["translate"] += words[i] + " "
            i += 1

    translated_dict["translate"] = translated_dict["translate"].strip()
    return translated_dict
