<template>
    <div class="lora_catd_content" :style="'left: ' + paddingLeft + 'px;top: '+paddingTop+'px;'" @mouseenter="handleCardEnter"
        @mouseleave="handleCardLeave">
        <div class="lora-detail__content" ref="loraContent">

            <div v-if="loading" class="lora-detail__loading">
                <svg viewBox="0 0 24 24" width="24" height="24" class="is-rotating">
                    <path d="M12 4V2C6.48 2 2 6.48 2 12H4C4 7.58 7.58 4 12 4Z" />
                </svg>
            </div>

            <div class="lora-detail__body">
                <!-- 标题 -->
                <div class="lora-detail__title">Lora 信息</div>

                <!-- 标签区域 -->
                <ul class="lora-detail__tags">
                    <li v-if="loraInfo.type" class="lora-detail__tag" :class="`-type-${loraInfo.type.toLowerCase()}`"
                        :title="t('lora.type')">
                        {{ loraInfo.type }}
                    </li>
                    <li v-if="loraInfo.baseModel" class="lora-detail__tag"
                        :class="`-basemodel-${loraInfo.baseModel.toLowerCase()}`" :title="t('lora.baseModel')">
                        {{ loraInfo.baseModel }}
                    </li>
                </ul>

                <!-- 信息表格 -->
                <table class="lora-detail__table">
                    <tbody>
                        <!-- 文件信息 -->
                        <tr>
                            <td class="label">{{ t('lora.file') }}</td>
                            <td colspan="2">{{ loraInfo.file }}</td>
                        </tr>

                        <!-- Hash值 -->
                        <tr>
                            <td class="label">{{ t('lora.hash') }}</td>
                            <td colspan="2" class="hash">{{ loraInfo.sha256 }}</td>
                        </tr>

                        <!-- Civitai链接 -->
                        <tr>
                            <td class="label">{{ t('lora.civitai') }}</td>
                            <td colspan="2">
                                <template v-if="civitaiLink">
                                    <a :href="civitaiLink" target="_blank" class="civitai-link">
                                        <svg viewBox="0 0 24 24" width="16" height="16" class="civitai-icon">
                                            <path
                                                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-4H8l4-7v4h3l-4 7z" />
                                        </svg>
                                        <span>{{ t('lora.viewOnCivitai') }}</span>
                                    </a>
                                    <button style="margin-left: 10px;" class="refresh-btn" @click="refreshLoraInfo">
                                        {{ t('lora.getCivitData') }}
                                    </button>
                                </template>
                                <template v-else-if="isCivitaiNotFound">
                                    <div class="not-found">
                                        <i>{{ t('lora.modelNotFound') }}</i>
                                        <svg viewBox="0 0 24 24" width="16" height="16" class="help-icon"
                                            :title="t('lora.modelNotFoundTip')">
                                            <path
                                                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z" />
                                        </svg>
                                    </div>
                                </template>
                                <template v-else>
                                    <button class="fetch-btn" @click="refreshLoraInfo">
                                        {{ t('lora.fetchFromCivitai') }}
                                    </button>
                                </template>
                            </td>
                        </tr>

                        <!-- 名称(可编辑) -->
                        <tr :class="{ 'is-editing': isEditing.name }">
                            <td class="label">
                                {{ t('lora.name') }}
                                <svg viewBox="0 0 24 24" width="16" height="16" class="help-icon"
                                    :title="t('lora.nameTip')">
                                    <path
                                        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z" />
                                </svg>
                            </td>
                            <td>
                                <input v-if="isEditing.name" v-model="editValues.name" type="text"
                                    @keyup.enter="saveEdit('name')" @keyup.esc="cancelEdit('name')" ref="nameInput" />
                                <span v-else class="text">{{ loraInfo.name }}</span>
                            </td>
                        </tr>

                        <!-- 基础模型 -->
                        <tr>
                            <td class="label">{{ t('lora.baseModel') }}</td>
                            <td colspan="2">{{
                                !loraInfo.baseModelFile && !loraInfo.baseModelFile
                                    ? ""
                                    : (loraInfo.baseModel || "") +
                                    (loraInfo.baseModelFile
                                        ? `
                                (${loraInfo.baseModelFile})`
                                        : "")
                            }}</td>
                        </tr>

                        <!-- 跳过层 -->
                        <tr>
                            <td class="label">{{ t('lora.skipClip') }}</td>
                            <td colspan="2">{{
                                (_t =
                                    (_s = loraInfo.raw) === null || _s === void 0
                                        ? void 0
                                        : _s.metadata) === null || _t === void 0
                                    ? void 0
                                    : _t.ss_clip_skip
                            }}</td>
                        </tr>


                        <!-- 其他可编辑字段 -->
                        <template v-for="field in editableFields" :key="field.key">
                            <tr :class="{ 'is-editing': isEditing[field.key] }">
                                <td class="label">
                                    {{ field.label }}
                                    <svg v-if="field.tip" viewBox="0 0 24 24" width="16" height="16" class="help-icon"
                                        :title="field.tip">
                                        <path
                                            d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z" />
                                    </svg>
                                </td>
                                <td>
                                    <span class="text">{{ loraInfo[field.key] }}</span>
                                </td>
                                <td class="actions">
                                    <button class="copy-btn" @click="copyToClipboard(loraInfo[field.key])"
                                        :title="t('lora.copy')">
                                        <svg class="svg-icon" viewBox="0 0 24 24" width="16" height="16">
                                            <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                                        </svg>
                                        {{ t('lora.copy') }}
                                    </button>
                                </td>
                            </tr>
                        </template>

                        <!-- 用户自定义的字段 -->
                        <template v-for="(field, key) in userEditFields" :key="key">
                            <tr :class="{ 'is-editing': isEditing[key] }">
                                <td class="label">
                                    <input v-if="isEditing[key]" v-model="field.label" type="text" />
                                    <span v-else>{{ field.label }}</span>
                                </td>
                                <td>
                                    <span class="text">{{ loraInfo.user_diy_fileds ?
                                        loraInfo.user_diy_fileds[key]?.value : '' }}</span>
                                </td>
                                <td class="actions">
                                    <button class="copy-btn" @click="copyToClipboard(loraInfo.user_diy_fileds[key]?.value)"
                                        :title="t('lora.copy')">
                                        <svg class="svg-icon" viewBox="0 0 24 24" width="16" height="16">
                                            <path d="M16 1H4c-1.1 0-2 .9-2 2v14h2V3h12V1zm3 4H8c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h11c1.1 0 2-.9 2-2V7c0-1.1-.9-2-2-2zm0 16H8V7h11v14z"/>
                                        </svg>
                                        {{ t('lora.copy') }}
                                    </button>
                                </td>
                            </tr>
                        </template>

                        <!-- 训练词 -->
                        <tr v-if="trainedWords.length">
                            <td class="label">
                                {{ t('lora.trainedWords') }}
                                <svg viewBox="0 0 24 24" width="16" height="16" class="help-icon"
                                    :title="t('lora.trainedWordsTip')">
                                    <path
                                        d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm1 17h-2v-2h2v2zm2.07-7.75l-.9.92C13.45 12.9 13 13.5 13 15h-2v-.5c0-1.1.45-2.1 1.17-2.83l1.24-1.26c.37-.36.59-.86.59-1.41 0-1.1-.9-2-2-2s-2 .9-2 2H8c0-2.21 1.79-4 4-4s4 1.79 4 4c0 .88-.36 1.68-.93 2.25z" />
                                </svg>
                                <div v-if="selectedWords.length" class="word-selection">
                                    {{ t('lora.selectedWords', { count: selectedWords.length }) }}
                                    <button class="copy-btn" @click="copySelectedWords">
                                        {{ t('common.copy') }}
                                    </button>
                                </div>
                            </td>
                            <td colspan="2">
                                <ul class="word-list">
                                    <li v-for="(word, index) in isCollapsed ? trainedWords.slice(0, 10) : trainedWords"
                                        :key="'words-' + index" class="word-item"
                                        :class="{ 'is-selected': isWordSelected(word.word), 'is-hidden': isCollapsed && index >= 10 }"
                                        @click="toggleWordSelection(word.word)">
                                        <span>{{ word.word }}</span>
                                        <svg v-if="word.civitai" viewBox="0 0 24 24" width="16" height="16"
                                            class="civitai-icon">
                                            <path
                                                d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15v-4H8l4-7v4h3l-4 7z" />
                                        </svg>
                                        <small v-if="word.count != null">{{ word.count }}</small>
                                    </li>
                                    <li v-if="trainedWords.length > 10" class="toggle-btn" @click="toggleCollapse">
                                        {{ isCollapsed ? t('common.showMore') : t('common.showLess') }}
                                    </li>
                                </ul>
                            </td>
                        </tr>

                    </tbody>
                </table>


                <!-- 图片 -->
                <ul class="lora-detail__images" v-if="loraInfo.images?.length" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;">
                    <li v-for="(img, index) in loraInfo.images" :key="index" class="lora-detail__image-item">
                        <figure>

                            <div class="image-wrapper" style="height: 200px;">
                                <img :src="img.url" style="width: 100%; height: 100%; object-fit: contain;" />
                            </div>

                            <figcaption class="image-info">
                                <span v-if="img.civitaiUrl" class="info-item">
                                    <a :href="img.civitaiUrl" target="_blank" class="civitai-link">
                                        C站 civitai
                                        <svg viewBox="0 0 24 24" width="16" height="16">
                                            <path
                                                d="M19 19H5V5h7V3H5a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7h-2v7zM14 3v2h3.59l-9.83 9.83 1.41 1.41L19 6.41V10h2V3h-7z" />
                                        </svg>
                                    </a>
                                </span>

                                <span v-if="img.seed" class="info-item">
                                    <label>种子 seed</label>
                                    {{ img.seed }}
                                </span>

                                <span v-if="img.steps" class="info-item">
                                    <label>步数 steps</label>
                                    {{ img.steps }}
                                </span>

                                <span v-if="img.cfg" class="info-item">
                                    <label>引导系数 cfg</label>
                                    {{ img.cfg }}
                                </span>

                                <span v-if="img.sampler" class="info-item">
                                    <label>采样器 sampler</label>
                                    {{ img.sampler }}
                                </span>

                                <span v-if="img.model" class="info-item">
                                    <label>基础模型 model</label>
                                    {{ img.model }}
                                </span>

                                <span v-if="img.positive" class="info-item">
                                    <label>正向提示词 positive</label>
                                    {{ img.positive }}
                                </span>

                                <span v-if="img.negative" class="info-item">
                                    <label>反向提示词 negative</label>
                                    {{ img.negative }}
                                </span>
                            </figcaption>
                        </figure>
                    </li>
                </ul>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import message from '@/utils/message'
