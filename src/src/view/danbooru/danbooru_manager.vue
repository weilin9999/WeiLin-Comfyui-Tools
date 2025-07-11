<template>
  <div class="danbooru-manager">
    <h2 class="title">{{ t('danbooruManager.title') }}</h2>

    <!-- 搜索和添加区域 -->
    <div class="action-bar">
      <div class="search-box">
        <input v-model="searchQuery" type="text" :placeholder="t('danbooruManager.searchPlaceholder')"
          @input="debouncedSearch" />
        <button class="search-btn" @click="searchTags">{{ t('tagManager.search') }}</button>
      </div>
      <button class="add-btn" @click="openAddDialog">{{ t('tagManager.addTag') }}</button>
      <button class="add-btn" @click="openImportDialog">{{ t('tagManager.importDanbooru') }}</button>
      <button class="batch-delete-btn" :class="{ 'disabled': selectedItems.length === 0 }"
        :disabled="selectedItems.length === 0" @click="confirmBatchDelete">
        {{ t('tagManager.hasDeleteAction') }} ({{ selectedItems.length }})
      </button>
    </div>

    <!-- 分页控制 -->
    <div class="pagination">
      <button :disabled="currentPage <= 1" @click="changePage(currentPage - 1)" class="page-btn">
        {{ t('loraManager.prevPage') }}
      </button>
      <span class="page-info">{{ currentPage }} / {{ totalPages }}</span>
      <button :disabled="currentPage >= totalPages" @click="changePage(currentPage + 1)" class="page-btn">
        {{ t('loraManager.nextPage') }}
      </button>
      <div class="page-size-control">
        <label>{{ t('danbooruManager.pageShow') }}</label>
        <input v-model.number="pageSize" type="number" min="10" max="500" @change="changePageSize"
          class="page-size-input" />
        <span>{{ t('danbooruManager.pageLimit') }}</span>
      </div>
    </div>

    <!-- 标签列表 -->
    <div class="tag-list" v-if="tagList.length > 0">
      <table style="table-layout: fixed;overflow: auto;">
        <thead>
          <tr>
            <th class="checkbox-column">
              <input type="checkbox" :checked="isAllSelected" @change="toggleSelectAll" />
            </th>
            <th class="id-column">ID</th>
            <th class="tag-column">{{ t('tagManager.description') }}</th>
            <th class="translate-column">{{ t('promptBox.translate') }}</th>
            <th class="color-column">{{ t('tagManager.backgroundColor') }}</th>
            <th class="hot-column">{{ t('danbooruManager.hot') }}</th>
            <th class="aliases-column">{{ t('danbooruManager.aliases') }}</th>
            <th class="control-column">{{ t('danbooruManager.controle') }}</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="tag in tagList" :key="tag.id_index">
            <td>
              <input type="checkbox" :value="tag.id_index" v-model="selectedItems" />
            </td>
            <td>{{ tag.id_index }}</td>
            <td>{{ tag.tag }}</td>
            <td>{{ tag.translate }}</td>
            <td>
              <div class="color-box" :style="{ backgroundColor: getColorById(tag.color_id) }"></div>
            </td>
            <td>{{ tag.hot }}</td>
            <td>{{ tag.aliases }}</td>
            <td>
              <button class="edit-btn" @click="openEditDialog(tag)">{{ t('common.edit') }}</button>
              <button style="margin-left:10px;" class="delete-btn" @click="confirmDelete(tag)">{{ t('common.delete')
                }}</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else class="no-results">{{ t('tagManager.noResults') }}</div>

    <!-- 添加/编辑对话框 -->
    <div class="dialog" v-if="showDialog">
      <div class="dialog-content">
        <h3>{{ isEditing ? t('tagManager.editTag') : t('tagManager.addTag') }}</h3>
        <div class="form-group">
          <label>{{ t('tagManager.description') }}</label>
          <input v-model="formData.tag" type="text" :placeholder="t('tagManager.descriptionPlaceholder')" />
        </div>
        <div class="form-group">
          <label>{{ t('promptBox.translate') }}</label>
          <input v-model="formData.translate" type="text" :placeholder="t('danbooruManager.translatePlaceholder')" />
        </div>
        <div class="form-group">
          <label>{{ t('tagManager.backgroundColor') }}</label>
          <select v-model="formData.color_id">
            <option v-for="(color, index) in colorOptions" :key="index" :value="index">
              {{ color.name }}
            </option>
          </select>
          <div class="color-preview" :style="{ backgroundColor: getColorById(formData.color_id) }"></div>
        </div>
        <div class="form-group">
          <label>Hot</label>
          <input v-model.number="formData.hot" type="number" min="0" />
        </div>
        <div class="form-group" v-if="!isEditing">
          <label>Aliases</label>
          <input v-model.number="formData.aliases" type="number" min="0" />
        </div>
        <div class="dialog-actions">
          <button @click="closeDialog">{{ t('common.cancel') }}</button>
          <button @click="submitForm">{{ t('common.save') }}</button>
        </div>
      </div>
    </div>

    <!-- 确认删除对话框 -->
    <div class="dialog" v-if="showDeleteConfirm">
      <div class="dialog-content">
        <h3>{{ t('common.confirmDelete') }}</h3>
        <p>{{ t('tagManager.deleteTagConfirm', { name: selectedTag?.tag || '' }) }}</p>
        <div class="dialog-actions">
          <button @click="showDeleteConfirm = false">{{ t('common.cancel') }}</button>
          <button class="delete-btn" @click="deleteTag">{{ t('common.delete') }}</button>
        </div>
      </div>
    </div>

    <!-- 批量删除确认对话框 -->
    <div class="dialog" v-if="showBatchDeleteConfirm">
      <div class="dialog-content">
        <h3>{{ t('danbooruManager.sureBatchDelete') }}</h3>
        <p>{{ t('danbooruManager.sureBatchDeleteTips1') }} {{ selectedItems.length }} {{ t('danbooruManager.sureBatchDeleteTips2') }}</p>
        <div class="dialog-actions">
          <button @click="showBatchDeleteConfirm = false">{{ t('common.cancel') }}</button>
          <button class="delete-btn" @click="batchDeleteTags">{{ t('danbooruManager.sureDelete') }}</button>
        </div>
      </div>
    </div>

    <!-- 遮罩层 -->
    <div class="overlay" v-if="showDialog || showDeleteConfirm || showBatchDeleteConfirm"></div>
    <importDanbooru ref="importDanbooruDialog" />
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import { danbooruApi } from "@/api/danbooru";
import message from "@/utils/message";
import { useI18n } from 'vue-i18n';
import importDanbooru from "./import_danbooru.vue"

