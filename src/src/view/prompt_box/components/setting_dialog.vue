<template>
  <Dialog v-model="dialogVisible" :title="t('promptBox.settings.title')">
    <div class="weilin-comfyui-settings-content">
      <div class="weilin-comfyui-settings-sidebar">
        <ul>
          <li :class="{ 'weilin-comfyui-active': selectedSetting === 'translator' }"
            @click="selectSetting('translator')">{{
              t('promptBox.settings.translator') }}</li>
          <li :class="{ 'weilin-comfyui-active': selectedSetting === 'setting_auto_complete_limit' }"
            @click="selectSetting('setting_auto_complete_limit')">{{
              t('promptBox.settings.setting_auto_complete_limit') }}</li>
          <li :class="{ 'weilin-comfyui-active': selectedSetting === 'setting_floating_ball' }"
            @click="selectSetting('setting_floating_ball')">{{
              t('promptBox.settings.setting_floating_ball') }}</li>
          <li :class="{ 'weilin-comfyui-active': selectedSetting === 'setting_prompt_box' }"
            @click="selectSetting('setting_prompt_box')">{{
              t('promptBox.settings.setting_prompt_box') }}</li>
          <li :class="{ 'weilin-comfyui-active': selectedSetting === 'setting_openai_box' }"
            @click="selectSetting('setting_openai_box')">{{
              t('promptBox.settings.setting_openai_box') }}</li>
          <!-- <li :class="{ 'weilin-comfyui-active': selectedSetting === 'setting_start_panel' }"
            @click="selectSetting('setting_start_panel')">{{
              t('promptBox.settings.setting_start_panel') }}</li> -->
          <li :class="{ 'weilin-comfyui-active': selectedSetting === 'setting_sponsor_me' }"
            @click="selectSetting('setting_sponsor_me')">{{
              t('promptBox.settings.setting_sponsor_me') }}</li>
        </ul>
      </div>
      <div class="weilin-comfyui-settings-main">
        <div v-if="selectedSetting === 'translator'">
          <h3>{{ t('promptBox.settings.translator') }}</h3>
          <div class="weilin-comfyui-setting-select">
            <label> {{ t('promptBox.settings.selectTranslater') }}</label>
            <select style="margin-left: 10px;" v-model="settingTranslater" class="weilin-comfyui-common-select">
              <option value="network"> {{ t('promptBox.settings.selectOptionNetworkTranslater') }}</option>
              <option value="translater">{{ t('promptBox.settings.selectOptionPythonTranslater') }}</option>
              <option value="openai">OpenAI API 翻译</option>
            </select>
            <button class="weilin-comfyui-install-button" @click="applyTranslaterSetting">
              {{ t('promptBox.settings.apply') }}
            </button>
          </div>
          <div class="weilin-comfyui-translator-settings">
            <div class="weilin-comfyui-group-box" v-if="settingTranslater == 'network'">
              <div class="weilin-comfyui-group-title">{{ t('promptBox.settings.selectOptionNetworkTranslaterTitle') }}
              </div>
              <div class="weilin-comfyui-note-top">{{ t('promptBox.settings.selectOptionNetworkTranslaterInfo')
              }}：https://github.com/xnx3/translate</div>
              <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.sourceLanguage') }}</label>
                <select v-model="savedSourceLanguage" class="weilin-comfyui-common-select">
                  <option value="auto">{{ t('promptBox.settings.auto_detect') }}</option>
                  <option value="chinese_simplified">{{ t('promptBox.settings.chinese_simplified') }}</option>
                  <option value="english">{{ t('promptBox.settings.english') }}</option>
                </select>
              </div>
              <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.targetLanguage') }}</label>
                <select v-model="savedTargetLanguage" class="weilin-comfyui-common-select">
                  <option value="chinese_simplified">{{ t('promptBox.settings.chinese_simplified') }}</option>
                  <option value="english">{{ t('promptBox.settings.english') }}</option>
                </select>
              </div>
              <button class="weilin-comfyui-save-button" @click="saveTranslatorSettings">
                {{ t('promptBox.settings.save') }}
              </button>
            </div>
            <div class="weilin-comfyui-group-box" v-if="settingTranslater == 'translater'">
              <div class="weilin-comfyui-group-title">{{ t('promptBox.settings.selectOptionPythonTranslaterTitle') }}
              </div>
              <div class="weilin-comfyui-note-top">{{ t('promptBox.settings.selectOptionPythonTranslaterInfo')
              }}：https://github.com/UlionTse/translators</div>
              <div class="weilin-comfyui-translater-innstall-status">
                <div class="weilin-comfyui-translater-install-label">
                  {{ t('promptBox.settings.nowTranlaterPackageState') }} {{ hasTranslaterPackage ?
                    t('promptBox.settings.tranlaterPackageStateTrue') : t('promptBox.settings.tranlaterPackageStateFlase')
                  }}
                </div>
                <div class="weilin-comfyui-translater-install-label" v-if="installTranslater">
                  {{ t('promptBox.settings.installTranslaterPackageInfo') }}
                </div>
                <div class="weilin-comfyui-translater-install-control" v-if="!hasTranslaterPackage">
                  <button :disabled="installTranslater" class="weilin-comfyui-install-button"
                    @click="installTranslaterPackage">
                    {{ installTranslater ? t('promptBox.settings.installed') : t('promptBox.settings.install') }}
                  </button>
                </div>
              </div>
              <div class="weilin-comfyui-translater-setting-box" v-if="hasTranslaterPackage">
                <div class="weilin-comfyui-setting-small-titile">{{ t('promptBox.settings.translaterSetting') }}</div>
                <div class="weilin-comfyui-setting-item">
                  <label>{{ t('promptBox.settings.chooseTranslaterSetting') }}</label>
                  <select v-model="selectedTranslatorService">
                    <option v-for="(item, index) in translaterSerives" :index="index" :key="'tran-item_' + index"
                      :value="item">{{ t('translaterService.' + item) }}</option>
                  </select>
                </div>
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
              <div class="weilin-comfyui-tranlater-text-box" v-if="hasTranslaterPackage">
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
            </div>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_auto_complete_limit'">
          <h3>{{ t('promptBox.settings.setting_auto_complete_limit') }}</h3>
          <div class="weilin-comfyui-floating-ball-settings">
            <div class="weilin-comfyui-setting-item">
              <label>{{ t('promptBox.settings.show_auto_limit') }}</label>
              <input type="number" v-model.number="saveAutoCompleteLimit" min="1" max="99999999" style="width: 100px;"
                :placeholder="t('promptBox.settings.showAutoLimitPlaceholder')" />
            </div>
            <div class="weilin-comfyui-setting-item">
              <label>{{ t('promptBox.settings.settingAutoCompleteWidth') }}</label>
              <input type="number" v-model.number="saveAutoCompleteWidth" min="5" style="width: 100px;"
                :placeholder="t('promptBox.settings.settingAutoCompleteWidthPlaceholder')" />
            </div>
            <div class="weilin-comfyui-setting-item">
              <label>{{ t('promptBox.settings.settingAutoCompleteHeight') }}</label>
              <input type="number" v-model.number="saveAutoCompleteHeight" min="5" style="width: 100px;"
                :placeholder="t('promptBox.settings.settingAutoCompleteHeightPlaceholder')" />
            </div>
            <button class="weilin-comfyui-save-button" @click="saveAutoCompleteSetting">
              {{ t('promptBox.settings.save') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_floating_ball'">
          <h3>{{ t('promptBox.settings.setting_floating_ball') }}</h3>
          <div class="weilin-comfyui-floating-ball-settings"
            style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
            <div class="weilin-comfyui-settings-column">
              <div class="weilin-comfyui-setting-item">
                <label>
                  <input type="checkbox" v-model="isFloatingBallEnabled" />
                  {{ t('promptBox.settings.enableFloatingBall') }}
                </label>
              </div>
              <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.floatingBallCount') }}</label>
                <input type="number" v-model.number="savedFloatingBallCount" min="1" max="100"
                  :placeholder="t('promptBox.settings.floatingBallCountPlaceholder')" />
              </div>
              <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.floatingBallSize') }}</label>
                <input type="number" v-model.number="savedFloatingBallSize" min="5" max="999999"
                  :placeholder="t('promptBox.settings.floatingBallSizePlaceholder')" />
              </div>
              <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.floatingBallHeight') }}</label>
                <input type="number" v-model.number="savedFloatingBallHeight" min="5" max="999999"
                  :placeholder="t('promptBox.settings.floatingBallHeightPlaceholder')" />
              </div>
            </div>
            <div class="weilin-comfyui-settings-column">
              <div class="weilin-comfyui-setting-item">
                <label>{{ t('promptBox.settings.skinSetting') }}</label>
                <select v-model="ballSkinType">
                  <option value="default">{{ t('promptBox.settings.defaultSkin') }}</option>
                  <option value="custom">{{ t('promptBox.settings.customSkin') }}</option>
                </select>
              </div>
              <div class="weilin-comfyui-setting-item" v-if="ballSkinType === 'custom'">
                <label>{{ t('promptBox.settings.uploadSkin') }}</label>
                <input type="file" accept="image/*" @change="handleSkinUpload" ref="skinUploader">
                <div class="weilin-comfyui-skin-preview" v-if="customSkinUrl">
                  <img :src="customSkinUrl" alt="Custom Skin Preview">
                </div>
              </div>
            </div>
            <div class="weilin-comfyui-setting-item" style="grid-column: span 2;">
              <label>{{ t('promptBox.settings.bgSetting') }}</label>
              <select v-model="bgType">
                <option value="gradient">{{ t('promptBox.settings.gradientBg') }}</option>
                <option value="transparent">{{ t('promptBox.settings.transparentBg') }}</option>
              </select>
            </div>
            <div class="weilin-comfyui-setting-item" v-if="bgType === 'gradient'" style="grid-column: span 2;">
              <label>{{ t('promptBox.settings.gradientColor') }}</label>
              <div style="display: flex; gap: 10px; align-items: center;">
                <input type="color" v-model="gradientColor1">
                <input type="color" v-model="gradientColor2">
                <button @click="resetGradientColors" style="margin-left: 10px;width: 200px;">
                  {{ t('promptBox.settings.resetToDefault') }}
                </button>
              </div>
            </div>
            <div class="weilin-comfyui-setting-item" style="grid-column: span 2;">
              <label>{{ t('promptBox.settings.borderRadius') }}</label>
              <input type="number" v-model.number="ballBorderRadius" min="0" max="50">
            </div>
            <button class="weilin-comfyui-save-button" style="grid-column: span 2;" @click="saveFloatingBallSettings">
              {{ t('promptBox.settings.save') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_prompt_box'">
          <h3>{{ t('promptBox.settings.setting_prompt_box') }}</h3>
          <div class="weilin-comfyui-floating-ball-settings">
            <div class="weilin-comfyui-setting-item">
              <label>
                <input type="checkbox" v-model="isCommaConversionEnabled" />
                {{ t('promptBox.settings.enableCommaConversion') }}
              </label>
            </div>
            <div class="weilin-comfyui-setting-item">
              <label>
                <input type="checkbox" v-model="isPeriodConversionEnabled" />
                {{ t('promptBox.settings.enablePeriodConversion') }}
              </label>
            </div>
            <div class="weilin-comfyui-setting-item">
              <label>
                <input type="checkbox" v-model="isBracketConversionEnabled" />
                {{ t('promptBox.settings.enableBracketConversion') }}
              </label>
            </div>
            <div class="weilin-comfyui-setting-item">
              <label>
                <input type="checkbox" v-model="isAngleBracketConversionEnabled" />
                {{ t('promptBox.settings.enableAngleBracketConversion') }}
              </label>
            </div>
            <div class="weilin-comfyui-setting-item">
              <label>
                <input type="checkbox" v-model="isUnderscoreToBracketEnabled" />
                {{ t('promptBox.settings.enableUnderscoreToBracket') }}
              </label>
            </div>
            <button class="weilin-comfyui-save-button" @click="savePromptBoxSettings">
              {{ t('promptBox.settings.save') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_openai_box'">
          <h3>{{ t('promptBox.settings.openaiSettings') }}</h3>
          <div class="weilin-comfyui-openai-settings">
            <div class="weilin-comfyui-setting-item">
              <label>{{ t('promptBox.settings.selectedOpenaiConfig') }}</label>
              <select v-model="selectedOpenaiIndex" @change="setOpenAiSelect">
                <option v-for="(item, index) in openaiSettings" :key="index" :value="index">
                  {{ item.model }} ({{ item.base_url }})
                </option>
              </select>
            </div>
            <div class="weilin-comfyui-config-list">
              <div v-for="(config, index) in openaiSettings" :key="index" class="weilin-comfyui-config-item">
                <div class="weilin-comfyui-config-header">
                  <span>{{ config.model }}</span>
                  <div class="weilin-comfyui-config-actions">
                    <button @click="toggleEditForm(index)">
                      {{ editingIndex === index ? t('promptBox.settings.cancel') : t('promptBox.settings.edit') }}
                    </button>
                    <button @click="deleteOpenaiConfig(index)">{{ t('promptBox.settings.delete') }}</button>
                  </div>
                </div>
                <div class="weilin-comfyui-config-form" v-if="editingIndex === index">
                  <div class="weilin-comfyui-form-group">
                    <label>{{ t('promptBox.settings.openai_api_key') }}:</label>
                    <input type="text" v-model="currentConfig.api_key"
                      :placeholder="t('promptBox.settings.openai_api_key_placeholder')" />
                  </div>
                  <div class="weilin-comfyui-form-group">
                    <label>{{ t('promptBox.settings.openai_base_url') }}:</label>
                    <input type="text" v-model="currentConfig.base_url"
                      :placeholder="t('promptBox.settings.openai_base_url_placeholder')" />
                  </div>
                  <div class="weilin-comfyui-form-group">
                    <label>{{ t('promptBox.settings.openai_model') }}:</label>
                    <input type="text" v-model="currentConfig.model"
                      :placeholder="t('promptBox.settings.openai_model_placeholder')" />
                  </div>
                  <div class="weilin-comfyui-form-actions">
                    <button @click="saveOpenaiConfig(index)">{{ t('promptBox.settings.save') }}</button>
                  </div>
                </div>
                <div class="weilin-comfyui-config-details" v-else>
                  <div>{{ t('promptBox.settings.openai_api_key') }}: {{ config.api_key ? '******' :
                    t('promptBox.settings.not_set') }}</div>
                  <div>{{ t('promptBox.settings.openai_base_url') }}: {{ config.base_url }}</div>
                </div>
              </div>
            </div>
            <div class="weilin-comfyui-config-form" v-if="showOpenaiForm">
              <div class="weilin-comfyui-form-group">
                <label>{{ t('promptBox.settings.openai_api_key') }}:</label>
                <input type="text" v-model="currentConfig.api_key"
                  :placeholder="t('promptBox.settings.openai_api_key_placeholder')" />
              </div>
              <div class="weilin-comfyui-form-group">
                <label>{{ t('promptBox.settings.openai_base_url') }}:</label>
                <input type="text" v-model="currentConfig.base_url"
                  :placeholder="t('promptBox.settings.openai_base_url_placeholder')" />
              </div>
              <div class="weilin-comfyui-form-group">
                <label>{{ t('promptBox.settings.openai_model') }}:</label>
                <input type="text" v-model="currentConfig.model"
                  :placeholder="t('promptBox.settings.openai_model_placeholder')" />
              </div>
              <div class="weilin-comfyui-form-actions">
                <button @click="cancelOpenaiConfig">{{ t('promptBox.settings.cancel') }}</button>
                <button @click="addOpenaiNewConfig">{{ t('promptBox.settings.save') }}</button>
              </div>
            </div>
            <button class="weilin-comfyui-add-button" @click="addOpenaiConfig" v-if="!showOpenaiForm">
              {{ t('promptBox.settings.addNewConfig') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_sponsor_me'">
          <h3>{{ t('promptBox.settings.setting_sponsor_me') }}</h3>
          <div class="weilin-comfyui-sponsor-me-settings">
            <h1>{{ t('promptBox.settings.sponsorMeTip') }}</h1>
            <h2>{{ t('promptBox.settings.sponsorMeLink') }}</h2>
            <button class="weilin-comfyui-sponsor-me-button" @click="sponsorMe">
              {{ t('promptBox.settings.sponsorMe') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_start_panel'">
          <h3>{{ t('promptBox.settings.setting_start_panel') }}</h3>
          <div class="weilin-comfyui-start-panel-settings">
            <h4>{{ t('promptBox.settings.startPanelTip') }}</h4>
            <button class="weilin-comfyui-start-panel-button" @click="startPanel">
              {{ t('promptBox.settings.startPanel') }}
            </button>
          </div>
        </div>
      </div>
    </div>
    <template #footer>
      <button @click="dialogVisible = false">{{ t('promptBox.settings.close') }}</button>
    </template>
  </Dialog>
</template>

<script setup>
import Dialog from '@/components/Dialog.vue'
import { ref, onMounted, onUnmounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { translatorApi } from '@/api/translator'
import { autocompleteApi } from '@/api/autocomplete'
import message from '@/utils/message'
import { languageApi } from '@/api/language'
import { openaiApi } from '@/api/openai'
import { translaterSerives, language } from "./translater"

const { t } = useI18n()

const dialogVisible = ref(false)
const selectedSetting = ref('translator')
const selectedTranslator = ref('baidu') // 默认选择的翻译器
const translationText = ref('') // 输入框内容
// 新增语言选择相关状态
const savedSourceLanguage = ref(localStorage.getItem('weilin_prompt_ui_sourceLanguage') || 'english');
const savedTargetLanguage = ref(localStorage.getItem('weilin_prompt_ui_targetLanguage') || 'chinese_simplified');

// 新增悬浮球设置相关状态
const savedFloatingBallCount = ref(localStorage.getItem('weilin_prompt_ui_floatingBallCount') || 1);
const savedFloatingBallSize = ref(localStorage.getItem('weilin_prompt_ui_floatingBallSize') || 66);
const savedFloatingBallHeight = ref(localStorage.getItem('weilin_prompt_ui_floatingBallHeightSize') || savedFloatingBallSize.value);
const isFloatingBallEnabled = ref(localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true');
const ballSkinType = ref(localStorage.getItem('weilin_prompt_ui_ballSkinType') || 'default')
const customSkinUrl = ref(localStorage.getItem('weilin_prompt_ui_customSkinUrl') || '')
const bgType = ref(localStorage.getItem('weilin_prompt_ui_bgType') || 'gradient')
const gradientColor1 = ref(localStorage.getItem('weilin_prompt_ui_gradientColor1') || '#6a11cb')
const gradientColor2 = ref(localStorage.getItem('weilin_prompt_ui_gradientColor2') || '#2575fc')
const ballBorderRadius = ref(localStorage.getItem('weilin_prompt_ui_ballBorderRadius') || 50)

// 提示词设置
const isCommaConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_comma_conversion') === 'true');
const isPeriodConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_period_conversion') === 'true');
const isBracketConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_bracket_conversion') === 'true');
const isAngleBracketConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion') === 'true');
const isUnderscoreToBracketEnabled = ref(localStorage.getItem('weilin_prompt_ui_underscore_to_bracket') === 'true');

// 翻译库设置
const selectedTranslatorService = ref('');
const sourceLanguage = ref('');
const targetLanguage = ref('');

// OpenAI 设置相关状态
const selectedOpenaiIndex = ref(0);
const openaiSettings = ref([]);
const showOpenaiForm = ref(false);
const currentConfig = ref({
  api_key: '',
  base_url: 'https://api.openai.com/v1',
  model: ''
});
const isEditing = ref(false);
const editingIndex = ref(-1);
const settingTranslater = ref('');

const installTranslater = ref(false)
const hasTranslaterPackage = ref(false)
const testTranslaterInputText = ref('')
const testTranslaterOutputText = ref('')

const saveAutoCompleteLimit = ref(25)
const saveAutoCompleteWidth = ref(localStorage.getItem('weilin_prompt_ui_auto_box_width') || 450);
const saveAutoCompleteHeight = ref(localStorage.getItem('weilin_prompt_ui_auto_box_height') || 350);

const selectSetting = (setting) => {
  selectedSetting.value = setting
  if (setting == "setting_auto_complete_limit") {
    getAutoCompleteSetting();
  }
}

const confirmTranslator = () => {
  // 处理确认翻译器的逻辑
  // console.log(`选择的翻译器: ${selectedTranslator.value}`)
  translatorApi
    .setTranslatorSetting({

    })
    .then((res) => {
      message({ type: "success", str: 'message.saveSuccess' });
    })
    .catch((err) => {
      message({ type: "warn", str: 'message.networkError' });
    });
}

const translate = () => {
  // 处理翻译逻辑
  // console.log(`翻译内容: ${translationText.value}`)
  translatorApi
    .translatorText({

    })
    .then((res) => {
      message({ type: "success", str: 'message.saveSuccess' });
    })
    .catch((err) => {
      message({ type: "warn", str: 'message.networkError' });
    });
}

const saveSettings = () => {
  dialogVisible.value = false
}


// 保存翻译设置
const saveTranslatorSettings = () => {
  // 将设置存储在 localStorage 中
  localStorage.setItem('weilin_prompt_ui_sourceLanguage', savedSourceLanguage.value);
  localStorage.setItem('weilin_prompt_ui_targetLanguage', savedTargetLanguage.value);
  window.parent.postMessage({ type: 'weilin_prompt_ui_translate_setting' }, '*');
  // 显示保存成功提示
  message({ type: "success", str: 'message.saveSuccess' });
}

// 添加皮肤上传处理函数
const handleSkinUpload = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = (e) => {
      customSkinUrl.value = e.target.result
      localStorage.setItem('weilin_prompt_ui_customSkinUrl', e.target.result)
    }
    reader.readAsDataURL(file)
  }
}

const resetGradientColors = () => {
  gradientColor1.value = '#6a11cb';
  gradientColor2.value = '#2575fc';
};

// 保存悬浮球设置
const saveFloatingBallSettings = () => {
  if (savedFloatingBallCount.value < 1 || savedFloatingBallSize.value < 5 || savedFloatingBallHeight.value < 5) {
    message({ type: "warn", str: 'message.error' });
    return;
  }
  // 将设置存储在 localStorage 中
  localStorage.setItem('weilin_prompt_ui_floatingBallEnabled', isFloatingBallEnabled.value);
  localStorage.setItem('weilin_prompt_ui_floatingBallCount', savedFloatingBallCount.value);
  localStorage.setItem('weilin_prompt_ui_floatingBallSize', savedFloatingBallSize.value);
  localStorage.setItem('weilin_prompt_ui_floatingBallHeightSize', savedFloatingBallHeight.value);
  localStorage.setItem('weilin_prompt_ui_ballSkinType', ballSkinType.value)
  localStorage.setItem('weilin_prompt_ui_bgType', bgType.value)
  localStorage.setItem('weilin_prompt_ui_gradientColor1', gradientColor1.value)
  localStorage.setItem('weilin_prompt_ui_gradientColor2', gradientColor2.value)
  localStorage.setItem('weilin_prompt_ui_ballBorderRadius', ballBorderRadius.value)
  localStorage.setItem('weilin_prompt_ui_floatingBallHeightSize', savedFloatingBallHeight.value)

  window.parent.postMessage({ type: 'weilin_prompt_ui_floating_ball_setting' }, '*');
  // 显示保存成功提示
  message({ type: "success", str: 'message.saveSuccess' });
}

// 保存提示词设置
const savePromptBoxSettings = () => {
  localStorage.setItem('weilin_prompt_ui_comma_conversion', isCommaConversionEnabled.value);
  localStorage.setItem('weilin_prompt_ui_period_conversion', isPeriodConversionEnabled.value);
  localStorage.setItem('weilin_prompt_ui_bracket_conversion', isBracketConversionEnabled.value);
  localStorage.setItem('weilin_prompt_ui_angle_bracket_conversion', isAngleBracketConversionEnabled.value);
  localStorage.setItem('weilin_prompt_ui_underscore_to_bracket', isUnderscoreToBracketEnabled.value);
  message({ type: "success", str: 'message.saveSuccess' });
};


// 加载 OpenAI 设置
const loadOpenaiSettings = () => {
  languageApi.getUserSetting().then(res => {
    openaiSettings.value = res.data.openai_settings;
    selectedOpenaiIndex.value = res.data.select_openai;
  })

};

// 添加新配置
const addOpenaiConfig = () => {
  currentConfig.value = {
    api_key: '',
    base_url: 'https://api.openai.com/v1',
    model: ''
  };
  isEditing.value = false;
  showOpenaiForm.value = true;
};

// 编辑配置
const editOpenaiConfig = (index) => {
  currentConfig.value = { ...openaiSettings.value[index] };
  isEditing.value = true;
  editingIndex.value = index;
  showOpenaiForm.value = true;
};

// 删除配置
const deleteOpenaiConfig = (index) => {
  openaiApi.deleteOpenAiSetting({
    index: index
  }).then(res => {
    loadOpenaiSettings()
    message({ type: "success", str: 'message.deleteSuccess' });
  }).catch(err => {
    message({ type: "warn", str: 'message.networkError' });
  })
};

// 切换编辑表单
const toggleEditForm = (index) => {
  if (editingIndex.value === index) {
    // 如果点击的是当前正在编辑的项，则取消编辑
    editingIndex.value = -1;
  } else {
    // 否则开始编辑该项
    currentConfig.value = { ...openaiSettings.value[index] };
    editingIndex.value = index;
  }
};

// 保存配置
const saveOpenaiConfig = (index) => {
  openaiApi.updateOpenAiSetting({
    index: index,
    ...currentConfig.value
  }).then(res => {
    loadOpenaiSettings()
    editingIndex.value = -1; // 保存后关闭编辑表单
    message({ type: "success", str: 'message.saveSuccess' });
  }).catch(err => {
    message({ type: "warn", str: 'message.networkError' });
  })
};

// 添加新配置
const addOpenaiNewConfig = () => {
  openaiApi.addOpenAiSetting({
    ...currentConfig.value
  }).then(res => {
    loadOpenaiSettings()
    showOpenaiForm.value = false;
    editingIndex.value = -1;
    message({ type: "success", str: 'message.saveSuccess' });
  }).catch(err => {
    message({ type: "warn", str: 'message.networkError' });
  })
};

// 取消编辑
const cancelOpenaiConfig = () => {
  showOpenaiForm.value = false;
  editingIndex.value = -1; // 保存后关闭编辑表单
};

// 设置选中
const setOpenAiSelect = () => {
  openaiApi.setOpenAiSelect({
    index: selectedOpenaiIndex.value
  }).then(res => {
    message({ type: "success", str: 'message.saveSuccess' });
  }).catch(err => {
    message({ type: "warn", str: 'message.networkError' });
  })
}

const sponsorMe = () => {
  window.open("https://afdian.com/a/weilin9999", '_blank');
}


// 启动面板
const startPanel = () => {
  languageApi.startPanel().then(res => {
    message({ type: "success", str: 'message.startPanelSuccess' });
  }).catch(err => {
    message({ type: "warn", str: 'message.startPanelFailed' });
  })
};


const getTranskatePackagesState = () => {
  translatorApi.getTranslatePackagesState().then(res => {
    // console.log(res)
    if (res.info == "ok") {
      hasTranslaterPackage.value = true;
    } else {
      hasTranslaterPackage.value = false;
    }
  }).catch(err => {
    message({ type: "warn", str: 'message.getTranslaterFail' });
  })
};

const getTranskateSetting = () => {
  translatorApi.getTranslateSetting().then(res => {
    // console.log(res)
    localStorage.setItem('weilin_prompt_ui_translater_setting', res.data);
    settingTranslater.value = res.data;
  }).catch(err => {
    message({ type: "warn", str: 'message.getTranslaterFail' });
  })
};

const applyTranslaterSetting = () => {
  translatorApi.applyTranslateSetting(settingTranslater.value).then(res => {
    // console.log(res)
    if (res.info == "ok") {
      localStorage.setItem('weilin_prompt_ui_translater_setting', settingTranslater.value);
      message({ type: "success", str: 'message.applyTranslaterSuccess' });
    } else {
      message({ type: "warn", str: 'message.applyToTranslaterFail' });
    }
  }).catch(err => {
    message({ type: "warn", str: 'message.applyTranslaterFail' });
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
  translatorApi.translaterInputText(testTranslaterInputText.value).then(res => {
    // console.log(res)
    testTranslaterOutputText.value = res.text;
  }).catch(err => {
    message({ type: "warn", str: 'message.translaterTestFail' });
  })
};

const installCheckInterval = ref(null);

const installTranslaterPackage = () => {
  installTranslater.value = true;
  translatorApi.installTranslatePackage().then(res => {
    installTranslater.value = false;
    hasTranslaterPackage.value = true;
    // console.log(res)
    message({ type: "success", str: 'message.tranlaterPackageInstallSuccess' });
  }).catch(err => {
    installTranslater.value = false;
    message({ type: "warn", str: 'message.tranlaterPackageInstallFail' });
  })
  // 开始定时检查
  // installTranslater.value = true;
  //   installCheckInterval.value = setInterval(() => {
  //     checkTranskatePackagesState();
  // }, 1000);
};

const checkTranskatePackagesState = () => {
  translatorApi.getTranslatePackagesState().then(res => {
    // console.log(res)
    if (res.info == "ok") {
      hasTranslaterPackage.value = true;
      // 停止定时器
      if (installCheckInterval.value) {
        clearInterval(installCheckInterval.value);
        installCheckInterval.value = null;
      }
      message({ type: "success", str: 'message.tranlaterPackageInstallSuccess' });
    } else {
      hasTranslaterPackage.value = false;
    }
  }).catch(err => {
    installTranslater.value = false;
    // 出错时也停止定时器
    if (installCheckInterval.value) {
      clearInterval(installCheckInterval.value);
      installCheckInterval.value = null;
    }
    message({ type: "warn", str: 'message.getTranslaterFail' });
  })
};


const getAutoCompleteSetting = async () => {
  await autocompleteApi.getAutocompleteLimit().then(res => {
    saveAutoCompleteLimit.value = res.data
  }).catch(err => {
    console.error(err)
    message({ type: "warn", str: 'message.networkError' });
  })
};

const saveAutoCompleteSetting = async () => {
  await autocompleteApi.updateAutocompleteLimit(saveAutoCompleteLimit.value).then(res => {
    message({ type: "success", str: 'message.saveSuccess' });
    localStorage.setItem('weilin_prompt_ui_auto_box_width', saveAutoCompleteWidth.value);
    localStorage.setItem('weilin_prompt_ui_auto_box_height', saveAutoCompleteHeight.value);
  }).catch(err => {
    console.error(err)
    message({ type: "warn", str: 'message.networkError' });
  })
}

// 初始化时加载设置
onMounted(() => {
  getTranskateBuktSetting();
  getTranskatePackagesState();
  getTranskateSetting();
  loadOpenaiSettings();
});

// 在组件卸载时清理定时器
onUnmounted(() => {
  if (installCheckInterval.value) {
    clearInterval(installCheckInterval.value);
  }
});


defineExpose({
  open: () => {
    selectedSetting.value = 'translator'
    selectedTranslator.value = 'baidu' // 默认选择的翻译器
    translationText.value = '' // 输入框内容
    // 新增语言选择相关状态
    savedSourceLanguage.value = localStorage.getItem('weilin_prompt_ui_sourceLanguage') || 'english';
    savedTargetLanguage.value = localStorage.getItem('weilin_prompt_ui_targetLanguage') || 'chinese_simplified';
    // 新增悬浮球设置相关状态
    savedFloatingBallCount.value = localStorage.getItem('weilin_prompt_ui_floatingBallCount') || 1;
    savedFloatingBallSize.value = localStorage.getItem('weilin_prompt_ui_floatingBallSize') || 5;
    isFloatingBallEnabled.value = localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true';
    // 提示词设置
    isCommaConversionEnabled.value = localStorage.getItem('weilin_prompt_ui_comma_conversion') === 'true';
    isPeriodConversionEnabled.value = localStorage.getItem('weilin_prompt_ui_period_conversion') === 'true';
    isBracketConversionEnabled.value = localStorage.getItem('weilin_prompt_ui_bracket_conversion') === 'true';
    isAngleBracketConversionEnabled.value = localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion') === 'true';
    isUnderscoreToBracketEnabled.value = localStorage.getItem('weilin_prompt_ui_underscore_to_bracket') === 'true';

    dialogVisible.value = true
  }
})
</script>

<style scoped>
.weilin-comfyui-settings-content {
  display: flex;
  min-width: 700px;
  background: var(--weilin-prompt-ui-gradient-bg);
  color: var(--weilin-prompt-ui-primary-text);
  border-radius: var(--weilin-prompt-ui-border-radius, 18px);
  box-shadow: var(--weilin-prompt-ui-box-shadow);
  padding: 18px 0;
}

.weilin-comfyui-settings-sidebar {
  width: 220px;
  border-right: 1px solid var(--weilin-prompt-ui-border-color);
  padding: 18px 0 18px 18px;
  background: var(--weilin-prompt-ui-gradient-bg);
  border-radius: 16px 0 0 16px;
  box-shadow: 2px 0 12px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-settings-sidebar ul {
  list-style-type: none;
  padding: 0;
}

.weilin-comfyui-settings-sidebar li {
  cursor: pointer;
  padding: 12px 18px;
  margin-bottom: 8px;
  border-radius: 8px;
  transition: background 0.3s, color 0.3s;
  font-weight: 500;
  font-size: 16px;
  color: var(--weilin-prompt-ui-title-color);
  letter-spacing: 0.5px;
}

.weilin-comfyui-settings-sidebar li:hover {
  background: var(--weilin-prompt-ui-hover-bg-color);
  color: var(--weilin-prompt-ui-label-color);
}

.weilin-comfyui-settings-sidebar .weilin-comfyui-active {
  background: var(--weilin-prompt-ui-gradient-primary);
  color: #fff;
  box-shadow: 0 2px 8px 0 var(--weilin-prompt-ui-btn-shadow);
}

.weilin-comfyui-settings-main {
  flex: 1;
  padding: 0 32px;
}

.weilin-comfyui-settings-main h3 {
  margin-top: 0;
  font-size: 22px;
  font-weight: 700;
  color: var(--weilin-prompt-ui-title-color);
  margin-bottom: 18px;
}

.weilin-comfyui-translator-settings,
.weilin-comfyui-floating-ball-settings {
  display: flex;
  align-items: stretch;
  margin-bottom: 20px;
  flex-direction: column;
  gap: 10px;
}

.weilin-comfyui-translator-settings select {
  margin-right: 10px;
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

.weilin-comfyui-setting-select {
  margin-bottom: 20px;
  background: var(--weilin-prompt-ui-card-bg);
  border-radius: 8px;
  padding: 12px 18px;
  box-shadow: 0 1px 4px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-group-box {
  padding: 20px;
  border: 1px solid var(--weilin-prompt-ui-card-border);
  border-radius: 10px;
  margin-bottom: 20px;
  background: var(--weilin-prompt-ui-primary-bg);
  box-shadow: 0 1px 8px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-group-title {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 16px;
  color: var(--weilin-prompt-ui-title-color);
}

.weilin-comfyui-note-top {
  margin: 10px 0;
  padding: 8px 12px;
  background: #e8f4ff;
  border: 1px solid #b3d8ff;
  border-radius: 6px;
  font-size: 13px;
  color: #004085;
  word-break: break-all;
}

.weilin-comfyui-tranlater-text-box {
  margin-top: 20px;
  padding: 16px;
  background: var(--weilin-prompt-ui-card-bg);
  border-radius: 10px;
  border: 1px solid var(--weilin-prompt-ui-card-border);
  box-shadow: 0 1px 8px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-tranlater-text-box .weilin-comfyui-setting-item {
  margin-bottom: 12px;
}

.weilin-comfyui-tranlater-text-box .weilin-comfyui-setting-item label {
  display: block;
  margin-bottom: 4px;
  font-size: 14px;
  color: var(--weilin-prompt-ui-label-color);
}

.weilin-comfyui-tranlater-text-box .weilin-comfyui-setting-item input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--weilin-prompt-ui-input-border);
  border-radius: 6px;
  background-color: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-label-color);
  transition: border-color 0.2s;
}

.weilin-comfyui-tranlater-text-box .weilin-comfyui-setting-item input:focus {
  outline: none;
  border-color: var(--weilin-prompt-ui-input-focus);
}

.weilin-comfyui-tranlater-text-box .weilin-comfyui-install-button {
  width: 100%;
  margin-top: 8px;
  padding: 8px 16px;
  background: var(--weilin-prompt-ui-btn-gradient);
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.weilin-comfyui-tranlater-text-box .weilin-comfyui-install-button:hover {
  background: var(--weilin-prompt-ui-btn-gradient-hover);
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

.weilin-comfyui-setting-small-titile {
  font-size: 16px;
  font-weight: 600;
  color: var(--weilin-prompt-ui-title-color);
  margin-bottom: 16px;
  padding-bottom: 8px;
  border-bottom: 1px solid var(--weilin-prompt-ui-card-border);
}

.weilin-comfyui-common-select {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--weilin-prompt-ui-input-border);
  border-radius: 6px;
  background-color: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-label-color);
  font-size: 14px;
  transition: border-color 0.2s;
}

.weilin-comfyui-common-select:focus {
  outline: none;
  border-color: var(--weilin-prompt-ui-input-focus);
}

.weilin-comfyui-skin-preview {
  max-width: 200px;
  max-height: 300px;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: var(--weilin-prompt-ui-btn-shadow);
  margin-top: 8px;
}

.weilin-comfyui-skin-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.weilin-comfyui-settings-column {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.weilin-comfyui-openai-settings {
  max-width: 800px;
  margin: 0 auto;
  background: var(--weilin-prompt-ui-card-bg);
  border-radius: var(--weilin-prompt-ui-border-radius);
  padding: 18px;
  box-shadow: var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-config-list {
  margin-top: 20px;
}

.weilin-comfyui-config-item {
  border: 1px solid var(--weilin-prompt-ui-card-border);
  border-radius: 8px;
  padding: 14px;
  margin-bottom: 12px;
  background: var(--weilin-prompt-ui-primary-bg);
  box-shadow: 0 1px 6px 0 var(--weilin-prompt-ui-card-shadow);
}

.weilin-comfyui-config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.weilin-comfyui-config-actions button {
  margin-left: 5px;
  padding: 4px 12px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-input-border);
  cursor: pointer;
  background: var(--weilin-prompt-ui-card-bg);
  color: var(--weilin-prompt-ui-label-color);
  font-weight: 500;
  transition: background 0.2s;
}

.weilin-comfyui-config-actions button:hover {
  background: var(--weilin-prompt-ui-gradient-primary);
  color: #fff;
}

.weilin-comfyui-config-details {
  font-size: 0.95em;
  color: var(--weilin-prompt-ui-secondary-text);
  padding-left: 8px;
}

.weilin-comfyui-config-form {
  margin-top: 10px;
  padding: 10px;
  background: var(--weilin-prompt-ui-primary-bg);
  border-radius: 8px;
}

.weilin-comfyui-form-group {
  margin-bottom: 10px;
}

.weilin-comfyui-form-group label {
  display: block;
  margin-bottom: 5px;
  color: var(--weilin-prompt-ui-label-color);
}

.weilin-comfyui-form-group input {
  width: 100%;
  padding: 7px;
  border-radius: 6px;
  border: 1px solid var(--weilin-prompt-ui-input-border);
  background: var(--weilin-prompt-ui-input-bg);
  color: var(--weilin-prompt-ui-label-color);
}

.weilin-comfyui-form-actions {
  text-align: right;
  margin-top: 10px;
}

.weilin-comfyui-add-button {
  margin-top: 20px;
  width: 100%;
  padding: 10px;
  background: var(--weilin-prompt-ui-btn-gradient);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 16px;
  box-shadow: var(--weilin-prompt-ui-btn-shadow);
  transition: background 0.2s;
}

.weilin-comfyui-add-button:hover {
  background: var(--weilin-prompt-ui-btn-gradient-hover);
}

.weilin-comfyui-sponsor-me-settings {
  background: var(--weilin-prompt-ui-card-bg);
  border-radius: var(--weilin-prompt-ui-border-radius);
  padding: 18px;
  box-shadow: var(--weilin-prompt-ui-card-shadow);
  text-align: center;
}

.weilin-comfyui-sponsor-me-button {
  margin-top: 18px;
  padding: 12px 32px;
  background: var(--weilin-prompt-ui-btn-gradient);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 18px;
  box-shadow: var(--weilin-prompt-ui-btn-shadow);
  transition: background 0.2s;
}

.weilin-comfyui-sponsor-me-button:hover {
  background: var(--weilin-prompt-ui-btn-gradient-hover);
}

.weilin-comfyui-start-panel-settings {
  background: var(--weilin-prompt-ui-card-bg);
  border-radius: var(--weilin-prompt-ui-border-radius);
  padding: 18px;
  box-shadow: var(--weilin-prompt-ui-card-shadow);
  text-align: center;
}

.weilin-comfyui-start-panel-button {
  margin-top: 18px;
  padding: 12px 32px;
  background: var(--weilin-prompt-ui-btn-gradient);
  color: #fff;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 18px;
  box-shadow: var(--weilin-prompt-ui-btn-shadow);
  transition: background 0.2s;
}

.weilin-comfyui-start-panel-button:hover {
  background: var(--weilin-prompt-ui-btn-gradient-hover);
}

/* 其他原有样式全部注释或删除，已全部重命名和美化 */
</style>