import { loraApi } from '@/api/lora'

const { t } = useI18n()
const loading = ref(false)
const loraInfo = ref({})
const loraContent = ref()


const userEditFields = ref({}) // 用户自定义字段

const props = defineProps({
    fileNmae: {
        type: String,
        required: true
    },
    paddingLeft: {
        type: Number,
        required: false,
        default: 100
    },
    paddingTop: {
        type: Number,
        required: false,
        default: 100
    },
})

const fileURL = ref('')
const emit = defineEmits(['cardLeave', 'cardenter'])

const handleCardLeave = () => {
    emit('cardLeave')
}
const handleCardEnter = () => {
    emit('cardenter')
}

// 编辑状态管理
const isEditing = ref({})
const editValues = ref({})
const selectedWords = ref([])

// 可编辑字段配置
const editableFields = [
    {
        key: 'strengthMin',
        label: t('lora.strengthMin'),
        tip: t('lora.strengthMinTip'),
        type: 'number'
    },
    {
        key: 'strengthMax',
        label: t('lora.strengthMax'),
        tip: t('lora.strengthMaxTip'),
        type: 'number'
    },
    {
        key: 'strWeight',
        label: t('lora.strWeight'),
        tip: t('lora.strWeightTip'),
        type: 'number'
    },
    {
        key: 'loraWorks',
        label: t('lora.promptWords'),
        tip: t('lora.promptWordsTip')
    }
]



