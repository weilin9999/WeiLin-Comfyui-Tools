import request from './request'

// 历史记录相关接口
export const historyApi = {
    // 获取历史记录
    getHistory: async () => {
        return await request({
            url: '/prompt/history/get_history',
            method: 'get'
        })
    },

    saveHistory:async (data) => {
        return await request({
            url: '/prompt/history/add_history',
            method: 'post',
            data
        })
    },

    deleteHistory:async (id) => {
        return await request({
            url: '/prompt/history/delete_history',
            method: 'post',
            data: { id_index: id }
        })
    },

    batchDeleteHistory:async(ids) => {
        return await request({
            url: '/prompt/history/batch_delete_history',
            method: 'post',
            data: { id_index: ids }
        })
    },

    getFavorite:async () => {
        return await request({
            url: '/prompt/collect_history/get_collect_history',
            method: 'get',
        })
    },

    addFavorite: async(data) => {
        return await request({
            url: '/prompt/collect_history/add_collect_history',
            method: 'post',
            data
        })
    },

    editFavorite:async (data) => {
        return await request({
            url: '/prompt/collect_history/edit_collect_history',
            method: 'post',
            data
        })
    },

    deleteFavorite: async(id) => {
        return await request({
            url: '/prompt/collect_history/delete_collect_history',
            method: 'post',
            data: { id_index: id }
        })
    },

    batchDeleteFavorite: async(ids) => {
        return await request({
            url: '/prompt/collect_history/batch_delete_collect_history',
            method: 'post',
            data: { id_indices: ids }
        })
    },

}