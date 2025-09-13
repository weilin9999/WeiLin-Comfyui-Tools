<template>
  <div class="main-label-manager">
    <div class="mlm-header">
      <input v-model="search" class="mlm-search" type="text" placeholder="搜索标签…" />
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

    <transition-group name="mlm" tag="div" class="mlm-list">
      <div
        v-for="(item, idx) in sortedList"
        :key="item.id"
        :class="[
          'mlm-item',
          { active: item.id === internalSelectedId, pinned: !!item.pinned, highlighted: !!item.highlighted },
          { dragging: draggingId === item.id, 'drag-over': dragOverId === item.id }
        ]"
        @click="selectItem(item)"
        :title="item.updatedAt ? formatTime(item.updatedAt) : ''"
        draggable="true"
        @dragstart="onDragStart(item, idx, $event)"
        @dragenter.prevent="onDragEnter(item)"
        @dragover.prevent
        @drop.prevent="onDrop(item)"
        @dragend="onDragEnd"
      >
        <div class="mlm-item-main">
          <span v-if="item.pinned" class="pin-badge">置顶</span>
          <span class="mlm-name">{{ item.name }}</span>
        </div>

        <div class="mlm-item-actions">
          <!-- 置顶：向上箭头（粗实心） -->
          <button :class="['mini-btn','pin',{active:item.pinned}]"
                  :title="item.pinned ? '取消置顶' : '置顶'"
                  @click.stop="togglePin(item)">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <path d="M4 14h4v6h8v-6h4L12 4 4 14z"/>
            </svg>
          </button>

          <!-- 高亮：实心星星 -->
          <button :class="['mini-btn','highlight',{active:item.highlighted}]"
                  :title="item.highlighted ? '取消高亮' : '高亮'"
                  @click.stop="toggleHighlight(item)">
            <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
              <path d="M12 17.27L18.18 21 16.54 13.97 22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/>
            </svg>
          </button>
        </div>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, defineExpose } from 'vue'

const STORAGE_KEY = 'weilin_prompt_ui_main_labels_v1'

const props = defineProps({ selectedId: { type: String, default: null } })
const emit = defineEmits(['select'])

const search = ref('')
const items = ref([]) // { id, name, content, createdAt, updatedAt, pinned, highlighted, order }
const internalSelectedId = ref(props.selectedId)

onMounted(() => {
  load()
  if (items.value.length === 0) {
    const id = genId()
    items.value.push({ id, name: '示例标签', content: '', createdAt: Date.now(), updatedAt: Date.now(), pinned: false, highlighted: false })
    save()
    internalSelectedId.value = id
    emit('select', getById(id))
  }
})

watch(() => props.selectedId, (v) => { internalSelectedId.value = v })

const sortTimeDesc = ref(true)
const sortNameAsc = ref(true)
const sortMode = ref('time') // 'time' | 'name' | 'manual'

// drag state
const draggingId = ref(null)
const dragOverId = ref(null)

const filtered = computed(() => {
  const q = search.value.trim().toLowerCase()
  if (!q) return items.value
  return items.value.filter(i => (i.name || '').toLowerCase().includes(q))
})