// 添加字段方法修改为：
const addField = () => {
    const newKey = `custom_${Date.now()}`
    if (!loraInfo.value.user_diy_fileds) {
        loraInfo.value.user_diy_fileds = {}
    }

    // 以对象形式存储字段
    userEditFields.value[newKey] = {
        label: '新字段',
        type: 'text'
    }

    // 使用结构化存储方式
    loraInfo.value.user_diy_fileds[newKey] = {
        label: '新字段',
        value: ''
    }
    editValues.value[newKey] = ''
    saveEdit(newKey)
}

// 删除字段方法修改为：
const removeField = async (key) => {
    delete userEditFields.value[key]
    delete editValues.value[key]
    if (loraInfo.value?.user_diy_fileds?.[key]) {
        delete loraInfo.value.user_diy_fileds[key]
        // console.log('Deleted field:', key, 'from user_diy_fileds:', loraInfo.value.user_diy_fileds)
    }
    await nextTick(async () => {
        await deleteInfo(key)
    })
}

onMounted(() => {
    init()
})

// 初始化
const init = () => {
    fileURL.value = props.fileNmae;
    loraInfo.value = {};
    selectedWords.value = [];
    editValues.value = {
        name: false,
        nameValue: "",
        min: false,
        minValue: "",
        max: false,
        maxValue: "",
        notes: false,
        notesValue: "",
        loraWorks: false,
        loraWorksValue: "",
    };
    loraApi
        .getLoraDetail({ file: fileURL.value, refresh: false, light: false })
        .then((res) => {
            // console.log(res.data.data)
            loraInfo.value = res.data;
            nextTick(function () {
                var _j, _k, _u, _v, _w, _x;
                loraInfo.value.name =
                    loraInfo.value.name ||
                    ((_k =
                        (_j = loraInfo.value.raw) === null || _j === void 0
                            ? void 0
                            : _j.metadata) === null || _k === void 0
                        ? void 0
                        : _k.ss_output_name === void 0
                            ? _k["modelspec.title"]
                            : _k.ss_output_name) ||
                    "";
                editValues.value.nameValue = loraInfo.value.name;
                loraInfo.value.strengthMin =
                    (_u = loraInfo.value.strengthMin) !== null && _u !== void 0
                        ? _u
                        : "";
                editValues.value.minValue = loraInfo.value.strengthMin;
                loraInfo.value.strengthMax =
                    (_v = loraInfo.value.strengthMax) !== null && _v !== void 0
                        ? _v
                        : "";
                editValues.value.maxValue = loraInfo.value.strengthMax;
                loraInfo.value.userNote =
                    (_w = loraInfo.value.userNote) !== null && _w !== void 0
                        ? _w
                        : "";
                editValues.value.notesValue = loraInfo.value.userNote;
                loraInfo.value.loraWorks =
                    (_x = loraInfo.value.loraWorks) !== null && _x !== void 0
                        ? _x
                        : "";
                editValues.value.loraWorksValue = loraInfo.value.loraWorks;

                userEditFields.value = loraInfo.value.user_diy_fileds;

                loading.value = false;
            });
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
            loading.value = false;
        });
}

