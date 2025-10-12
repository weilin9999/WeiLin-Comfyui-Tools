import request from './request'

export const aiServerApi = {

    getAiServerSetting: async (path) => {
        return await request({
            url: '/ai_server/get_settings',
            method: 'post',
            data: { }
        })
    },

    updateAiServerSetting: async (data) => {
        return await request({
            url: '/ai_server/update_settings',
            method: 'post',
            data
        })
    },

    getAiModels: async () => {
        return await request({
            url: '/ai_server/get_ai_models',
            method: 'post',
            data: { }
        })
    },
}