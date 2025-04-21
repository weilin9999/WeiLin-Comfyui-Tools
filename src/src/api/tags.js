import request from './request'
// 添加前缀常量
const STORAGE_PREFIX = 'weilin_tools_'
// 提示词相关接口
export const tagsApi = {

    // 获取提示词列表
    getTagsList: async (params) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: '/prompt/get_group_tags',
            method: 'get',
            params: {...params,lang:savedLocale}
        })
    },

    // 添加主分类
    addPrimaryCategory: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: `/prompt/add_new_f_group`,
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 编辑主分类
    editPrimaryCategory: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: `/prompt/edit_f_group`,
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 删除主分类
    deletePrimaryCategory: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: `/prompt/delete_f_group`,
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 添加子分类
    addSubCategory: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: `/prompt/add_new_s_group`,
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 编辑子分类
    editSubCategory: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: `/prompt/edit_s_group`,
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 删除子分类
    deleteSubCategory: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: `/prompt/delete_s_group`,
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 添加提示词
    addNewTags: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: '/prompt/new_tags',
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 编辑提示词
    editTags: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: '/prompt/edit_tags',
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 删除提示词
    deleteTags: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: '/prompt/delete_tags',
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 批量删除提示词
    batchDeleteTags: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
            return await request({
            url: '/prompt/batch_delete_tags',
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 移动标签
    moveTag: async (data) => {
        // 从 localStorage 获取保存的语言设置
        const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
        return await request({
            url: '/prompt/move_tag',
            method: 'post',
            data: {...data,lang:savedLocale}
        })
    },

    // 获取选择的标签列表
    getTagsGroupList: async () => {
        return await request({
            url: '/prompt/get_groups_list',
            method: 'post',
        })
    },

    // 执行SQL数组脚本
    runSQLToServer: async (arr) => {
        return await request({
            url: '/prompt/run_sql_text',
            method: 'post',
            timeout: 0,
            data: {
                sql: arr
            }
        })
    },
} 