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
    // 获取翻译包信息
    getTranslatePackagesState: () => {
        return request({
            url: '/translate/get/packages/state',
            method: 'post',
            data: {  }
        })
    },
    // 获取翻译设置
    getTranslateSetting: () => {
        return request({
            url: '/translate/get/setting',
            method: 'post',
            data: {  }
        })
    },
    // 应用翻译设置
    applyTranslateSetting: (ss) => {
        return request({
            url: '/translate/apply_setting',
            method: 'post',
            data: { setting: ss  }
        })
    },
    // 安装翻译包
    installTranslatePackage: () => {
        return request({
            url: '/translate/install/translaterpackage',
            method: 'post',
            timeout: 0,
            data: {  }
        })
    },
    // 获取翻译库设置
    getTranslateBuktSetting: () => {
        return request({
            url: '/translate/get/tran_setting',
            method: 'post',
            data: {  }
        })
    },
    // 应用翻译库设置
    saveTranslateSetting: (a,b,c) => {
        return request({
            url: '/translate/save_tran/setting',
            method: 'post',
            data: { service: a,source_lang:b,target_lang:c  }
        })
    },
    // 翻译文本
    translaterText: (text) => {
        return request({
            url: '/translate/tran/text',
            method: 'post',
            timeout: 0,
            data: { text }
        })
    },
    // 翻译输入的文本
    translaterInputText: (text) => {
        return request({
            url: '/translate/tran/input',
            method: 'post',
            timeout: 0,
            data: { text }
        })
    },
}