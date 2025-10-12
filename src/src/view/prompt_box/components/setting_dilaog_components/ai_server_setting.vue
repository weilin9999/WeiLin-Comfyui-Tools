<template>
    <div class="ai-server-setting-panel">
        <div class="weilin-comfyui-translater-setting-box">
            <div class="weilin-comfyui-setting-item">
                <label>API Key</label>
                <input type="text" v-model="aiServerSettingData.api_key" placeholder="请输入API Key"
                    class="weilin-comfyui-common-select" />
            </div>
            <div class="weilin-comfyui-setting-item">
                <label>AI平台</label>
                <select v-model="aiServerSettingData.base_url" disabled class="weilin-comfyui-common-select">
                    <option value="https://api.siliconflow.cn/v1">硅基AI</option>
                </select>
            </div>
            <div class="weilin-comfyui-setting-item">
                <label>Model（获取前请先填写完API Key点击保存后再获取！）</label>
                <div style="display: flex; gap: 10px;">
                    <select v-model="aiServerSettingData.model" class="weilin-comfyui-common-select" style="flex:1;">
                        <option v-for="model in aiModelsData.data" :key="model.id" :value="model.id">
                            {{ model.id }}
                        </option>
                    </select>
                    <button type="button" class="weilin-comfyui-install-button" style="width:auto;min-width:120px;"
                        @click="getAiModelsFunc">
                        获取模型列表
                    </button>
                </div>
            </div>
            <button class="weilin-comfyui-save-button" @click="updateAiServerSettingFunc">保存AI平台设置</button>
        </div>
        <div class="weilin-comfyui-translater-setting-box">
            <div class="weilin-comfyui-setting-small-titile">{{ t('promptBox.settings.translaterSetting') }}</div>
            <div class="weilin-comfyui-language-selectors">
                <div class="weilin-comfyui-setting-item">
                    <label>{{ t('promptBox.settings.translaterLangSourceSetting') }}</label>
                    <select v-model="sourceLanguage">
                        <option v-for="(item, index) in language" :index="index" :key="'lan-item_' + index"
                            :value="item.translator">{{ t('translaterLanguage.' + item.language) }}</option>
                    </select>
                </div>
                <div class="weilin-comfyui-setting-item">
                    <label>{{ t('promptBox.settings.translaterLangTargeSetting') }}</label>
                    <select v-model="targetLanguage">
                        <option v-for="(item, index) in language" :index="index" :key="'lan-mu-item_' + index"
                            :value="item.translator">{{ t('translaterLanguage.' + item.language) }}</option>
                    </select>
                </div>
            </div>
            <button class="weilin-comfyui-install-button" @click="saveTranslaterSetting">
                {{ t('promptBox.settings.saveTranslaterSetting') }}
            </button>
        </div>

        <div class="weilin-comfyui-translater-setting-box">
            <div class="weilin-comfyui-setting-small-titile">{{ t('promptBox.settings.testTranslaterTitle') }}</div>
            <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.inputTestTranslater') }}</label>
                <input type="text" v-model="testTranslaterInputText"
                    :placeholder="t('promptBox.settings.inputTestTranslaterPlaceholder')" />
            </div>
            <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.outPutTestTranslater') }}</label>
                <input type="text" v-model="testTranslaterOutputText" readonly
                    :placeholder="t('promptBox.settings.outPutTestTranslaterPlaceholder')" />
            </div>
            <button class="weilin-comfyui-install-button" @click="translaterTextTest">
                {{ t('promptBox.settings.testingTranslater') }}
            </button>
        </div>
        <!-- <div class="weilin-comfyui-setting-item">
            <label>Temperature</label>
            <input type="number" v-model.number="aiServerSettingData.temperature" min="0" max="2" step="0.01" class="weilin-comfyui-common-select" />
        </div>
        <div class="weilin-comfyui-setting-item">
            <label>Top P</label>
            <input type="number" v-model.number="aiServerSettingData.top_p" min="0" max="1" step="0.01" class="weilin-comfyui-common-select" />
        </div>
        <div class="weilin-comfyui-setting-item">
            <label>Max Tokens</label>
            <input type="number" v-model.number="aiServerSettingData.max_tokens" min="1" max="32768" class="weilin-comfyui-common-select" />
        </div> -->
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { aiServerApi } from '@/api/ai_server'
import { translatorApi } from '@/api/translator'
import { language } from "../translater"
import message from '@/utils/message'

const { t } = useI18n()

// 翻译库设置
const selectedTranslatorService = ref('');
const sourceLanguage = ref('');
const targetLanguage = ref('');
const testTranslaterOutputText = ref('');
const testTranslaterInputText = ref('');

const aiServerSettingData = ref({
    api_key: "",
    base_url: "https://api.siliconflow.cn/v1",
    model: "",
    temperature: 0,
    top_p: 0.7,
    max_tokens: 4096
})
const aiModelsData = ref({ object: 'list', data: [] });

