<template>
  <Dialog v-model="dialogVisible" :title="t('importDialog.selectTitle')">
    <div class="tag-manager">
      <!-- 已选择分类显示区域 -->
      <div class="selected-categories-container">
        <div class="selected-categories-header">
          <span>{{ t('importDialog.selectedCategories') }}</span>
          <button class="clear-all-btn" @click="clearAllSelected" v-if="selectGroupsData.length > 0">
            {{ t('importDialog.clearAll') }}
          </button>
        </div>
        <div class="selected-categories-content">
          <!-- 一级分类（没有子分类的选择） -->
          <div class="selected-category-section" v-if="primaryCategories.length > 0">
            <div class="section-title">{{ t('importDialog.primaryCategories') }}</div>
            <div class="selected-items">
              <div v-for="(item, index) in primaryCategories" :key="'primary-' + index" class="selected-item">
                <span class="category-name">{{ item.group.name }}</span>
                <button class="remove-selected-btn" @click="removeSelected(getPrimaryIndex(item))">×</button>
              </div>
            </div>
          </div>

          <!-- 二级分类（有子分类的选择） -->
          <div class="selected-category-section" v-if="subCategories.length > 0">
            <div class="section-title">{{ t('importDialog.subCategories') }}</div>
            <div class="selected-items">
              <div v-for="(item, index) in subCategories" :key="'sub-' + index" class="selected-item">
                <span class="category-name">{{ item.group.name }}</span>
                <span class="separator">></span>
                <span class="subcategory-name">{{ item.sub.name }}</span>
                <button class="remove-selected-btn" @click="removeSelected(getSubIndex(item))">×</button>
              </div>
            </div>
          </div>

          <!-- 没有选择任何分类时显示 -->
          <div v-if="selectGroupsData.length === 0" class="no-selected">
            {{ t('importDialog.noSelectedCategories') }}
          </div>
        </div>
      </div>

      <!-- 分类导航区域 -->
      <div class="category-tabs">


        <!-- 一级分类 tabs -->
        <div class="tabs-wrapper primary-tabs">
          <div class="tabs-scroll">
            <div v-for="(category, index) in categories" :key="'Tabss-' + index" class="tab-item"
              :class="{ active: selectedCategory?.p_uuid === category.p_uuid }" :style="{
                backgroundColor: selectedCategory?.p_uuid === category.p_uuid ? 'var(--weilin-prompt-ui-primary-bg)' : category.color,
                color: selectedCategory?.p_uuid === category.p_uuid ? 'var(--weilin-prompt-ui-primary-text)' : getContrastColor(category.color)
              }" @click="selectCategory(category)">
              <span class="tab-text">{{ category.name }}</span>
              <button class="select-tab-btn" @click.stop="selectCategoryOnly(category)"
                :title="t('importDialog.selectCategory')">
                <svg viewBox="0 0 24 24" width="28" height="28">
                  <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>

        <!-- 分组 tabs -->
        <div class="tabs-wrapper group-tabs" v-if="selectedCategory">
          <div class="tabs-scroll">
            <div v-for="(group, index) in selectedCategory.groups" :key="'TabsSw-' + index" class="tab-item" :class="{
              active: selectedGroup?.g_uuid === group.g_uuid,
              disabled: isGroupDisabled(selectedCategory)
            }" :style="{
              backgroundColor: selectedGroup?.g_uuid === group.g_uuid ? 'var(--weilin-prompt-ui-primary-bg)' : group.color,
              color: selectedGroup?.g_uuid === group.g_uuid ? 'var(--weilin-prompt-ui-primary-text)' : getContrastColor(group.color),
              opacity: isGroupDisabled(selectedCategory) ? '0.5' : '1',
              cursor: isGroupDisabled(selectedCategory) ? 'not-allowed' : 'pointer'
            }" @click="isGroupDisabled(selectedCategory) ? null : selectGroup(group)">
              <span class="tab-text">{{ group.name }}</span>
              <button class="select-tab-btn" @click.stop="selectGroupWithCategory(selectedCategory, group)"
                :disabled="isGroupDisabled(selectedCategory)" :title="t('importDialog.selectSubcategory')"
                v-if="!isGroupDisabled(selectedCategory)">
                <svg viewBox="0 0 24 24" width="28" height="28">
                  <path fill="currentColor" d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"></path>
                </svg>
              </button>
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
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
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
const selectGroupsData = ref([]); // 存储选中的分类和子分类

const dialogVisible = ref(false)
const selectActionIndex = ref(0)


