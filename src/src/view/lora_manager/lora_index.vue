<template>
  <div :class="`${prefix}lora-manager`">
    <div class="lora-manager-top-bar">
      <!-- 添加搜索框 -->
      <input 
        v-model="searchQuery"
        :class="`${prefix}search-input`"
        :placeholder="t('loraManager.searchPlaceholder')"
      />
      <button :class="`${prefix}refresh-btn`" @click="refreshList" :title="t('loraManager.refresh')">
        <svg :class="[`${prefix}refresh-icon`, { 'is-rotating': isRefreshing }]" viewBox="0 0 24 24" width="20"
          height="20">
          <path
            d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
        </svg>
      </button>

      <button style="margin-left: 10px;" :class="`${prefix}refresh-btn`" @click="getAllLoraList" :title="t('loraManager.cacheAll')">
        <svg  :class="[`${prefix}refresh-icon`, { 'is-rotating': isRefreshing }]" viewBox="0 0 24 24" width="20" height="20">
          <path
            d="M19 12v7H5v-7H3v7c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2v-7h-2zm-6 .67l2.59-2.58L17 11.5l-5 5-5-5 1.41-1.41L11 12.67V3h2z" />
        </svg>
      </button>
    </div>


    <!-- 主分类导航 -->
    <div :class="`${prefix}category-nav`">
      <button :class="[`${prefix}category-btn`, { active: currentCategory === 'all' }]" @click="selectCategory('all')">
        {{ t('loraManager.all') }}
      </button>
      <button v-for="category in categories" :key="category"
        :class="[`${prefix}category-btn`, { active: currentCategory === category }]" @click="selectCategory(category)">
        {{ category }}
      </button>
    </div>

    <!-- 子分类导航 -->
    <div v-if="subCategories.length > 0" :class="`${prefix}subcategory-nav`">
      <button v-for="subCategory in subCategories" :key="subCategory"
        :class="[`${prefix}category-btn`, { active: currentSubCategory === subCategory }]"
        @click="currentSubCategory = subCategory">
        {{ subCategory }}
      </button>
    </div>

    <div :class="`${prefix}lora-list`">
      <div v-for="lora in filteredLoraList" :key="lora.file_path" :class="`${prefix}lora-item`"
        @click="openLoraDetail(lora)">
        <div :class="`${prefix}lora-item-content`">
          <div :class="`${prefix}lora-preview`">
            <img v-if="lora.preview" :src="lora.preview" :alt="lora.model_name" :title="lora.model_name" />
            <div v-else :class="`${prefix}no-preview`">
              <svg viewBox="0 0 24 24" width="24" height="24">
                <path
                  d="M21 19V5c0-1.1-.9-2-2-2H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2zM8.5 13.5l2.5 3.01L14.5 12l4.5 6H5l3.5-4.5z" />
              </svg>
            </div>
          </div>
          <div :class="`${prefix}lora-info`">
            <h4 :class="`${prefix}lora-name`" :title="retLoraName(lora)">{{ retLoraName(lora) }}</h4>
            <p :class="`${prefix}lora-path`" :title="lora.file_path">{{ lora.file_path }}</p>
            <p :class="`${prefix}lora-path`" :title="t('loraManager.loraWorks')">{{ lora.loraWorks }}</p>
          </div>
        </div>
      </div>
    </div>
    <loraDetail ref="loraDetailRef" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { loraApi } from '@/api/lora'
import loraDetail from './lora_detail.vue'
import message from "@/utils/message"

const prefix = "weilin_prompt_ui_"
const { t } = useI18n()
const isRefreshing = ref(false)
const currentCategory = ref('all')
const currentSubCategory = ref('')
const intervalId = ref(null)
const searchQuery = ref('')

const props = defineProps({
  loraManager: {
    type: String,
    default: 'look'
  }
})

// 存储处理后的数据结构
const loraData = ref({
  categories: [],          // 主分类
  allLoras: [],           // 所有lora文件
  categorizedLoras: {},   // 按分类存储的lora文件
  subCategories: {}       // 存储子分类信息
})

const retLoraName = (lora)=>{
  if(lora.local_info.name && lora.local_info.name !== '' && lora.local_info.name.length > 0){
    return lora.local_info.name
  }else{
    return lora.name
  }
}

const loraDetailRef = ref()

const openLoraDetail = (loraData) => {
  if (props.loraManager === 'addLora') {
    selectLora(loraData)
  } else {
    loraDetailRef.value.open(loraData)
  }
}

// 获取文件的分类信息
const getFileCategories = (path) => {
  const parts = path.split(/[\/\\]/)
  if (parts.length === 1) return { main: 'root', sub: null }

  const main = parts[0]
  // 如果是文件，则不包含在子分类中
  if (parts[parts.length - 1].includes('.')) {
    const subParts = parts.slice(1, -1)
    const sub = subParts.length > 0 ? subParts.join('/') : 'root'
    return { main, sub }
  } else {
    // 如果是目录，则包含在子分类中
    const sub = parts.slice(1).join('/')
    return { main, sub }
  }
}

