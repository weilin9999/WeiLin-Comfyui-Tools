import request from './request'
// 自动补全相关接口
export const autocompleteApi = {
    // 自动补全获取
    getAutocomplete: async (text) => {
        return await request({
            url: '/prompt/fast/autocomplete',
            method: 'post',
            data: { query: text }
        })
    },

    getAutocompleteLimit: async () => {
        return await request({
            url: '/get/setting/get_auto_limit_setting',
            method: 'post'
        })
    },

    updateAutocompleteLimit: async (limit) => {
        return await request({
            url: '/update/setting/update_auto_limit_setting',
            method: 'post',
            data: {
                limit: limit
            }
        })
    },
}