const copyToClipboard = (text) => {
  navigator.clipboard.writeText(text)
    .then(() => {
      message({ type: "success", str: "已复制到剪贴板" });
    })
    .catch(err => {
    //   console.error("复制失败:", err);
      message({ type: "error", str: "复制失败" });
    });
}

// 计算属性
const civitaiLink = computed(() => {
    return loraInfo.value.links?.find(link => link.includes('civitai.com/models'))
})

const isCivitaiNotFound = computed(() => {
    return loraInfo.value.raw?.civitai?.error === 'Model not found'
})

const trainedWords = computed(() => {
    return loraInfo.value.trainedWords || []
})

// 方法
const refreshLoraInfo = async () => {
    const scrollPosition = loraContent.value?.scrollTop || 0
    loading.value = true;
    loraApi
        .getLoraRefresh({ file: fileURL.value })
        .then((res) => {
            // console.log(res.data.data)
            loraInfo.value = res.data;

            nextTick(function () {
                var _j, _k, _u, _v, _w;
                loraInfo.value.name =
                    loraInfo.value.name ||
                    ((_k =
                        (_j = loraInfo.value.raw) === null || _j === void 0
                            ? void 0
                            : _j.metadata) === null || _k === void 0
                        ? void 0
                        : _k.ss_output_name === void 0
                            ? _k["modelspec.title"]
                            : _k.ss_output_name) ||
                    "";
                editValues.value.nameValue = loraInfo.value.name;
                loraInfo.value.strengthMin =
                    (_u = loraInfo.value.strengthMin) !== null && _u !== void 0
                        ? _u
                        : "";
                editValues.value.minValue = loraInfo.value.strengthMin;
                loraInfo.value.strengthMax =
                    (_v = loraInfo.value.strengthMax) !== null && _v !== void 0
                        ? _v
                        : "";
                editValues.value.maxValue = loraInfo.value.strengthMax;
                loraInfo.value.userNote =
                    (_w = loraInfo.value.userNote) !== null && _w !== void 0
                        ? _w
                        : "";
                editValues.value.notesValue = loraInfo.value.userNote;

                loading.value = false;
            });

            nextTick(function () {
                loading.value = false;
            });

            // 恢复滚动位置
            if (loraContent.value) {
                loraContent.value.scrollTop = scrollPosition
            }

            message({ type: "success", str: 'message.dataLoaded' });
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
            loading.value = false;
        });
}

