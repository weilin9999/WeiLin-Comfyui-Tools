<template>
  <Teleport to="#weilin_comfyui_tools_prompt_ui_div">
    <div
      ref="windowRef"
      class="weilin_prompt_ui_draggable-window"
      :style="{
        left: `${currentPosition.x}px`,
        top: `${currentPosition.y}px`,
        width: `${currentSize.width}px`,
        height: `${currentSize.height}px`,
        zIndex: zIndex
      }"
      @mousedown="setActive"
    >
      <!-- 窗口标题栏 -->
      <div class="weilin_prompt_ui_window-header" @mousedown.stop="handleHeaderMouseDown">
        <div class="weilin_prompt_ui_window-title">
          {{ title }}
        </div>
        <button class="weilin_prompt_ui_close-btn" @click="close">×</button>
      </div>

      <!-- 内容区域 -->
      <div class="weilin_prompt_ui_window-content" @scroll="handleScroll">
        <slot></slot>
      </div>

      <!-- 调整大小的手柄（四角） -->
      <div
        class="weilin_prompt_ui_resize-handle weilin_prompt_ui_resize-handle-nw"
        :title="t('common.windowSize')"
      ></div>
      <div
        class="weilin_prompt_ui_resize-handle weilin_prompt_ui_resize-handle-ne"
        :title="t('common.windowSize')"
      ></div>
      <div
        class="weilin_prompt_ui_resize-handle weilin_prompt_ui_resize-handle-sw"
        :title="t('common.windowSize')"
      ></div>
      <div
        class="weilin_prompt_ui_resize-handle weilin_prompt_ui_resize-handle-se"
        :title="t('common.windowSize')"
      ></div>
    </div>
  </Teleport>
</template>

<script setup>
  import { ref, onMounted, onUnmounted, watch } from 'vue'
  import interact from 'interactjs'
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
      default: 'default_window_name'
    }
  })

  const { t } = useI18n()

  const emit = defineEmits(['update:position', 'update:size', 'active', 'close'])
  const windowRef = ref(null)
  let interactable = null
  let activeInteraction = null

  // 当前位置和大小状态
  const currentPosition = ref({ x: 0, y: 0 })
  const currentSize = ref({ width: 600, height: 400 })

  // 监听 props 中的 position 变化 - 优化：移除频繁的postMessage
  watch(
    () => props.position,
    (newPosition) => {
      if (newPosition) {
        currentPosition.value = { ...newPosition }
      }
    },
    { immediate: true, deep: true }
  )

  // 监听 props 中的 size 变化 - 优化：移除频繁的postMessage
  watch(
    () => props.size,
    (newSize) => {
      if (newSize) {
        currentSize.value = { ...newSize }
      }
    },
    { immediate: true, deep: true }
  )

  // 优化：使用节流函数限制滚动事件频率
  let scrollThrottleTimer = null
  const handleScroll = () => {
    if (scrollThrottleTimer) {
      return
    }
    scrollThrottleTimer = setTimeout(() => {
      window.parent.postMessage(
        { type: `weilin_prompt_ui_window_change_${props.name}_scroll` },
        '*'
      )
      scrollThrottleTimer = null
    }, 100)
  }

  const clampPosition = (x, y, width = currentSize.value.width) => {
    const viewportWidth = window.innerWidth
    const viewportHeight = window.innerHeight
    const minLeftSpace = 100
    return {
      x: Math.min(Math.max(minLeftSpace - width, x), viewportWidth - 100),
      y: Math.min(Math.max(100, y), viewportHeight - 100)
    }
  }

  const forceStopInteraction = () => {
    if (!activeInteraction) {
      return
    }
    activeInteraction.stop()
    activeInteraction = null
  }

  const isPointerReleased = (event) => {
    const buttons = event?.buttons ?? event?.originalEvent?.buttons
    return buttons === 0
  }

  const ensurePointerPressed = (event) => {
    if (!isPointerReleased(event)) {
      return false
    }
    forceStopInteraction()
    return true
  }

  const handleWindowBlur = () => {
    forceStopInteraction()
  }

  const initInteract = () => {
    if (!windowRef.value) return

    interactable = interact(windowRef.value)
      .draggable({
        allowFrom: '.weilin_prompt_ui_window-header',
        ignoreFrom: '.weilin_prompt_ui_close-btn,.weilin_prompt_ui_resize-handle',
        listeners: {
          start(event) {
            activeInteraction = event.interaction
          },
          move(event) {
            if (ensurePointerPressed(event)) {
              return
            }
            const next = clampPosition(
              currentPosition.value.x + event.dx,
              currentPosition.value.y + event.dy
            )
            currentPosition.value = next
            emit('update:position', next)
          },
          end() {
            activeInteraction = null
          }
        }
      })
      .resizable({
        edges: {
          top: '.weilin_prompt_ui_resize-handle-nw, .weilin_prompt_ui_resize-handle-ne',
          right: '.weilin_prompt_ui_resize-handle-ne, .weilin_prompt_ui_resize-handle-se',
          bottom: '.weilin_prompt_ui_resize-handle-sw, .weilin_prompt_ui_resize-handle-se',
          left: '.weilin_prompt_ui_resize-handle-nw, .weilin_prompt_ui_resize-handle-sw'
        },
        modifiers: [
          interact.modifiers.restrictSize({
            min: { width: 200, height: 200 }
          })
        ],
        listeners: {
          start(event) {
            activeInteraction = event.interaction
          },
          move(event) {
            if (ensurePointerPressed(event)) {
              return
            }
            const nextSize = {
              width: event.rect.width,
              height: event.rect.height
            }
            const nextPosition = clampPosition(
              currentPosition.value.x + event.deltaRect.left,
              currentPosition.value.y + event.deltaRect.top,
              nextSize.width
            )

            currentPosition.value = nextPosition
            currentSize.value = nextSize
            emit('update:position', nextPosition)
            emit('update:size', nextSize)
          },
          end() {
            activeInteraction = null
          }
        }
      })
  }

  // 在组件挂载时初始化位置和大小
  onMounted(() => {
    if (props.position) {
      currentPosition.value = clampPosition(
        props.position.x,
        props.position.y,
        props.size?.width || currentSize.value.width
      )
    }

    if (props.size) {
      currentSize.value = { ...props.size }
    }

    initInteract()
    window.addEventListener('blur', handleWindowBlur)
    window.addEventListener('mouseup', forceStopInteraction)
    window.addEventListener('pointerup', forceStopInteraction)
  })

  // 组件卸载时清理定时器和交互绑定
  onUnmounted(() => {
    if (scrollThrottleTimer) {
      clearTimeout(scrollThrottleTimer)
      scrollThrottleTimer = null
    }
    window.removeEventListener('blur', handleWindowBlur)
    window.removeEventListener('mouseup', forceStopInteraction)
    window.removeEventListener('pointerup', forceStopInteraction)
    forceStopInteraction()
    if (interactable) {
      interactable.unset()
      interactable = null
    }
  })

  const setActive = () => {
    emit('active')
  }

  const close = () => {
    emit('close')
  }

  // 处理标题栏点击
  const handleHeaderMouseDown = () => {
    // 先设置为活动窗口，拖拽行为由 interact.js 处理
    setActive()
  }
