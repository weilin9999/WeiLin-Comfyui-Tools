<template>
  <Dialog v-model="dialogVisible" :title="t('importDialog.selectTitle')">
    <div class="tag-manager">
      <!-- 分类导航区域 -->
      <div class="category-tabs">
        <!-- 一级分类 tabs -->
        <div class="tabs-wrapper primary-tabs">
          <div class="tabs-scroll">
            <div v-for="(category, index) in categories" :key="'Tabss-' + index" class="tab-item"
              :class="{ active: selectedCategory?.name === category.name }" :style="{
                backgroundColor: selectedCategory?.name === category.name ? 'var(--primary-color)' : category.color,
                color: selectedCategory?.name === category.name ? '#ffffff' : getContrastColor(category.color)
              }" @click="selectCategory(category)" >
              <span class="tab-text">{{ category.name }}</span>
            </div>
          </div>
        </div>

        <!-- 分组 tabs -->
        <div class="tabs-wrapper group-tabs" v-if="selectedCategory">
          <div class="tabs-scroll">
            <div v-for="(group, index) in selectedCategory.groups" :key="'TabsSw-' + index" class="tab-item"
              :class="{ active: selectedGroup?.name === group.name }" :style="{
                backgroundColor: selectedGroup?.name === group.name ? 'var(--primary-color)' : group.color,
                color: selectedGroup?.name === group.name ? '#ffffff' : getContrastColor(group.color)
              }" @click="selectGroup(group)">
              <span class="tab-text">{{ group.name }}</span>
            </div>
          </div>
        </div>
      </div>

    </div>
    <template #footer>
      <button @click="dialogVisible = false">{{ t('promptBox.settings.close') }}</button>
      <button @click="selectSureThis">{{ t('importDialog.sureSelect') }}</button>
    </template>
  </Dialog>
</template>

<script setup>
import Dialog from '@/components/Dialog.vue'
import { ref, onMounted, onBeforeUnmount } from 'vue'
import { useI18n } from 'vue-i18n'
import { tagsApi } from '@/api/tags'
import message from '@/utils/message'

const { t } = useI18n()

const emit = defineEmits(['sureSelect'])

// 状态管理
const categories = ref([]);
const selectedCategory = ref(null)
const selectedGroup = ref(null)
const selectedTags = ref([]); // 用于存储选中的标签ID
const isDeleteTagAction = ref(false)

const dialogVisible = ref(false)

// 获取标签列表
const getTagsList = () => {
  window.postMessage({
    type: 'weilin_prompt_ui_tag_manager_refresh_select'
  }, '*')
}

const refreshTagsGoThis = async () => {
  try {
    const res = await tagsApi.getTagsGroupList()
    // console.log(res)
    categories.value = res.info
    // 如果当前分组存在，重新设置当前分组
    if (selectedGroup.value) {
      const group = categories.value
        .flatMap(category => category.groups) // 获取所有分组
        .find(g => g.p_uuid === selectedGroup.value.p_uuid); // 根据 p_uuid 查找当前分组

      if (group) {
        selectedGroup.value = group; // 重新设置当前分组
      } else {
        selectedGroup.value = null; // 如果分组不存在，重置为 null
      }
    }

    // 如果当前分类存在，重新设置当前分类
    if (selectedCategory.value) {
      const category = categories.value.find(c => c.p_uuid === selectedCategory.value.p_uuid); // 根据 p_uuid 查找当前分类

      if (category) {
        selectedCategory.value = category; // 重新设置当前分类
      } else {
        selectedCategory.value = null; // 如果分类不存在，重置为 null
      }
    }
  } catch (error) {
    console.error('获取标签列表失败:', error)
  }
}


// 添加获取对比色的函数
const getContrastColor = (backgroundColor) => {
  // 如果背景色是透明的，返回默认文本颜色
  if (!backgroundColor || backgroundColor === 'transparent') {
    return 'var(--primary-text)'
  }

  // 解析 RGB 值
  let r, g, b, a = 1
  if (backgroundColor.startsWith('rgba')) {
    const matches = backgroundColor.match(/rgba\((\d+),\s*(\d+),\s*(\d+),\s*([\d.]+)\)/)
    if (matches) {
      [, r, g, b, a] = matches.map(Number)
    }
  } else if (backgroundColor.startsWith('rgb')) {
    const matches = backgroundColor.match(/rgb\((\d+),\s*(\d+),\s*(\d+)\)/)
    if (matches) {
      [, r, g, b] = matches.map(Number)
    }
  }

  // 如果透明度太低，返回默认文本颜色
  if (a < 0.5) {
    return 'var(--primary-text)'
  }

  // 计算亮度
  const brightness = (r * 299 + g * 587 + b * 114) / 1000
  return brightness > 128 ? '#000000' : '#ffffff'
}



