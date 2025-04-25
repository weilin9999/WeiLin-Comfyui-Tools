<template>
  <Teleport to="#weilin_comfyui_tools_prompt_ui_div">
    <div class="weilin_prompt_ui_draggable-window" :style="{
      left: `${currentPosition.x}px`,
      top: `${currentPosition.y}px`,
      width: `${currentSize.width}px`,
      height: `${currentSize.height}px`,
      zIndex: zIndex
    }" @mousedown="setActive">
      <!-- 窗口标题栏 -->
      <div class="weilin_prompt_ui_window-header" @mousedown.stop="handleHeaderMouseDown">
        <div class="weilin_prompt_ui_window-title">{{ title }}</div>
        <button class="weilin_prompt_ui_close-btn" @click="close">×</button>
      </div>

      <!-- 内容区域 -->
      <div class="weilin_prompt_ui_window-content" @scroll="handleScroll">
        <slot></slot>
      </div>

      <!-- 调整大小的手柄 -->
      <div class="weilin_prompt_ui_resize-handle" :title="t('common.windowSize')" @mousedown.stop="startResize"></div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  position: {
    type: Object,
    required: true
  },
  size: {
    type: Object,
    required: true
  },
  zIndex: {
    type: Number,
    default: 1
  },
  name: {
    type: String,
    default: "default_window_name"
  }
})

const { t } = useI18n()

const emit = defineEmits(['update:position', 'update:size', 'active', 'close'])

// 当前位置和大小状态
const currentPosition = ref({ x: 0, y: 0 })
const currentSize = ref({ width: 600, height: 400 })

// 监听 props 中的 position 变化
watch(() => props.position, (newPosition) => {
  if (newPosition) {
    currentPosition.value = { ...newPosition }
    window.parent.postMessage({ type: `weilin_prompt_ui_window_change_${props.name}_position` }, '*')
  }
}, { immediate: true, deep: true })

// 监听 props 中的 size 变化
watch(() => props.size, (newSize) => {
  if (newSize) {
    currentSize.value = { ...newSize }
    window.parent.postMessage({ type: `weilin_prompt_ui_window_change_${props.name}_size` }, '*')
  }
}, { immediate: true, deep: true })

const handleScroll = () => {
  window.parent.postMessage({ type: `weilin_prompt_ui_window_change_${props.name}_scroll` }, '*')
}

// 在组件挂载时初始化位置和大小
onMounted(() => {
   // 设置初始位置
   if (props.position) {
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    // 边界检测
    let x = props.position.x;
    let y = props.position.y;
    
    // 确保左侧不超出边界
    x = Math.max(50, x);
    // 确保右侧不超出边界
    x = Math.min(x, viewportWidth - (props.size?.width || currentSize.value.width));
    // 确保顶部不超出边界
    y = Math.max(50, y);
    // 确保底部不超出边界
    y = Math.min(y, viewportHeight - (props.size?.height || currentSize.value.height));
    
    currentPosition.value = { x, y };
  }
  
  // 设置初始大小
  if (props.size) {
    currentSize.value = { ...props.size };
  }
})

// 拖动相关状态和方法
const isDragging = ref(false)
const dragOffset = ref({ x: 0, y: 0 })

const startDrag = (event) => {
  isDragging.value = true
  dragOffset.value = {
    x: event.clientX - currentPosition.value.x,
    y: event.clientY - currentPosition.value.y
  }
  document.addEventListener('mousemove', handleDrag)
  document.addEventListener('mouseup', stopDrag)
}

const handleDrag = (event) => {
  if (isDragging.value) {
    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    
    let newX = event.clientX - dragOffset.value.x;
    let newY = event.clientY - dragOffset.value.y;
    
    // 确保左侧不超出边界
    newX = Math.max(50, newX);
    // 确保右侧不超出边界
    newX = Math.min(newX, viewportWidth - currentSize.value.width);
    // 确保顶部不超出边界
    newY = Math.max(50, newY);
    // 确保底部不超出边界
    newY = Math.min(newY, viewportHeight - currentSize.value.height);
    
    const newPosition = {
      x: newX,
      y: newY
    };
    
    currentPosition.value = newPosition;
    emit('update:position', newPosition);
  }
}

const stopDrag = () => {
  isDragging.value = false
  document.removeEventListener('mousemove', handleDrag)
  document.removeEventListener('mouseup', stopDrag)
}

// 调整大小相关状态和方法
const isResizing = ref(false)
const resizeStartPos = ref({ x: 0, y: 0 })
const resizeStartSize = ref({ width: 0, height: 0 })

const startResize = (event) => {
  isResizing.value = true
  resizeStartPos.value = { x: event.clientX, y: event.clientY }
  resizeStartSize.value = { ...currentSize.value }
  document.addEventListener('mousemove', handleResize)
  document.addEventListener('mouseup', stopResize)
}

const handleResize = (event) => {
  if (isResizing.value) {
    const deltaX = event.clientX - resizeStartPos.value.x
    const deltaY = event.clientY - resizeStartPos.value.y
    const newSize = {
      width: Math.max(200, resizeStartSize.value.width + deltaX),
      height: Math.max(200, resizeStartSize.value.height + deltaY)
    }
    currentSize.value = newSize
    emit('update:size', newSize)
  }
}

const stopResize = () => {
  isResizing.value = false
  document.removeEventListener('mousemove', handleResize)
  document.removeEventListener('mouseup', stopResize)
}

const setActive = () => {
  emit('active')
}

const close = () => {
  emit('close')
}

// 处理标题栏点击
const handleHeaderMouseDown = (event) => {
  // 先设置为活动窗口
  setActive()
  // 然后开始拖动
  startDrag(event)
}
</script>

<style scoped>
.weilin_prompt_ui_draggable-window {
  position: absolute;
  background: var(--weilin-prompt-ui-primary-bg);
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  z-index: calc(100 * 100 * 100 * 90);
}

.weilin_prompt_ui_window-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--weilin-prompt-ui-secondary-bg);
  cursor: move;
  user-select: none;
}

.weilin_prompt_ui_window-title {
  font-size: 14px;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
  margin-right: 8px;
  color: var(--weilin-prompt-ui-primary-text);
}

.weilin_prompt_ui_close-btn {
  border: none;
  background: none;
  font-size: 20px;
  cursor: pointer;
  padding: 0 4px;
  color: var(--weilin-prompt-ui-secondary-text);
}

.weilin_prompt_ui_close-btn:hover {
  color: #ff4d4f;
}

.weilin_prompt_ui_window-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px;
  background: var(--weilin-prompt-ui-primary-bg);
}

.weilin_prompt_ui_resize-handle {
  position: absolute;
  right: 0;
  bottom: 0;
  width: 16px;
  height: 16px;
  cursor: se-resize;
  user-select: none;
}

.weilin_prompt_ui_resize-handle::after {
  content: '';
  position: absolute;
  right: 7px;
  bottom: 4px;
  width: 8px;
  height: 8px;
  border-right: 2px solid #999;
  border-bottom: 2px solid #999;
}

.weilin_prompt_ui_window-content::-webkit-scrollbar {
  width: 6px;
}

.weilin_prompt_ui_window-content::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.weilin_prompt_ui_window-content::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 3px;
}

.weilin_prompt_ui_window-content::-webkit-scrollbar-thumb:hover {
  background: #555;
}
</style>