const { t } = useI18n();
const searchQuery = ref('');
const tagList = ref([]);
const currentPage = ref(1);
const totalPages = ref(1);
const pageSize = ref(100);
const isLoading = ref(false);

// 对话框控制
const showDialog = ref(false);
const showDeleteConfirm = ref(false);
const showBatchDeleteConfirm = ref(false);
const isEditing = ref(false);
const selectedTag = ref(null);

// 表单数据
const formData = ref({
  tag: '',
  translate: '',
  color_id: 0,
  hot: 0,
  aliases: 0
});

// 颜色选项
const colorOptions = [
  { name: '默认', color: '#888888' },
  { name: '红色', color: '#FF6666' },
  { name: '绿色', color: '#66FF66' },
  { name: '蓝色', color: '#6666FF' },
  { name: '黄色', color: '#FFFF66' },
  { name: '紫色', color: '#FF66FF' },
  { name: '青色', color: '#66FFFF' },
  { name: '橙色', color: '#FF9966' },
  { name: '粉色', color: '#FF99CC' },
  { name: '棕色', color: '#996633' }
];

// 根据ID获取颜色
const getColorById = (id) => {
  return colorOptions[id] ? colorOptions[id].color : colorOptions[0].color;
};

// 防抖搜索
let searchTimeout = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1;
    searchTags();
  }, 300)
}


// 搜索标签
const searchTags = async () => {
  isLoading.value = true;
  selectedItems.value = []; // 搜索时清空选择
  try {
    const response = await danbooruApi.searchDanbooru(
      searchQuery.value,
      currentPage.value,
      pageSize.value
    );

    if (response && response.data) {
      // 直接使用API返回的数据结构
      tagList.value = response.data.data || [];
      totalPages.value = response.data.total_pages || 1;
    } else {
      tagList.value = [];
      totalPages.value = 1;
    }
  } catch (error) {
    console.error('搜索标签失败:', error);
    message({ type: 'error', str: t('message.searchFailed') });
    tagList.value = [];
  } finally {
    isLoading.value = false;
  }
};

// 切换页码
const changePage = (page) => {
  if (page < 1 || page > totalPages.value) return;
  currentPage.value = page;
  searchTags();
};

// 修改分页大小
const changePageSize = () => {
  if (pageSize.value < 10) pageSize.value = 10;
  if (pageSize.value > 500) pageSize.value = 500;
  currentPage.value = 1;
  selectedItems.value = []; // 清空选择
  searchTags();
};

// 打开添加对话框
const openAddDialog = () => {
  isEditing.value = false;
  formData.value = {
    tag: '',
    translate: '',
    color_id: 0,
    hot: 0,
    aliases: 0
  };
  showDialog.value = true;
};

