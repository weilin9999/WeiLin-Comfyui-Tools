<template>
    <Dialog v-model="dialogVisible" :title="t('tagManager.addTag')">
        <div class="tag-manager">
            <div class="form-group">
                <label>{{ t('importDialog.selectGroup') }}</label>
                <div class="select-group-item">
                    <input type="text"
                        :value="currentTag.id_index != '' ? (selectedGroup.group.name + ' -> ' + selectedGroup.sub.name) : '请选择分组'"
                        readonly :placeholder="t('importDialog.selectGroup')">
                    <button class="add-tag-btn" style="margin-left: 10px;min-width: fit-content;"
                        @click="selectTagGroup">{{ t('importDialog.selectGroup')
                        }}</button>
                </div>
            </div>
            <div class="form-group">
                <label>{{ t('tagManager.text') }}</label>
                <input type="text" v-model="currentTag.desc" :placeholder="t('tagManager.textPlaceholder')">
            </div>
            <div class="form-group">
                <label>{{ t('tagManager.description') }}</label>
                <textarea v-model="currentTag.text" :placeholder="t('tagManager.descriptionPlaceholder')" rows="4">
            </textarea>
            </div>
            <div class="form-group">
                <label>{{ t('tagManager.backgroundColor') }}</label>
                <div class="color-picker">
                    <div class="color-preview" :style="{ backgroundColor: previewColor }">
                    </div>
                    <div class="color-controls">
                        <input type="color" v-model="colorPickerState.hex" @input="updateColor" class="color-input">
                        <div class="alpha-control">
                            <input type="range" v-model.number="colorPickerState.alpha" min="0" max="100"
                                @input="updateColor" class="alpha-slider">
                            <span class="alpha-value">{{ colorPickerState.alpha }}%</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <template #footer>
            <button @click="dialogVisible = false">{{ t('common.cancel') }}</button>
            <button @click="saveTag">{{ t('common.confirm') }}</button>
        </template>
    </Dialog>

    <TagGroupSelect ref="tagGroupSelectItem" @sureSelect="sureSelectThis" />
</template>

<script setup>
import Dialog from '@/components/Dialog.vue'
import { ref, onMounted, onBeforeUnmount, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { tagsApi } from '@/api/tags'
import message from '@/utils/message'
import TagGroupSelect from "../../tag_manager/tag_group_select.vue"

const { t } = useI18n()

const emit = defineEmits(['sureSelect'])
const tagGroupSelectItem = ref(null)
const dialogVisible = ref(false)

const currentTag = ref({
    text: '',
    desc: '',
    id_index: '',
    color: 'rgba(255, 123, 2, .4)'
})

const rgbaToColorPickerState = (rgba) => {
    const match = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/);
    if (match) {
        const [, r, g, b, a] = match;
        const hex = `#${((1 << 24) + (parseInt(r) << 16) + (parseInt(g) << 8) + parseInt(b)).toString(16).slice(1)}`;
        const alpha = a ? Math.round(parseFloat(a) * 100) : 100; // 将 alpha 转换为百分比
        return { hex, alpha };
    }
    return { hex: '#ff7b02', alpha: 40 }; // 默认值
};

const selectedGroup = ref({
    "group": {
        "id_index": 0,
        "name": "",
        "color": "",
        "create_time": 0,
        "p_uuid": "",
    },
    "sub": {
        "id_index": 0,
        "name": "",
        "color": "",
        "create_time": 0,
        "g_uuid": "",
        "p_uuid": ""
    }
})

// 颜色选择器状态
const colorPickerState = ref({
    hex: '#ff7b02',
    alpha: 40
})

// 预览颜色计算属性
const previewColor = computed(() => {
    return hexToRgba(colorPickerState.value.hex, colorPickerState.value.alpha)
})

// 更新颜色（统一处理分类和标签）
const updateColor = () => {
    const color = hexToRgba(colorPickerState.value.hex, colorPickerState.value.alpha)
    currentTag.value.color = color
}

