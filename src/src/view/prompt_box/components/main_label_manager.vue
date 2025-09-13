<template>
  <div class="main-label-manager">
    <div class="mlm-header">
      <input
        v-model="search"
        class="mlm-search"
        type="text"
        placeholder="搜索标签…"
      />
      <button class="mlm-add" @click="createNew">+ 新建标签</button>
      <div class="mlm-grid">
        <button class="mlm-sort" @click="toggleTimeSort">
          按时间 {{ sortTimeDesc ? '后→先' : '先→后' }}
        </button>
        <button class="mlm-sort" @click="toggleNameSort">
          按名称 {{ sortNameAsc ? 'A→Z' : 'Z→A' }}
        </button>
        <button class="mlm-edit" :disabled="!current" @click="renameSelected">编辑</button>
        <button class="mlm-delete" :disabled="!current" @click="deleteSelected">删除</button>
      </div>
    </div>

    <div class="mlm-list">
      <div
        v-for="item in sortedList"
        :key="item.id"
        :class="['mlm-item', { active: item.id === internalSelectedId }]"
        @click="selectItem(item)"
        :title="item.updatedAt ? formatTime(item.updatedAt) : ''"
      >
        <span class="mlm-name">{{ item.name }}</span>
      </div>
    </div>

    <!-- 原底部操作区已上移到新建按钮下方 -->
  </div>
  
</template>

<script setup>
import { ref, computed, watch, onMounted, defineExpose } from 'vue'

const STORAGE_KEY = 'weilin_prompt_ui_main_labels_v1'

// 选中项由内部维护，也允许父组件通过 props 设置初始选中
const props = defineProps({
  selectedId: { type: String, default: null }
})

const emit = defineEmits(['select'])

const search = ref('')
const items = ref([]) // { id, name, content, createdAt, updatedAt }
const internalSelectedId = ref(props.selectedId)

onMounted(() => {
  load()
  // 如果没有任何标签，创建一个默认的示例
  if (items.value.length === 0) {
    const id = genId()
    items.value.push({
      id,
      name: '示例标签',
      content: '',
      createdAt: Date.now(),
      updatedAt: Date.now()
    })
    save()
    internalSelectedId.value = id
    emit('select', getById(id))
  }
})

watch(() => props.selectedId, (v) => {
  internalSelectedId.value = v
})

const sortTimeDesc = ref(true)
const sortNameAsc = ref(true)
const sortMode = ref('time') // 'time' | 'name'

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(i =>
    (i.name || '').toLowerCase().includes(q)
  )
})

// 新的排序逻辑：根据 sortMode 决定按时间或名称排序
const sortedList = computed(() => {
  const arr = [...filtered.value]

  const cmpName = (a, b) => {
    const na = (a.name || '')
    const nb = (b.name || '')
    let cmp = na.localeCompare(nb, undefined, { numeric: true, sensitivity: 'base' })
    if (!sortNameAsc.value) cmp = -cmp
    return cmp
  }

  const cmpTime = (a, b) => {
    let cmp = a.createdAt - b.createdAt
    if (sortTimeDesc.value) cmp = -cmp
    return cmp
  }

  arr.sort((a, b) => {
    if (sortMode.value === 'name') {
      const n = cmpName(a, b)
      if (n !== 0) return n
      return cmpTime(a, b)
    }
    const t = cmpTime(a, b)
    if (t !== 0) return t
    return cmpName(a, b)
  })

  return arr
})

const sortedAndFiltered = computed(() => {
  const arr = [...filtered.value]
  // 使用创建时间进行“按时间”排序，编辑不会改变顺序
  arr.sort((a, b) => {
    // 时间排序（使用 createdAt）
    if (a.createdAt !== b.createdAt) {
      return sortTimeDesc.value ? (b.createdAt - a.createdAt) : (a.createdAt - b.createdAt)
    }
    // 名称排序作为次序
    const na = (a.name || '').toLowerCase()
    const nb = (b.name || '').toLowerCase()
    if (na === nb) return 0
    return sortNameAsc.value ? (na < nb ? -1 : 1) : (na > nb ? -1 : 1)
  })
  return arr
})

const current = computed(() => getById(internalSelectedId.value))

function genId() {
  return 'mlm_' + Math.random().toString(36).slice(2) + '_' + Date.now()
}

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const arr = raw ? JSON.parse(raw) : []
    // 兼容旧数据，补齐创建/更新时间
    items.value = arr.map(i => ({
      ...i,
      createdAt: i?.createdAt ?? i?.updatedAt ?? Date.now(),
      updatedAt: i?.updatedAt ?? i?.createdAt ?? Date.now(),
    }))
  } catch (e) {
    items.value = []
  }
}

