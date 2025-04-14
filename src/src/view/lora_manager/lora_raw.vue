<template>
    <DraggableWindow v-if="isOpen" :title="t('lora.rawTitle')" :position="windows.loraRaw.position"
        :size="windows.loraRaw.size" :z-index="windowManager.getZIndex('loraRaw')"
        @update:position="updatePosition('loraRaw', $event)" @update:size="updateSize('loraRaw', $event)"
        @active="windowManager.setActiveWindow('loraRaw')" @close="closeWindow('loraRaw')">
        <template #default>
            <div class="lora-raw__content">
                <JsonViewer :value="loraInfo" copyable sort theme="dark" />
            </div>
        </template>
    </DraggableWindow>

</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import DraggableWindow from '@/components/DraggableWindow.vue'
import { windowManager } from '@/utils/windowManager'

import { JsonViewer } from "vue3-json-viewer"

const { t } = useI18n()
const loraInfo = ref({})
const isOpen = ref(false)

const STORAGE_PREFIX = 'weilin_tools_'

// 默认窗口配置
const DEFAULT_WINDOWS = {
    loraRaw: {
        visible: false,
        position: { x: 150, y: 150 },
        size: { width: 800, height: 600 }
    }
}

// 从 localStorage 获取窗口状态
const getInitialWindowState = () => {
    try {
        const savedState = localStorage.getItem(`${STORAGE_PREFIX}loraRawState`)
        if (savedState) {
            const parsedState = JSON.parse(savedState)

            // 检查并补充缺失的窗口配置
            const mergedState = { ...DEFAULT_WINDOWS }

            // 将保存的状态合并到默认配置中
            if (parsedState.loraRaw) {
                mergedState.loraRaw = {
                    ...DEFAULT_WINDOWS.loraRaw,  // 默认值
                    ...parsedState.loraRaw       // 保存的值
                }
            }

            return mergedState
        }
    } catch (error) {
        console.error('Error loading window states:', error)
    }

    return { ...DEFAULT_WINDOWS }
}

// 窗口状态管理
const windows = ref(getInitialWindowState())

// 监听窗口状态变化并保存
watch(windows, (newState) => {
    try {
        localStorage.setItem(`${STORAGE_PREFIX}loraRawState`, JSON.stringify(newState))
    } catch (error) {
        console.error('Error saving window states:', error)
    }
}, { deep: true })

// 组件挂载时注册窗口
onMounted(() => {
    windowManager.registerWindow('loraRaw')
})

// 组件卸载时注销窗口
onUnmounted(() => {
    windowManager.unregisterWindow('loraRaw')
})

// 关闭窗口
const closeWindow = (windowName) => {
    isOpen.value = false
}

// 更新窗口位置
const updatePosition = (windowName, newPosition) => {
    if (windows.value[windowName]) {
        windows.value[windowName].position = { ...newPosition }
    }
}

// 更新窗口大小
const updateSize = (windowName, newSize) => {
    if (windows.value[windowName]) {
        windows.value[windowName].size = { ...newSize }
    }
}

// 打开窗口
const open = (loraRawData) => {
    isOpen.value = true
    windowManager.setActiveWindow('loraRaw')
    loraInfo.value = loraRawData
}

defineExpose({
    open
})

const emit = defineEmits(['close', 'update'])
</script>

<style scoped>

.lora-raw__content {
    height: 100%;
    padding: 20px;
    overflow-y: auto;
    color: var(--weilin-prompt-ui-primary-text);
}

</style>