onMounted(() => {
  // 添加全局点击事件监听
  window.addEventListener('message', handleMessage)
})

onBeforeUnmount(() => {
  window.removeEventListener('message', handleMessage)
})



// 选择分类
const selectCategory = (category) => {
  selectedCategory.value = category
  selectedGroup.value = null
  isDeleteTagAction.value = false
  selectedTags.value = []
}

// 选择分组
const selectGroup = (group) => {
  selectedGroup.value = group
  isDeleteTagAction.value = false
  selectedTags.value = []
}


// 处理消息
const handleMessage = (event) => {
  // console.log(event.data.type)
  if (event.data.type === 'weilin_prompt_ui_tag_manager_refresh_select') {
    refreshTagsGoThis()
  }
}

const selectSureThis = () => {
  if(selectedGroup.value == null || selectedCategory.value == null){
    message({ type: "warn", str: 'message.pleaseSelectGroup' });
    return
  }
  emit('sureSelect', {group: selectedCategory.value , sub: selectedGroup.value });
  dialogVisible.value = false
}


defineExpose({
    open: () => {
      getTagsList()
      dialogVisible.value = true
    }
})
</script>

<style scoped>
.tag-manager {
  display: flex;
  flex-direction: column;
  padding: 0 16px 16px 16px;
  background: var(--weilin-prompt-ui-primary-bg);
  height: 100%;
  box-sizing: border-box;
}

.category-tabs {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-bottom: 16px;
}

.tabs-wrapper {
  position: relative;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.tabs-scroll {
  display: flex;
  gap: 2px;
  padding: 0 2px 2px;
  flex-wrap: wrap;
  align-items: flex-end;
}

/* 自定义滚动条样式 */
.tabs-scroll::-webkit-scrollbar {
  height: 10px;
  /* 设置滚动条高度 */
}

.tabs-scroll::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
  /* 滚动条轨道颜色 */
}

.tabs-scroll::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  /* 滚动条颜色 */
  border-radius: 3px;
  /* 滚动条圆角 */
}

.tabs-scroll::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
  /* 滚动条悬停颜色 */
}

.tab-item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 2px 15px;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-bottom: none;
  position: relative;
  font-size: 10px;
  height: 34px;
  min-width: unset;
  width: fit-content;
}

.tab-text {
  flex: 0 0 auto;
  white-space: nowrap;
  text-align: center;
  margin: 0 4px;
  color: var(--weilin-prompt-ui-primary-text);
}

.tab-actions {
  display: flex;
  gap: 2px;
  align-items: center;
  transition: opacity 0.3s;
  position: absolute;
  margin-left: 0;
  top: -25px;
  padding: 5px;
  background-color: #00000080;
  border-radius: 4px;
  z-index: 1000;
}

.action-btn {
  padding: 4px;
  background: none;
  border: none;
  cursor: pointer;
  opacity: 0.7;
  transition: opacity 0.3s;
  color: inherit;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  opacity: 1;
}

.action-icon {
  width: 16px;
  height: 16px;
  fill: currentColor;
}

.add-tab {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 4px 12px;
  background: none;
  border: 1px dashed var(--weilin-prompt-ui-border-color);
  border-radius: 4px 4px 0 0;
  color: var(--weilin-prompt-ui-secondary-text);
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
  font-size: 13px;
  height: 28px;
  width: fit-content;
}

.add-tab:hover {
  color: var(--weilin-prompt-ui-primary-color);
  border-color: var(--weilin-prompt-ui-primary-color);
  background: var(--weilin-prompt-ui-secondary-bg);
}

.plus-icon {
  font-size: 16px;
  line-height: 1;
}

/* 暗色主题适配 */
:root[data-theme="dark"] .tab-item {
  background: var(--weilin-prompt-ui-primary-bg);
}

:root[data-theme="dark"] .tab-item:hover {
  background: var(--weilin-prompt-ui-secondary-bg);
}

:root[data-theme="dark"] .add-tab:hover {
  background: var(--weilin-prompt-ui-secondary-bg);
}

.tags-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.tags-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.tags-title {
  font-size: 20px;
  font-weight: bolder;
  color: var(--weilin-prompt-ui-primary-text);
}

.tags-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding: 16px;
}

.tag-wrapper {
  display: inline-flex;
  min-width: 100px;
  max-width: 200px;
  flex-direction: column;
}

.tag-content {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: fit-content;
}

.tag-main {
  position: relative;
  display: inline-flex;
  align-items: center;
  padding: 6px 12px;
  border-radius: 8px 8px 0 0;
  font-size: 13px;
  font-weight: 500;
  color: var(--weilin-prompt-ui-primary-text);
  transition: all 0.3s ease;
  cursor: default;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-bottom: none;
  width: 100%;
  box-sizing: border-box;
  justify-content: center;
}

