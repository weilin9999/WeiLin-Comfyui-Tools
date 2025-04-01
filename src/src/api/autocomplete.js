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
}