import request from './request'
// OpenAI 相关接口
export const openaiApi = {
    // 更新设置
    updateOpenAiSetting: async (data) => {
        return await request({
            url: '/prompt/openai/update_settings',
            method: 'post',
            data
        })
    },

    // 添加设置
    addOpenAiSetting: async (data) => {
        return await request({
            url: '/prompt/openai/add_setting',
            method: 'post',
            data
        })
    },

    // 删除设置
    deleteOpenAiSetting: async (data) => {
        return await request({
            url: '/prompt/openai/delete_setting',
            method: 'post',
            data
        })
    },

    // 设置选中
    setOpenAiSelect: async (data) => {
        return await request({
            url: '/prompt/openai/set_select',
            method: 'post',
            data
        })
    },

    getOpenAiSetting: async () => {
        return await request({
            url: '/prompt/openai/get_settings',
            method: 'get'
        })
    }

}