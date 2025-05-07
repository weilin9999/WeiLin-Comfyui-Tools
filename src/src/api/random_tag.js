import request from './request'
// 翻译相关接口
export const randomTagApi = {
    // 获取模板列表
    getTemplateList: async () => {
        return await request({
            url: '/random_template/get_template_list',
            method: 'post',
        })
    },

    getTemplateData: async (name) => {
        return await request({
            url: '/random_template/get_template_data',
            method: 'post',
            data: { name }
        })
    },

    saveTemplateData: async (data) => {
        return await request({
            url: '/random_template/save_template',
            method: 'post',
            data: { data}
        })
    },

    updateTemplateData: async (name,data) => {
        return await request({
            url: '/random_template/update_template',
            method: 'post',
            data: { name , data}
        })
    },

    deleteTemplateData: async (name) => {
        return await request({
            url: '/random_template/delete_template',
            method: 'post',
            data: { name}
        })
    },

    getRandomTemplateApple: async () => {
        return await request({
            url: '/get/setting/get_random_template_setting',
            method: 'post'
        })
    },

    updateRandomTemplateApple: async (path) => {
        return await request({
            url: '/update/setting/update_random_template_setting',
            method: 'post',
            data: {
                path
            }
        })
    },

    goRandomTemplate: async () => {
        return await request({
            url: '/random_template/go_random_template',
            method: 'post',
        })
    },
  
}