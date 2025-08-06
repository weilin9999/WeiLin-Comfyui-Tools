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
            <div v-else v-for="(result, index) in searchResults" :key="`${index}-search_item`"
              class="search-result-item" @click="navigateToResult(result)">
              <div class="result-content">
                <span class="result-text">
                  {{ result.name || result.text }}
                </span>
                <span class="result-path">
                  {{ result.where }}
                </span>
              </div>
            </div>
          </div>
        </div>

        <button class="import-btn" @click="showImportDialog">
          {{ t('tagManager.importTags') }}
        </button>

      </div>

      <!-- 高级设置 -->
      <div class="toolbar-bottom">
        <div class="group-edit-mode">
          <label>
            <input type="checkbox" v-model="isAutoAddSearchTag" :true-value="1" :false-value="0" />
            {{ t('tagManager.autoAddSearchTag') }}
          </label>
        </div>
        <!-- 新增修改标签尺寸按钮 -->
        <button class="tab-size-btn" @click="showTabSizeDialog">
          {{ t('tagManager.modifyTabSize') }}
        </button>
      </div>

    </div>

    <!-- 分类导航区域 -->
    <div class="category-tabs">
      <!-- 一级分类 tabs -->
      <div class="tabs-wrapper primary-tabs">
        <div class="tabs-scroll">
          <div v-for="(category, index) in categories" :key="'Tabss-' + index" class="tab-item"
            :class="{ active: selectedCategory?.name === category.name }" :style="{
              backgroundColor: selectedCategory?.name === category.name ? 'var(--primary-color)' : category.color,
              color: selectedCategory?.name === category.name ? '#ffffff' : getContrastColor(category.color),
              width: tabSizeConfig.primaryTab.width === 'fit-content' ? 'fit-content' : tabSizeConfig.primaryTab.width + 'px',
              height: tabSizeConfig.primaryTab.height + 'px',
              fontSize: tabSizeConfig.primaryTab.fontSize + 'px'
            }" @click="selectCategory(category)" @mouseenter="showTabActions(index)"
            @mouseleave="hideTabActions(index)">
            <span class="tab-text">{{ category.name }}</span>
            <div class="tab-actions" v-if="hoverTabsActionFrist == 'TabID-' + index">
              <button class="action-btn move" @click.stop="openMoveGroupDialog(category, 1)"
                :title="t('tagManager.moveGroup')">
                <svg viewBox="0 0 24 24" class="move-icon">
                  <path d="M13 6v3h8V6h-8zm0 5v3h8v-3h-8zm-8 5v3h8v-3H5zm0-5v3h8v-3H5zm0-5v3h8V6H5z" />
                </svg>
              </button>
              <button class="action-btn edit" @click.stop="editCategory(category)" :title="t('tagManager.edit')">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path
                    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                </svg>
              </button>
              <button class="action-btn share" @click.stop="shareCategory(category)" :title="t('tagManager.share')">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path
                    d="M18 16.08c-.76 0-1.44.3-1.96.77L8.91 12.7c.05-.23.09-.46.09-.7s-.04-.47-.09-.7l7.05-4.11c.54.5 1.25.81 2.04.81 1.66 0 3-1.34 3-3s-1.34-3-3-3-3 1.34-3 3c0 .24.04.47.09.7L8.04 9.81C7.5 9.31 6.79 9 6 9c-1.66 0-3 1.34-3 3s1.34 3 3 3c.79 0 1.5-.31 2.04-.81l7.12 4.16c-.05.21-.08.43-.08.65 0 1.61 1.31 2.92 2.92 2.92 1.61 0 2.92-1.31 2.92-2.92s-1.31-2.92-2.92-2.92z" />
                </svg>
              </button>
              <button class="action-btn delete" @click.stop="deleteCategory(category)" :title="t('tagManager.delete')">
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
              <input type="checkbox" v-model="editGroupCategroy" :true-value="1" :false-value="0" />
              {{ editGroupCategroy == 1 ? t('tagManager.exitEditMode') : t('tagManager.editGroupMode') }}
            </label>
          </div>

        </div>
      </div>

      <!-- 二级分类 分组 tabs -->
      <div class="tabs-wrapper group-tabs" v-if="selectedCategory">
        <div class="tabs-scroll">
          <div v-for="(group, index) in subCategories" :key="'TabsSw-' + index" class="tab-item"
            :class="{ active: selectedGroup?.name === group.name }" :style="{
              backgroundColor: selectedGroup?.name === group.name ? 'var(--primary-color)' : group.color,
              color: selectedGroup?.name === group.name ? '#ffffff' : getContrastColor(group.color),
              width: tabSizeConfig.groupTab.width === 'fit-content' ? 'fit-content' : tabSizeConfig.groupTab.width + 'px',
              height: tabSizeConfig.groupTab.height + 'px',
              fontSize: tabSizeConfig.groupTab.fontSize + 'px'
            }" @click="selectGroup(group)" @mouseenter="showTabActionsGroup(index)"
            @mouseleave="hideTabActionsGroup(index)">
            <span class="tab-text">{{ group.name }}</span>
            <div class="tab-actions" v-if="hoverTabsActionSecond == 'TabID-' + index">
              <button class="action-btn move" @click.stop="openMoveGroupDialog(group, 2)"
                :title="t('tagManager.moveGroup')">
                <svg viewBox="0 0 24 24" class="move-icon">
                  <path d="M13 6v3h8V6h-8zm0 5v3h8v-3h-8zm-8 5v3h8v-3H5zm0-5v3h8v-3H5zm0-5v3h8V6H5z" />
                </svg>
              </button>
              <button class="action-btn edit" @click.stop="editGroup(group)" :title="t('tagManager.edit')">
                <svg viewBox="0 0 24 24" class="action-icon">
                  <path
                    d="M3 17.25V21h3.75L17.81 9.94l-3.75-3.75L3 17.25zM20.71 7.04c.39-.39.39-1.02 0-1.41l-2.34-2.34c-.39-.39-1.02-.39-1.41 0l-1.83 1.83 3.75 3.75 1.83-1.83z" />
                </svg>
              </button>
              <button class="action-btn delete" @click.stop="deleteGroup(group)" :title="t('tagManager.delete')">
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
              <input type="checkbox" v-model="editGroupTabs" :true-value="1" :false-value="0" />
              {{ editGroupTabs == 1 ? t('tagManager.exitEditMode') : t('tagManager.editGroupMode') }}
            </label>
          </div>
        </div>
      </div>
    </div>

    <!-- Tag列表 标签内容区域 -->
    <div class="tags-content">
      <div class="tags-header">
        <div class="tags-title">{{ selectedGroup ? selectedGroup.name : t('tagManager.selectCategory') }}</div>
        <div class="tags-actions">
          <button class="add-btn" @click="showAddTagDialog" :disabled="!selectedGroup">
            <span class="plus-icon">+</span>
            {{ t('tagManager.addTag') }}
          </button>

          <!-- 批量分享按钮 -->
          <button v-if="isShareTagAction" class="share-selected-btn" @click="shareSelectedTags"
            :disabled="!selectedTags.length">
            {{ t('tagManager.shareSelected') }}
          </button>
          <button v-else class="share-btn" @click="shareTagAction" :disabled="!selectedGroup">
            {{ t('tagManager.batchShare') }}
          </button>
          <button v-if="isShareTagAction" class="cancel-delete-btn" @click="cancelShareAction">
            {{ t('tagManager.cancelShare') }}
          </button>

          <!-- 批量删除功能 -->
          <button v-if="isDeleteTagAction" class="delete-btn" @click="deleteSelectedTags"
            :disabled="!selectedTags.length">
            {{ t('tagManager.deleteSelected') }}
          </button>
          <button v-else class="delete-action-btn" @click="deleteTagAction" :disabled="!selectedGroup">
            {{ t('tagManager.hasDeleteAction') }}
          </button>
          <button v-if="isDeleteTagAction" class="cancel-delete-btn" @click="cancelDeleteAction">
            {{ t('tagManager.cancelDelete') }}
          </button>
        </div>
      </div>

      <div class="tags-grid" v-if="selectedGroup">
        <div v-for="tag in currentTags" :key="'tag-grid-' + tag.id_index"
          :class="highlightedTagId === tag.id_index ? 'tag-wrapper highlight' : 'tag-wrapper'">
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
          <input v-if="isSelectTagAction" type="checkbox" v-model="selectedTags" :value="tag.id_index"
            class="tag-checkbox" />
        </div>
      </div>
    </div>

    <!-- 分类对话框 -->
    <div v-if="showCategoryDialog" class="weilin-tools-dialog-overlay">
      <div class="weilin-tools-dialog-content" @mousedown.stop>
        <div class="weilin-tools-dialog-header">
          <h2>{{ getCategoryDialogTitle() }}</h2>
          <button class="close-btn" @click="closeCategoryDialog">×</button>
        </div>
        <div class="weilin-tools-dialog-body">
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
        <div class="weilin-tools-dialog-footer">
          <button class="cancel-btn" @click="closeCategoryDialog">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="saveCategory">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

    <!-- 标签对话框 -->
    <div v-if="showTagDialog" class="weilin-tools-dialog-overlay">
      <div class="weilin-tools-dialog-content" @mousedown.stop>
        <div class="weilin-tools-dialog-header">
          <h2>{{ isEditingTag ? t('tagManager.editTag') : t('tagManager.addTag') }}</h2>
          <button class="close-btn" @click="closeTagDialog">×</button>
        </div>
        <div class="weilin-tools-dialog-body">
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
        <div class="weilin-tools-dialog-footer">
          <button class="cancel-btn" @click="closeTagDialog">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="saveTag">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

    <!-- 确认删除对话框 -->
    <div v-if="showDeleteDialog" class="weilin-tools-dialog-overlay">
      <div class="weilin-tools-dialog-content confirm-weilin-tools-dialog" @mousedown.stop>
        <div class="weilin-tools-dialog-header">
          <h2>{{ t('common.confirmDelete') }}</h2>
          <button class="close-btn" @click="closeDeleteDialog">×</button>
        </div>
        <div class="weilin-tools-dialog-body">
          <p class="confirm-message">{{ deleteConfirmMessage }}</p>
        </div>
        <div class="weilin-tools-dialog-footer">
          <button class="cancel-btn" @click="closeDeleteDialog">{{ t('common.cancel') }}</button>
          <button class="delete-btn" @click="confirmDelete">{{ t('common.delete') }}</button>
        </div>
      </div>
    </div>

    <!-- 移动标签对话框 -->
    <div v-if="showMoveDialog" class="weilin-tools-dialog-overlay">
      <div class="weilin-tools-dialog-content">
        <div class="weilin-tools-dialog-header">
          <h2>{{ t('tagManager.moveTag') }}</h2>
          <button class="close-btn" @click="showMoveDialog = false">×</button>
        </div>
        <div class="weilin-tools-dialog-body">
          <div class="form-group">
            <label>{{ t('tagManager.targetTag') }}</label>
            <select v-model="moveTargetTagId" class="form-select">
              <option v-for="tag in currentTags" :key="tag.id_index" :value="tag.id_index">
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
        <div class="weilin-tools-dialog-footer">
          <button class="cancel-btn" @click="showMoveDialog = false">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="confirmMove">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>


    <!-- 移动分组对话框 -->
    <div v-if="showMoveGroupDialog" class="weilin-tools-dialog-overlay">
      <div class="weilin-tools-dialog-content">
        <div class="weilin-tools-dialog-header">
          <h2>{{ t('tagManager.moveGroup') }}</h2>
          <button class="close-btn" @click="showMoveGroupDialog = false">×</button>
        </div>
        <div class="weilin-tools-dialog-body">
          <div class="form-group">
            <label>{{ t('tagManager.targetGroup') }}</label>
            <select v-model="moveTargetGroupId" class="form-select">
              <option v-for="(item, index) in availableGroup" :key="'group_move_id' + index" :value="item.id_index">
                {{ item.name }}
              </option>
            </select>
          </div>
          <div class="form-group">
            <label>{{ t('tagManager.movePosition') }}</label>
            <div class="radio-group">
              <label>
                <input class="radio-input" type="radio" v-model="moveGroupPosition" value="before" />
                {{ t('tagManager.moveGroupBefore') }}
              </label>
              <label>
                <input class="radio-input" type="radio" v-model="moveGroupPosition" value="after" />
                {{ t('tagManager.moveGroupAfter') }}
              </label>
            </div>
          </div>
        </div>
        <div class="weilin-tools-dialog-footer">
          <button class="cancel-btn" @click="showMoveGroupDialog = false">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="confirmMoveGroup">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

    <!-- 标签尺寸配置对话框 -->
    <div v-if="showTabSizeConfig" class="weilin-tools-dialog-overlay">
      <div class="weilin-tools-dialog-content tab-size-weilin-tools-dialog" @mousedown.stop>
        <div class="weilin-tools-dialog-header">
          <h2>{{ t('tagManager.tabSizeConfig') }}</h2>
          <button class="close-btn" @click="closeTabSizeDialog">×</button>
        </div>
        <div class="weilin-tools-dialog-body">
          <!-- 一级分类配置 -->
          <div class="config-section">
            <h3>{{ t('tagManager.primaryTabConfig') }}</h3>
            <div class="form-group">
              <label>{{ t('tagManager.tabWidth') }}</label>
              <div class="width-control">
                <label class="radio-label">
                  <input type="radio" v-model="tabSizeConfig.primaryTab.width" value="fit-content" />
                  {{ t('tagManager.fitContent') }}
                </label>
                <label class="radio-label">
                  <input type="radio" v-model="tabSizeConfig.primaryTab.width" value="custom" />
                  {{ t('tagManager.customWidth') }}
                </label>
                <input v-if="tabSizeConfig.primaryTab.width !== 'fit-content'" type="number"
                  v-model.number="tabSizeConfig.primaryTab.width" min="50" max="300" class="number-input" />
              </div>
            </div>
            <div class="form-group">
              <label>{{ t('tagManager.tabHeight') }} ({{ tabSizeConfig.primaryTab.height }}px)</label>
              <input type="range" v-model.number="tabSizeConfig.primaryTab.height" min="20" max="60"
                class="range-input" />
            </div>
            <div class="form-group">
              <label>{{ t('tagManager.fontSize') }} ({{ tabSizeConfig.primaryTab.fontSize }}px)</label>
              <input type="range" v-model.number="tabSizeConfig.primaryTab.fontSize" min="8" max="20"
                class="range-input" />
            </div>
          </div>

          <!-- 二级分类配置 -->
          <div class="config-section">
            <h3>{{ t('tagManager.groupTabConfig') }}</h3>
            <div class="form-group">
              <label>{{ t('tagManager.tabWidth') }}</label>
              <div class="width-control">
                <label class="radio-label">
                  <input type="radio" v-model="tabSizeConfig.groupTab.width" value="fit-content" />
                  {{ t('tagManager.fitContent') }}
                </label>
                <label class="radio-label">
                  <input type="radio" v-model="tabSizeConfig.groupTab.width" value="custom" />
                  {{ t('tagManager.customWidth') }}
                </label>
                <input v-if="tabSizeConfig.groupTab.width !== 'fit-content'" type="number"
                  v-model.number="tabSizeConfig.groupTab.width" min="50" max="300" class="number-input" />
              </div>
            </div>
            <div class="form-group">
              <label>{{ t('tagManager.tabHeight') }} ({{ tabSizeConfig.groupTab.height }}px)</label>
              <input type="range" v-model.number="tabSizeConfig.groupTab.height" min="20" max="60"
                class="range-input" />
            </div>
            <div class="form-group">
              <label>{{ t('tagManager.fontSize') }} ({{ tabSizeConfig.groupTab.fontSize }}px)</label>
              <input type="range" v-model.number="tabSizeConfig.groupTab.fontSize" min="8" max="20"
                class="range-input" />
            </div>
          </div>
        </div>
        <div class="weilin-tools-dialog-footer">
          <button class="reset-btn" @click="resetTabSizeConfig">{{ t('tagManager.resetDefault') }}</button>
          <button class="cancel-btn" @click="closeTabSizeDialog">{{ t('common.cancel') }}</button>
          <button class="confirm-btn" @click="saveTabSizeConfig">{{ t('common.confirm') }}</button>
        </div>
      </div>
    </div>

    <ImportTagDialog ref="importTagDialogItem" />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { tagsApi } from '@/api/tags'
