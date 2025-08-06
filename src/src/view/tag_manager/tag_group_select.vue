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

</style>
