<template>
  <div :class="`${prefix}lora-manager`">
    <div class="lora-manager-top-bar">
      <!-- 添加搜索框 -->
      <input v-model="searchQuery" :class="`${prefix}search-input`" :placeholder="t('loraManager.searchPlaceholder')"
        @input="debouncedSearch" />

      <button :class="`${prefix}refresh-btn`" @click="refreshList" :title="t('loraManager.refresh')">
        <svg :class="[`${prefix}refresh-icon`, { 'is-rotating': isRefreshing }]" viewBox="0 0 24 24" width="20"
          height="20">
          <path
            d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
        </svg>
      </button>

      <button style="margin-left: 10px;" :class="`${prefix}refresh-btn`" @click="getAllLoraList"
        :title="t('loraManager.cacheAll')">
        <svg :class="[`${prefix}refresh-icon`, { 'is-rotating': isRefreshing }]" viewBox="0 0 24 24" width="20"
          height="20">
          <path
            d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2z" />
        </svg>
      </button>

      <!-- 添加复选框区域 -->
      <div class="checkbox-container">
        <label :class="`${prefix}checkbox-label`">
          <input type="checkbox" v-model="showHoverInfo" :class="`${prefix}checkbox`" />
          <span>悬浮信息</span>
        </label>
        <label :class="`${prefix}checkbox-label`" v-if="loraManager == 'prompt_inner'">
          <input type="checkbox" v-model="clickAddTag" :class="`${prefix}checkbox`" />
          <span>点击添加Tag</span>
        </label>
      </div>
    </div>

    <!-- 主分类导航 -->
    <div :class="`${prefix}category-nav`" v-if="!isSearch">
      <button v-for="(category) in Object.keys(folderList)" :key="category"
        :class="[`${prefix}category-btn`, { active: currentCategory === category }]" @click="selectCategory(category)">
        {{ category === '/' ? t('loraManager.root') : category == "all" ? t('loraManager.all') : category }}
      </button>
    </div>

    <!-- 子分类导航 -->
    <div v-if="currentCategory != 'all' && !isSearch" :class="`${prefix}subcategory-nav`">
      <button v-for="subCategory in Object.keys(selectFolder)" :key="subCategory"
        :class="[`${prefix}category-btn`, { active: currentSubCategory === subCategory }]"
        @click="selectSecondCategory(subCategory)">
        {{ subCategory === '/' ? t('loraManager.root') : subCategory == "all" ? t('loraManager.all') : subCategory }}
      </button>
    </div>

    <!-- 使用虚拟滚动列表 -->
    <div :class="`${prefix}lora-list-container`" ref="scrollContainer" @scroll="handleScroll">
      <div v-if="isLoading && !isLoadingMore" class="loading-indicator">
        {{ t('loraManager.loading') }}
      </div>
      <div v-else-if="paginatedLoraList.length === 0" class="empty-list">
        {{ t('loraManager.noResults') }}
      </div>

      <div :class="`${prefix}lora-list`"
        style="display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 12px;">
        <div v-for="lora in paginatedLoraList" :key="lora.file_path" :class="`${prefix}lora-card`" ref="loraCardRef"
          @click="openLoraDetail(lora)" @mouseover="(e) => handleMouseHover(lora.name, e)"
          @mouseleave="handleMouseLeave"
          style="display: flex; flex-direction: column; min-height: 200px; cursor: pointer;">
          <div :class="`${prefix}lora-preview`"
            style="flex: 1; display: flex; align-items: center; justify-content: center; overflow: hidden;width: 100%;">
            <img v-if="lora.preview" :src="lora.preview" :alt="lora.model_name" :title="lora.model_name" loading="lazy"
              style="width: 100%; height: 100%; object-fit: contain; min-height: 150px;" />
            <div v-else :class="`${prefix}no-preview`"
              style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; min-height: 150px;">
              <svg viewBox="0 0 24 24" width="24" height="24">
                <path
                  d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" />
              </svg>
            </div>
          </div>
          <div :class="`${prefix}lora-name`" style="padding: 8px; text-align: center;
            word-break: break-word;
            white-space: normal;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
            min-height: 40px;
            max-height: 40px; /* 添加固定高度 */
            line-height: 1.2;
            text-overflow: ellipsis;"> <!-- 添加文本溢出省略号 -->
            {{ retLoraName(lora) }}
          </div>
        </div>
      </div>

      <div>
        <!-- 加载更多提示 -->
        <div v-if="isLoadingMore" class="loading-more">
          {{ t('loraManager.loadingMore') }}
        </div>
        <div v-if="!isLoadingMore && hasLoadedAll" class="no-more-data">
          {{ t('loraManager.noMoreData') }}
        </div>
      </div>

    </div>

    <loraDetail ref="loraDetailRef" />
    <LoraCard ref="loraCardItem" v-if="showCard" :fileNmae="hoveFileName" :paddingLeft="paddingLeftValue"
      :paddingTop="paddingTopValue" @cardLeave="handleEnterLeave" @cardenter="handEnterCard" />

  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import { loraApi } from '@/api/lora'
