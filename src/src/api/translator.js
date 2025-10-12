import request from './request'
// 翻译相关接口
export const translatorApi = {
    // 离线翻译
    getTranslateLocal: async (text) => {
        return await request({
            url: '/prompt/local/translate',
            method: 'post',
            data: { phrase: text }
        })
    },
    // 获取翻译包信息
    getTranslatePackagesState: async () => {
        return await request({
            url: '/translate/get/packages/state',
            method: 'post',
            data: {  }
        })
    },
    // 获取翻译设置
    getTranslateSetting: async () => {
        return await request({
            url: '/translate/get/setting',
            method: 'post',
            data: {  }
        })
    },
    // 应用翻译设置
    applyTranslateSetting: async (ss) => {
        return await request({
            url: '/translate/apply_setting',
            method: 'post',
            data: { setting: ss  }
        })
    },
    // 安装翻译包
    installTranslatePackage: async () => {
        return await request({
            url: '/translate/install/translaterpackage',
            method: 'post',
            timeout: 0,
            data: {  }
        })
    },
    // 获取翻译库设置
    getTranslateBuktSetting: async () => {
        return await request({
            url: '/translate/get/tran_setting',
            method: 'post',
            data: {  }
        })
    },
    // 应用翻译库设置
    saveTranslateSetting: async (a,b,c) => {
        return await request({
            url: '/translate/save_tran/setting',
            method: 'post',
            data: { service: a,source_lang:b,target_lang:c  }
        })
    },
    // 翻译文本
    translaterText: async (str_object, text) => {
        return await request({
            url: '/translate/tran/text',
            method: 'post',
            timeout: 0,
            data: { str_object, text }
        })
    },
    // 翻译输入的文本
    translaterInputText: async (str_object, text) => {
        return await request({
            url: '/translate/tran/input',
            method: 'post',
            timeout: 0,
            data: { str_object, text }
        })
    },
}