const updateAiServerSettingFunc = () => {
    aiServerApi.updateAiServerSetting(aiServerSettingData.value).then(res => {
        if (res.info == "ok") {
            message({ type: "success", str: 'message.saveSuccess' });
        } else {
            message({ type: "warn", str: 'message.saveFailed' });
        }
    }).catch(err => {
        message({ type: "warn", str: 'message.saveFailed' });
    })
};

const getAiServerSettingFunc = () => {
    aiServerApi.getAiServerSetting().then(res => {
        aiServerSettingData.value = res.data;
    }).catch(err => {
        message({ type: "warn", str: 'message.getTranslaterFail' });
    })
};

const getAiModelsFunc = () => {
    aiServerApi.getAiModels().then(res => {
        aiModelsData.value = res.data;
    }).catch(err => {
        message({ type: "warn", str: 'message.getTranslaterFail' });
    })
};


const getTranskateBuktSetting = () => {
    translatorApi.getTranslateBuktSetting().then(res => {
        selectedTranslatorService.value = res.data.translate_service
        sourceLanguage.value = res.data.translate_source_lang
        targetLanguage.value = res.data.translate_target_lang
    }).catch(err => {
        message({ type: "warn", str: 'message.getTranslaterFail' });
    })
};

const saveTranslaterSetting = () => {
    translatorApi.saveTranslateSetting(selectedTranslatorService.value,
        sourceLanguage.value,
        targetLanguage.value).then(res => {
            // console.log(res)
            if (res.info == "ok") {
                message({ type: "success", str: 'message.saveSuccess' });
            } else {
                message({ type: "warn", str: 'message.saveFailed' });
            }
        }).catch(err => {
            message({ type: "warn", str: 'message.saveFailed' });
        })
};

// 翻译文本
const translaterTextTest = () => {

    testTranslaterOutputText.value = ''
    let needTranslateData = { text: testTranslaterInputText.value, translate: '' }
    const jsonString = JSON.stringify(needTranslateData)

    translatorApi.translaterInputText(jsonString, "").then(res => {
        if (res) {
            if (res.data) {
                const jsonData = JSON.parse(res.data)
                // console.log(jsonData)
                // token.translate = jsonData.translate
                testTranslaterOutputText.value = jsonData.translate
            }
        }
    }).catch(err => {
        message({ type: "warn", str: 'message.translaterTestFail' });
    })

};

onMounted(() => {
    getAiServerSettingFunc();
    getAiModelsFunc();
    getTranskateBuktSetting();
});
</script>

<style scoped>
.ai-server-setting-panel {
    display: flex;
    flex-direction: column;
    gap: 0;
    padding: 0;
    border-radius: 12px;
    box-shadow: none;
}


.weilin-comfyui-setting-item {
    margin-bottom: 18px;
    background: var(--weilin-prompt-ui-card-bg);
    border-radius: 8px;
    padding: 12px 18px;
    box-shadow: 0 1px 4px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-setting-item label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--weilin-prompt-ui-label-color);
}

.weilin-comfyui-setting-item select,
.weilin-comfyui-setting-item input[type="number"],
.weilin-comfyui-setting-item input[type="text"] {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--weilin-prompt-ui-input-border);
    border-radius: 6px;
    background-color: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-label-color);
    font-size: 15px;
    transition: border-color 0.2s;
}

.weilin-comfyui-setting-item select:focus,
.weilin-comfyui-setting-item input:focus {
    border-color: var(--weilin-prompt-ui-input-focus);
    outline: none;
}


.weilin-comfyui-save-button,
.weilin-comfyui-install-button {
    width: 100%;
    padding: 12px;
    background: var(--weilin-prompt-ui-btn-gradient);
    color: #fff;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-weight: 600;
    font-size: 16px;
    margin-top: 8px;
    box-shadow: var(--weilin-prompt-ui-btn-shadow);
    transition: background 0.2s;
}

.weilin-comfyui-save-button:hover,
.weilin-comfyui-install-button:hover {
    background: var(--weilin-prompt-ui-btn-gradient-hover);
}


.weilin-comfyui-setting-small-titile {
    font-size: 16px;
    font-weight: 600;
    color: var(--weilin-prompt-ui-title-color);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 1px solid var(--weilin-prompt-ui-card-border);
}

.weilin-comfyui-translater-setting-box {
    margin-top: 20px;
    padding: 16px;
    background: var(--weilin-prompt-ui-card-bg);
    border-radius: 10px;
    border: 1px solid var(--weilin-prompt-ui-card-border);
    box-shadow: 0 1px 8px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-translater-setting-box .weilin-comfyui-language-selectors {
    display: flex;
    gap: 16px;
    margin: 12px 0;
}

.weilin-comfyui-translater-setting-box .weilin-comfyui-language-selectors .weilin-comfyui-setting-item {
    flex: 1;
}
</style>