import loraDetail from './lora_detail.vue'
import message from "@/utils/message"
import LoraCard from './lora_card.vue'

const prefix = "weilin_prompt_ui_"
const { t } = useI18n()
const isRefreshing = ref(false)
const isLoading = ref(false)
const isLoadingMore = ref(false) // 加载更多状态
const hasLoadedAll = ref(false) // 是否已加载全部
const currentCategory = ref('all')
const currentSubCategory = ref('')
const intervalId = ref(null)
const searchQuery = ref('')
const scrollContainer = ref(null)
const showCard = ref(false)
const hoveFileName = ref('')
const paddingLeftValue = ref(100)
const paddingTopValue = ref(0)
const loraCardRef = ref()
const isEnterCatd = ref(false)
const isHovering = ref(false);
const loraCardItem = ref()

const showHoverInfo = ref(localStorage.getItem('weilin_prompt_ui_showHoverInfo'));
const clickAddTag = ref(localStorage.getItem('weilin_prompt_ui_clickAddTag'));

if (showHoverInfo.value === null || showHoverInfo.value === undefined || showHoverInfo.value === '') {
  localStorage.setItem('weilin_prompt_ui_showHoverInfo', true);
  showHoverInfo.value = true;
}
if (clickAddTag.value === null || clickAddTag.value === undefined || clickAddTag.value === '') {
  localStorage.setItem('weilin_prompt_ui_clickAddTag', false);
  clickAddTag.value = false;
}

const props = defineProps({
  loraManager: {
    type: String,
    default: 'look'
  }
})


// 监听复选框变化并保存到本地存储
watch(showHoverInfo, (newVal) => {
  localStorage.setItem('weilin_prompt_ui_showHoverInfo', newVal);
});

watch(clickAddTag, (newVal) => {
  localStorage.setItem('weilin_prompt_ui_clickAddTag', newVal);
});


// 分页相关
const currentPage = ref(1)
const pageSize = ref(50) // 每页显示的数量
const totalPages = computed(() => {
  if (currentCategory.value === 'all') {
    const rootFolder = selectFolder.value
    if (rootFolder) {
      const valuesArray = Object.values(rootFolder)
      return Math.ceil(valuesArray.length / pageSize.value)
    }
  } else {
    const rootFolder = selectFolder.value[currentSubCategory.value]
    if (rootFolder) {
      const valuesArray = Object.values(rootFolder)
      return Math.ceil(valuesArray.length / pageSize.value)
    }
    return 1
  }
})

const handEnterCard = () => {
  // console.log("enter")
  isEnterCatd.value = true;
  isHovering.value = true;
}
const handleMouseHover = (fileName, event) => {
  if (!showHoverInfo.value || showHoverInfo.value == "false") return; // 如果不显示悬浮信息，直接返回

  isHovering.value = true;
  if (hoveFileName.value === fileName && showCard.value) return;

  const hoveredCard = event.currentTarget;
  const cardRect = hoveredCard.getBoundingClientRect();
  const viewportHeight = window.innerHeight;
  const cardWidth = 450; // LoraCard的宽度

  // 计算最佳显示位置 - 居中显示
  let position = {
    left: cardRect.left + (cardRect.width - cardWidth) / 2, // 居中计算
    top: cardRect.top + cardRect.height + 10 // 默认在下方显示
  };

  // 检查底部空间是否足够
  if (position.top + 310 > viewportHeight) {
    // 底部空间不足，改为在上方显示
    position.top = cardRect.top - 310;
  }

  // 确保不会超出视窗边界
  position.left = Math.max(10, Math.min(position.left, window.innerWidth - cardWidth - 10));
  position.top = Math.max(10, Math.min(position.top, viewportHeight - 310));

  paddingLeftValue.value = position.left;
  paddingTopValue.value = position.top;

  showCard.value = true;
  hoveFileName.value = fileName;
  nextTick(() => {
    loraCardItem.value.refresh()
  })
}