function save() {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value))
}

function getById(id) {
  return items.value.find(i => i.id === id) || null
}

function selectItem(item) {
  internalSelectedId.value = item.id
  emit('select', { ...item })
}

function createNew() {
  const name = window.prompt('新建标签名称：', '')
  if (!name) return
  const id = genId()
  const obj = { id, name: name.trim(), content: '', createdAt: Date.now(), updatedAt: Date.now() }
  items.value.unshift(obj)
  save()
  internalSelectedId.value = id
  emit('select', { ...obj })
}

function renameSelected() {
  const node = current.value
  if (!node) return
  const name = window.prompt('重命名标签：', node.name || '')
  if (!name) return
  node.name = name.trim()
  node.updatedAt = Date.now()
  save()
}

function deleteSelected() {
  const node = current.value
  if (!node) return
  if (!window.confirm(`确定删除标签“${node.name}”吗？`)) return
  const idx = items.value.findIndex(i => i.id === node.id)
  if (idx >= 0) items.value.splice(idx, 1)
  save()
  if (items.value.length) {
    internalSelectedId.value = items.value[0].id
    emit('select', { ...items.value[0] })
  } else {
    internalSelectedId.value = null
    emit('select', null)
  }
}

function toggleTimeSort() {
  sortMode.value = 'time'
  sortTimeDesc.value = !sortTimeDesc.value
}
function toggleNameSort() {
  sortMode.value = 'name'
  sortNameAsc.value = !sortNameAsc.value
}

function updateSelectedContent(newContent) {
  const n = current.value
  if (!n) return
  n.content = newContent ?? ''
  n.updatedAt = Date.now()
  // 轻量防抖：延迟写入
  clearTimeout(updateTimer)
  updateTimer = setTimeout(() => save(), 400)
}

let updateTimer = null

function formatTime(ts) {
  try {
    const d = new Date(ts)
    return `${d.getFullYear()}-${(d.getMonth()+1).toString().padStart(2,'0')}-${d.getDate().toString().padStart(2,'0')} ${d.getHours().toString().padStart(2,'0')}:${d.getMinutes().toString().padStart(2,'0')}`
  } catch { return '' }
}

defineExpose({ updateSelectedContent })
</script>

<style scoped>
.main-label-manager {
  width: 280px;
  min-width: 280px;
  max-width: 280px;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
  padding: 10px 8px;
  border-right: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-primary-bg);
  /* 独立滚动布局的关键：限制整体高度并让列表内部滚动 */
  height: 100%;
  max-height: calc(100vh - var(--weilin-left-panel-offset, 100px)); /* 预留顶部窗口标题/边距，可按需调整 */
  overflow: hidden; /* 防止随列表增长而拉长整体页面 */
}

.mlm-header {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.mlm-search {
  width: 100%;
  height: 32px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
  padding: 0 8px;
}

.mlm-add {
  background: #28a745;
  color: #fff;
  border: none;
  border-radius: 6px;
  height: 32px;
  width: 100%;
  cursor: pointer;
}

.mlm-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  width: 100%;
}

.mlm-list {
  margin-top: 8px;
  flex: 1 1 auto;
  min-height: 0; /* 允许在 flex 布局中被压缩，从而触发滚动 */
  overflow-y: auto;
  padding-right: 4px;
}
.mlm-list::-webkit-scrollbar {
  width: 6px;
}
.mlm-list::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

.mlm-item {
  display: flex;
  align-items: center;
  min-height: 36px;
  padding: 6px 10px;
  margin: 6px 0;
  background: var(--weilin-prompt-ui-secondary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid var(--weilin-prompt-ui-border-color);
}
.mlm-item.active {
  outline: 2px solid var(--weilin-prompt-ui-primary-color);
}
.mlm-name {
  font-size: 13px;
}

.mlm-sort {
  height: 32px;
  font-size: 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-button-bg);
  color: var(--weilin-prompt-ui-button-text);
  border-radius: 4px;
  width: 100%;
  cursor: pointer;
}
.mlm-edit,
.mlm-delete {
  height: 32px;
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-button-bg);
  color: var(--weilin-prompt-ui-button-text);
  width: 100%;
  cursor: pointer;
}
.mlm-delete {
  background: #a52a2a20;
  color: #ff6b6b;
}

.mlm-grid button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}
</style>
