import { createI18n } from 'vue-i18n'
import zh_CN from './locales/zh_CN'
import en_US from './locales/en_US'
import { useTagStore } from '@/stores/tagStore'
import { languageApi } from '@/api/language'

// 延迟获取 pinia 实例
const getTagStore = () => {
  return useTagStore()
}

// 创建 i18n 实例
const i18n = createI18n({
  legacy: false,
  locale: 'zh_CN', // 默认语言
  fallbackLocale: 'zh_CN',
  messages: {
    zh_CN,
    en_US
  }
})

// 延迟初始化语言设置
const initLocale = () => {
  const tagStore = getTagStore()
  languageApi.getUserSetting().then(res => {
    tagStore.setUserSetting(res.data)
    const savedLocale = tagStore.userSetting?.user_lang || 'zh_CN'
    i18n.global.locale.value = savedLocale
  })
}

// 导出设置语言的方法
export const setLocale = (locale) => {
  i18n.global.locale.value = locale
  const tagStore = getTagStore()
  tagStore.setUserSetting({ user_lang: locale })
}

// 导出初始化方法
export const initI18n = () => {
  initLocale()
}

export default i18n