const toggleEdit = (field) => {
    if (isEditing.value[field]) {
        saveEdit(field)
    } else {
        startEdit(field)
    }
}

const startEdit = (field) => {
    isEditing.value[field] = true
    // 区分普通字段和自定义字段
    if (field in userEditFields.value) {
        editValues.value[field] = loraInfo.value.user_diy_fileds?.[field]?.value || ''
    } else {
        editValues.value[field] = loraInfo.value[field]
    }
    // 自动聚焦输入框
    nextTick(() => {
        if (field === 'name' && nameInput.value) {
            nameInput.value.focus()
        }
    })
}

const saveEdit = (fieldKey) => {
    const isCustomField = fieldKey in userEditFields.value

    if (isCustomField) {
        if (!loraInfo.value.user_diy_fileds) {
            loraInfo.value.user_diy_fileds = {}
        }
        // 更新自定义字段的值
        loraInfo.value.user_diy_fileds[fieldKey] = {
            label: userEditFields.value[fieldKey].label,
            value: editValues.value[fieldKey]
        }
    } else {
        loraInfo.value[fieldKey] = editValues.value[fieldKey]
    }

    saveInfo(loraInfo.value)
    isEditing.value[fieldKey] = false
}

const cancelEdit = (field) => {
    isEditing.value[field] = false
    editValues.value[field] = loraInfo.value[field]
}

const saveInfo = (param) => {
    const scrollPosition = loraContent.value?.scrollTop || 0
    // console.log(scrollPosition)
    loading.value = true;
    loraApi
        .postLoraSave(fileURL.value, param)
        .then((res) => {
            // console.log(res.data.data)
            loraInfo.value = res.data;
            nextTick(function () {
                var _j, _k, _u, _v, _w;
                loraInfo.value.name =
                    loraInfo.value.name ||
                    ((_k =
                        (_j = loraInfo.value.raw) === null || _j === void 0
                            ? void 0
                            : _j.metadata) === null || _k === void 0
                        ? void 0
                        : _k.ss_output_name === void 0
                            ? _k["modelspec.title"]
                            : _k.ss_output_name) ||
                    "";
                editValues.value.nameValue = loraInfo.value.name;
                loraInfo.value.strengthMin =
                    (_u = loraInfo.value.strengthMin) !== null && _u !== void 0
                        ? _u
                        : "";
                editValues.value.minValue = loraInfo.value.strengthMin;
                loraInfo.value.strengthMax =
                    (_v = loraInfo.value.strengthMax) !== null && _v !== void 0
                        ? _v
                        : "";
                editValues.value.maxValue = loraInfo.value.strengthMax;
                loraInfo.value.userNote =
                    (_w = loraInfo.value.userNote) !== null && _w !== void 0
                        ? _w
                        : "";
                editValues.value.notesValue = loraInfo.value.userNote;

                loading.value = false;

                nextTick(function () {
                    // 恢复滚动位置
                    if (loraContent.value) {
                        loraContent.value.scrollTop = scrollPosition
                    }
                });
            });

            message({ type: "success", str: 'message.saveSuccess' });
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
            // console.log(err)
            loading.value = false;
        });
}


