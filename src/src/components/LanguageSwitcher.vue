<template>
  <div class="language-selector" ref="selectorRef">
    <div class="language-selector-content">
      <div v-for="(lang, index) in languages" :style="{ 'margin-top': index === 0 ? '0' : '2px' }" :key="lang.code"
        class="language-option" :class="{ active: currentLang === lang.code }" @click="switchLanguage(lang.code)">
        <span class="lang-name">{{ lang.name }}</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits } from 'vue'
import { useI18n } from 'vue-i18n'
import { setLocale } from '@/i18n'
import { useTagStore } from '@/stores/tagStore'
import { languageApi } from '@/api/language'
import message from "@/utils/message"

const { t } = useI18n()
const selectorRef = ref(null)
const tagStore = useTagStore()
const currentLang = computed(() => tagStore.userSetting.user_lang)

const languages = [
  { code: 'zh_CN', name: '简体中文' },
  { code: 'en_US', name: 'English' },
  // { code: 'ja_JP', name: '日本語' },
  // { code: 'ko_KR', name: '한국어' },
  // { code: 'ru_RU', name: 'Русский' },
  // { code: 'es_ES', name: 'Español' },
  // { code: 'fr_FR', name: 'Français' },
  // { code: 'de_DE', name: 'Deutsch' },
  // { code: 'it_IT', name: 'Italiano' },
  // { code: 'pt_PT', name: 'Português' },
]

const emit = defineEmits(['close'])

const switchLanguage = (locale) => {
  setLanguage(locale)
  emit('close', {})
}

const setLanguage = (lang) => {
  languageApi.setUserLanguage(lang).then(res => {
    setLocale(lang)
    window.postMessage({
      type: 'weilin_prompt_ui_tag_manager_refresh'
    }, '*')
    window.postMessage({
      type: 'weilin_prompt_ui_refresh_all_data'
    }, '*')
    message({ type: "success", str: 'message.setLanguageSuccess' })
  }).catch(err => {
    message({ type: "warn", str: 'message.setLanguageFailed' })
  })
}

// 暴露给父组件的方法，用于设置位置
const setPosition = (buttonRect) => {
  if (!selectorRef.value) return

  const selector = selectorRef.value
  selector.style.position = 'fixed'
  selector.style.top = `${buttonRect.bottom}px`
  //   selector.style.left = `${buttonRect.left}px`
}

defineExpose({ setPosition })
</script>

<style scoped>
.language-selector {
  min-width: 140px;
  background: var(--weilin-prompt-ui-primary-bg);
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 8px;
  box-shadow: 0 4px 12px var(--weilin-prompt-ui-shadow-color);
  z-index: 1000;
}

.language-selector-content {
  padding: 4px;
}

.language-option {
  padding: 8px 16px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 4px;
  color: var(--weilin-prompt-ui-primary-text);
  font-size: 14px;
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.language-option:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.language-option.active {
  color: var(--weilin-prompt-ui-primary-color);
  background-color: var(--weilin-prompt-ui-hover-bg-color);
  font-weight: 500;
}

.lang-name {
  display: block;
}
</style>