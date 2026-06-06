import request from './request'
// 添加前缀常量
const STORAGE_PREFIX = 'weilin_tools_'

// 前端缓存机制
const tagCache = {
  categories: null,
  subCategories: {},
  tags: {},
  lastUpdated: 0
}

// 缓存有效期（5分钟）
const CACHE_DURATION = 5 * 60 * 1000

// 清除缓存
const clearCache = () => {
  tagCache.categories = null
  tagCache.subCategories = {}
  tagCache.tags = {}
  tagCache.lastUpdated = 0
}

// 提示词相关接口
export const tagsApi = {
  // 获取提示词列表（带缓存）
  getTagsList: async (params) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'

    // 检查缓存
    const now = Date.now()
    if (tagCache.categories && now - tagCache.lastUpdated < CACHE_DURATION) {
      return tagCache.categories
    }

    // 缓存过期，重新获取
    const result = await request({
      url: '/prompt/get_group_tags',
      method: 'get',
      params: { ...params, lang: savedLocale }
    })

    // 更新缓存
    tagCache.categories = result
    tagCache.lastUpdated = now

    return result
  },

  // 添加主分类
  addPrimaryCategory: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/add_new_f_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 编辑主分类
  editPrimaryCategory: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/edit_f_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 删除主分类
  deletePrimaryCategory: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/delete_f_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 添加子分类
  addSubCategory: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/add_new_s_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 编辑子分类
  editSubCategory: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/edit_s_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 删除子分类
  deleteSubCategory: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/delete_s_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 添加提示词
  addNewTags: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/new_tags',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 编辑提示词
  editTags: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/edit_tags',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 删除提示词
  deleteTags: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/delete_tags',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 批量删除提示词
  batchDeleteTags: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/batch_delete_tags',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 移动标签
  moveTag: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/move_tag',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 获取选择的标签列表
  getTagsGroupList: () => {
    return request({
      url: '/prompt/get_groups_list',
      method: 'post'
    })
  },

  // 执行SQL数组脚本
  runSQLToServer: async (arr) => {
    const result = await request({
      url: '/prompt/run_sql_text',
      method: 'post',
      timeout: 0,
      data: {
        sql: arr
      }
    })
    clearCache()
    return result
  },

  // 移动主分组
  moveMainGroup: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/move_group',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  // 移动子分组
  moveSubGroup: async (data) => {
    // 从 localStorage 获取保存的语言设置
    const savedLocale = localStorage.getItem(`${STORAGE_PREFIX}userLocale`) || 'zh_CN'
    const result = await request({
      url: '/prompt/move_subgroup',
      method: 'post',
      data: { ...data, lang: savedLocale }
    })
    clearCache()
    return result
  },

  getTagMainGroup: () => {
    return request({
      url: '/prompt/get_tag_groups',
      method: 'post'
    })
  },

  // eslint-disable-next-line camelcase
  getTagSubGroup: (p_uuid) => {
    return request({
      url: '/prompt/get_tag_subgroups',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { p_uuid }
    })
  },

  // eslint-disable-next-line camelcase
  getTagList: (g_uuid) => {
    return request({
      url: '/prompt/get_tag_tags',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { g_uuid }
    })
  },

  searchTag: (keyword) => {
    return request({
      url: '/prompt/search_tags',
      method: 'post',
      data: { keyword }
    })
  },

  // 获取生成选项（checkpoint列表、采样器、尺寸预设）
  getGenerationOptions: () => {
    return request({
      url: '/tag_image/options',
      method: 'post'
    })
  },

  // 提交生成任务
  // eslint-disable-next-line camelcase
  generateTagImage: (t_uuid, params) => {
    return request({
      url: '/tag_image/generate',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { t_uuid, params }
    })
  },

  // 按 task_id 查询任务状态
  getTagImageStatus: (task_id) => {
    return request({
      url: '/tag_image/status',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { task_id }
    })
  },

  // 按 t_uuid 查询任务状态（页面刷新恢复用）
  // eslint-disable-next-line camelcase
  getTagImageStatusByUuid: (t_uuid) => {
    return request({
      url: `/tag_image/status/${t_uuid}`,
      method: 'get'
    })
  },

  // 重新生成（删除旧图再生成）
  // eslint-disable-next-line camelcase
  regenerateTagImage: (t_uuid, params) => {
    return request({
      url: '/tag_image/generate',
      method: 'post',
      // eslint-disable-next-line camelcase
      data: { t_uuid, params, regenerate: true }
    })
  },

  // 批量生成
  batchGenerateTagImages: (tags, params) => {
    return request({
      url: '/tag_image/batch_generate',
      method: 'post',
      data: { tags, params }
    })
  }
}
