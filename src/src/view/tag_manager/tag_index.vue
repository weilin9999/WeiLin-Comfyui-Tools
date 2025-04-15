<template>
  <div class="tag-manager">
    <!-- 顶部工具栏 -->
    <div class="toolbar">
     <div class="toolbar-top">
      <button class="refresh-btn" @click="refreshTags">
        <svg viewBox="0 0 24 24" width="16" height="16" class="refresh-icon">
          <path
            d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
        </svg>
      </button>

      <div class="search-container">
        <input type="text" v-model="searchQuery" :placeholder="t('tagManager.searchPlaceholder')" class="search-input"
          ref="searchInput" @input="isSearching = searchQuery.trim().length > 0" />
        <!-- 搜索结果 -->
        <div v-if="isSearching" class="search-results" :style="searchResultsStyle">
          <div v-if="searchResults.length === 0" class="no-results">
            {{ t('tagManager.noResults') }}
          </div>
          <div v-else v-for="result in searchResults" :key="`${result.type}-${result.item.name || result.item.text}`"
            class="search-result-item" @click="navigateToResult(result)">
            <div class="result-content">
              <span class="result-text">
                {{ result.item.name || result.item.text }}
              </span>
              <span class="result-path">
                {{ result.path.join(' > ') }}
              </span>
            </div>
          </div>
        </div>
      </div>
     </div>

      <!-- 高级设置 -->
      <div class="group-edit-mode">
        <label>
          <input 
            type="checkbox" 
            v-model="isAutoAddSearchTag" 
            :true-value="1" 
            :false-value="0"
          />
          {{ t('tagManager.autoAddSearchTag') }}
        </label>
      </div>
    </div>

    <!-- 分类导航区域 -->
    <div class="category-tabs">
      <!-- 一级分类 tabs -->
      <div class="tabs-wrapper primary-tabs">
        <div class="tabs-scroll">
          <div v-for="(category,index) in categories" :key="'Tabss-'+index" class="tab-item"
            :class="{ active: selectedCategory?.name === category.name }" :style="{
              backgroundColor: selectedCategory?.name === category.name ? 'var(--primary-color)' : category.color,
              color: selectedCategory?.name === category.name ? '#ffffff' : getContrastColor(category.color)
            }" @click="selectCategory(category)"
            @mouseenter="showTabActions(index)"
            @mouseleave="hideTabActions(index)">
            <span class="tab-text">{{ category.name }}</span>
            <div class="tab-actions" v-if="hoverTabsActionFrist=='TabID-'+index">
              <button class="action-btn edit" @click.stop="editCategory(category)">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path
                    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                </svg>
              </button>
              <button class="action-btn delete" @click.stop="deleteCategory(category)">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                </svg>
              </button>
            </div>
          </div>
          <button class="add-tab" @click="showAddCategoryDialog('primary')">
            <span class="plus-icon">+</span>
            {{ t('tagManager.addPrimaryCategory') }}
          </button>

          <div class="group-edit-mode">
            <label>
              <input 
                type="checkbox" 
                v-model="editGroupCategroy" 
                :true-value="1" 
                :false-value="0"
              />
              {{ editGroupCategroy == 1 ? t('tagManager.exitEditMode'): t('tagManager.editGroupMode') }}
            </label>
          </div>

        </div>
      </div>

      <!-- 分组 tabs -->
      <div class="tabs-wrapper group-tabs" v-if="selectedCategory">
        <div class="tabs-scroll">
          <div v-for="(group,index) in selectedCategory.groups" :key="'TabsSw-'+index" class="tab-item"
            :class="{ active: selectedGroup?.name === group.name }" :style="{
              backgroundColor: selectedGroup?.name === group.name ? 'var(--primary-color)' : group.color,
              color: selectedGroup?.name === group.name ? '#ffffff' : getContrastColor(group.color)
            }" @click="selectGroup(group)"
             @mouseenter="showTabActionsGroup(index)"
             @mouseleave="hideTabActionsGroup(index)">
            <span class="tab-text">{{ group.name }}</span>
            <div class="tab-actions" v-if="hoverTabsActionSecond == 'TabID-'+index">
              <button class="action-btn edit" @click.stop="editGroup(group)">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path
                    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                </svg>
              </button>
              <button class="action-btn delete" @click.stop="deleteGroup(group)">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                </svg>
              </button>
            </div>
          </div>
          <button class="add-tab" v-if="selectedCategory" @click="showAddCategoryDialog('group')">
            <span class="plus-icon">+</span>
            {{ t('tagManager.addGroup') }}
          </button>
          <div class="group-edit-mode">
            <label>
              <input 
                type="checkbox" 
                v-model="editGroupTabs" 
                :true-value="1" 
                :false-value="0"
              />
              {{ editGroupTabs == 1 ? t('tagManager.exitEditMode'): t('tagManager.editGroupMode') }}
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- 标签内容区域 -->
    <div class="tags-content">
      <div class="tags-header">
        <div class="tags-title">{{ selectedGroup ? selectedGroup.name : t('tagManager.selectCategory') }}</div>
        <div class="tags-actions">
          <button class="add-btn" @click="showAddTagDialog" :disabled="!selectedGroup">
            <span class="plus-icon">+</span>
            {{ t('tagManager.addTag') }}
          </button>
          <button v-if="isDeleteTagAction" class="delete-btn" @click="deleteSelectedTags"
            :disabled="!selectedTags.length">
            {{ t('tagManager.deleteSelected') }}
          </button>
          <button v-else class="has-delete-action-btn" @click="deleteTagAction" :disabled="!selectedGroup">
            {{ t('tagManager.hasDeleteAction') }}
          </button>
          <button v-if="isDeleteTagAction" class="cancel-delete-btn" @click="cancelDeleteAction">
            {{ t('tagManager.cancelDelete') }}
          </button>
        </div>
      </div>

      <div class="tags-grid" v-if="selectedGroup">
        <div v-for="tag in currentTags" :key="'tag-grid-'+tag.id_index" :class="highlightedTagId === tag.id_index ? 'tag-wrapper highlight':'tag-wrapper'">
          <div class="tag-content" @click="handleTagClick(tag)">
            <div class="tag-main" :style="{ backgroundColor: tag.color || 'transparent' }">
              {{ tag.desc }}
              <div class="tag-actions">
                <button class="action-btn move" @click.stop="openMoveDialog(tag)" :title="t('tagManager.moveTag')">
                  <svg viewBox="0 0 24 24" class="move-icon">
                    <path d="M13 6v3h8V6h-8zm0 5v3h8v-3h-8zm-8 5v3h8v-3H5zm0-5v3h8v-3H5zm0-5v3h8V6H5z" />
                  </svg>
                </button>
                <button class="action-btn edit" @click.stop="editTag(tag)" :title="t('tagManager.editTag')">
                  <svg viewBox="0 0 24 24" class="edit-icon">
                    <path
                      d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                  </svg>
                </button>
                <button class="action-btn delete" @click.stop="deleteTag(tag)" :title="t('tagManager.deleteTag')">
                  <svg viewBox="0 0 24 24" class="delete-icon">
                    <path d="M6 19c0 1.1.9 2 2 2h8c1.1 0 2-.9 2-2V7H6v12zM19 4h-3.5l-1-1h-5l-1 1H5v2h14V4z" />
                  </svg>
                </button>
              </div>
            </div>
            <div class="tag-desc">{{ tag.text }}</div>
          </div>
          <input v-if="isDeleteTagAction" type="checkbox" v-model="selectedTags" :value="tag.id_index"
            class="tag-checkbox" />
        </div>
      </div>
    </div>

    <!-- 分类对话框 -->
    <div v-if="showCategoryDialog" class="dialog-overlay">
      <div class="dialog-content" @mousedown.stop>
        <div class="dialog-header">
          <h2>{{ getCategoryDialogTitle() }}</h2>
          <button class="close-btn" @click="closeCategoryDialog">×</button>
        </div>
        <div class="dialog-body">
          <div class="form-group" v-if="categoryType == 'primary'">
            <label>{{ t('tagManager.categoryName') }}</label>
            <input type="text" v-model="currentCategory.name" :placeholder="t('tagManager.categoryNamePlaceholder')"
              @keyup.enter="saveCategory">
          </div>
          <div class="form-group" v-if="categoryType == 'group'">
            <label>{{ t('tagManager.groupName') }}</label>
            <input type="text" v-model="currentGroup.name" :placeholder="t('tagManager.groupNamePlaceholder')"
              @keyup.enter="saveCategory">
          </div>
          <div class="form-group">
            <label>{{ t('tagManager.backgroundColor') }}</label>
            <div class="color-picker">
              <div class="color-preview" :style="{ backgroundColor: previewColor }">
              </div>
              <div class="color-controls">
                <input type="color" v-model="colorPickerState.hex" @input="updateColor" class="color-input">
                <div class="alpha-control">
                  <input type="range" v-model.number="colorPickerState.alpha" min="0" max="100" @input="updateColor"
                    class="alpha-slider">
                  <span class="alpha-value">{{ colorPickerState.alpha }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="closeCategoryDialog">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="saveCategory">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

    <!-- 标签对话框 -->
    <div v-if="showTagDialog" class="dialog-overlay">
      <div class="dialog-content" @mousedown.stop>
        <div class="dialog-header">
          <h2>{{ isEditingTag ? t('tagManager.editTag') : t('tagManager.addTag') }}</h2>
          <button class="close-btn" @click="closeTagDialog">×</button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>{{ t('tagManager.text') }}</label>
            <input type="text" v-model="currentTag.desc" :placeholder="t('tagManager.textPlaceholder')">
          </div>
          <div class="form-group">
            <label>{{ t('tagManager.description') }}</label>
            <textarea v-model="currentTag.text" :placeholder="t('tagManager.descriptionPlaceholder')" rows="4">
            </textarea>
          </div>
          <div class="form-group">
            <label>{{ t('tagManager.backgroundColor') }}</label>
            <div class="color-picker">
              <div class="color-preview" :style="{ backgroundColor: previewColor }">
              </div>
              <div class="color-controls">
                <input type="color" v-model="colorPickerState.hex" @input="updateColor" class="color-input">
                <div class="alpha-control">
                  <input type="range" v-model.number="colorPickerState.alpha" min="0" max="100" @input="updateColor"
                    class="alpha-slider">
                  <span class="alpha-value">{{ colorPickerState.alpha }}%</span>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="closeTagDialog">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="saveTag">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

    <!-- 确认删除对话框 -->
    <div v-if="showDeleteDialog" class="dialog-overlay">
      <div class="dialog-content confirm-dialog" @mousedown.stop>
        <div class="dialog-header">
          <h2>{{ t('common.confirmDelete') }}</h2>
          <button class="close-btn" @click="closeDeleteDialog">×</button>
        </div>
        <div class="dialog-body">
          <p class="confirm-message">{{ deleteConfirmMessage }}</p>
        </div>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="closeDeleteDialog">{{ t('common.cancel') }}</button>
          <button class="delete-btn" @click="confirmDelete">{{ t('common.delete') }}</button>
        </div>
      </div>
    </div>

    <!-- 移动标签对话框 -->
    <div v-if="showMoveDialog" class="dialog-overlay">
      <div class="dialog-content">
        <div class="dialog-header">
          <h2>{{ t('tagManager.moveTag') }}</h2>
          <button class="close-btn" @click="showMoveDialog = false">×</button>
        </div>
        <div class="dialog-body">
          <div class="form-group">
            <label>{{ t('tagManager.targetTag') }}</label>
            <select v-model="moveTargetTagId" class="form-select">
              <option v-for="tag in availableTags" :key="tag.id_index" :value="tag.id_index">
                {{ tag.desc + ' --> ' + tag.text }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>{{ t('tagManager.movePosition') }}</label>
            <div class="radio-group">
              <label>
                <input class="radio-input" type="radio" v-model="movePosition" value="before" />
                {{ t('tagManager.moveBefore') }}
              </label>
              <label>
                <input class="radio-input" type="radio" v-model="movePosition" value="after" />
                {{ t('tagManager.moveAfter') }}
              </label>
            </div>
          </div>
        </div>
        <div class="dialog-footer">
          <button class="cancel-btn" @click="showMoveDialog = false">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="confirmMove">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { tagsApi } from '@/api/tags'
import message from '@/utils/message'
import { useTagStore } from '@/stores/tagStore';

const tagStore = useTagStore();
const { t } = useI18n()

// 状态管理
const categories = ref([]);
const selectedCategory = ref(null)
const selectedGroup = ref(null)
const showCategoryDialog = ref(false)
const showTagDialog = ref(false)
const isEditingCategory = ref(false)
const isEditingTag = ref(false)
const categoryType = ref('primary') // 'primary' 或 'group'
const selectedTags = ref([]); // 用于存储选中的标签ID
const isDeleteTagAction = ref(false)

const hoverTabsActionFrist = ref('None');
const hoverTabsActionSecond = ref('None');
const editGroupTabs = ref(0); // 添加编辑模式状态
const editGroupCategroy = ref(0); // 添加编辑模式状态

const highlightedTagId = ref(null); // 添加高亮状态
const isAutoAddSearchTag = ref(0); // 添加高亮状态

// 新增状态变量
const showMoveDialog = ref(false);
const moveTargetTagId = ref(null);
const movePosition = ref('before');
const currentMoveTagId = ref(null);

const props = defineProps({
  tagManager: {
    type: String,
    default: 'prompt'
  }
})

// 当前编辑的数据
const currentCategory = ref({
  name: '',
  color: 'rgba(255, 123, 2, .4)',
  id_index: '',
  groups: []
})

const currentGroup = ref({
  name: '',
  id_index: '',
  color: 'rgba(255, 123, 2, .4)',
  tags: []
})

const currentTag = ref({
  text: '',
  desc: '',
  id_index: '',
  color: 'rgba(255, 123, 2, .4)'
})

const rgbaToColorPickerState = (rgba) => {
  const match = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/);
  if (match) {
    const [, r, g, b, a] = match;
    const hex = `#${((1 << 24) + (parseInt(r) << 16) + (parseInt(g) << 8) + parseInt(b)).toString(16).slice(1)}`;
    const alpha = a ? Math.round(parseFloat(a) * 100) : 100; // 将 alpha 转换为百分比
    return { hex, alpha };
  }
  return { hex: '#FFFFFF', alpha: 100 }; // 默认值
};

// 获取标签列表
const getTagsList = () => {
  window.postMessage({
    type: 'weilin_prompt_ui_tag_manager_refresh'
  }, '*')
}

const refreshTagsGoThis = async () => {
  try {
    const res = await tagsApi.getTagsList()
    tagStore.setCategories(res.data);
    categories.value = tagStore.categories
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



onMounted(() => {
  updateSearchResultsStyle() // 初始化样式
  // 添加全局点击事件监听
  window.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', updateSearchResultsStyle)
  window.addEventListener('message', handleMessage)
  window.addEventListener('keydown', handleKeydown) // 监听键盘事件
  categories.value = tagStore.categories
  if (categories.value.length <= 0 ){
    getTagsList()
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', updateSearchResultsStyle)
  window.removeEventListener('message', handleMessage)
  window.removeEventListener('keydown', handleKeydown) // 移除键盘事件监听
})

// 当前分组下的标签
const currentTags = computed(() => {
  if (!selectedGroup.value) return []
  return selectedGroup.value.tags || []
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

// 显示添加分类对话框
const showAddCategoryDialog = (type) => {
  categoryType.value = type
  isEditingCategory.value = false
  colorPickerState.value = rgbaToColorPickerState('rgba(255, 123, 2, .4)')
  if (type === 'primary') {
    currentCategory.value = {
      name: '',
      color: 'rgba(255, 123, 2, .4)',
      groups: []
    }
  } else {
    currentGroup.value = {
      name: '',
      color: 'rgba(255, 123, 2, .4)',
      tags: []
    }
  }
  showCategoryDialog.value = true
}

// 编辑分类
const editCategory = (category) => {
  isEditingCategory.value = true
  categoryType.value = 'primary'
  currentCategory.value = { ...category }
  colorPickerState.value = rgbaToColorPickerState(category.color)
  showCategoryDialog.value = true
}

// 编辑分组
const editGroup = (group) => {
  isEditingCategory.value = true
  categoryType.value = 'group'
  currentGroup.value = { ...group }
  colorPickerState.value = rgbaToColorPickerState(group.color)
  showCategoryDialog.value = true
}

// 保存分类或分组
const saveCategory = () => {
  if (categoryType.value === 'primary') {
    if (!currentCategory.value.name) {
      message({ type: "warn", str: 'tagManager.categoryNameRequired' });
      return
    }

    if (isEditingCategory.value) {
      const index = categories.value.findIndex(c => c.id_index === currentCategory.value.id_index)
      if (index !== -1) {
        // console.log(categories.value)
        tagsApi
          .editPrimaryCategory({
            id_index: currentCategory.value.id_index,
            name: currentCategory.value.name,
            color: currentCategory.value.color,
          })
          .then((res) => {
            if (res.code === 200) {
              getTagsList()
              message({ type: "success", str: 'message.editSuccess' });
            } else if (res.code === 201) {
              message({ type: "error", str: 'message.editNameExist' });
            } else {
              message({ type: "error", str: 'message.editFailed' });
            }
          })
          .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
          });
      }
    } else {
      tagsApi
        .addPrimaryCategory({
          name: currentCategory.value.name,
          color: currentCategory.value.color,
        })
        .then((res) => {
          if (res.code === 200) {
            getTagsList()
            message({ type: "success", str: 'message.addSuccess' });
          } else if (res.code === 201) {
            message({ type: "error", str: 'message.editNameExist' });
          } else {
            message({ type: "error", str: 'message.addFailed' });
          }
        })
        .catch((err) => {
          message({ type: "warn", str: 'message.networkError' });
        });
    }
  } else {
    if (!currentGroup.value.name) {
      message({ type: "warn", str: 'tagManager.groupNameRequired' });
      return
    }

    if (isEditingCategory.value) {
      tagsApi
        .editSubCategory({
          id_index: currentGroup.value.id_index,
          name: currentGroup.value.name,
          color: currentGroup.value.color,
        })
        .then((res) => {
          if (res.code === 200) {
            getTagsList()
            message({ type: "success", str: 'message.editSuccess' });
          } else if (res.code === 201) {
            message({ type: "error", str: 'message.editNameExist' });
          } else {
            message({ type: "error", str: 'message.editFailed' });
          }
        })
        .catch((err) => {
          message({ type: "warn", str: 'message.networkError' });
        });
    } else {
      tagsApi
        .addSubCategory({
          name: currentGroup.value.name,
          color: currentGroup.value.color,
          key: selectedCategory.value.id_index,
          p_uuid: selectedCategory.value.p_uuid,
        })
        .then((res) => {
          if (res.code === 200) {
            getTagsList()
            message({ type: "success", str: 'message.addSuccess' });
          } else if (res.code === 201) {
            message({ type: "error", str: 'message.editNameExist' });
          } else {
            message({ type: "error", str: 'message.editFailed' });
          }
        })
        .catch((err) => {
          message({ type: "warn", str: 'message.networkError' });
        });
    }
  }

  closeCategoryDialog()
}

// 获取分类对话框标题
const getCategoryDialogTitle = () => {
  if (isEditingCategory.value) {
    return categoryType.value === 'primary'
      ? t('tagManager.editPrimaryCategory')
      : t('tagManager.editSubCategory')
  }
  return categoryType.value === 'primary'
    ? t('tagManager.addPrimaryCategory')
    : t('tagManager.addSubCategory')
}

// 关闭分类对话框
const closeCategoryDialog = () => {
  showCategoryDialog.value = false
  currentCategory.value = {
    id: '',
    name: '',
    parentId: null,
    subCategories: [],
    backgroundColor: 'transparent'
  }
  // 重置颜色选择器
  colorPickerState.value = {
    hex: '#FFFFFF',
    alpha: 0
  }
}

// 标签相关方法
const tags = ref([])

// 显示添加标签对话框
const showAddTagDialog = () => {
  if (!selectedGroup.value) return

  isEditingTag.value = false
  currentTag.value = {
    id: '',
    text: '',
    desc: '',
    categoryId: selectedGroup.value.id,
    g_uuid: selectedGroup.value.g_uuid,
    backgroundColor: currentGroup.value.color // 设置默认颜色
  }
  // 初始化颜色选择器
  colorPickerState.value = rgbaToColorPickerState(currentGroup.value.color)
  showTagDialog.value = true
}

// 编辑标签
const editTag = (tag) => {
  isEditingTag.value = true
  currentTag.value = { ...tag }
  colorPickerState.value = rgbaToColorPickerState(tag.color)
  showTagDialog.value = true
}

// 保存标签
const saveTag = () => {
  if (!currentTag.value.text || !currentTag.value.desc) {
    message({ type: "warn", str: 'tagManager.textRequired' });
    return
  }

  if (isEditingTag.value && selectedGroup.value) {
    tagsApi
      .editTags({
        id_index: currentTag.value.id_index,
        text: currentTag.value.text,
        desc: currentTag.value.desc,
        color: currentTag.value.color,
      })
      .then((res) => {
        getTagsList()
        window.postMessage({
          type: 'weilin_prompt_ui_refresh_all_data',
        }, '*')
        message({ type: "success", str: 'message.editSuccess' });
      })
      .catch((err) => {
        message({ type: "warn", str: 'message.networkError' });
      });
  } else if (selectedGroup.value) {
    tagsApi
      .addNewTags({
        id_index: selectedGroup.value.id_index,
        g_uuid: selectedGroup.value.g_uuid,
        text: currentTag.value.text,
        desc: currentTag.value.desc,
        color: currentTag.value.color ? currentTag.value.color : 'rgba(255, 123, 2, .4)',
      })
      .then((res) => {
        getTagsList()
        window.postMessage({
          type: 'weilin_prompt_ui_refresh_all_data',
        }, '*')
        message({ type: "success", str: 'message.addSuccess' });
      })
      .catch((err) => {
        message({ type: "warn", str: 'message.networkError' });
      });
  }

  closeTagDialog()
}

// 关闭标签对话框
const closeTagDialog = () => {
  showTagDialog.value = false
  currentTag.value = {
    text: '',
    desc: '',
    color: 'rgba(255, 123, 2, .4)'
  }
  isEditingTag.value = false
}

// 颜色选择器状态
const colorPickerState = ref({
  hex: '#FFFFFF',
  alpha: 100
})

// 预览颜色计算属性
const previewColor = computed(() => {
  return hexToRgba(colorPickerState.value.hex, colorPickerState.value.alpha)
})

// 更新颜色（统一处理分类和标签）
const updateColor = () => {
  const color = hexToRgba(colorPickerState.value.hex, colorPickerState.value.alpha)
  if (showCategoryDialog.value) {
    if (categoryType.value === 'primary') {
      currentCategory.value.color = color
    } else {
      currentGroup.value.color = color
    }
  } else if (showTagDialog.value) {
    currentTag.value.color = color
  }
}

// 改进的 RGBA 转换函数
const hexToRgba = (hex, alpha) => {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha / 100})`
}

// 改进的 RGBA 解析函数
const parseRgba = (rgba) => {
  if (!rgba || rgba === 'transparent') {
    return { hex: '#FFFFFF', alpha: 0 }
  }

  const match = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/)
  if (match) {
    const [, r, g, b, a] = match
    const hex = '#' + [r, g, b].map(x => {
      const hex = parseInt(x).toString(16)
      return hex.length === 1 ? '0' + hex : hex
    }).join('')

    return {
      hex: hex,
      alpha: Math.round((a || 1) * 100)
    }
  }
  return { hex: '#FFFFFF', alpha: 0 }
}

// 搜索相关的状态
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// 搜索处理函数
const handleSearch = () => {
  isSearching.value = searchQuery.value.trim().length > 0
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) {
    searchResults.value = []
    return
  }

  const results = []

  // 搜索分类
  categories.value.forEach(category => {
    // 确保 name 是字符串
    const categoryName = String(category?.name || '')
    if (categoryName && categoryName.toLowerCase().includes(query)) {
      results.push({
        type: 'category',
        item: category,
        path: [categoryName]
      })
    }

    // 搜索分组
    category.groups?.forEach(group => {
      // 确保 name 是字符串
      const groupName = String(group?.name || '')
      if (groupName && groupName.toLowerCase().includes(query)) {
        results.push({
          type: 'group',
          item: group,
          path: [categoryName, groupName]
        })
      }

      // 搜索标签
      group.tags?.forEach(tag => {
        // 确保 text 和 desc 是字符串
        const tagText = String(tag?.text || '')
        const tagDesc = String(tag?.desc || '')

        if (
          (tagText && tagText.toLowerCase().includes(query)) ||
          (tagDesc && tagDesc.toLowerCase().includes(query))
        ) {
          results.push({
            type: 'tag',
            item: tag,
            path: [categoryName, groupName, tagText]
          })
        }
      })
    })
  })

  searchResults.value = results
}

// 监听搜索输入
watch(searchQuery, () => {
  handleSearch()
})

// 跳转到搜索结果
const navigateToResult = (result) => {
  if (!result?.type || !result?.item) return

  if (result.type === 'category') {
    if (result.item) {
      selectCategory(result.item)
    }
  } else if (result.type === 'group') {
    const category = categories.value.find(
      c => c?.groups?.some(g => String(g?.name) === String(result.item?.name))
    )
    if (category && result.item) {
      selectCategory(category)
      selectGroup(result.item)
    }
  } else if (result.type === 'tag') {
    const category = categories.value.find(c =>
      c?.groups?.some(g => g?.tags?.some(t => String(t?.text) === String(result.item?.text)))
    )
    if (category) {
      const group = category.groups?.find(g =>
        g?.tags?.some(t => String(t?.text) === String(result.item?.text))
      )
      if (group) {
        selectCategory(category)
        selectGroup(group)

        if (isAutoAddSearchTag.value == 1){
          // 发送消息通知
          window.postMessage({
            type: 'weilin_prompt_ui_insertTag',
            tagText: result.item.text
          }, '*')
        }

        // 设置高亮标签
        highlightedTagId.value = result.item.id_index;

        // 5秒后取消高亮
        setTimeout(() => {
          highlightedTagId.value = null;
        }, 5000);

      }
    }
  }
  searchQuery.value = '' // 清空搜索
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

// 添加标签点击处理函数
const handleTagClick = (tag) => {
  if (props.tagManager === 'prompt') {
    // 发送消息通知
    window.postMessage({
      type: 'weilin_prompt_ui_insertTag',
      tagText: tag.text
    }, '*')
  }
}

// 删除相关状态
const showDeleteDialog = ref(false)
const deleteType = ref('') // 'category', 'group', 或 'tag'
const itemToDelete = ref(null)
const deleteConfirmMessage = computed(() => {
  if (!itemToDelete.value) return ''

  switch (deleteType.value) {
    case 'category':
      return t('tagManager.deletePrimaryCategoryConfirm', { name: itemToDelete.value.name })
    case 'group':
      return t('tagManager.deleteGroupConfirm', { name: itemToDelete.value.name })
    case 'tag':
      return t('tagManager.deleteTagConfirm', { name: itemToDelete.value.text })
    case 'deleteSelected':
      return t('tagManager.confirmDeleteSelected')
    default:
      return ''
  }
})

// 删除分类
const deleteCategory = (category) => {
  deleteType.value = 'category'
  itemToDelete.value = category
  showDeleteDialog.value = true
}

// 删除分组
const deleteGroup = (group) => {
  deleteType.value = 'group'
  itemToDelete.value = group
  showDeleteDialog.value = true
}

// 删除标签
const deleteTag = (tag) => {
  deleteType.value = 'tag'
  itemToDelete.value = tag
  showDeleteDialog.value = true
}

// 确认删除
const confirmDelete = async () => {
  try {
    switch (deleteType.value) {
      case 'category':
        tagsApi
          .deletePrimaryCategory({
            p_uuid: itemToDelete.value.p_uuid,
          })
          .then((res) => {
            getTagsList()
            message({ type: "success", str: 'message.deleteSuccess' });
          })
          .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
          });
        break

      case 'group':
        tagsApi
          .deleteSubCategory({
            g_uuid: itemToDelete.value.g_uuid,
          })
          .then((res) => {
            getTagsList()
            message({ type: "success", str: 'message.deleteSuccess' });
          })
          .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
          });
        break

      case 'tag':
        tagsApi
          .deleteTags({
            id_index: itemToDelete.value.id_index,
          })
          .then((res) => {
            getTagsList()
            window.postMessage({
              type: 'weilin_prompt_ui_refresh_all_data',
            }, '*')
            message({ type: "success", str: 'message.deleteSuccess' });
          })
          .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
          });
        break

      case 'deleteSelected':
        tagsApi
          .batchDeleteTags({
            id_indexs: selectedTags.value,
          })
          .then((res) => {
            getTagsList()
            window.postMessage({
              type: 'weilin_prompt_ui_refresh_all_data',
            }, '*')
            message({ type: "success", str: 'message.deleteSuccess' });
          })
          .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
          });
        break
    }

    closeDeleteDialog()
  } catch (error) {
    console.error('删除失败:', error)
  }
}


// 打开移动对话框
const openMoveDialog = (tag) => {
  currentMoveTagId.value = tag.id_index;
  showMoveDialog.value = true;
};

// 确认移动
const confirmMove = async () => {
  try {
    tagsApi.moveTag({
      id_index: currentMoveTagId.value,
      reference_id_index: moveTargetTagId.value,
      position: movePosition.value
    }).then((res) => {
      getTagsList();
      showMoveDialog.value = false;
      message({ type: 'success', str: t('message.moveSuccess') });
    }).catch((err) => {
      message({ type: 'error', str: t('message.moveFailed') });
    });
  } catch (error) {
    console.error('移动标签失败:', error);
    message({ type: 'error', str: t('message.moveFailed') });
  }
};

// 计算可移动的目标标签
const availableTags = computed(() => {
  return selectedGroup.value.tags.filter(tag => tag.id_index !== currentMoveTagId.value);
});


const deleteTagAction = () => {
  isDeleteTagAction.value = true
}

const cancelDeleteAction = () => {
  isDeleteTagAction.value = false
  selectedTags.value = []
}

const deleteSelectedTags = () => {
  if (selectedTags.value.length === 0) return;

  // 确认删除操作
  deleteType.value = 'deleteSelected'
  itemToDelete.value = {}
  showDeleteDialog.value = true
};

// 关闭删除对话框
const closeDeleteDialog = () => {
  showDeleteDialog.value = false
  deleteType.value = ''
  itemToDelete.value = null
}

// 刷新标签列表
const refreshTags = async () => {
  try {
    await getTagsList()
  } catch (error) {
    console.error('刷新标签列表失败:', error)
  }
}

const searchInput = ref()

const searchResultsStyle = ref({}) // 使用 ref 来存储样式

// 计算搜索结果的样式
const updateSearchResultsStyle = () => {
  if (searchInput.value) {
    const rect = searchInput.value.getBoundingClientRect() // 获取搜索框的位置信息
    searchResultsStyle.value = {
      position: 'fixed', // 设置为 fixed
      top: `${rect.bottom}px`, // 在输入框下方
      left: `${rect.left}px`, // 与输入框左对齐
      width: `${rect.width}px`, // 宽度与输入框一致
      zIndex: 1000, // 确保在最上层
    }
  }
}

// 处理消息
const handleMessage = (event) => {
  // console.log(event.data.type)
  if (event.data.type === 'weilin_prompt_ui_window_change_tagManager_position') {
    updateSearchResultsStyle()
  } else if (event.data.type === 'weilin_prompt_ui_window_change_tagManager_size') {
    updateSearchResultsStyle()
  } else if (event.data.type === 'weilin_prompt_ui_window_change_tagManager_scroll') {
    updateSearchResultsStyle()
  } else if (event.data.type === 'weilin_prompt_ui_window_change_promptBox_position') {
    updateSearchResultsStyle()
  } else if (event.data.type === 'weilin_prompt_ui_window_change_promptBox_size') {
    updateSearchResultsStyle()
  } else if (event.data.type === 'weilin_prompt_ui_window_change_promptBox_scroll') {
    updateSearchResultsStyle()
  } else if (event.data.type === 'weilin_prompt_ui_window_change_click_outside') {
    // console.log(event.data.event)
  } else if (event.data.type === 'weilin_prompt_ui_tag_manager_refresh') {
    refreshTagsGoThis()
  }
}

// 处理点击事件，关闭搜索结果框
const handleClickOutside = (event) => {
  if (isSearching.value && !searchInput.value.contains(event.target)) {
    isSearching.value = false // 关闭搜索结果框
  }
}

// 处理键盘事件
const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    isSearching.value = false // 关闭搜索结果框
  }
}

const showTabActions = (index) => {
  if (editGroupCategroy.value == 1){
    hoverTabsActionFrist.value = 'TabID-'+index;
  }
};

const hideTabActions = (index) => {
  hoverTabsActionFrist.value = 'None';
};

const showTabActionsGroup = (index) => {
  if (editGroupTabs.value == 1){
    hoverTabsActionSecond.value = 'TabID-'+index;
  }
};

const hideTabActionsGroup = (index) => {
  hoverTabsActionSecond.value = 'None';
};

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
</style>