</script>

<style scoped>
  .weilin_prompt_ui_draggable-window {
    position: absolute;
    background: var(--weilin-prompt-ui-primary-bg);
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 8px;
    box-shadow: 0 2px 12px 0 rgb(0 0 0 / 0.1);
    overflow: hidden;
    display: flex;
    flex-direction: column;
    z-index: 100;
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
    overflow: hidden auto;
    padding: 16px;
    background: var(--weilin-prompt-ui-primary-bg);
  }

  .weilin_prompt_ui_resize-handle {
    position: absolute;
    width: 14px;
    height: 14px;
    user-select: none;
    opacity: 0.75;
    transition: opacity 0.2s ease;
  }

  .weilin_prompt_ui_resize-handle:hover {
    opacity: 1;
  }

  .weilin_prompt_ui_resize-handle::after {
    content: '';
    position: absolute;
    inset: 2px;
  }

  .weilin_prompt_ui_resize-handle-se {
    right: 0;
    bottom: 0;
    cursor: se-resize;
  }

  .weilin_prompt_ui_resize-handle-se::after {
    border-right: 2px solid #999;
    border-bottom: 2px solid #999;
  }

  .weilin_prompt_ui_resize-handle-ne {
    right: 0;
    top: 0;
    cursor: ne-resize;
  }

  .weilin_prompt_ui_resize-handle-ne::after {
    border-right: 2px solid #999;
    border-top: 2px solid #999;
  }

  .weilin_prompt_ui_resize-handle-sw {
    left: 0;
    bottom: 0;
    cursor: sw-resize;
  }

  .weilin_prompt_ui_resize-handle-sw::after {
    border-left: 2px solid #999;
    border-bottom: 2px solid #999;
  }

  .weilin_prompt_ui_resize-handle-nw {
    left: 0;
    top: 0;
    cursor: nw-resize;
  }

  .weilin_prompt_ui_resize-handle-nw::after {
    border-left: 2px solid #999;
    border-top: 2px solid #999;
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