// 计算属性：获取一级分类（没有子分类的选择）
const primaryCategories = computed(() => {
  return selectGroupsData.value.filter(item => !item.sub);
});

// 计算属性：获取二级分类（有子分类的选择）
const subCategories = computed(() => {
  return selectGroupsData.value.filter(item => item.sub);
});

// 获取一级分类在原数组中的索引
const getPrimaryIndex = (item) => {
  return selectGroupsData.value.findIndex(i =>
    i.group.p_uuid === item.group.p_uuid && !i.sub
  );
};

// 获取二级分类在原数组中的索引
const getSubIndex = (item) => {
  return selectGroupsData.value.findIndex(i =>
    i.group.p_uuid === item.group.p_uuid &&
    i.sub && i.sub.g_uuid === item.sub.g_uuid
  );
};

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
  if (isGroupDisabled(selectedCategory.value)) return;
  selectedGroup.value = group
  isDeleteTagAction.value = false
  selectedTags.value = []
}

// 判断分组是否被禁用（当一级分类被选中时，其二级分类被禁用）
const isGroupDisabled = (category) => {
  if (!category) return false;
  // 只有当一级分类本身被选中时，才禁用其二级分类
  return selectGroupsData.value.some(item =>
    item.group.p_uuid === category.p_uuid && !item.sub
  );
}

// 仅选择一级分类
const selectCategoryOnly = (category) => {
  // 检查是否已经选择了该分类
  const existingIndex = selectGroupsData.value.findIndex(item =>
    item.group.p_uuid === category.p_uuid && !item.sub
  );

  if (existingIndex !== -1) {
    // 如果已经选择了，则移除
    selectGroupsData.value.splice(existingIndex, 1);
  } else {
    // 移除该分类下的所有子分类选择
    selectGroupsData.value = selectGroupsData.value.filter(item =>
      item.group.p_uuid !== category.p_uuid
    );

    // 添加新的选择（只保留必要的字段）
    selectGroupsData.value.push({
      group: {
        p_uuid: category.p_uuid,
        name: category.name
      },
      sub: null
    });
  }
}

// 选择二级分类及其所属的一级分类
const selectGroupWithCategory = (category, group) => {
  if (isGroupDisabled(category)) return;

  // 检查是否已经选择了该分类和子分类
  const existingIndex = selectGroupsData.value.findIndex(item =>
    item.group.p_uuid === category.p_uuid &&
    item.sub && item.sub.g_uuid === group.g_uuid
  );

  if (existingIndex !== -1) {
    // 如果已经选择了，则移除
    selectGroupsData.value.splice(existingIndex, 1);
  } else {
    // 检查是否选择了该分类本身（不带子分类）
    const categoryOnlyIndex = selectGroupsData.value.findIndex(item =>
      item.group.p_uuid === category.p_uuid && !item.sub
    );

    // 如果选择了分类本身，需要先移除
    if (categoryOnlyIndex !== -1) {
      selectGroupsData.value.splice(categoryOnlyIndex, 1);
    }

    // 添加新的选择（只保留必要的字段）
    selectGroupsData.value.push({
      group: {
        p_uuid: category.p_uuid,
        name: category.name
      },
      sub: group ? {
        g_uuid: group.g_uuid,
        name: group.name
      } : null
    });
  }
}

// 移除已选择的项目
const removeSelected = (index) => {
  selectGroupsData.value.splice(index, 1);
}

// 清除所有选择
const clearAllSelected = () => {
  selectGroupsData.value = [];
}

// 处理消息
const handleMessage = (event) => {
  // console.log(event.data.type)
  if (event.data.type === 'weilin_prompt_ui_tag_manager_refresh_select') {
    refreshTagsGoThis()
  }
}

const selectSureThis = () => {
  if (selectGroupsData.value.length === 0) {
    message({ type: "warn", str: 'message.pleaseSelectGroup' });
    return
  }
  // console.log(selectGroupsData.value)
  emit('sureSelect', { data: selectGroupsData.value, index: selectActionIndex.value });
  dialogVisible.value = false
}

