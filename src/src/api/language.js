import request from './request'
// 语言相关接口
export const languageApi = {
    // 获取用户设置
    getUserSetting: async () => {
        return await request({
            url: '/user_init/get_settings',
            method: 'get',
        })
    },

    // 设置用户语言
    setUserLanguage: async (data) => {
        return await request({
            url: '/user_init/set_user_lang',
            method: 'post',
            data: {user_lang: data}
        })
    },

    // 启动面板
    startPanel: async () => {
        return await request({
            url: '/panel/start',
            method: 'post'
        })
    }
}