.tag-desc {
  font-size: 12px;
  color: var(--weilin-prompt-ui-secondary-text);
  text-align: center;
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
  background-color: var(--weilin-prompt-ui-secondary-bg);
  padding: 6px 12px;
  border-radius: 0 0 8px 8px;
  width: 100%;
  box-sizing: border-box;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-top: none;
}

.tag-actions {
  background-color: rgba(0, 0, 0, 0.5);
  border-radius: 6px;
  position: absolute;
  right: 8px;
  display: inline-flex;
  opacity: 0;
  transition: opacity 0.2s ease;
  top: -15px;
}

.tag-content:hover .tag-actions {
  opacity: 1;
}

.action-btn {
  padding: 2px;
  background: none;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn svg {
  width: 12px;
  height: 12px;
  fill: var(--weilin-prompt-ui-secondary-text);
  transition: fill 0.2s ease;
}

.action-btn:hover svg {
  fill: var(--weilin-prompt-ui-primary-text);
}

/* 添加动画效果 */
.tag-content:hover {
  transform: translateY(-1px);
  filter: drop-shadow(0 2px 4px var(--weilin-prompt-ui-shadow-color));
}

.tag-wrapper:active .tag-content {
  transform: translateY(0);
}

/* 没有描述时的样式 */
.tag-wrapper:not(:has(.tag-desc)) .tag-main {
  border-radius: 16px;
  border-bottom: 1px solid var(--border-color);
}

/* 滚动条样式 */
.primary-tabs::-webkit-scrollbar,
.sub-tabs::-webkit-scrollbar {
  height: 6px;
  /* 横向滚动条的高度 */
  width: 6px;
}

.primary-tabs::-webkit-scrollbar-track,
.sub-tabs::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
  border-radius: 3px;
}

.primary-tabs::-webkit-scrollbar-thumb,
.sub-tabs::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.primary-tabs::-webkit-scrollbar-thumb:hover,
.sub-tabs::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

/* 对话框样式 */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.dialog-content {
  background: var(--weilin-prompt-ui-primary-bg);
  border-radius: 8px;
  min-width: 400px;
  max-width: 90%;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  box-sizing: border-box;
}

.dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.dialog-header h2 {
  margin: 0;
  font-size: 18px;
  color: var(--primary-text);
}

.dialog-body {
  padding: 20px;
  box-sizing: border-box;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding: 16px 20px;
  border-top: 1px solid var(--border-color);
}

.form-group {
  margin-bottom: 16px;
  box-sizing: border-box;
  width: 100%;
}

.form-group:last-child {
  margin-bottom: 0;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: var(--primary-text);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
  font-size: 14px;
  transition: all 0.3s ease;
  box-sizing: border-box;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 0 0 2px rgba(var(--weilin-prompt-ui-primary-color-rgb), 0.1);
}

.cancel-btn,
.confirm-btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.cancel-btn {
  background: none;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  color: var(--weilin-prompt-ui-secondary-text);
}

.confirm-btn {
  background: var(--weilin-prompt-ui-primary-color);
  border: none;
  color: white;
}

.cancel-btn:hover {
  background: var(--weilin-prompt-ui-hover-bg-color);
}

.confirm-btn:hover {
  opacity: 0.9;
}

.close-btn {
  border: none;
  background: none;
  font-size: 20px;
  color: var(--weilin-prompt-ui-secondary-text);
  cursor: pointer;
  padding: 4px;
  line-height: 1;
}

.close-btn:hover {
  color: var(--weilin-prompt-ui-primary-text);
}

/* 确认对话框特定样式 */
.confirm-dialog {
  min-width: 300px !important;
  max-width: 400px !important;
  width: 90%;
  box-sizing: border-box;
}

.confirm-message {
  margin: 0;
  color: var(--weilin-prompt-ui-primary-text);
  text-align: center;
}

