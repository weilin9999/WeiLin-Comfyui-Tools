<template>
  <div :class="`${prefix}lora-stack`"
    :style="[{ width: isOpen ? '300px' : '0' }, { paddingRight: isOpen ? '16px' : '0' }]">
    <div :class="`${prefix}lora-content`">
      <div :class="`${prefix}lora-header`">
        <h3 :class="`${prefix}lora-title`">{{ t('controls.loraStack') }}</h3>
        <div class="header-actions">
          <button :class="`${prefix}add-btn`" @click="openLoraManager" :title="t('controls.addLora')">
            <svg viewBox="0 0 24 24" width="16" height="16">
              <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
            </svg>
          </button>
          <button :class="`${prefix}close-btn`" @click="$emit('close')">
            <svg viewBox="0 0 24 24" width="16" height="16">
              <path
                d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
            </svg>
          </button>
        </div>
      </div>
      <div :class="`${prefix}lora-body`">
        <div :class="`${prefix}lora-list`">
          <div v-for="lora in selectedLoras" :key="lora.name" class="lora-item">
            <div class="lora-info">
              <div class="lora-header">
                <span class="lora-name" :title="lora.name">{{ lora.name }}</span>
                <div class="lora-actions">
                  <button class="look-on-btn" @click="lookOnLora(lora)" :title="t('controls.lookOnLora')">
                    <svg viewBox="0 0 1024 1024" width="14" height="14">
                      <path
                        d="M576.5 930.2H163.1c-52.9 0-96-43.1-96-96v-672c0-52.9 43.1-96 96-96h672c52.9 0 96 43.1 96 96V577c0 17.7-14.3 32-32 32s-32-14.3-32-32V162.2c0-17.6-14.4-32-32-32h-672c-17.6 0-32 14.4-32 32v672c0 17.6 14.4 32 32 32h413.4c17.7 0 32 14.3 32 32s-14.3 32-32 32z"
                        p-id="3466"></path>
                      <path
                        d="M692.4 322.3H245.7c-17.7 0-32-14.3-32-32s14.3-32 32-32h446.7c17.7 0 32 14.3 32 32s-14.3 32-32 32zM388.5 530.2H245.7c-17.7 0-32-14.3-32-32s14.3-32 32-32h142.7c17.7 0 32 14.3 32 32 0.1 17.6-14.3 32-31.9 32zM388.5 738H245.7c-17.7 0-32-14.3-32-32s14.3-32 32-32h142.7c17.7 0 32 14.3 32 32 0.1 17.7-14.3 32-31.9 32z"
                        p-id="3467"></path>
                      <path
                        d="M624.1 792.5c-94.8 0-172-77.2-172-172s77.2-172 172-172 172 77.2 172 172-77.1 172-172 172z m0-280c-59.6 0-108 48.4-108 108s48.4 108 108 108 108-48.4 108-108-48.4-108-108-108z"
                        p-id="3468"></path>
                      <path
                        d="M820.8 864.2L710.5 753.9c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L866 818.9c12.5 12.5 12.5 32.8 0 45.3s-32.7 12.5-45.2 0z"
                        p-id="3469"></path>
                    </svg>
                  </button>
                  <button class="remove-btn" @click="removeLora(lora)" :title="t('controls.removeLora')">
                    <svg viewBox="0 0 24 24" width="14" height="14">
                      <path
                        d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
                    </svg>
                  </button>
                </div>
              </div>
              <div class="lora-weights">
                <div class="weight-item">
                  <label>{{ t('loraManager.modelWeight') }}</label>
                  <input type="number" v-model="lora.weight" class="lora-weight" min="0" max="2" step="0.1" />
                </div>
                <div class="weight-item">
                  <label>{{ t('loraManager.textEncoderWeight') }}</label>
                  <input type="number" v-model="lora.text_encoder_weight" class="lora-weight" min="0" max="2"
                    step="0.1" />
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <loraDetail ref="loraDetailLoraStackRef"/>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
import loraDetail from '@/view/lora_manager/lora_detail.vue'

const prefix = "weilin_prompt_ui_"
const { t } = useI18n()

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  selectedLoras: {
    type: Array,
    default: []
  }
})

const emit = defineEmits(['close', 'update:selectedLoras'])

// 打开Lora管理器
const openLoraManager = () => {
  window.postMessage({ type: 'weilin_prompt_ui_openLoraManager_addLora' }, '*')
}

