import request from './request'
// OpenAI 相关接口
export const openaiApi = {
    // 更新设置
    updateOpenAiSetting: (data) => {
        return request({
            url: '/prompt/openai/update_settings',
            method: 'post',
            data
        })
    },

    // 添加设置
    addOpenAiSetting: (data) => {
        return request({
            url: '/prompt/openai/add_setting',
            method: 'post',
            data
        })
    },

    // 删除设置
    deleteOpenAiSetting: (data) => {
        return request({
            url: '/prompt/openai/delete_setting',
            method: 'post',
            data
        })
    },

    // 设置选中
    setOpenAiSelect: (data) => {
        return request({
            url: '/prompt/openai/set_select',
            method: 'post',
            data
        })
    },

    getOpenAiSetting: () => {
        return request({
            url: '/prompt/openai/get_settings',
            method: 'get'
        })
    }

}