import request from './request'

export const danbooruApi = {
    // 查询获取Danbooru列表
    searchDanbooru: async (search="",page=1,limit=100) => {
        /* 
            search: "girl",  // 可选，搜索关键词
            page: 1,        // 可选，默认1
            limit: 20       // 可选，默认100
        */
        return await request({
            url: '/danbooru/get_tags',
            method: 'post',
            data: { search,page,limit }
        })
    },
    addDanbooruTag: async (data) => {
        /*
            {
                tag: "new_tag",
                color_id: 1,      // 可选，默认0
                translate: "新标签", // 可选
                hot: 0,          // 可选，默认0
                aliases: 0       // 可选，默认0
            }
        */
        return await request({
            url: '/danbooru/add_tag',
            method: 'post',
            data: data
        })
    },
    updateDanbooruTag: async (data) => {
        /*
            {
                id: 123,  // 标签ID
                update_data: {
                translate: "更新后的翻译",
                hot: 1
                }
            }
        */
        return await request({
            url: '/danbooru/update_tag',
            method: 'post',
            timeout: 0,
            data:data
        })
    },
    deleteDanbooruTag: async (id) => {
        /*
            {
                id: 123  // 要删除的标签ID
            }
        */
        return await request({
            url: '/danbooru/delete_tag',
            method: 'post',
            timeout: 0,
            data:{ id }
        })
    },
    batchDeleteDanbooruTags: async (values) => {
        return await request({
            url: '/danbooru/batch_delete_tag',
            method: 'post',
            timeout: 0,
            data:{ values }
        })
    },
     // 执行SQL数组脚本
    runSQLToServer: async (arr) => {
        return await request({
            url: '/danbooru/run_sql_text',
            method: 'post',
            timeout: 0,
            data: {
                sql: arr
            }
        })
    },
}