const handleMouseLeave = () => {
  isHovering.value = false;
  setTimeout(() => {
    if (!isEnterCatd.value && !isHovering.value) {
      showCard.value = false;
      hoveFileName.value = "";
      isEnterCatd.value = false;
    }
  }, 200)
}

const handleEnterLeave = () => {
  showCard.value = false;
  hoveFileName.value = "";
  isEnterCatd.value = false;
}

const folderList = ref([])
const selectFolder = ref([])
const seed = ref('')
const actionAct = ref(0)

const openSetSeed = (action, newSeed) => {
  actionAct.value = action
  seed.value = newSeed
}

const getFolderList = async () => {
  try {
    const res = await loraApi.getLoraFolderList()
    folderList.value = res.data
  } catch (error) {
    console.error('Failed to get folder list:', error)
    message({ type: "error", str: 'message.loadFailed' })
  }
}

// 处理滚动事件
const handleScroll = () => {
  if (!scrollContainer.value || isLoadingMore.value || hasLoadedAll.value) return

  const container = scrollContainer.value
  // 当滚动到距离底部100px时触发加载更多
  if (container.scrollHeight - container.scrollTop - container.clientHeight < 100) {
    loadMoreData()
  }
}

const isSearch = ref(false)
// 防抖搜索
let searchTimeout = null
const debouncedSearch = () => {
  if (searchTimeout) clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    if (searchQuery.value.length > 0) {
      isSearch.value = true
      searchLoraList()
    } else {
      isSearch.value = false
      refreshList()
    }
  }, 300)
}

const retLoraName = (lora) => {
  if (lora.local_info?.name && lora.local_info.name !== '' && lora.local_info.name.length > 0) {
    return lora.local_info.name
  } else {
    return lora.name
  }
}

const loraDetailRef = ref()

const openLoraDetail = (loraData) => {
  if (props.loraManager === 'addLora') {
    selectLora(loraData)
  } else if (props.loraManager === 'prompt_inner' && clickAddTag.value) {
    // 如果启用了点击添加Tag，则直接添加Tag而不打开详情
    addLoraTag(loraData);
  } else {
    loraDetailRef.value.open(loraData)
  }
}

const searchLoraList = async () => {
  try {
    const res = await loraApi.searchLoraGetFolderList(searchQuery.value)
    selectFolder.value = res.data
    if (selectFolder.value.length > 0) {
      currentPage.value = 1 // 重置页码
      const valuesArray = Object.values(selectFolder.value)
      // 根据当前页码获取对应的50条数据
      const startIndex = (currentPage.value - 1) * 50
      const endIndex = startIndex + 50
      const pageData = valuesArray.slice(startIndex, endIndex)
      getRangeLoraList(pageData)
    }
  } catch (error) {
    console.error('Failed to get folder list:', error)
    message({ type: "error", str: 'message.loadFailed' })
  }
}


// 分页后的列表
const paginatedLoraList = ref([])

// 选择分类时重置子分类和页码
const selectCategory = (category) => {
  if (category === "all") {
    paginatedLoraList.value = []
    currentCategory.value = category
    currentSubCategory.value = "/"
    selectFolder.value = folderList.value[category]
    const rootFolder = selectFolder.value
    if (rootFolder) {
      hasLoadedAll.value = false
      currentPage.value = 1 // 重置页码
      const valuesArray = Object.values(rootFolder)
      // 根据当前页码获取对应的50条数据
      const startIndex = (currentPage.value - 1) * 50
      const endIndex = startIndex + 50
      const pageData = valuesArray.slice(startIndex, endIndex)
      getRangeLoraList(pageData)
    }
  } else {
    paginatedLoraList.value = []
    currentCategory.value = category
    currentSubCategory.value = "/"
    selectFolder.value = folderList.value[category]
    const rootFolder = selectFolder.value["/"]
    if (rootFolder) {
      hasLoadedAll.value = false
      currentPage.value = 1 // 重置页码
      const valuesArray = Object.values(rootFolder)
      // 根据当前页码获取对应的50条数据
      const startIndex = (currentPage.value - 1) * 50
      const endIndex = startIndex + 50
      const pageData = valuesArray.slice(startIndex, endIndex)
      getRangeLoraList(pageData)
    }
  }

}

