<template>
  <Teleport to="#weilin_comfyui_tools_prompt_ui_div">
    <Transition :name="`${prefix}dialog-fade`">
      <div v-if="modelValue" :class="`${prefix}dialog-overlay`"  @click="handleOverlayClick">
        <Transition :name="`${prefix}dialog-slide`">
          <div :style="{ 'width': width  }" :class="`${prefix}dialog`" @click.stop>
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
  },
  width: {
    type: String,
    default: '60%'
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
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.18);
  backdrop-filter: blur(2px);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.weilin_prompt_ui_dialog {
  background: var(--weilin-prompt-ui-primary-bg);
  border-radius: 20px;
  box-shadow: 0 8px 32px var(--weilin-prompt-ui-shadow-color);
  margin: 0;
  position: relative;
  overflow: hidden;
  border: none;
  display: flex;
  flex-direction: column;
  min-width: 400px;
  width: 70%;
  max-width: 70%;
  min-height: 200px;
  max-height: 75vh;
}

.weilin_prompt_ui_dialog-header {
  padding: 20px 28px 12px 28px;
  border-bottom: none;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: transparent;
}

.weilin_prompt_ui_dialog-title {
  margin: 0;
  font-size: 18px;
  color: var(--weilin-prompt-ui-title-color);
  font-weight: 700;
  letter-spacing: 0.01em;
}

.weilin_prompt_ui_dialog-close {
  border: none;
  background: none;
  cursor: pointer;
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s;
  padding: 0;
}

.weilin_prompt_ui_dialog-close:hover {
  background: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_dialog-close svg {
  fill: var(--weilin-prompt-ui-secondary-text);
  transition: fill 0.2s;
}

.weilin_prompt_ui_dialog-close:hover svg {
  fill: var(--weilin-prompt-ui-danger-color);
}

.weilin_prompt_ui_dialog-content {
  padding: 0 28px 20px 28px;
  color: var(--weilin-prompt-ui-primary-text);
  overflow-y: auto;
  flex: 1;
  line-height: 1.7;
  font-size: 15px;
  max-height: calc(75vh - 120px);
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
  transition: background 0.2s;
}

.weilin_prompt_ui_dialog-content::-webkit-scrollbar-thumb:hover {
  background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

.weilin_prompt_ui_dialog-footer {
  padding: 16px 28px;
  border-top: none;
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background: transparent;
  margin-top: auto;
}

.weilin_prompt_ui_dialog-fade-enter-active,
.weilin_prompt_ui_dialog-fade-leave-active {
  transition: opacity 0.25s;
}
.weilin_prompt_ui_dialog-fade-enter-from,
.weilin_prompt_ui_dialog-fade-leave-to {
  opacity: 0;
}

.weilin_prompt_ui_dialog-slide-enter-active {
  transition: all 0.25s cubic-bezier(.4,0,.2,1);
}
.weilin_prompt_ui_dialog-slide-leave-active {
  transition: all 0.18s cubic-bezier(.4,0,.2,1);
}
.weilin_prompt_ui_dialog-slide-enter-from {
  opacity: 0;
  transform: translateY(-16px) scale(0.98);
}
.weilin_prompt_ui_dialog-slide-leave-to {
  opacity: 0;
  transform: translateY(16px) scale(0.98);
}

/* 按钮样式简约化 */
.weilin_prompt_ui_dialog-footer :slotted(button) {
  padding: 8px 22px;
  border-radius: 10px;
  border: none;
  background: var(--weilin-prompt-ui-btn-gradient);
  color: #fff;
  cursor: pointer;
  font-size: 15px;
  font-weight: 500;
  box-shadow: var(--weilin-prompt-ui-btn-shadow);
  transition: background 0.2s;
}

.weilin_prompt_ui_dialog-footer :slotted(button:hover) {
  background: var(--weilin-prompt-ui-btn-gradient-hover);
}

.weilin_prompt_ui_dialog-footer :slotted(button:last-child) {
  background: var(--weilin-prompt-ui-btn-gradient);
  color: #fff;
}

.weilin_prompt_ui_dialog-footer :slotted(button:last-child:hover) {
  background: var(--weilin-prompt-ui-btn-gradient-hover);
  color: #fff;
}
</style>