// 打开编辑对话框
const openEditDialog = (tag) => {
  isEditing.value = true;
  selectedTag.value = tag;
  formData.value = {
    id: tag.id_index, // 使用id_index作为ID
    tag: tag.tag,
    translate: tag.translate || '',
    color_id: tag.color_id || 0,
    hot: tag.hot || 0,
    aliases: tag.aliases || 0
  };
  showDialog.value = true;
};

// 关闭对话框
const closeDialog = () => {
  showDialog.value = false;
};

// 关闭所有对话框
const closeAllDialogs = () => {
  showDialog.value = false;
  showDeleteConfirm.value = false;
  showBatchDeleteConfirm.value = false;
};

// 提交表单
const submitForm = async () => {
  // 表单验证
  if (!formData.value.tag) {
    message({ type: 'error', str: t('tagManager.textRequired') });
    return;
  }

  try {
    if (isEditing.value) {
      // 编辑标签
      const response = await danbooruApi.updateDanbooruTag({
        id: formData.value.id,
        update_data: {
          tag: formData.value.tag,
          translate: formData.value.translate,
          color_id: formData.value.color_id,
          hot: formData.value.hot,
          aliases: formData.value.aliases
        }
      });

      if (response && response.code === 200) {
        message({ type: 'success', str: t('message.editSuccess') });
        searchTags(); // 刷新列表
      } else {
        message({ type: 'error', str: t('message.editFailed') });
      }
    } else {
      // 添加标签
      const response = await danbooruApi.addDanbooruTag({
        tag: formData.value.tag,
        translate: formData.value.translate,
        color_id: formData.value.color_id,
        hot: formData.value.hot,
        aliases: formData.value.aliases
      });

      if (response && response.code === 200) {
        message({ type: 'success', str: t('message.addSuccess') });
        searchTags(); // 刷新列表
      } else {
        message({ type: 'error', str: t('message.addFailed') });
      }
    }

    closeDialog();
  } catch (error) {
    console.error('提交表单失败:', error);
    message({ type: 'error', str: isEditing.value ? t('message.editFailed') : t('message.addFailed') });
  }
};

// 确认删除
const confirmDelete = (tag) => {
  selectedTag.value = tag;
  showDeleteConfirm.value = true;
};

// 删除标签
const deleteTag = async () => {
  if (!selectedTag.value || !selectedTag.value.id_index) return;

  try {
    const response = await danbooruApi.deleteDanbooruTag(selectedTag.value.id_index);

    if (response && response.code === 200) {
      message({ type: 'success', str: t('message.deleteSuccess') });
      searchTags(); // 刷新列表
    } else {
      message({ type: 'error', str: t('message.deleteFailed') });
    }

    showDeleteConfirm.value = false;
  } catch (error) {
    console.error('删除标签失败:', error);
    message({ type: 'error', str: t('message.deleteFailed') });
  }
};

// 批量选择相关
const selectedItems = ref([]);

// 计算属性：是否全选
const isAllSelected = computed(() => {
  return tagList.value.length > 0 && selectedItems.value.length === tagList.value.length;
});

// 切换全选
const toggleSelectAll = () => {
  if (isAllSelected.value) {
    selectedItems.value = [];
  } else {
    selectedItems.value = tagList.value.map(tag => tag.id_index);
  }
};

// 确认批量删除
const confirmBatchDelete = () => {
  if (selectedItems.value.length === 0) return;
  showBatchDeleteConfirm.value = true;
};

// 执行批量删除
const batchDeleteTags = async () => {
  if (selectedItems.value.length === 0) return;

  try {
    // 这里假设API支持批量删除，如果不支持需要循环调用单个删除
    const response = await danbooruApi.batchDeleteDanbooruTags(selectedItems.value);

    if (response && response.code === 200) {
      message({ type: 'success', str: `成功删除 ${selectedItems.value.length} 个标签` });
      selectedItems.value = [];
      searchTags(); // 刷新列表
    } else {
      message({ type: 'error', str: '批量删除失败' });
    }
  } catch (error) {
    console.error('批量删除失败:', error);
    // 如果批量删除API不存在，尝试逐个删除
    message({ type: 'error', str: '批量删除失败' });
  }

  showBatchDeleteConfirm.value = false;
};

const importDanbooruDialog = ref();

const openImportDialog = () => {
  importDanbooruDialog.value.open();
};

// 组件挂载时加载数据
onMounted(() => {
  searchTags();
});
</script>