const selectSecondCategory = (subCategory) => {
  if (subCategory != currentSubCategory.value) {
    currentSubCategory.value = subCategory
    paginatedLoraList.value = []
    const rootFolder = selectFolder.value[currentSubCategory.value]
    if (rootFolder) {
      hasLoadedAll.value = false
      currentPage.value = 1 // 重置页码
      const valuesArray = Object.values(rootFolder)
      // 根据当前页码获取对应的50条数据
      const startIndex = (currentPage.value - 1) * 50
      const endIndex = startIndex + 50
      const pageData = valuesArray.slice(startIndex, endIndex)
      getRangeLoraList(pageData)
    }
  }
}


const getRangeLoraList = async (arr) => {
  const res = await loraApi.getLoraRangeList(arr)
  if (currentPage.value === 1) {
    paginatedLoraList.value = res.data.loras
  } else {
    paginatedLoraList.value = paginatedLoraList.value.concat(res.data.loras)
  }
}

const getAllLoraList = async () => {
  if (intervalId.value != null) {
    message({ type: "warn", str: 'message.isLoading' })
    return
  }

  try {
    message({ type: "success", str: 'message.isLoadingPleaseWait' })
    await loraApi.getAllLoraList()
    // 每秒调用一次 getAllLoraStatus
    intervalId.value = setInterval(async () => {
      await getAllLoraStatus()
    }, 1000)
  } catch (error) {
    console.error('Failed to get all lora list:', error)
    message({ type: "error", str: 'message.loadFailed' })
  }
}

const getAllLoraStatus = async () => {
  try {
    const res = await loraApi.getAllLoraStatus()

    if (res.data.isLoading === false) {
      clearInterval(intervalId.value)
      intervalId.value = null
      message({ type: "success", str: 'message.loaddingSuccess' })
      // 加载完成后刷新列表
      await refreshList()
    } else {
      message({ type: "warn", str: 'message.loaddingPrc', name: res.data.progress })
    }
  } catch (error) {
    console.error('Failed to get lora status:', error)
    clearInterval(intervalId.value)
    intervalId.value = null
    message({ type: "error", str: 'message.loadFailed' })
  }
}

const refreshList = async () => {
  if (isRefreshing.value) return
  isRefreshing.value = true
  currentPage.value = 1 // 刷新时重置页码
  hasLoadedAll.value = false
  isLoadingMore.value = false

  try {
    await getFolderList()
    nextTick(() => {
      selectCategory('all')
    })
  } catch (error) {
    console.error('Failed to refresh lora list:', error)
  } finally {
    isRefreshing.value = false
  }
}


// 加载更多数据
const loadMoreData = async () => {
  // 如果已经是最后一页，标记为全部加载完成
  if (currentPage.value >= totalPages.value) {
    hasLoadedAll.value = true
    return
  }

  isLoadingMore.value = true

  try {
    // 增加页码
    currentPage.value++
    // 加载更多数据
    if (isSearch.value) {
      selectFolder.value = res.data
      if (selectFolder.value.length > 0) {
        const valuesArray = Object.values(selectFolder.value)
        // 根据当前页码获取对应的50条数据
        const startIndex = (currentPage.value - 1) * 50
        const endIndex = startIndex + 50
        const pageData = valuesArray.slice(startIndex, endIndex)
        getRangeLoraList(pageData)
      }
    } else {
      if (currentCategory.value === "all") {
        selectFolder.value = folderList.value[currentCategory.value]
        const rootFolder = selectFolder.value
        if (rootFolder) {
          const valuesArray = Object.values(rootFolder)
          // 根据当前页码获取对应的50条数据
          const startIndex = (currentPage.value - 1) * 50
          const endIndex = startIndex + 50
          const pageData = valuesArray.slice(startIndex, endIndex)
          getRangeLoraList(pageData)
        }
      } else {
        const rootFolder = selectFolder.value[currentSubCategory.value]
        if (rootFolder) {
          const valuesArray = Object.values(rootFolder)
          // 根据当前页码获取对应的50条数据
          const startIndex = (currentPage.value - 1) * 50
          const endIndex = startIndex + 50
          const pageData = valuesArray.slice(startIndex, endIndex)
          getRangeLoraList(pageData)
        }
      }
    }


  } finally {
    isLoadingMore.value = false
  }
}

// 重置加载状态
const resetLoadingState = () => {
  currentPage.value = 1
  hasLoadedAll.value = false
  isLoadingMore.value = false
}

// 监听分类和搜索变化，重置页码和加载状态
watch([currentCategory, currentSubCategory, searchQuery], () => {
  resetLoadingState()
})

// 组件挂载时加载数据
onMounted(() => {
  refreshList()
})