const sortedList = computed(() => {
  const arr = [...filtered.value]

  // manual sort: keep groups (pinned > highlighted > normal),
  // but order within the same group by `order` value
  if (sortMode.value === 'manual') {
    const groupWeight = (x) => (x.pinned ? 0 : x.highlighted ? 1 : 2)
    return arr.sort((a, b) => {
      const gw = groupWeight(a) - groupWeight(b)
      if (gw !== 0) return gw
      const ao = a.order ?? 0
      const bo = b.order ?? 0
      if (ao !== bo) return ao - bo
      // fallback by created time to keep stable
      return (a.createdAt ?? 0) - (b.createdAt ?? 0)
    })
  }

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

  const groupWeight = (x) => (x.pinned ? 0 : x.highlighted ? 1 : 2)

  arr.sort((a, b) => {
    const gw = groupWeight(a) - groupWeight(b)
    if (gw !== 0) return gw
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

const current = computed(() => getById(internalSelectedId.value))

function genId() { return 'mlm_' + Math.random().toString(36).slice(2) + '_' + Date.now() }

function load() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    const arr = raw ? JSON.parse(raw) : []
    items.value = arr.map((i, idx) => ({
      id: i.id ?? genId(),
      name: i.name ?? '未命名',
      content: i.content ?? '',
      createdAt: i.createdAt ?? i.updatedAt ?? Date.now(),
      updatedAt: i.updatedAt ?? i.createdAt ?? Date.now(),
      pinned: !!i.pinned,
      highlighted: !!i.highlighted,
      order: typeof i.order === 'number' ? i.order : idx,
    }))
  } catch {
    items.value = []
  }
}

function save() { localStorage.setItem(STORAGE_KEY, JSON.stringify(items.value)) }

function getById(id) { return items.value.find(i => i.id === id) || null }

function selectItem(item) {
  internalSelectedId.value = item.id
  emit('select', { ...item })
}

function createNew() {
  const name = window.prompt('新建标签名称：', '')
  if (!name) return
  const id = genId()
  const now = Date.now()
  const obj = { id, name: name.trim(), content: '', createdAt: now, updatedAt: now, pinned: false, highlighted: false }
  if (sortMode.value === 'manual') {
    const normals = items.value.filter(x => !x.pinned && !x.highlighted)
    const maxOrder = normals.reduce((m, x) => {
      return Math.max(m, typeof x.order === 'number' ? x.order : m)
    }, -1)
    obj.order = maxOrder + 1
  }
  items.value.push(obj)
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

function toggleTimeSort() { sortMode.value = 'time'; sortTimeDesc.value = !sortTimeDesc.value }
function toggleNameSort() { sortMode.value = 'name'; sortNameAsc.value = !sortNameAsc.value }

function togglePin(item) { item.pinned = !item.pinned; item.updatedAt = Date.now(); save() }
function toggleHighlight(item) { item.highlighted = !item.highlighted; item.updatedAt = Date.now(); save() }

function updateSelectedContent(newContent) {
  const n = current.value
  if (!n) return
  n.content = newContent ?? ''
  n.updatedAt = Date.now()
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

// ===== Drag-and-drop manual sort =====
function ensureManualOrderSeed() {
  const list = sortedList.value
  list.forEach((it, i) => { it.order = i })
}

function onDragStart(item, idx, ev) {
  try { ev.dataTransfer.effectAllowed = 'move' } catch {}
  draggingId.value = item.id
  dragOverId.value = null
  // seed current order first, then switch to manual
  ensureManualOrderSeed()
  sortMode.value = 'manual'
}

function onDragEnter(item) {
  if (!draggingId.value) return
  dragOverId.value = item.id
}

function onDrop(targetItem) {
  if (!draggingId.value) return
  const fromId = draggingId.value
  const toId = targetItem?.id
  if (!toId || fromId === toId) return onDragEnd()

  const list = [...sortedList.value]
  const from = list.findIndex(x => x.id === fromId)
  const to = list.findIndex(x => x.id === toId)
  if (from < 0 || to < 0) return onDragEnd()
  const [moved] = list.splice(from, 1)
  list.splice(to, 0, moved)
  list.forEach((it, i) => { it.order = i })
  save()
  onDragEnd()
}

function onDragEnd() {
  draggingId.value = null
  dragOverId.value = null
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
  height: 100%;
  max-height: calc(100vh - var(--weilin-left-panel-offset, 100px));
  overflow: hidden;
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
  max-height: var(--weilin-main-label-list-max-height, 720px);
  flex: 0 0 auto;
  overflow-y: auto;
  padding-right: 4px;
}
.mlm-list::-webkit-scrollbar { width: 6px; }
.mlm-list::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
}

/* ========== 列表项样式 ========== */
.mlm-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 38px;
  padding: 10px 12px;
  margin: 6px 0;
  background: var(--weilin-prompt-ui-secondary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  border-radius: 10px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  transition: background 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease, transform 0.1s ease;
}
.mlm-item.dragging { opacity: 0.6; }
.mlm-item.drag-over { outline: 2px dashed var(--weilin-prompt-ui-primary-color); outline-offset: 2px; box-shadow: none !important; }
.mlm-item:hover {
  background: color-mix(in srgb, var(--weilin-prompt-ui-secondary-bg) 90%, #fff 10%);
  border-color: color-mix(in srgb, var(--weilin-prompt-ui-border-color) 40%, #fff 20%);
  box-shadow: 0 2px 6px rgba(0,0,0,0.15);
  transform: translateY(-1px);
}
.mlm-item.active:not(.drag-over) {
  outline: none;
  box-shadow: 0 0 0 2px color-mix(in srgb, var(--weilin-prompt-ui-primary-color) 35%, transparent);
}

/* 置顶行：浅黄底 + 左侧色条 + 阴影 */
.mlm-item.pinned {
  background: color-mix(in srgb, #d89614 12%, var(--weilin-prompt-ui-secondary-bg));
  border-left: 4px solid #d89614;
  box-shadow: 0 2px 6px rgba(0,0,0,0.25);
}
.mlm-item.pinned:hover {
  box-shadow: 0 3px 8px rgba(0,0,0,0.3);
}

/* 高亮行：浅蓝底 + 左侧色条 + 阴影 */
.mlm-item.highlighted {
  background: color-mix(in srgb, var(--weilin-prompt-ui-primary-color) 12%, var(--weilin-prompt-ui-secondary-bg));
  border-left: 4px solid var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 2px 6px rgba(0,0,0,0.2);
}
.mlm-item.highlighted:hover {
  box-shadow: 0 3px 8px rgba(0,0,0,0.3);
}

.mlm-item-main {
  display: flex;
  align-items: center;
  gap: 8px;
  overflow: hidden;
}

.mlm-name {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  text-overflow: ellipsis;
  overflow: hidden;
}

.pin-badge {
  background: color-mix(in srgb, #d89614 25%, transparent);
  color: #d89614;
  border: 1.5px solid #d89614;
  border-radius: 14px;
  padding: 2px 10px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.5px;
  text-transform: uppercase;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.mlm-item-actions {
  display: flex;
  gap: 6px;
}

/* ========== 操作按钮样式 ========== */
.mini-btn {
  width: 32px;
  height: 32px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #000;
  background: transparent;
  border-radius: 8px;
  color: #fff;
  cursor: pointer;
  transition: background 0.15s ease, border-color 0.15s ease, color 0.15s ease, transform 0.1s ease;
}
.mini-btn:hover { background: rgba(255,255,255,0.06); }
.mini-btn:active { transform: translateY(1px); }
.mini-btn:focus-visible {
  outline: 2px solid color-mix(in srgb, #fff 50%, transparent);
  outline-offset: 2px;
}
.mini-btn svg { width: 18px; height: 18px; }

/* 激活态：置顶=黄底白图标，高亮=蓝底白图标 */
.mini-btn.pin.active {
  background: #d89614;
  border-color: #d89614;
  color: #fff;
}
.mini-btn.highlight.active {
  background: var(--weilin-prompt-ui-primary-color);
  border-color: var(--weilin-prompt-ui-primary-color);
  color: #fff;
}

/* ========== 排序/编辑/删除按钮 ========== */
.mlm-sort,
.mlm-edit,
.mlm-delete {
  height: 32px;
  width: 100%;
  font-size: 12px;
  border-radius: 6px;
  border: 1px solid color-mix(in srgb, var(--weilin-prompt-ui-border-color) 70%, transparent);
  background: color-mix(in srgb, var(--weilin-prompt-ui-button-bg) 90%, #000 10%);
  color: var(--weilin-prompt-ui-button-text);
  transition: background 0.15s ease, border-color 0.15s ease;
}
.mlm-sort:hover,
.mlm-edit:hover,
.mlm-delete:hover {
  background: color-mix(in srgb, var(--weilin-prompt-ui-button-bg) 80%, #fff 20%);
}
.mlm-delete {
  color: #ff6b6b;
  background: color-mix(in srgb, #ff6b6b 10%, transparent);
  border-color: color-mix(in srgb, #ff6b6b 30%, transparent);
}
.mlm-grid button:disabled {
  cursor: not-allowed;
  opacity: 0.7;
}

/* transition-group move animation */
.mlm-move {
  transition: transform 0.18s ease;
}
.mlm-enter-active,
.mlm-leave-active {
  transition: opacity 0.18s ease, transform 0.18s ease;
}
.mlm-enter-from,
.mlm-leave-to {
  opacity: 0.01;
  transform: scale(0.98);
}
</style>
