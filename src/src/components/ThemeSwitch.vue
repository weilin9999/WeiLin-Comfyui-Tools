<template>
  <button class="theme-switch" @click="toggleTheme" :title="t('theme.toggle')">
    <div class="switch-icon">
      <!-- 月亮图标 -->
      <svg v-if="isDark" class="moon" viewBox="0 0 24 24">
        <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
      </svg>
      <!-- 太阳图标 -->
      <svg v-else class="sun" viewBox="0 0 24 24">
        <circle cx="12" cy="12" r="5"/>
        <path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/>
      </svg>
    </div>
    <!-- 添加插槽以支持文本显示 -->
    <slot :isDark="isDark"></slot>
  </button>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const STORAGE_PREFIX = 'weilin_tools_'
const THEME_KEY = `${STORAGE_PREFIX}theme`

// 获取主题设置
const isDark = ref(localStorage.getItem(THEME_KEY) === 'dark')

// 切换主题
const toggleTheme = () => {
  isDark.value = !isDark.value
  const container = document.getElementById('weilin_comfyui_tools_prompt_ui_div')
  if (container) {
    container.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  }
  localStorage.setItem(THEME_KEY, isDark.value ? 'dark' : 'light')
}

</script>

<style scoped>
.theme-switch {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.2s ease;
}

.theme-switch:hover {
  background: var(--weilin-prompt-ui-hover-bg-color);
}

.theme-switch:active {
  transform: scale(0.95);
}

.switch-icon {
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.sun, .moon {
  width: 20px;
  height: 20px;
  stroke: var(--weilin-prompt-ui-icon-color);
  fill: none;
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: all 0.3s ease;
}

.moon {
  fill: var(--weilin-prompt-ui-icon-color);
}

/* 添加旋转动画 */
.theme-switch:hover .sun,
.theme-switch:hover .moon {
  transform: rotate(30deg);
}
</style> 