.delete-btn {
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  background: var(--weilin-prompt-ui-danger-color, #ff4d4f);
  border: none;
  color: white;
  transition: all 0.3s ease;
}

.delete-btn:hover {
  opacity: 0.9;
}

.has-delete-action-btn {
  background: var(--weilin-prompt-ui-primary-color);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.has-delete-action-btn:hover {
  opacity: 0.9;
}

.cancel-delete-btn {
  background: none;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  color: var(--weilin-prompt-ui-secondary-text);
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.cancel-delete-btn:hover {
  background: var(--weilin-prompt-ui-hover-bg-color);
}

/* 对话框动画 */
.dialog-overlay {
  animation: fadeIn 0.2s ease;
}

.dialog-content {
  animation: slideIn 0.2s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }

  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    transform: translateY(-20px);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.color-picker {
  display: flex;
  gap: 12px;
  padding: 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-secondary-bg);
}

.color-preview {
  width: 48px;
  height: 48px;
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background-image: linear-gradient(45deg, #ccc 25%, transparent 25%),
    linear-gradient(-45deg, #ccc 25%, transparent 25%),
    linear-gradient(45deg, transparent 75%, #ccc 75%),
    linear-gradient(-45deg, transparent 75%, #ccc 75%);
  background-size: 10px 10px;
  background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
}

.color-controls {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.color-input {
  width: 100%;
  height: 32px;
  padding: 0;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  cursor: pointer;
}

.alpha-control {
  display: flex;
  align-items: center;
  gap: 8px;
}

.alpha-slider {
  flex: 1;
  height: 8px;
  -webkit-appearance: none;
  background: linear-gradient(to right, transparent, currentColor);
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
}

.alpha-slider::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--weilin-prompt-ui-primary-color);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.alpha-value {
  min-width: 48px;
  text-align: right;
  color: var(--weilin-prompt-ui-secondary-text);
}

/* 确保标签和分类显示透明背景 */
.primary-tab,
.sub-tab,
.tag-card {
  position: relative;
  background-color: transparent;
}

/* 搜索区域样式 */
.search-container {
  position: relative;
  z-index: 100;
}

.search-input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
  font-size: 14px;
}

.search-input:focus {
  outline: none;
  border-color: var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 0 0 2px var(--weilin-prompt-ui-primary-color-fade);
}

.search-results {
  position: fixed;
  top: 60px;
  left: 0;
  right: 0;
  max-height: 300px;
  overflow-y: auto;
  background: var(--weilin-prompt-ui-primary-bg);
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  margin-top: 4px;
  box-shadow: 0 2px 8px var(--weilin-prompt-ui-shadow-color);
  z-index: 1000;
}

.search-result-item {
  padding: 8px 12px;
  cursor: pointer;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.search-result-item:last-child {
  border-bottom: none;
}

.search-result-item:hover {
  background: var(--weilin-prompt-ui-hover-bg);
}

.result-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.result-text {
  font-size: 14px;
  color: var(--weilin-prompt-ui-primary-text);
}

.result-path {
  font-size: 12px;
  color: var(--weilin-prompt-ui-secondary-text);
}

.no-results {
  padding: 12px;
  text-align: center;
  color: var(--weilin-prompt-ui-secondary-text);
  font-size: 14px;
}

.tab-item.active {
  border-color: var(--weilin-prompt-ui-primary-color);
}

.tab-item.active .action-btn {
  color: #ffffff;
}

.tab-content {
  display: flex;
  align-items: center;
  gap: 4px;
}

.add-btn {
  font-size: 14px;
}

.toolbar {
  flex-direction: column;
  padding: 12px 16px;
}

.toolbar .toolbar-top {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 10px;
}

.refresh-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  padding: 0;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-secondary-bg);
  cursor: pointer;
  transition: all 0.2s ease;
}

.refresh-btn:hover {
  background: var(--weilin-prompt-ui-hover-bg);
  border-color: var(--weilin-prompt-ui-primary-color);
}

.refresh-icon {
  fill: var(--weilin-prompt-ui-primary-text);
}

.search-container {
  flex: 1;
}

.tags-actions {
  width: fit-content;
  display: flex;
  flex-direction: row;
  align-items: center;
  gap: 12px;
}

.tag-checkbox {
  margin-top: 3px;
  /* 复选框与标签文本之间的间距 */
}

.radio-input {
  width: 16px !important;
  height: 16px !important;
  margin-top: 3px;
}

.group-edit-mode {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  padding: 4px 12px;
  background: none;
  border: 1px dashed var(--weilin-prompt-ui-border-color);
  border-radius: 4px 4px 0 0;
  color: var(--weilin-prompt-ui-secondary-text);
  cursor: pointer;
  transition: all 0.3s;
  white-space: nowrap;
  font-size: 13px;
  height: 28px;
  width: fit-content;
  cursor: pointer;
}

.group-edit-mode:hover {
  color: var(--weilin-prompt-ui-primary-color);
  border-color: var(--weilin-prompt-ui-primary-color);
  background: var(--weilin-prompt-ui-secondary-bg);
}


.highlight {
  border: 2px solid var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 0 8px rgba(255, 123, 2, 0.6);
  transform: scale(1.05);
  transition: all 0.3s ease;
}

/* 添加按钮样式 */
.import-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background-color: var(--weilin-prompt-ui-primary-color);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.import-btn:hover {
  opacity: 0.9;
}

.import-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background-color: var(--weilin-prompt-ui-secondary-bg);
}
</style>