// 选择Lora
const selectLora = (lora) => {
  if (actionAct.value === 0) {
    window.postMessage({
      type: 'weilin_prompt_ui_selectLora',
      lora: {
        name: lora.model_name,
        display_name: retLoraName(lora),
        lora: lora.name,
        weight: lora.local_info?.strengthMin ? lora.local_info.strengthMin : 1,
        text_encoder_weight: lora.local_info?.strWeight ? lora.local_info.strWeight : 1,
        loraWorks: lora.local_info?.loraWorks ? lora.local_info.loraWorks : '',
      }
    }, '*')
  } else if (actionAct.value === 1) {
    window.postMessage({
      type: 'weilin_prompt_ui_selectLora_stack_' + seed.value,
      lora: {
        name: lora.model_name,
        display_name: retLoraName(lora),
        lora: lora.name,
        weight: lora.local_info?.strengthMin ? lora.local_info.strengthMin : 1,
        text_encoder_weight: lora.local_info?.strWeight ? lora.local_info.strWeight : 1,
        loraWorks: lora.local_info?.loraWorks ? lora.local_info.loraWorks : '',
      }
    }, '*')
  } else if (actionAct.value === 2) {
    window.postMessage({
      type: 'weilin_prompt_ui_selectLora_stack_node_' + seed.value,
      lora: {
        name: lora.model_name,
        display_name: retLoraName(lora),
        lora: lora.name,
        weight: lora.local_info?.strengthMin ? lora.local_info.strengthMin : 1,
        text_encoder_weight: lora.local_info?.strWeight ? lora.local_info.strWeight : 1,
        loraWorks: lora.local_info?.loraWorks ? lora.local_info.loraWorks : '',
      }
    }, '*')
  }
}



// 添加Lora标签的函数
const addLoraTag = (loraData) => {
  // 发送消息添加标签
  window.postMessage({
    type: 'weilin_prompt_ui_addLoraTag_inner',
    lora: {
      tag: `<wlr:${loraData.model_name}:${loraData.local_info?.strengthMin ? loraData.local_info.strengthMin : 1}:${loraData.local_info?.strWeight ? loraData.local_info.strWeight : 1}>`,
      loraWorks: loraData.local_info?.loraWorks ? loraData.local_info.loraWorks : '',
    }
  }, '*');
  // 显示提示消息
  // message({ type: "success", str: `已添加Lora标签: ${loraName}` });
}

defineExpose({
  openSetSeed
})

</script>

<style scoped>
.weilin_prompt_ui_lora-manager {
  overflow: hidden;
  background: var(--weilin-prompt-ui-primary-bg);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.weilin_prompt_ui_lora-manager-container {
  padding: 16px;
}

.weilin_prompt_ui_lora-list-container {
  flex: 1;
  overflow-y: auto;
  position: relative;
  padding-right: 8px;
  box-sizing: border-box;
}

.weilin_prompt_ui_lora-list-container::-webkit-scrollbar {
  width: 6px;
}

.weilin_prompt_ui_lora-list-container::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
  border-radius: 3px;
}

.weilin_prompt_ui_lora-list-container::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.weilin_prompt_ui_lora-list-container::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}


.weilin_prompt_ui_lora-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  padding-bottom: 16px;
  padding-top: 5px;
}

.weilin_prompt_ui_lora-item {
  padding: 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 8px;
  background: var(--weilin-prompt-ui-primary-bg);
  transition: all 0.3s ease;
  cursor: pointer;
}

.weilin_prompt_ui_lora-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--weilin-prompt-ui-shadow-color);
}

.weilin_prompt_ui_lora-item-content {
  display: flex;
  gap: 12px;
}

.weilin_prompt_ui_lora-preview {
  width: 80px;
  height: 80px;
  border-radius: 6px;
  overflow: hidden;
  background: var(--weilin-prompt-ui-secondary-bg);
  display: flex;
  align-items: center;
  justify-content: center;
}

.weilin_prompt_ui_lora-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.weilin_prompt_ui_no-preview {
  display: flex;
  align-items: center;
  justify-content: center;
}

.weilin_prompt_ui_no-preview svg {
  fill: var(--weilin-prompt-ui-secondary-text);
}

.weilin_prompt_ui_lora-info {
  flex: 1;
  overflow: hidden;
}