import message from '@/utils/message'
import { useTagStore } from '@/stores/tagStore';
import ImportTagDialog from "./import_tag.vue";
import yaml from 'js-yaml';

const tagStore = useTagStore();
const { t } = useI18n()

// 状态管理
const categories = ref([]);
const selectedCategory = ref(null)
const subCategories = ref([])
const currentTags = ref([])


const selectedGroup = ref(null)
const showCategoryDialog = ref(false)
const showTagDialog = ref(false)
const isEditingCategory = ref(false)
const isEditingTag = ref(false)
const categoryType = ref('primary') // 'primary' 或 'group'
const selectedTags = ref([]); // 用于存储选中的标签ID
const isSelectTagAction = ref(false)
const showMoveGroupDialog = ref(false)
import { uuidv7 } from "uuidv7";

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


const moveGroupPosition = ref('before');
const currentMoveGroupId = ref(null);
const moveTargetGroupId = ref(null);

// 批量删除
const isDeleteTagAction = ref(false);
// 批量分享
const isShareTagAction = ref(false);


// 新增状态变量
const showTabSizeConfig = ref(false)
const tabSizeConfig = ref({
  primaryTab: {
    width: 'fit-content',
    height: 34,
    fontSize: 10
  },
  groupTab: {
    width: 'fit-content',
    height: 34,
    fontSize: 10
  }
})

