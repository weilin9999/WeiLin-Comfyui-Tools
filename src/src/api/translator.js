import request from './request'
// 翻译相关接口
export const translatorApi = {
    // 离线翻译
    getTranslateLocal: (text) => {
        return request({
            url: '/prompt/local/translate',
            method: 'post',
            data: { phrase: text }
        })
    },
}