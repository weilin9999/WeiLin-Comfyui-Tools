<template>
    <DraggableWindow v-if="isOpen" :title="t('utils.tranToWeb')" :position="windows.tranToWeb.position"
        :size="windows.tranToWeb.size" :z-index="windowManager.getZIndex('tranToWeb')"
        @update:position="updatePosition('tranToWeb', $event)" @update:size="updateSize('tranToWeb', $event)"
        @active="windowManager.setActiveWindow('tranToWeb')" @close="closeWindow('tranToWeb')">
        <template #default>
            <div class="utils_tran_web__content" 
                 @dragover.prevent="handleDragOver"
                 @drop.prevent="handleDrop"
                 @paste="handlePaste">
                <div v-if="!htmlContent" class="drop-zone">
                    {{ t('utils.dropOrPasteImage') }}
                </div>
                <div v-else class="preview-container">
                    <iframe :srcdoc="htmlContent" class="html-preview"></iframe>
                    <div class="action-buttons">
                        <button @click="downloadHtml">{{ t('utils.downloadHtml') }}</button>
                        <!-- <button @click="copyToClipboard">{{ t('utils.copyHtml') }}</button> -->
                        <button @click="clearContent">{{ t('utils.clear') }}</button>
                    </div>
                </div>
            </div>
        </template>
    </DraggableWindow>

</template>

<script setup>
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import DraggableWindow from '@/components/DraggableWindow.vue'
import { windowManager } from '@/utils/windowManager'
import message from "@/utils/message";

const emit = defineEmits(['close', 'update'])
const { t } = useI18n()
const isOpen = ref(false)
const htmlContent = ref('')
const imageData = ref(null)

const STORAGE_PREFIX = 'weilin_tools_'

// 默认窗口配置
const DEFAULT_WINDOWS = {
    tranToWeb: {
        visible: false,
        position: { x: 150, y: 150 },
        size: { width: 800, height: 600 }
    }
}

// 从 localStorage 获取窗口状态
const getInitialWindowState = () => {
    try {
        const savedState = localStorage.getItem(`${STORAGE_PREFIX}tranToWebState`)
        if (savedState) {
            const parsedState = JSON.parse(savedState)

            // 检查并补充缺失的窗口配置
            const mergedState = { ...DEFAULT_WINDOWS }

            // 将保存的状态合并到默认配置中
            if (parsedState.tranToWeb) {
                mergedState.tranToWeb = {
                    ...DEFAULT_WINDOWS.tranToWeb,  // 默认值
                    ...parsedState.tranToWeb       // 保存的值
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
        localStorage.setItem(`${STORAGE_PREFIX}tranToWebState`, JSON.stringify(newState))
    } catch (error) {
        console.error('Error saving window states:', error)
    }
}, { deep: true })

// 组件挂载时注册窗口
onMounted(() => {
    windowManager.registerWindow('tranToWeb')
})

// 组件卸载时注销窗口
onUnmounted(() => {
    windowManager.unregisterWindow('tranToWeb')
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
const open = () => {
    isOpen.value = true
    windowManager.setActiveWindow('tranToWeb')
}



const handleDragOver = (e) => {
    e.dataTransfer.dropEffect = 'copy'
}

const handleDrop = (e) => {
    const file = e.dataTransfer.files[0]
    if (file && file.type.startsWith('image/')) {
        processImageFile(file)
    }
}

const handlePaste = (e) => {
    const items = e.clipboardData.items
    for (let i = 0; i < items.length; i++) {
        if (items[i].type.startsWith('image/')) {
            const blob = items[i].getAsFile()
            processImageFile(blob)
            break
        }
    }
}

const processImageFile = (file) => {
    const reader = new FileReader()
    reader.onload = (e) => {
        // 获取原始图片数据
        const originalData = e.target.result
        // 进行简单加密（使用Base64编码后再次编码）
        const encryptedData = btoa(originalData)
        imageData.value = encryptedData
        generateHtml()
    }
    reader.readAsDataURL(file)
}

const generateHtml = () => {
    htmlContent.value = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>WeiLin Comfyui Tools - Image to HTML</title>
            <style>
                body { margin: 0; padding: 0; }
                img { max-width: 100%; height: auto; }
            </style>
            <script>
                window.onload = function() {
                    // 解密图片数据
                    try {
                        const encryptedData = "${imageData.value}";
                        const originalData = atob(encryptedData);
                        document.getElementById('decrypted-img').src = originalData;
                        document.getElementById('decrypted-img').style.display = 'block';
                    } catch(e) {
                        console.error('解密失败:', e);
                        document.body.innerHTML = '<p>图片解密失败</p>';
                    }
                };
            <\/script>
        </head>
        <body>
            <img id="decrypted-img" style="display:none;" />
        </body>
        </html>
    `
}

const downloadHtml = () => {
    const blob = new Blob([htmlContent.value], { type: 'text/html' })
    const url = URL.createObjectURL(blob)
    const a = document.createElement('a')
    a.href = url
    a.download = 'image-to-html.html'
    document.body.appendChild(a)
    a.click()
    document.body.removeChild(a)
    URL.revokeObjectURL(url)
}

const copyToClipboard = async () => {
    try {
        const blob = new Blob([htmlContent.value], { type: 'text/html' });
        const clipboardItem = new ClipboardItem({ 'text/html': blob });
        await navigator.clipboard.write([clipboardItem]);
        message({ type: "warn", str: 'utils.copySuccess' });
    } catch (err) {
        console.error('Failed to copy file:', err);
        // 回退到文本复制方式
        try {
            await navigator.clipboard.writeText(htmlContent.value);
            message({ type: "success", str: 'utils.copySuccess' });
        } catch (textErr) {
            console.error('Failed to copy text:', textErr);
            message({ type: "warn", str: 'utils.copyFailed' });
        }
    }
}

// 在script部分添加clearContent方法
const clearContent = () => {
    htmlContent.value = ''
    imageData.value = null
}



defineExpose({
    open
})
</script>

<style scoped>

.utils_tran_web__content {
    height: 100%;
    padding: 20px;
    overflow-y: auto;
    color: var(--weilin-prompt-ui-primary-text);
}


.drop-zone {
    width: 100%;
    height: 300px;
    border: 2px dashed #ccc;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #666;
    font-size: 1.2em;
}

.preview-container {
    display: flex;
    flex-direction: column;
    height: 100%;
}

.html-preview {
    flex: 1;
    width: 100%;
    border: 1px solid #ccc;
    margin-bottom: 10px;
}

.action-buttons {
    display: flex;
    gap: 10px;
}

.action-buttons button {
    padding: 8px 16px;
    background-color: var(--weilin-prompt-ui-primary);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.action-buttons button:hover {
    background-color: var(--weilin-prompt-ui-primary-hover);
}

</style>