.weilin_prompt_ui_lora-name {
  margin: 0 0 4px;
  font-size: 16px;
  color: var(--weilin-prompt-ui-primary-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.weilin_prompt_ui_lora-path {
  margin: 0;
  font-size: 12px;
  color: var(--weilin-prompt-ui-secondary-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.weilin_prompt_ui_refresh-btn {
  border: none;
  background: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.weilin_prompt_ui_refresh-btn:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_refresh-icon {
  fill: var(--weilin-prompt-ui-secondary-text);
  transition: transform 0.5s ease;
}

.weilin_prompt_ui_refresh-icon.is-rotating {
  animation: rotate 1s linear infinite;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

.weilin_prompt_ui_header-right {
  display: flex;
  align-items: center;
}

.weilin_prompt_ui_category-nav {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
  min-height: 40px;
  /* 添加最小高度 */
  max-height: 100px;
  overflow-y: auto;
}

.weilin_prompt_ui_category-nav::-webkit-scrollbar {
  width: 6px;
}

.weilin_prompt_ui_category-nav::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
  border-radius: 3px;
}

.weilin_prompt_ui_category-nav::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.weilin_prompt_ui_category-nav::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

.weilin_prompt_ui_category-btn {
  padding: 6px 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-primary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  cursor: pointer;
  transition: all 0.3s ease;
}

.weilin_prompt_ui_category-btn:hover {
  background: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_category-btn.active {
  background: var(--weilin-prompt-ui-primary-color);
  color: #fff;
  border-color: var(--weilin-prompt-ui-primary-color);
}

.weilin_prompt_ui_subcategory-nav {
  display: flex;
  gap: 8px;
  margin-bottom: 16px;
  margin-top: -8px;
  flex-wrap: wrap;
  padding-left: 16px;
  min-height: 40px;
  /* 确保与category-nav一致 */
  max-height: 100px;
  overflow-y: auto;
}


.weilin_prompt_ui_subcategory-nav::-webkit-scrollbar {
  width: 6px;
}

.weilin_prompt_ui_subcategory-nav::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
  border-radius: 3px;
}

.weilin_prompt_ui_subcategory-nav::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.weilin_prompt_ui_subcategory-nav::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}


.lora-manager-top-bar {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

/* 添加搜索框样式 */
.weilin_prompt_ui_search-input {
  flex: 1;
  margin-right: 10px;
  padding: 6px 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-primary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  transition: all 0.3s ease;
}

.weilin_prompt_ui_search-input:focus {
  outline: none;
  border-color: var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 0 0 2px rgba(var(--weilin-prompt-ui-primary-color), 0.2);
}

/* 分页控制样式 */
.pagination-controls {
  display: flex;
  justify-content: center;
  align-items: center;
  margin: 10px 0;
  gap: 10px;
}

.weilin_prompt_ui_page-btn {
  padding: 6px 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-primary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  cursor: pointer;
  transition: all 0.3s ease;
}

.weilin_prompt_ui_page-btn:hover:not(:disabled) {
  background: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.page-info {
  color: var(--weilin-prompt-ui-secondary-text);
}

.loading-indicator,
.empty-list {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 200px;
  color: var(--weilin-prompt-ui-secondary-text);
  font-size: 16px;
}

.loading-more,
.no-more-data {
  text-align: center;
  padding: 15px 0;
  color: var(--weilin-prompt-ui-secondary-text);
  font-size: 14px;
}

.no-more-data {
  color: var(--weilin-prompt-ui-secondary-text);
  opacity: 0.8;
}

.weilin_prompt_ui_lora-card {
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 8px;
  background: var(--weilin-prompt-ui-primary-bg);
  transition: all 0.3s ease;
  overflow: hidden;
  aspect-ratio: 1/1.3;
  /* position: relative; */
  /* 保持卡片比例 */
}

.weilin_prompt_ui_lora-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px var(--weilin-prompt-ui-shadow-color);
  border: 1px solid var(--weilin-prompt-ui-primary-color-hover);
}

.weilin_prompt_ui_lora-preview {
  aspect-ratio: 1/1;
  /* 保持图片区域为正方形 */
}

.weilin_prompt_ui_lora-name {
  margin: 0;
  font-size: 14px;
  color: var(--weilin-prompt-ui-primary-text);
  word-break: break-word;
  white-space: normal;
  line-height: 1.2;
}


.lora-manager-top-bar {
  display: flex;
  align-items: center;
  padding: 8px;
  gap: 8px;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.checkbox-container {
  display: flex;
  margin-left: auto;
  gap: 12px;
}

.weilin_prompt_ui_checkbox-label {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: var(--weilin-prompt-ui-primary-text);
  cursor: pointer;
}

.weilin_prompt_ui_checkbox {
  cursor: pointer;
}
</style>
