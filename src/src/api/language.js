import request from './request'
// 语言相关接口
export const languageApi = {
    // 获取用户设置
    getUserSetting: () => {
        return request({
            url: '/user_init/get_settings',
            method: 'get',
        })
    },

    // 设置用户语言
    setUserLanguage: (data) => {
        return request({
            url: '/user_init/set_user_lang',
            method: 'post',
            data: {user_lang: data}
        })
    },

    // 启动面板
    startPanel: () => {
        return request({
            url: '/panel/start',
            method: 'post'
        })
    }
}