from ..dao.dao import fetch_all

async def fuzzy_search(query, limit=10):
    """模糊查询，先查询 tag_tags 表，然后查询 danbooru_tag 表，按匹配度排序"""
    results = []

    # 查询 tag_tags 表，添加排序逻辑
    tag_tags_query = '''
        SELECT text, desc, color, -1 AS color_id,
               CASE 
                   WHEN text = ? THEN 100  -- 完全匹配
                   WHEN text LIKE ? THEN 90  -- 前缀匹配
                   WHEN text LIKE ? THEN 80  -- 包含匹配
                   WHEN desc = ? THEN 70  -- 描述完全匹配
                   WHEN desc LIKE ? THEN 60  -- 描述前缀匹配
                   WHEN desc LIKE ? THEN 50  -- 描述包含匹配
                   ELSE 0
               END AS match_score
        FROM tag_tags
        WHERE text LIKE ? OR desc LIKE ?
        ORDER BY match_score DESC
        LIMIT ?
    '''
    tag_tags_results = await fetch_all('tags', tag_tags_query, (
        query,                # 完全匹配
        f'{query}%',          # 前缀匹配
        f'%{query}%',         # 包含匹配
        query,                # 描述完全匹配
        f'{query}%',          # 描述前缀匹配
        f'%{query}%',         # 描述包含匹配
        f'%{query}%',         # WHERE条件
        f'%{query}%',          # WHERE条件
        limit                 # 限制返回条数
    ))
    
    for result in tag_tags_results:
        results.append({
            "text": result[0],
            "desc": result[1],
            "color": result[2],
            "color_id": result[3],
            "match_score": result[4]  # 保存匹配分数用于后续排序
        })

    # 如果结果不足十个，继续查询 danbooru_tag 表
    if len(results) < limit:
        remaining_limit = limit - len(results)
        danbooru_tag_query = '''
            SELECT tag, translate, NULL AS color, color_id,
                   CASE 
                       WHEN tag = ? THEN 100  -- 完全匹配
                       WHEN tag LIKE ? THEN 90  -- 前缀匹配
                       WHEN tag LIKE ? THEN 80  -- 包含匹配
                       WHEN translate = ? THEN 70  -- 翻译完全匹配
                       WHEN translate LIKE ? THEN 60  -- 翻译前缀匹配
                       WHEN translate LIKE ? THEN 50  -- 翻译包含匹配
                       ELSE 0
                   END AS match_score
            FROM danbooru_tag
            WHERE tag LIKE ? OR translate LIKE ?
            ORDER BY match_score DESC
            LIMIT ?
        '''
        danbooru_tag_results = await fetch_all('danbooru', danbooru_tag_query, (
            query,                # 完全匹配
            f'{query}%',          # 前缀匹配
            f'%{query}%',         # 包含匹配
            query,                # 翻译完全匹配
            f'{query}%',          # 翻译前缀匹配
            f'%{query}%',         # 翻译包含匹配
            f'%{query}%',         # WHERE条件
            f'%{query}%',         # WHERE条件
            remaining_limit
        ))
        
        for result in danbooru_tag_results:
            results.append({
                "text": result[0],
                "desc": result[1],
                "color": result[2],
                "color_id": result[3],
                "match_score": result[4]  # 保存匹配分数
            })

    # 根据匹配分数对所有结果进行排序
    results.sort(key=lambda x: x["match_score"], reverse=True)
    
    # 移除匹配分数字段，返回前10个结果
    for result in results:
        if "match_score" in result:
            del result["match_score"]
            
    return results[:limit]