// 处理原始数据，构建数据结构
const processLoraData = (data) => {
  const categories = new Set()
  const categorizedLoras = {}
  const subCategories = {}

  // 处理所有路径，先提取目录结构
  data.path.forEach(path => {
    const { main, sub } = getFileCategories(path)
    if (main !== 'root') {
      categories.add(main)
      if (!categorizedLoras[main]) {
        categorizedLoras[main] = {}
        subCategories[main] = new Set()
      }
      if (sub) {
        // 只添加目录路径，不添加文件名
        const dirParts = sub.split('/')
        if (dirParts[dirParts.length - 1].includes('.')) {
          dirParts.pop()
        }
        if (dirParts.length === 0) {
          subCategories[main].add('root')
        } else {
          subCategories[main].add(dirParts.join('/'))
        }
      }
    }
  })

  // 处理所有文件
  data.loras.forEach(lora => {
    const { main, sub } = getFileCategories(lora.basename)
    if (main === 'root') {
      if (!categorizedLoras.root) categorizedLoras.root = { '': [] }
      categorizedLoras.root[''].push(lora)
    } else {
      if (!categorizedLoras[main]) {
        categorizedLoras[main] = {}
      }
      // 对于文件，使用其所在的目录路径作为key
      const dirPath = sub ? sub.split('/').filter(part => !part.includes('.')).join('/') || 'root' : ''
      if (!categorizedLoras[main][dirPath]) {
        categorizedLoras[main][dirPath] = []
      }
      categorizedLoras[main][dirPath].push(lora)
    }
  })

  // 转换 Set 为数组并排序
  const sortedCategories = Array.from(categories).sort()
  sortedCategories.push('root')

  // 转换子分类 Set 为排序后的数组，确保 'root' 在最后
  const processedSubCategories = {}
  for (const category in subCategories) {
    const subCats = Array.from(subCategories[category])
    const rootIndex = subCats.indexOf('root')
    if (rootIndex !== -1) {
      subCats.splice(rootIndex, 1)
      subCats.sort()
      subCats.push('root')
    } else {
      subCats.sort()
    }
    processedSubCategories[category] = subCats
  }

  return {
    categories: sortedCategories,
    allLoras: data.loras,
    categorizedLoras,
    subCategories: processedSubCategories
  }
}

// 获取当前分类的子分类
const subCategories = computed(() => {
  if (currentCategory.value === 'all' || currentCategory.value === 'root') {
    return []
  }
  return loraData.value.subCategories[currentCategory.value] || []
})

// 根据当前分类和子分类获取显示的文件列表
const filteredLoraList = computed(() => {
  let list = []
  
  // 先根据分类获取基础列表
  if (currentCategory.value === 'all') {
    list = loraData.value.allLoras
  } else {
    const categoryData = loraData.value.categorizedLoras[currentCategory.value]
    if (!categoryData) return []
    
    if (currentCategory.value === 'root' || !currentSubCategory.value) {
      list = categoryData[''] || []
    } else {
      list = categoryData[currentSubCategory.value] || []
    }
  }

  // 如果有搜索词，进行过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    return list.filter(lora => {
      // 优先匹配 local_info.name
      if (lora.local_info?.name) {
        return lora.local_info.name.toLowerCase().includes(query)
      }
      // 如果没有 local_info.name，则匹配 name
      return lora.name.toLowerCase().includes(query)
    })
  }

  return list
})

// 选择分类时重置子分类
const selectCategory = (category) => {
  currentCategory.value = category
  currentSubCategory.value = 'root'
}

// 获取分类列表
const categories = computed(() => {
  return loraData.value.categories
})

const getLoraList = async () => {
  const res = await loraApi.getLoraList()
  // 处理数据并存储
  loraData.value = processLoraData(res.data)
}

const getAllLoraList = async () => {
  if (intervalId.value != null) {
    message({ type: "warn", str: 'message.isLoading' })
  }
  const res = await loraApi.getAllLoraList()
  // 处理数据并存储
  // loraData.value = processLoraData(res.data)
  
  // 每秒调用一次 getAllLoraStatus
  intervalId.value = setInterval(async () => {
    await getAllLoraStatus()
  }, 1000)

  // 假设在某个条件下需要停止调用，可以使用 clearInterval(intervalId)
}

const getAllLoraStatus = async () => {
  const res = await loraApi.getAllLoraStatus()
  // console.log(res)
  if (res.data.isLoading == false) {
    clearInterval(intervalId.value)
    message({ type: "success", str: 'message.loaddingSuccess'})
  }else{
    message({ type: "warn", str: 'message.loaddingPrc', name: res.data.progress})
  }
  // 处理数据并存储
  // loraData.value = processLoraData(res.data)
}

const refreshList = async () => {
  if (isRefreshing.value) return
  isRefreshing.value = true
  try {
    await getLoraList()
  } catch (error) {
    console.error('Failed to refresh lora list:', error)
  } finally {
    isRefreshing.value = false
  }
}

onMounted(() => {
  getLoraList()
})

// 选择Lora
const selectLora = (lora) => {
  // console.log(lora)
  window.postMessage({
    type: 'weilin_prompt_ui_selectLora',
    lora: {
      name: lora.model_name,
      lora: lora.name,
      weight: lora.local_info.strengthMin ? lora.local_info.strengthMin : 0.5,
      text_encoder_weight: lora.local_info.strWeight ? lora.local_info.strWeight : 0.5,
      loraWorks: lora.local_info.loraWorks ? lora.local_info.loraWorks : '',
    }
  }, '*')
}


</script>

<style scoped>
.weilin_prompt_ui_lora-manager {
  overflow: hidden;
  background: var(--weilin-prompt-ui-primary-bg);
}

.weilin_prompt_ui_lora-manager-container {
  padding: 16px;
}

.weilin_prompt_ui_lora-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
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
  object-fit: cover;
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
</style>
