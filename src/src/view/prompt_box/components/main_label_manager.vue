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
    </div>

    <div class="mlm-list">
      <div
        v-for="item in sortedAndFiltered"
        :key="item.id"
        :class="['mlm-item', { active: item.id === internalSelectedId }]"
        @click="selectItem(item)"
        :title="item.updatedAt ? formatTime(item.updatedAt) : ''"
      >
        <span class="mlm-name">{{ item.name }}</span>
      </div>
    </div>

    <div class="mlm-footer">
      <div class="mlm-sorts">
        <button class="mlm-sort" @click="toggleTimeSort">
          按时间 {{ sortTimeDesc ? '后→先' : '先→后' }}
        </button>
        <button class="mlm-sort" @click="toggleNameSort">
          按名称 {{ sortNameAsc ? 'A→Z' : 'Z→A' }}
        </button>
      </div>
      <div class="mlm-actions">
        <button class="mlm-edit" :disabled="!current" @click="renameSelected">编辑</button>
        <button class="mlm-delete" :disabled="!current" @click="deleteSelected">删除</button>
      </div>
    </div>
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

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(i =>
    (i.name || '').toLowerCase().includes(q)
  )
})

const sortedAndFiltered = computed(() => {
  const arr = [...filtered.value]
  // 优先使用时间排序，再用名称排序作为次序
  arr.sort((a, b) => {
    // 时间排序
    if (a.updatedAt !== b.updatedAt) {
      return sortTimeDesc.value ? (b.updatedAt - a.updatedAt) : (a.updatedAt - b.updatedAt)
    }
    // 名称排序
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
    items.value = raw ? JSON.parse(raw) : []
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

function toggleTimeSort() { sortTimeDesc.value = !sortTimeDesc.value }
function toggleNameSort() { sortNameAsc.value = !sortNameAsc.value }

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
}

.mlm-header {
  display: flex;
  gap: 8px;
}

.mlm-search {
  flex: 1;
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
  padding: 0 10px;
  cursor: pointer;
}

.mlm-list {
  margin-top: 8px;
  flex: 1;
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

.mlm-footer {
  margin-top: 8px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.mlm-sorts {
  display: flex;
  gap: 6px;
}
.mlm-sort {
  flex: 1;
  height: 28px;
  font-size: 12px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-button-bg);
  color: var(--weilin-prompt-ui-button-text);
  border-radius: 4px;
}
.mlm-actions {
  display: flex;
  gap: 6px;
}
.mlm-edit,
.mlm-delete {
  flex: 1;
  height: 30px;
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-button-bg);
  color: var(--weilin-prompt-ui-button-text);
}
.mlm-delete {
  background: #a52a2a20;
  color: #ff6b6b;
}
</style>