// 默认配置
const defaultTabSizeConfig = {
  primaryTab: {
    width: 'fit-content',
    height: 34,
    fontSize: 10
  },
  groupTab: {
    width: 'fit-content',
    height: 34,
    fontSize: 10
  }
}

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
    await tagsApi.getTagMainGroup().then((res) => {
      // console.log(res);
      categories.value = res
    }).catch((err) => {
      console.error(err);
      message({ type: "warn", str: 'message.networkError' });
    });

    // 如果当前分类存在，重新设置当前分类
    if (selectedCategory.value) {
      // console.log(selectedCategory.value)
      await getSubCategories(selectedCategory.value.p_uuid);
    }

    // 选择了二级分类就获取tag
    if (selectedGroup.value) {
      // console.log(selectedGroup.value)
      await getTagList(selectedGroup.value.g_uuid);
    }

  } catch (error) {
    console.error('Tag管理器列表失败:', error)
  }
}


const getSubCategories = async (p_uuid) => {
  try {
    await tagsApi.getTagSubGroup(p_uuid).then((res) => {
      // console.log(res);
      subCategories.value = res
    }).catch((err) => {
      console.error(err);
      message({ type: "warn", str: 'message.networkError' });
    });
  } catch (error) {
    console.error('二级分类列表失败:', error)
  }
}