// 改进的 RGBA 转换函数
const hexToRgba = (hex, alpha) => {
    const r = parseInt(hex.slice(1, 3), 16)
    const g = parseInt(hex.slice(3, 5), 16)
    const b = parseInt(hex.slice(5, 7), 16)
    return `rgba(${r}, ${g}, ${b}, ${alpha / 100})`
}

const selectTagGroup = () => {
    tagGroupSelectItem.value.open()
}

// 保存标签
const saveTag = () => {
    if (!currentTag.value.text || !currentTag.value.desc || !selectedGroup.value.sub.id_index || !selectedGroup.value.sub.g_uuid) {
        message({ type: "warn", str: 'tagManager.textRequired' });
        return
    }

    tagsApi
        .addNewTags({
            id_index: selectedGroup.value.sub.id_index,
            g_uuid: selectedGroup.value.sub.g_uuid,
            text: currentTag.value.text,
            desc: currentTag.value.desc,
            color: currentTag.value.color ? currentTag.value.color : 'rgba(255, 123, 2, .4)',
        })
        .then((res) => {
            window.postMessage({
                type: 'weilin_prompt_ui_refresh_all_data',
            }, '*')
            message({ type: "success", str: 'message.addSuccess' });
            closeTagDialog()
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
        });

}

// 关闭标签对话框
const closeTagDialog = () => {
    currentTag.value = {
        id_index: '',
        text: '',
        desc: '',
        color: 'rgba(255, 123, 2, .4)'
    }
    dialogVisible.value = false
}


const sureSelectThis = (data) => {
    // console.log('选择的分类：', data)
    selectedGroup.value = data
    currentTag.value.id_index = data.sub.id_index
}


defineExpose({
    open: (text, translate) => {
        currentTag.value = {
            id_index: '',
            text: '',
            desc: '',
            color: 'rgba(255, 123, 2, .4)'
        }
        currentTag.value.text = text
        currentTag.value.desc = translate
        dialogVisible.value = true
    }
})
</script>
<style scoped>
.tag-manager {
    display: flex;
    flex-direction: column;
    padding: 0 16px 16px 16px;
    background: var(--weilin-prompt-ui-primary-bg);
    height: 100%;
    box-sizing: border-box;
}


.form-group {
    margin-bottom: 16px;
    box-sizing: border-box;
    width: 100%;
}

.form-group:last-child {
    margin-bottom: 0;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: var(--primary-text);
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-primary-text);
    font-size: 14px;
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--weilin-prompt-ui-primary-color);
    box-shadow: 0 0 0 2px rgba(var(--weilin-prompt-ui-primary-color-rgb), 0.1);
}


.color-picker {
    display: flex;
    gap: 12px;
    padding: 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-secondary-bg);
}

.color-preview {
    width: 48px;
    height: 48px;
    border-radius: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    background-image: linear-gradient(45deg, #ccc 25%, transparent 25%),
        linear-gradient(-45deg, #ccc 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #ccc 75%),
        linear-gradient(-45deg, transparent 75%, #ccc 75%);
    background-size: 10px 10px;
    background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
}

.color-controls {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.color-input {
    width: 100%;
    height: 32px;
    padding: 0;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    cursor: pointer;
}

.alpha-control {
    display: flex;
    align-items: center;
    gap: 8px;
}

.alpha-slider {
    flex: 1;
    height: 8px;
    -webkit-appearance: none;
    background: linear-gradient(to right, transparent, currentColor);
    border-radius: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
}

.alpha-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--weilin-prompt-ui-primary-color);
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.alpha-value {
    min-width: 48px;
    text-align: right;
    color: var(--weilin-prompt-ui-secondary-text);
}

.select-group-item {
    display: flex;
    align-items: center;
}

.add-tag-btn {
    background-color: var(--weilin-prompt-ui-primary-color);
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: background-color 0.3s;
}

.add-tag-btn:hover {
    background-color: var(--weilin-prompt-ui-primary-color-hover);
}
</style>