// 添加Lora
const addLora = (lora) => {
  // 检查是否已存在
  if (!props.selectedLoras.find(item => item.name === lora.name)) {
    props.selectedLoras.push({
      name: lora.name,
      weight: 1,
      text_encoder_weight: 1,
      ...lora
    })
    emit('update:selectedLoras', props.selectedLoras)
  }
}

// 移除Lora
const removeLora = (lora) => {
  const index = props.selectedLoras.findIndex(item => item.name === lora.name)
  if (index > -1) {
    props.selectedLoras.splice(index, 1)
    emit('update:selectedLoras', props.selectedLoras)
  }
}


const loraDetailLoraStackRef  = ref()

const lookOnLora = (loraData) => {
  // console.log('lookOnLora', loraData)
  loraDetailLoraStackRef.value.open({name: loraData.lora})
}

// 监听来自Lora管理器的消息
window.addEventListener('message', (event) => {
  if (event.data.type === 'weilin_prompt_ui_selectLora') {
    addLora(event.data.lora)
  }
})

defineExpose({
  addLora,
  removeLora
})
</script>

<style scoped>
.weilin_prompt_ui_lora-stack {
  top: 0;
  left: 0;
  height: 100%;
  background: var(--weilin-prompt-ui-primary-bg);
  transition: width 0.3s ease;
  overflow: hidden;
  box-sizing: border-box;
}

.weilin_prompt_ui_lora-content {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  margin-left: 0;
}

.weilin_prompt_ui_lora-header {
  padding: 8px 16px;
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: var(--weilin-prompt-ui-secondary-bg);
  border-top-right-radius: 8px;
  border-top-left-radius: 8px;
}

.weilin_prompt_ui_lora-header h3 {
  margin: 0;
  font-size: 16px;
  color: var(--weilin-prompt-ui-primary-text);
}

.weilin_prompt_ui_close-btn {
  border: none;
  background: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.weilin_prompt_ui_close-btn:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_close-btn svg {
  fill: var(--weilin-prompt-ui-secondary-text);
}

.weilin_prompt_ui_lora-body {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
}

.weilin_prompt_ui_lora-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.weilin_prompt_ui_lora-title {
  margin: 0;
  font-size: 16px;
  color: var(--weilin-prompt-ui-primary-text);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.header-actions {
  display: flex;
  gap: 8px;
  align-items: center;
}

.weilin_prompt_ui_add-btn {
  border: none;
  background: none;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.weilin_prompt_ui_add-btn:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.weilin_prompt_ui_add-btn svg {
  fill: var(--weilin-prompt-ui-secondary-text);
}

.lora-item {
  background: var(--weilin-prompt-ui-secondary-bg);
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 8px;
  margin-bottom: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
}

.lora-item:hover {
  border-color: var(--weilin-prompt-ui-primary-color);
  box-shadow: 0 2px 8px var(--weilin-prompt-ui-shadow-color);
}

.lora-info {
  display: flex;
  flex-direction: column;
  width: 100%;
}

.lora-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 12px;
  background: var(--weilin-prompt-ui-primary-bg);
  border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.lora-name {
  font-size: 14px;
  font-weight: 500;
  color: var(--weilin-prompt-ui-primary-text);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  max-width: 200px;
}

.lora-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.lora-weights {
  padding: 12px;
  background: var(--weilin-prompt-ui-secondary-bg);
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.weight-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.weight-item label {
  font-size: 12px;
  color: var(--weilin-prompt-ui-secondary-text);
  min-width: 60px;
}

.lora-weight {
  flex: 1;
  width: 100%;
  padding: 6px 8px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-primary-text);
  font-size: 13px;
  transition: all 0.3s ease;
}

.lora-weight:hover {
  border-color: var(--weilin-prompt-ui-primary-color);
}

.lora-weight:focus {
  border-color: var(--weilin-prompt-ui-primary-color);
  outline: none;
  box-shadow: 0 0 0 2px var(--weilin-prompt-ui-primary-color-fade);
}

.remove-btn,
.look-on-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4px;
  border: none;
  background: transparent;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
}

.remove-btn:hover,
.look-on-btn:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.remove-btn svg,
.look-on-btn svg {
  fill: var(--weilin-prompt-ui-secondary-text);
}

.remove-btn:hover svg {
  fill: var(--weilin-prompt-ui-danger-color);
}

.look-on-btn:hover svg {
  fill: var(--weilin-prompt-ui-primary-color);
}

</style>
