from ..dao.dao import fetch_all

def fuzzy_search(query):
    """模糊查询，先查询 tag_tags 表，然后查询 danbooru_tag 表"""
    results = []

    # 查询 tag_tags 表
    tag_tags_query = '''
        SELECT text, desc, color, -1 AS color_id
        FROM tag_tags
        WHERE text LIKE ? OR desc LIKE ?
        LIMIT 10
    '''
    tag_tags_results = fetch_all(tag_tags_query, (f'%{query}%', f'%{query}%'))
    for result in tag_tags_results:
        results.append({
            "text": result[0],
            "desc": result[1],
            "color": result[2],
            "color_id": result[3]
        })

    # 如果结果不足十个，继续查询 danbooru_tag 表
    if len(results) < 10:
        remaining_limit = 10 - len(results)
        danbooru_tag_query = '''
            SELECT tag, translate, NULL AS color, color_id
            FROM danbooru_tag
            WHERE tag LIKE ? OR translate LIKE ?
            LIMIT ?
        '''
        danbooru_tag_results = fetch_all(danbooru_tag_query, (f'%{query}%', f'%{query}%', remaining_limit))
        for result in danbooru_tag_results:
            results.append({
                "text": result[0],
                "desc": result[1],
                "color": result[2],
                "color_id": result[3]
            })

    return results[:10]