const deleteInfo = async (param) => {
    const scrollPosition = loraContent.value?.scrollTop || 0
    // console.log(scrollPosition)
    loading.value = true;
    await loraApi
        .postLoraDelet(fileURL.value, param)
        .then((res) => {
            // console.log(res.data.data)
            loraInfo.value = res.data;
            nextTick(function () {
                var _j, _k, _u, _v, _w;
                loraInfo.value.name =
                    loraInfo.value.name ||
                    ((_k =
                        (_j = loraInfo.value.raw) === null || _j === void 0
                            ? void 0
                            : _j.metadata) === null || _k === void 0
                        ? void 0
                        : _k.ss_output_name === void 0
                            ? _k["modelspec.title"]
                            : _k.ss_output_name) ||
                    "";
                editValues.value.nameValue = loraInfo.value.name;
                loraInfo.value.strengthMin =
                    (_u = loraInfo.value.strengthMin) !== null && _u !== void 0
                        ? _u
                        : "";
                editValues.value.minValue = loraInfo.value.strengthMin;
                loraInfo.value.strengthMax =
                    (_v = loraInfo.value.strengthMax) !== null && _v !== void 0
                        ? _v
                        : "";
                editValues.value.maxValue = loraInfo.value.strengthMax;
                loraInfo.value.userNote =
                    (_w = loraInfo.value.userNote) !== null && _w !== void 0
                        ? _w
                        : "";
                editValues.value.notesValue = loraInfo.value.userNote;

                loading.value = false;

                nextTick(function () {
                    // 恢复滚动位置
                    if (loraContent.value) {
                        loraContent.value.scrollTop = scrollPosition
                    }
                });
            });

            message({ type: "success", str: 'message.deleteSuccess' });
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
            // console.log(err)
            loading.value = false;
        });
}

const toggleWordSelection = (word) => {
    const index = selectedWords.value.indexOf(word)
    if (index === -1) {
        selectedWords.value.push(word)
    } else {
        selectedWords.value.splice(index, 1)
    }
}

const isWordSelected = (word) => {
    return selectedWords.value.includes(word)
}

const copySelectedWords = async () => {
    if (!selectedWords.value.length) return

    navigator.clipboard.writeText(selectedWords.value).then(
        (res) => {
            message({ type: "success", str: 'message.copySuccess' });
        },
        (err) => {
            message({ type: "warn", str: 'message.copyFailed' });
        }
    )
}

const isCollapsed = ref(true); // 添加展开/收起状态

const toggleCollapse = () => {
    isCollapsed.value = !isCollapsed.value;
}

const refresh = () => {
    init()
}

defineExpose({
    refresh
})

</script>

<style scoped>
.lora-detail {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 1000;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--weilin-prompt-ui-primary-text);
}

.lora-detail__content {
    height: 100%;
    padding: 20px;
    overflow-y: auto;
    color: var(--weilin-prompt-ui-primary-text);
}

.lora-detail__loading {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}


.svg-icon {
    fill: var(--weilin-prompt-ui-primary-text);
}

.lora-detail__body {
    height: 100%;
}

/* 表格样式 */
.lora-detail__table {
    width: 100%;
    border-collapse: collapse;
}

.lora-detail__table td {
    padding: 12px;
    border-bottom: 1px solid var(--weilin-prompt-ui-border);
}

.lora-detail__table td.label {
    width: 280px;
    color: var(--weilin-prompt-ui-label);
    font-weight: 500;
}

.lora-detail__table td.actions {
    width: 130px;
    text-align: right;
    display: flex;
    flex-direction: row;
    align-items: center;
}

/* 标签样式 */
.lora-detail__tags {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
    margin-bottom: 20px;
}

.lora-detail__tag {
    padding: 4px 12px;
    border-radius: 16px;
    font-size: 14px;
}

/* 按钮样式 */
.edit-btn,
.refresh-btn,
.fetch-btn,
.copy-btn {
    padding: 6px 12px;
    border-radius: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    background: var(--weilin-prompt-ui-button-bg);
    color: var(--weilin-prompt-ui-button-text);
    cursor: pointer;
    transition: all 0.3s;
}

.edit-btn:hover,
.refresh-btn:hover,
.fetch-btn:hover,
.copy-btn:hover {
    background: var(--weilin-prompt-ui-button-hover);
}

/* 输入框样式 */
input {
    width: 100%;
    padding: 8px;
    border-radius: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    background-color: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-input-text);
}

input:focus {
    border-color: var(--weilin-prompt-ui-primary);
    outline: none;
}