defineExpose({
  open: (index,data) => {
    getTagsList()
    selectActionIndex.value = index
    selectGroupsData.value = data
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
  height: 8px;
}

.tabs-scroll::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
}

.tabs-scroll::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.tabs-scroll::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

.tab-item {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
  padding: 4px 15px;
  border-radius: 4px 4px 0 0;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-bottom: none;
  position: relative;
  font-size: 12px;
  height: 34px;
  min-width: unset;
  width: fit-content;
  box-shadow: 0 -2px 5px rgba(0, 0, 0, 0.05);
}

.tab-item:hover {
  background-color: var(--weilin-prompt-ui-secondary-bg) !important;
}

.tab-item .active {
  box-shadow: 0 -2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.tab-text {
  flex: 0 0 auto;
  white-space: nowrap;
  text-align: center;
  margin: 0 4px;
  font-weight: 500;
}

/* 已选择分类显示区域 */
.selected-categories-container {
  background-color: var(--weilin-prompt-ui-secondary-bg);
  border-radius: 8px;
  padding: 12px;
  margin-bottom: 16px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  box-shadow: 0 2px 6px var(--weilin-prompt-ui-shadow-color);
}

.selected-categories-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  font-weight: bold;
  color: var(--weilin-prompt-ui-primary-text);
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
  padding-bottom: 8px;
}

.clear-all-btn {
  background: none;
  border: none;
  color: var(--weilin-prompt-ui-primary-color);
  cursor: pointer;
  font-size: 12px;
  padding: 2px 8px;
  border-radius: 4px;
  transition: all 0.2s;
}

.clear-all-btn:hover {
  background-color: var(--weilin-prompt-ui-primary-color-10);
  text-decoration: none;
}

.selected-categories-content {
  min-height: 40px;
  max-height: 200px;
  overflow-y: auto;
}

.selected-categories-content::-webkit-scrollbar {
  width: 6px;
}

.selected-categories-content::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
}

.selected-categories-content::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.selected-categories-content::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

.no-selected {
  color: var(--weilin-prompt-ui-secondary-text);
  font-style: italic;
  text-align: center;
  padding: 10px 0;
}

/* 分类区域样式 */
.selected-category-section {
  margin-bottom: 12px;
}

.selected-category-section:last-child {
  margin-bottom: 0;
}

.section-title {
  font-size: 12px;
  color: var(--weilin-prompt-ui-secondary-text);
  margin-bottom: 8px;
  font-weight: 500;
  padding-left: 4px;
}

.selected-items {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.selected-item {
  display: flex;
  align-items: center;
  background-color: var(--weilin-prompt-ui-tag-bg);
  border-radius: 4px;
  padding: 4px 8px;
  font-size: 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  transition: all 0.2s;
}

.selected-item:hover {
  background-color: var(--weilin-prompt-ui-tag-bg-hover);
}

.category-name {
  font-weight: bold;
  color: var(--weilin-prompt-ui-primary-text);
}

.separator {
  margin: 0 4px;
  color: var(--weilin-prompt-ui-secondary-text);
}

.subcategory-name {
  color: var(--weilin-prompt-ui-primary-text);
}

.remove-selected-btn {
  background: none;
  border: none;
  color: var(--weilin-prompt-ui-secondary-text);
  cursor: pointer;
  margin-left: 6px;
  font-size: 14px;
  padding: 0 4px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}

.remove-selected-btn:hover {
  color: var(--weilin-prompt-ui-danger-color);
  background-color: var(--weilin-prompt-ui-danger-color-10);
}

/* 选择按钮样式 */
.select-tab-btn {
  background: none;
  border: none;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  color: inherit;
  opacity: 0.7;
  transition: all 0.2s ease;
  margin-left: 4px;
}

.select-tab-btn:hover {
  opacity: 1;
  background-color: rgba(255, 255, 255, 0.2);
  transform: scale(1.1);
}

.select-tab-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.tab-item.disabled {
  pointer-events: none;
}

/* 对话框底部按钮样式 */
:deep(.dialog-footer) {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 12px 16px;
  border-top: 1px solid var(--weilin-prompt-ui-border-color);
}

:deep(.dialog-footer button) {
  padding: 6px 16px;
  border-radius: 4px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.3s;
}

:deep(.dialog-footer button:first-child) {
  background-color: var(--weilin-prompt-ui-button-bg);
  color: var(--weilin-prompt-ui-button-text);
  border: 1px solid var(--weilin-prompt-ui-border-color);
}

:deep(.dialog-footer button:first-child:hover) {
  background-color: var(--weilin-prompt-ui-button-hover);
}

:deep(.dialog-footer button:last-child) {
  background-color: var(--weilin-prompt-ui-primary-color);
  color: white;
  border: none;
}

:deep(.dialog-footer button:last-child:hover) {
  background-color: var(--weilin-prompt-ui-primary-color-hover);
}
</style>