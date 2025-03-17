<template>
    <div :class="`${prefix}lora-stack`">
        <div :class="`${prefix}lora-content`">
            <div :class="`${prefix}lora-body`">
                <div :class="`${prefix}lora-list`">
                    <div v-for="item in nodeLists" :key="item.id" class="lora-item">
                        <div class="lora-info">
                            <div class="lora-header">
                                <span class="lora-name" :title="item.title">#{{ item.id }} - {{ item.title }}</span>
                            </div>
                            <div class="lora-weights">
                                <div class="weight-item">
                                    <div class="text-label" :title="item.text">
                                        {{ item.text }}
                                    </div>
                                </div>
                                <div class="weight-item">
                                    <div class="center-box">
                                        <button @click="openPromptUI(item.seed)" class="open-button">{{ t('nodeListWindow.openPromptUI') }}</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { useI18n } from 'vue-i18n'

const prefix = "weilin_prompt_ui_"
const { t } = useI18n()

const nodeLists = ref([])

// 监听来自Lora管理器的消息
window.addEventListener('message', (event) => {
    if (event.data.type === 'weilin_prompt_ui_update_node_list_info') {
        nodeLists.value = event.data.nodeList
        // console.log(nodeLists.value)
    }
})

const openPromptUI = (seed) => {
    window.postMessage({ type: 'weilin_prompt_ui_prompt_open_node_wit_seed', seed: seed }, '*')
}

onMounted(() => {
    window.postMessage({ type: 'weilin_prompt_ui_prompt_get_node_list_info' }, '*')
})

</script>

<style scoped>
.weilin_prompt_ui_lora-stack {
    top: 0;
    left: 0;
    height: 100%;
    background: var(--weilin-prompt-ui-primary-bg);
    transition: width 0.3s ease;
    width: 100%;
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

.center-box {
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.text-label {
    color: var(--weilin-prompt-ui-primary-text);
    width: 100%;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
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

.open-button {
    width: fit-content;
    padding: 4px;
    background-color: var(--weilin-prompt-ui-primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.2s;
    font-size: 14px;
}

.open-button:hover {
    background-color: var(--weilin-prompt-ui-primary-color-hover);
}
</style>