const getTagList = async (g_uuid) => {
  try {
    await tagsApi.getTagList(g_uuid).then((res) => {
      // console.log(res);
      currentTags.value = res
    }).catch((err) => {
      console.error(err);
      message({ type: "warn", str: 'message.networkError' });
    });
  } catch (error) {
    console.error('Tag列表失败:', error)
  }
}


onMounted(() => {
  updateSearchResultsStyle() // 初始化样式
  // 添加全局点击事件监听
  window.addEventListener('click', handleClickOutside)
  window.addEventListener('resize', updateSearchResultsStyle)
  window.addEventListener('message', handleMessage)
  window.addEventListener('keydown', handleKeydown) // 监听键盘事件

  // 加载标签尺寸配置
  loadTabSizeConfig()

  // categories.value = tagStore.categories
  // if (categories.value.length <= 0) {
  getTagsList()
  // }
})

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside)
  window.removeEventListener('resize', updateSearchResultsStyle)
  window.removeEventListener('message', handleMessage)
  window.removeEventListener('keydown', handleKeydown) // 移除键盘事件监听
})


// 选择分类
const selectCategory = async (category) => {
  // console.log(category.p_uuid)
  selectedCategory.value = category
  selectedGroup.value = null
  isSelectTagAction.value = false
  selectedTags.value = []
  await getSubCategories(category.p_uuid)
}