/* 词列表样式 */
.word-list {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.word-item {
    padding: 4px 12px;
    border-radius: 16px;
    background: var(--weilin-prompt-ui-tag-bg);
    color: var(--weilin-prompt-ui-tag-text);
    cursor: pointer;
    transition: all 0.3s;
    display: flex;
    align-items: center;
    gap: 4px;
}

.word-item:hover {
    background: var(--weilin-prompt-ui-tag-hover);
}

.word-item.is-selected {
    background: var(--weilin-prompt-ui-primary-color);
    color: #fff;
}

/* 动画 */
.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
    opacity: 0;
}

.is-rotating {
    animation: rotate 1s linear infinite;
}

@keyframes rotate {
    from {
        transform: rotate(0deg);
    }

    to {
        transform: rotate(360deg);
    }
}

/* 图片列表容器 */
.lora-detail__images {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    padding: 20px;
    list-style: none;
    margin: 0;
}

/* 单个图片项 */
.lora-detail__image-item {
    position: relative;
    background: var(--weilin-prompt-ui-secondary-bg);
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 8px var(--weilin-prompt-ui-shadow-color);
    transition: transform 0.3s ease;
}

.lora-detail__image-item:hover {
    transform: translateY(-2px);
}

/* 图片包装器 */
.image-wrapper {
    position: relative;
    width: 100%;
    padding-top: 100%;
    /* 1:1 宽高比 */
    overflow: hidden;
}

.image-wrapper img {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    object-fit: contain;
    transition: transform 0.3s ease;
}

.image-wrapper:hover img {
    transform: scale(1.05);
}

/* 图片操作按钮 */
.image-action {
    position: absolute;
    top: 12px;
    right: 12px;
    background: rgba(0, 0, 0, 0.6);
    color: #fff;
    padding: 6px 12px;
    border-radius: 4px;
    opacity: 0;
    transition: all 0.3s ease;
    cursor: pointer;
    font-size: 13px;
    backdrop-filter: blur(4px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    z-index: 1;
}

.image-wrapper:hover .image-action {
    opacity: 1;
}

.image-action:hover {
    background: rgba(0, 0, 0, 0.8);
    transform: translateY(-1px);
}

/* 图片信息区域 */
.image-info {
    padding: 16px;
    background: var(--weilin-prompt-ui-secondary-bg);
}

/* 信息项 */
.info-item {
    display: block;
    margin-bottom: 8px;
    font-size: 13px;
    color: var(--weilin-prompt-ui-secondary-text);
    word-break: break-all;
}

.info-item:last-child {
    margin-bottom: 0;
}

/* 信息标签 */
.info-item label {
    display: inline-block;
    color: var(--weilin-prompt-ui-label);
    margin-right: 8px;
    font-weight: 500;
}

/* Civitai链接样式 */
.civitai-link {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: var(--weilin-prompt-ui-primary-color);
    text-decoration: none;
    transition: opacity 0.3s ease;
}

.civitai-link:hover {
    opacity: 0.8;
}

.civitai-icon {
    fill: currentColor;
}

/* 提示词区域样式 */
.info-item:has(label:contains("正向提示词")),
.info-item:has(label:contains("反向提示词")) {
    background: var(--weilin-prompt-ui-tag-bg);
    padding: 8px;
    border-radius: 4px;
    margin-top: 12px;
}

/* 图片参数信息网格布局 */
.image-params {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
    gap: 8px;
    margin-bottom: 12px;
}

.param-item {
    background: var(--weilin-prompt-ui-tag-bg);
    padding: 4px 8px;
    border-radius: 4px;
    font-size: 12px;
}

/* 响应式调整 */
@media (max-width: 768px) {
    .lora-detail__images {
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 16px;
        padding: 16px;
    }

    .image-info {
        padding: 12px;
    }
}

.word-item .is-hidden {
    display: none;
}

.toggle-btn {
    cursor: pointer;
    color: var(--primary-color);
    text-align: center;
    padding: 4px;
    margin-top: 8px;
}

.toggle-btn:hover {
    text-decoration: underline;
}

.lora_catd_content {
    position: fixed;
    width: 680px;
    height: 300px;
    z-index: 999999999;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background-color: var(--weilin-prompt-ui-primary-bg);
    padding: 6px;
    box-sizing: border-box;
}
</style>