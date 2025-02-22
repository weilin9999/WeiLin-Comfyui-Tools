<template>
  <Teleport to="#weilin_comfyui_tools_prompt_ui_div">
    <Transition :name="`${prefix}dialog-fade`">
      <div v-if="modelValue" :class="`${prefix}dialog-overlay`"  @click="handleOverlayClick">
        <Transition :name="`${prefix}dialog-slide`">
          <div :class="`${prefix}dialog`" @click.stop>
            <div :class="`${prefix}dialog-header`">
              <h3 :class="`${prefix}dialog-title`">{{ title }}</h3>
              <button :class="`${prefix}dialog-close`" @click="close">
                <svg viewBox="0 0 24 24" width="16" height="16">
                  <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>
                </svg>
              </button>
            </div>
            <div :class="`${prefix}dialog-content`">
              <slot></slot>
            </div>
            <div :class="`${prefix}dialog-footer`" v-if="$slots.footer">
              <slot name="footer"></slot>
            </div>
          </div>
        </Transition>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
const prefix = "weilin_prompt_ui_"

const props = defineProps({
  modelValue: Boolean,
  title: {
    type: String,
    default: '标题'
  },
  closeOnClickOverlay: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue'])

const close = () => {
  emit('update:modelValue', false)
}

const handleOverlayClick = () => {
  if (props.closeOnClickOverlay) {
    close()
  }
}
</script>

<style scoped>
.weilin_prompt_ui_dialog-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.weilin_prompt_ui_dialog {
  background: var(--weilin-prompt-ui-primary-bg);
  border-radius: 12px;
  box-shadow: 0 4px 24px var(--weilin-prompt-ui-shadow-color);
  min-width: 320px;
  max-width: 90vw;
  max-height: 90vh;
  width: fit-content;
  margin: 20px;
  position: relative;
  overflow: hidden;
  border: 1px solid var(--weilin-prompt-ui-border-color);
}

.weilin_prompt_ui_dialog-header {
  padding: 16px 20px;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--weilin-prompt-ui-secondary-bg);
}

.weilin_prompt_ui_dialog-title {
  margin: 0;
  font-size: 16px;
  color: var(--weilin-prompt-ui-primary-text);
  font-weight: 600;
  letter-spacing: 0.01em;
}

.weilin_prompt_ui_dialog-close {
  border: none;
  background: none;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  padding: 0;
}

.weilin_prompt_ui_dialog-close:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_dialog-close svg {
  fill: var(--weilin-prompt-ui-secondary-text);
  transition: fill 0.2s ease;
}

.weilin_prompt_ui_dialog-close:hover svg {
  fill: #ff4d4f;
}

.weilin_prompt_ui_dialog-content {
  padding: 20px;
  color: var(--weilin-prompt-ui-primary-text);
  overflow-y: auto;
  max-height: calc(90vh - 140px);
  line-height: 1.6;
}

.weilin_prompt_ui_dialog-content::-webkit-scrollbar {
  width: 6px;
}

.weilin_prompt_ui_dialog-content::-webkit-scrollbar-track {
  background: var(--weilin-prompt-ui-scrollbar-track);
  border-radius: 3px;
}

.weilin_prompt_ui_dialog-content::-webkit-scrollbar-thumb {
  background: var(--weilin-prompt-ui-scrollbar-thumb);
  border-radius: 3px;
  transition: background 0.2s ease;
}

.weilin_prompt_ui_dialog-content::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

.weilin_prompt_ui_dialog-footer {
  padding: 16px 20px;
  border-top: 1px solid var(--weilin-prompt-ui-border-color);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: var(--weilin-prompt-ui-secondary-bg);
}

/* 遮罩层动画 */
.weilin_prompt_ui_dialog-fade-enter-active,
.weilin_prompt_ui_dialog-fade-leave-active {
  transition: opacity 0.3s ease;
}

.weilin_prompt_ui_dialog-fade-enter-from,
.weilin_prompt_ui_dialog-fade-leave-to {
  opacity: 0;
}

/* 对话框动画 */
.weilin_prompt_ui_dialog-slide-enter-active {
  transition: all 0.3s ease-out;
}

.weilin_prompt_ui_dialog-slide-leave-active {
  transition: all 0.2s ease-in;
}

.weilin_prompt_ui_dialog-slide-enter-from {
  opacity: 0;
  transform: translateY(-20px);
}

.weilin_prompt_ui_dialog-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}

/* 按钮样式 */
.weilin_prompt_ui_dialog-footer :slotted(button) {
  padding: 8px 16px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  background: var(--weilin-prompt-ui-primary-bg);
  color: var(--weilin-prompt-ui-primary-text);
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s ease;
}

.weilin_prompt_ui_dialog-footer :slotted(button:hover) {
  border-color: #40a9ff;
  color: #40a9ff;
}

.weilin_prompt_ui_dialog-footer :slotted(button:last-child) {
  background: #1890ff;
  color: white;
  border-color: #1890ff;
}

.weilin_prompt_ui_dialog-footer :slotted(button:last-child:hover) {
  background: #40a9ff;
  border-color: #40a9ff;
  color: white;
}
</style> 