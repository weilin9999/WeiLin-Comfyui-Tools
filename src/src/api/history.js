import request from './request'

// 历史记录相关接口
export const historyApi = {
    // 获取历史记录
    getHistory: () => {
        return request({
            url: '/prompt/history/get_history',
            method: 'get'
        })
    },

    saveHistory: (data) => {
        return request({
            url: '/prompt/history/add_history',
            method: 'post',
            data
        })
    },

    deleteHistory: (id) => {
        return request({
            url: '/prompt/history/delete_history',
            method: 'post',
            data: { id_index: id }
        })
    },

    batchDeleteHistory: (ids) => {
        return request({
            url: '/prompt/history/batch_delete_history',
            method: 'post',
            data: { id_index: ids }
        })
    },

    getFavorite: () => {
        return request({
            url: '/prompt/collect_history/get_collect_history',
            method: 'get',
        })
    },

    addFavorite: (data) => {
        return request({
            url: '/prompt/collect_history/add_collect_history',
            method: 'post',
            data
        })
    },

    editFavorite: (data) => {
        return request({
            url: '/prompt/collect_history/edit_collect_history',
            method: 'post',
            data
        })
    },

    deleteFavorite: (id) => {
        return request({
            url: '/prompt/collect_history/delete_collect_history',
            method: 'post',
            data: { id_index: id }
        })
    },

    batchDeleteFavorite: (ids) => {
        return request({
            url: '/prompt/collect_history/batch_delete_collect_history',
            method: 'post',
            data: { id_indices: ids }
        })
    },

}