<style scoped>
.danbooru-manager {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.title {
  margin: 0 0 20px;
  padding: 10px 0;
  text-align: center;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color, #ddd);
  color: var(--weilin-prompt-ui-primary-text, #333);
}

.action-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 10px;
}

.search-box {
  display: flex;
  flex: 1;
  margin-right: 10px;
}

.search-box input {
  flex: 1;
  padding: 8px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
}

.search-btn,
.add-btn,
.page-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: var(--weilin-prompt-ui-primary-color, #409eff);
  color: white;
  cursor: pointer;
  margin-left: 10px;
}

.search-btn:hover,
.add-btn:hover,
.page-btn:hover {
  background-color: var(--weilin-prompt-ui-primary-color-hover, #66b1ff);
}

.search-btn:disabled,
.page-btn:disabled {
  background-color: var(--weilin-prompt-ui-disabled-color, #a0cfff);
  cursor: not-allowed;
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
  flex-wrap: wrap;
}

.page-info {
  margin: 0 15px;
  color: var(--weilin-prompt-ui-primary-text, #333);
}

.page-size-control {
  display: flex;
  align-items: center;
  gap: 5px;
  color: var(--weilin-prompt-ui-primary-text, #333);
}

.page-size-input {
  width: 80px;
  padding: 4px 8px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
  text-align: center;
}

.tag-list {
  flex: 1;
  overflow-y: auto;
  border: 1px solid var(--weilin-prompt-ui-border-color, #ddd);
  border-radius: 4px;
}

table {
  width: 100%;
  border-collapse: collapse;
}

th,
td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color, #ddd);
  color: var(--weilin-prompt-ui-primary-text);
}

th {
  background-color: var(--weilin-prompt-ui-background-secondary, #f5f7fa);
  color: var(--weilin-prompt-ui-primary-text, #333);
  font-weight: bold;
  position: sticky;
  top: 0;
  z-index: 10;
}

/* 固定各列宽度 */
.id-column {
  width: 60px;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.tag-column {
  width: 20%;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.translate-column {
  width: 20%;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.color-column {
  width: 120px;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.hot-column {
  width: 80px;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.aliases-column {
  width: 100px;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.control-column {
  width: 160px;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

/* 复选框列 */
.checkbox-column {
  width: 50px;
  background-color: var(--weilin-prompt-ui-secondary-bg, #f5f7fa);
}

.checkbox-column input[type="checkbox"] {
  margin: 0;
  width: auto;
}

tr:hover {
  background-color: var(--weilin-prompt-ui-input-bg, #f5f7fa);
}

.color-box {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color, #ddd);
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.edit-btn {
  background-color: var(--weilin-prompt-ui-warning-color, #e6a23c);
  color: white;
}

.delete-btn {
  background-color: var(--weilin-prompt-ui-danger-color, #f56c6c);
  color: white;
}

.edit-btn:hover {
  background-color: var(--weilin-prompt-ui-warning-color-hover, #ebb563);
}

.delete-btn:hover {
  background-color: var(--weilin-prompt-ui-danger-color-hover, #f78989);
}

.no-results {
  padding: 20px;
  text-align: center;
  color: var(--weilin-prompt-ui-secondary-text, #909399);
  font-style: italic;
}

/* 对话框样式 */
.dialog {
  position: fixed;
  top: 40%;
  z-index: 1001;
  width: 400px;
  max-width: 90%;
  background-color: var(--weilin-prompt-ui-primary-bg, #fff);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}


.dialog-content {
  padding: 20px;
}

.dialog h3 {
  margin-top: 0;
  margin-bottom: 20px;
  color: var(--weilin-prompt-ui-primary-text, #333);
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  color: var(--weilin-prompt-ui-primary-text, #333);
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
}

.color-preview {
  width: 30px;
  height: 30px;
  margin-top: 5px;
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color, #ddd);
}

.dialog-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
}

.dialog-actions button {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-left: 10px;
}

.dialog-actions button:first-child {
  background-color: var(--weilin-prompt-ui-cancel-color, #909399);
  color: white;
}

.dialog-actions button:last-child {
  background-color: var(--weilin-prompt-ui-primary-color, #409eff);
  color: white;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}

input {
  padding: 8px;
  margin-right: 8px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
}

input:focus {
  outline: none;
  border-color: var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 0 0 2px var(--weilin-prompt-ui-primary-color-fade);
}

.batch-delete-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  background-color: var(--weilin-prompt-ui-danger-color, #f56c6c);
  color: white;
  cursor: pointer;
  transition: all 0.3s;
}

.batch-delete-btn:hover:not(.disabled) {
  background-color: var(--weilin-prompt-ui-danger-color-hover, #f78989);
}

.batch-delete-btn.disabled {
  background-color: var(--weilin-prompt-ui-disabled-color, #a0cfff);
  cursor: not-allowed;
  opacity: 0.6;
}
</style>