// 选择分组
const selectGroup = async (group) => {
  selectedGroup.value = group
  isSelectTagAction.value = false
  selectedTags.value = []
  await getTagList(group.g_uuid)
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

// 搜索相关的状态
const searchQuery = ref('')
const searchResults = ref([])
const isSearching = ref(false)

// 搜索处理函数
const handleSearch = async () => {
  isSearching.value = searchQuery.value.trim().length > 0
  const query = searchQuery.value.trim().toLowerCase()
  if (!query) {
    searchResults.value = []
    return
  }

  searchResults.value = []
  // 搜索匹配
  await tagsApi.searchTag(query)
    .then((res) => {
      searchResults.value = res
    })
    .catch((err) => {
      message({ type: "warn", str: 'message.networkError' });
    });

}

// 监听搜索输入
watch(searchQuery, () => {
  handleSearch()
})

// 跳转到搜索结果
const navigateToResult = async (result) => {
  // 先根据p_uuid查找并选择一级分类
  const primaryCategory = categories.value.find(cat => cat.p_uuid === result.p_uuid);
  if (primaryCategory) {
    await selectCategory(primaryCategory).then(async () => {
      // 然后根据g_uuid查找并选择二级分类
      await nextTick(async () => {
        const group = subCategories.value.find(g => g.g_uuid === result.g_uuid);
        if (group) {
          await selectGroup(group).then(async () => {
            // 最后高亮显示对应的标签
            await nextTick(() => {

              if (isAutoAddSearchTag.value == 1) {
                // 发送消息通知
                window.postMessage({
                  type: 'weilin_prompt_ui_insertTag',
                  tagText: result.text
                }, '*')
              }

              highlightedTagId.value = result.id_index;
              // 滚动到该标签位置
              setTimeout(() => {
                const tagElement = document.querySelector(`.tag-wrapper.highlight`);
                if (tagElement) {
                  tagElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }
              }, 100);

              // 5秒后取消高亮
              setTimeout(() => {
                highlightedTagId.value = null;
              }, 5000);
            });
          });
        }
      });
    });
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


// 分享整个一级目录
const shareCategory = async (category) => {
  // console.log(category)
  // 生成一级分类SQL
  const groupSql = `INSERT OR REPLACE INTO "tag_groups" ("name", "color", "create_time", "p_uuid") VALUES ('${category.name.replace(/'/g, "''")}', '${category.color}', ${category.create_time}, '${category.p_uuid}');`;
  try {
    await tagsApi.getTagSubGroup(category.p_uuid).then((res) => {
      // console.log(res);
      const groupData = res
      // 生成二级分类和标签SQL
      const tagSqls = [];
      groupData.forEach(async (group) => {
        const subGroupSql = `INSERT OR REPLACE INTO "tag_subgroups" ("name", "color", "create_time", "p_uuid", "g_uuid") VALUES ('${group.name.replace(/'/g, "''")}', '${group.color}', ${group.create_time}, '${group.p_uuid}', '${group.g_uuid}');`;
        tagSqls.push(subGroupSql);

        try {
          await tagsApi.getTagList(group.g_uuid).then((res) => {
            // console.log(res);
            const currentTags = res
            currentTags.forEach(tag => {
              const tagSql = `INSERT OR REPLACE INTO "tag_tags" ("text", "desc", "color", "create_time", "g_uuid", "t_uuid") VALUES ('${tag.text.replace(/'/g, "''")}', '${tag.desc.replace(/'/g, "''")}', '${tag.color}', ${tag.create_time}, '${tag.g_uuid}', '${uuidv7()}');`;
              tagSqls.push(tagSql);
            });
          }).catch((err) => {
            console.error(err);
            message({ type: "warn", str: 'message.networkError' });
          });
        } catch (error) {
          console.error('Tag列表失败:', error)
          message({ type: "warn", str: 'message.shareTagError' });
        }
      });

      // 合并所有SQL语句
      const sqlContent = [groupSql, ...tagSqls].join('\n');

      // 创建下载链接
      const blob = new Blob([sqlContent], { type: 'text/sql' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = `${category.name}_export_${Date.now()}.sql`;
      link.click();

      message({ type: "success", str: 'tagManager.outputSuccess' });
    }).catch((err) => {
      console.error(err);
      message({ type: "warn", str: 'message.networkError' });
    });

  } catch (error) {
    console.error('二级分类列表失败:', error)
    message({ type: "warn", str: 'message.shareGroupError' });
  }

};

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

const availableGroup = ref([])
const actionMoveGroup = ref(1)
// 打开移动对话框 Group
const openMoveGroupDialog = (group, action) => {
  actionMoveGroup.value = action
  if (action === 1) {
    availableGroup.value = categories.value
    currentMoveGroupId.value = group.id_index;
    showMoveGroupDialog.value = true;
  } else {
    // console.log(group)
    availableGroup.value = subCategories.value
    currentMoveGroupId.value = group.id_index;
    showMoveGroupDialog.value = true;
  }
  // console.log(group)
}


const confirmMoveGroup = async () => {
  if (actionMoveGroup.value === 1) {
    try {
      tagsApi.moveMainGroup({
        id_index: currentMoveGroupId.value,
        reference_id_index: moveTargetGroupId.value,
        position: moveGroupPosition.value
      }).then((res) => {
        getTagsList();
        showMoveGroupDialog.value = false;
        message({ type: 'success', str: t('message.moveSuccess') });
      }).catch((err) => {
        message({ type: 'error', str: t('message.moveFailed') });
      });
    } catch (error) {
      console.error('移动标签失败:', error);
      message({ type: 'error', str: t('message.moveFailed') });
    }
  } else {
    try {
      tagsApi.moveSubGroup({
        id_index: currentMoveGroupId.value,
        reference_id_index: moveTargetGroupId.value,
        position: moveGroupPosition.value
      }).then((res) => {
        getTagsList();
        showMoveGroupDialog.value = false;
        message({ type: 'success', str: t('message.moveSuccess') });
      }).catch((err) => {
        message({ type: 'error', str: t('message.moveFailed') });
      });
    } catch (error) {
      console.error('移动标签失败:', error);
      message({ type: 'error', str: t('message.moveFailed') });
    }
  }

}

const deleteTagAction = () => {
  isSelectTagAction.value = true
  isDeleteTagAction.value = true
}

const cancelDeleteAction = () => {
  isSelectTagAction.value = false
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


const shareTagAction = () => {
  isSelectTagAction.value = true
  isShareTagAction.value = true
}

const cancelShareAction = () => {
  isSelectTagAction.value = false
  isShareTagAction.value = false
  selectedTags.value = []
}

const shareSelectedTags = () => {
  if (selectedTags.value.length === 0) {
    message({ type: "warn", str: 'tagManager.noTagsSelected' });
    return;
  }

  // 获取选中的标签
  const selectedTagItems = selectedGroup.value.tags.filter(tag =>
    selectedTags.value.includes(tag.id_index)
  );

  // 生成YAML内容
  const yamlContent = {};
  selectedTagItems.forEach(tag => {
    yamlContent[tag.text] = tag.desc;
  });

  // 创建下载链接
  const blob = new Blob([yaml.dump(yamlContent)], { type: 'text/yaml' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.download = `selected_tags_export_${Date.now()}.yaml`;
  link.click();

  message({ type: "success", str: 'tagManager.outputSuccess' });
  cancelShareAction();
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
  if (editGroupCategroy.value == 1) {
    hoverTabsActionFrist.value = 'TabID-' + index;
  }
};

const hideTabActions = (index) => {
  hoverTabsActionFrist.value = 'None';
};

const showTabActionsGroup = (index) => {
  if (editGroupTabs.value == 1) {
    hoverTabsActionSecond.value = 'TabID-' + index;
  }
};

const hideTabActionsGroup = (index) => {
  hoverTabsActionSecond.value = 'None';
};

const importTagDialogItem = ref()
const showImportDialog = () => {
  importTagDialogItem.value.open()
}

// 从localStorage读取配置
const loadTabSizeConfig = () => {
  const defaultTabData = JSON.parse(JSON.stringify(defaultTabSizeConfig))
  try {
    const saved = localStorage.getItem('weilin_tag_manager_tab_size_config')
    if (saved) {
      const parsed = JSON.parse(saved)
      tabSizeConfig.value = { ...defaultTabData, ...parsed }
    } else {
      tabSizeConfig.value = { ...defaultTabData }
    }
  } catch (error) {
    console.error('读取标签尺寸配置失败:', error)
    tabSizeConfig.value = { ...defaultTabData }
  }
}

// 保存配置到localStorage
const saveTabSizeConfig = () => {
  try {
    localStorage.setItem('weilin_tag_manager_tab_size_config', JSON.stringify(tabSizeConfig.value))
    message({ type: "success", str: 'tagManager.tabSizeConfigSaved' });
    showTabSizeConfig.value = false
  } catch (error) {
    console.error('保存标签尺寸配置失败:', error)
    message({ type: "error", str: 'tagManager.tabSizeConfigSaveFailed' });
  }
}

// 显示配置对话框
const showTabSizeDialog = () => {
  showTabSizeConfig.value = true
}

// 关闭配置对话框
const closeTabSizeDialog = () => {
  showTabSizeConfig.value = false
  // 重新从localStorage加载，撤销未保存的更改
  loadTabSizeConfig()
}

// 重置为默认值
const resetTabSizeConfig = () => {
  const defaultTabData = JSON.parse(JSON.stringify(defaultTabSizeConfig))
  tabSizeConfig.value = { ...defaultTabData }
}

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
.weilin-tools-dialog-overlay {
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

.weilin-tools-dialog-content {
  background: var(--weilin-prompt-ui-primary-bg);
  border-radius: 8px;
  min-width: 400px;
  max-width: 90%;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
  box-sizing: border-box;
  z-index: 10099;
}

.weilin-tools-dialog-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.weilin-tools-dialog-header h2 {
  margin: 0;
  font-size: 18px;
  color: var(--primary-text);
}

.weilin-tools-dialog-body {
  padding: 20px;
  box-sizing: border-box;
}

.weilin-tools-dialog-footer {
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
.confirm-weilin-tools-dialog {
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

.delete-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
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
.weilin-tools-dialog-overlay {
  animation: fadeIn 0.2s ease;
}

.weilin-tools-dialog-content {
  animation: slideIn 0.2s ease;
  z-index: 10099;
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

.toolbar-bottom {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 5px;
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


.share-btn {
  background: var(--weilin-prompt-ui-primary-color);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.share-btn:hover {
  opacity: 0.9;
}

.share-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


.delete-action-btn {
  background: var(--weilin-prompt-ui-primary-color);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.delete-action-btn:hover {
  opacity: 0.9;
}

.delete-action-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.share-selected-btn {
  background: var(--weilin-prompt-ui-success-color);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.share-selected-btn:hover {
  opacity: 0.9;
}

.share-selected-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}


/* 新增按钮样式 */
.tab-size-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background-color: var(--weilin-prompt-ui-secondary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 12px;
  white-space: nowrap;
}

.tab-size-btn:hover {
  background-color: var(--weilin-prompt-ui-hover-bg);
  border-color: var(--weilin-prompt-ui-primary-color);
}

/* 标签尺寸配置对话框样式 */
.tab-size-weilin-tools-dialog {
  min-width: 500px;
  max-width: 600px;
}

.config-section {
  margin-bottom: 24px;
  padding: 16px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 8px;
  background: var(--weilin-prompt-ui-secondary-bg);
}

.config-section h3 {
  margin: 0 0 16px 0;
  color: var(--weilin-prompt-ui-primary-text);
  font-size: 16px;
}

.width-control {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.radio-label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.radio-label input[type="radio"] {
  width: auto !important;
  margin: 0;
}

.number-input {
  width: 100px !important;
  margin-top: 8px;
}

.range-input {
  width: 100%;
  height: 8px;
  -webkit-appearance: none;
  background: var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  outline: none;
}

.range-input::-webkit-slider-thumb {
  -webkit-appearance: none;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--weilin-prompt-ui-primary-color);
  cursor: pointer;
  border: 2px solid white;
  box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.reset-btn {
  background: var(--weilin-prompt-ui-warning-color, #faad14);
  border: none;
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
}

.reset-btn:hover {
  opacity: 0.9;
}
</style>
