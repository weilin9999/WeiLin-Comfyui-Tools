<template>
  <Dialog v-model="dialogVisible" :title="t('promptBox.settings.title')">
    <div class="settings-content">
      <div class="settings-sidebar">
        <ul>
          <li :class="{ active: selectedSetting === 'translator' }" @click="selectSetting('translator')">{{
            t('promptBox.settings.translator') }}</li>
          <li :class="{ active: selectedSetting === 'setting_floating_ball' }"
            @click="selectSetting('setting_floating_ball')">{{
              t('promptBox.settings.setting_floating_ball') }}</li>
          <li :class="{ active: selectedSetting === 'setting_prompt_box' }"
            @click="selectSetting('setting_prompt_box')">{{
              t('promptBox.settings.setting_prompt_box') }}</li>
          <li :class="{ active: selectedSetting === 'setting_openai_box' }"
            @click="selectSetting('setting_openai_box')">{{
              t('promptBox.settings.setting_openai_box') }}</li>
          <!-- <li :class="{ active: selectedSetting === 'setting_start_panel' }"
            @click="selectSetting('setting_start_panel')">{{
              t('promptBox.settings.setting_start_panel') }}</li> -->
          <li :class="{ active: selectedSetting === 'setting_sponsor_me' }"
            @click="selectSetting('setting_sponsor_me')">{{
              t('promptBox.settings.setting_sponsor_me') }}</li>
        </ul>
      </div>
      <div class="settings-main">
        <div v-if="selectedSetting === 'translator'">
          <h3>{{ t('promptBox.settings.translator') }}</h3>
          <div class="translator-settings">
            <!-- 选择源语言 -->
            <div class="setting-item">
              <label>{{ t('promptBox.settings.sourceLanguage') }}</label>
              <select v-model="savedSourceLanguage">
                <option value="auto">{{ t('promptBox.settings.auto_detect') }}</option>
                <option value="chinese_simplified">{{ t('promptBox.settings.chinese_simplified') }}</option>
                <option value="english">{{ t('promptBox.settings.english') }}</option>
              </select>
            </div>

            <!-- 选择目标语言 -->
            <div class="setting-item">
              <label>{{ t('promptBox.settings.targetLanguage') }}</label>
              <select v-model="savedTargetLanguage">
                <option value="chinese_simplified">{{ t('promptBox.settings.chinese_simplified') }}</option>
                <option value="english">{{ t('promptBox.settings.english') }}</option>
              </select>
            </div>

            <!-- 保存按钮 -->
            <button class="save-button" @click="saveTranslatorSettings">
              {{ t('promptBox.settings.save') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_floating_ball'">
          <h3>{{ t('promptBox.settings.setting_floating_ball') }}</h3>
          <div class="floating-ball-settings">

            <!-- 是否启用悬浮球 -->
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="isFloatingBallEnabled" />
                {{ t('promptBox.settings.enableFloatingBall') }}
              </label>
            </div>
            <!-- 悬浮球数量 -->
            <div class="setting-item">
              <label>{{ t('promptBox.settings.floatingBallCount') }}</label>
              <input type="number" v-model.number="savedFloatingBallCount" min="1" max="20" style="width: 100px;"
                :placeholder="t('promptBox.settings.floatingBallCountPlaceholder')" />
            </div>

            <!-- 悬浮球大小 -->
            <div class="setting-item">
              <label>{{ t('promptBox.settings.floatingBallSize') }}</label>
              <input type="number" v-model.number="savedFloatingBallSize" min="66" max="500" style="width: 100px;"
                :placeholder="t('promptBox.settings.floatingBallSizePlaceholder')" />
            </div>

            <!-- 保存按钮 -->
            <button class="save-button" @click="saveFloatingBallSettings">
              {{ t('promptBox.settings.save') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_prompt_box'">
          <h3>{{ t('promptBox.settings.setting_prompt_box') }}</h3>
          <div class="floating-ball-settings">

            <!-- 是否启用全角逗号转半角逗号 -->
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="isCommaConversionEnabled" />
                {{ t('promptBox.settings.enableCommaConversion') }}
              </label>
            </div>
            <!-- 是否启用全角句号转半角句号 -->
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="isPeriodConversionEnabled" />
                {{ t('promptBox.settings.enablePeriodConversion') }}
              </label>
            </div>
            <!-- 是否启用全角括号转半角括号 -->
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="isBracketConversionEnabled" />
                {{ t('promptBox.settings.enableBracketConversion') }}
              </label>
            </div>
            <!-- 是否启用全角尖括号转半角尖括号 -->
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="isAngleBracketConversionEnabled" />
                {{ t('promptBox.settings.enableAngleBracketConversion') }}
              </label>
            </div>

            <!-- 是否启用下划线替换成括号 -->
            <div class="setting-item">
              <label>
                <input type="checkbox" v-model="isUnderscoreToBracketEnabled" />
                {{ t('promptBox.settings.enableUnderscoreToBracket') }}
              </label>
            </div>

            <!-- 保存按钮 -->
            <button class="save-button" @click="savePromptBoxSettings">
              {{ t('promptBox.settings.save') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_openai_box'">
          <h3>{{ t('promptBox.settings.openaiSettings') }}</h3>
          <div class="openai-settings">
            <!-- 当前选择的 OpenAI 配置 -->
            <div class="setting-item">
              <label>{{ t('promptBox.settings.selectedOpenaiConfig') }}</label>
              <select v-model="selectedOpenaiIndex" @change="setOpenAiSelect">
                <option v-for="(item, index) in openaiSettings" :key="index" :value="index">
                  {{ item.model }} ({{ item.base_url }})
                </option>
              </select>
            </div>

            <!-- 配置列表 -->
            <div class="config-list">
              <div v-for="(config, index) in openaiSettings" :key="index" class="config-item">
                <div class="config-header">
                  <span>{{ config.model }}</span>
                  <div class="config-actions">
                    <button @click="toggleEditForm(index)">
                      {{ editingIndex === index ? t('promptBox.settings.cancel') : t('promptBox.settings.edit') }}
                    </button>
                    <button @click="deleteOpenaiConfig(index)">{{ t('promptBox.settings.delete') }}</button>
                  </div>
                </div>

                <!-- 编辑表单 -->
                <div class="config-form" v-if="editingIndex === index">
                  <div class="form-group">
                    <label>{{ t('promptBox.settings.openai_api_key') }}:</label>
                    <input type="text" v-model="currentConfig.api_key"
                      :placeholder="t('promptBox.settings.openai_api_key_placeholder')" />
                  </div>
                  <div class="form-group">
                    <label>{{ t('promptBox.settings.openai_base_url') }}:</label>
                    <input type="text" v-model="currentConfig.base_url"
                      :placeholder="t('promptBox.settings.openai_base_url_placeholder')" />
                  </div>
                  <div class="form-group">
                    <label>{{ t('promptBox.settings.openai_model') }}:</label>
                    <input type="text" v-model="currentConfig.model"
                      :placeholder="t('promptBox.settings.openai_model_placeholder')" />
                  </div>
                  <div class="form-actions">
                    <button @click="saveOpenaiConfig(index)">{{ t('promptBox.settings.save') }}</button>
                  </div>
                </div>

                <!-- 配置详情 -->
                <div class="config-details" v-else>
                  <div>{{ t('promptBox.settings.openai_api_key') }}: {{ config.api_key ? '******' :
                    t('promptBox.settings.not_set') }}</div>
                  <div>{{ t('promptBox.settings.openai_base_url') }}: {{ config.base_url }}</div>
                </div>
              </div>
            </div>

            <!-- 新增/编辑表单 -->
            <div class="config-form" v-if="showOpenaiForm">
              <div class="form-group">
                <label>{{ t('promptBox.settings.openai_api_key') }}:</label>
                <input type="text" v-model="currentConfig.api_key"
                  :placeholder="t('promptBox.settings.openai_api_key_placeholder')" />
              </div>
              <div class="form-group">
                <label>{{ t('promptBox.settings.openai_base_url') }}:</label>
                <input type="text" v-model="currentConfig.base_url"
                  :placeholder="t('promptBox.settings.openai_base_url_placeholder')" />
              </div>
              <div class="form-group">
                <label>{{ t('promptBox.settings.openai_model') }}:</label>
                <input type="text" v-model="currentConfig.model"
                  :placeholder="t('promptBox.settings.openai_model_placeholder')" />
              </div>
              <div class="form-actions">
                <button @click="cancelOpenaiConfig">{{ t('promptBox.settings.cancel') }}</button>
                <button @click="addOpenaiNewConfig">{{ t('promptBox.settings.save') }}</button>
              </div>
            </div>

            <!-- 新增按钮 -->
            <button class="add-button" @click="addOpenaiConfig" v-if="!showOpenaiForm">
              {{ t('promptBox.settings.addNewConfig') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_sponsor_me'">
          <h3>{{ t('promptBox.settings.setting_sponsor_me') }}</h3>
          <div class="sponsor-me-settings">
            <h1>{{ t('promptBox.settings.sponsorMeTip') }}</h1>
            <h2>{{ t('promptBox.settings.sponsorMeLink') }}</h2>
            <button class="sponsor-me-button" @click="sponsorMe">
              {{ t('promptBox.settings.sponsorMe') }}
            </button>
          </div>
        </div>
        <div v-if="selectedSetting === 'setting_start_panel'">
          <h3>{{ t('promptBox.settings.setting_start_panel') }}</h3>
          <div class="start-panel-settings">
            <h4>{{ t('promptBox.settings.startPanelTip') }}</h4>
            <button class="start-panel-button" @click="startPanel">
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
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { translatorApi } from '@/api/translator'
import message from '@/utils/message'
import { languageApi } from '@/api/language'
import { openaiApi } from '@/api/openai'

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
const isFloatingBallEnabled = ref(localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true');
// 提示词设置
const isCommaConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_comma_conversion') === 'true');
const isPeriodConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_period_conversion') === 'true');
const isBracketConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_bracket_conversion') === 'true');
const isAngleBracketConversionEnabled = ref(localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion') === 'true');
const isUnderscoreToBracketEnabled = ref(localStorage.getItem('weilin_prompt_ui_underscore_to_bracket') === 'true');

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


const selectSetting = (setting) => {
  selectedSetting.value = setting
}

const confirmTranslator = () => {
  // 处理确认翻译器的逻辑
  console.log(`选择的翻译器: ${selectedTranslator.value}`)
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
  console.log(`翻译内容: ${translationText.value}`)
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

// 保存悬浮球设置
const saveFloatingBallSettings = () => {
  if (savedFloatingBallCount.value < 1 || savedFloatingBallSize.value < 66) {
    message({ type: "warn", str: 'message.error' });
    return;
  }
  // 将设置存储在 localStorage 中
  localStorage.setItem('weilin_prompt_ui_floatingBallEnabled', isFloatingBallEnabled.value);
  localStorage.setItem('weilin_prompt_ui_floatingBallCount', savedFloatingBallCount.value);
  localStorage.setItem('weilin_prompt_ui_floatingBallSize', savedFloatingBallSize.value);
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

// 初始化时加载设置
onMounted(() => {
  loadOpenaiSettings();
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
    savedFloatingBallSize.value = localStorage.getItem('weilin_prompt_ui_floatingBallSize') || 66;
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
.settings-content {
  display: flex;
  min-width: 600px;
  background-color: var(--weilin-prompt-ui-primary-bg);
  color: var(--weilin-prompt-ui-primary-text);
}

.settings-sidebar {
  width: 200px;
  border-right: 1px solid var(--weilin-prompt-ui-border-color);
  padding-right: 10px;
  background-color: var(--weilin-prompt-ui-secondary-bg);
}

.settings-sidebar ul {
  list-style-type: none;
  padding: 0;
}

.settings-sidebar li {
  cursor: pointer;
  padding: 10px;
  transition: background-color 0.3s;
}

.settings-sidebar li:hover {
  background-color: var(--weilin-prompt-ui-hover-bg-color);
}

.settings-sidebar li.active {
  background-color: var(--weilin-prompt-ui-primary-color);
  color: white;
}

.settings-main {
  flex: 1;
  padding-left: 20px;
}

.settings-main h3 {
  margin-top: 0;
}

.translator-settings,
.floating-ball-settings {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  flex-direction: column;
}

.translator-settings select {
  margin-right: 10px;
}

.translation-input {
  display: flex;
  align-items: center;
}

.translation-input input {
  flex: 1;
  margin-right: 10px;
}


.setting-item {
  margin-bottom: 20px;
}

.setting-item label {
  display: block;
  margin-bottom: 8px;
  font-weight: 500;
}

.setting-item select {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  background-color: var(--weilin-prompt-ui-primary-bg);
  color: var(--weilin-prompt-ui-primary-text);
}

.save-button {
  width: 100%;
  padding: 10px;
  background-color: var(--weilin-prompt-ui-primary-color);
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.2s;
}

.save-button:hover {
  background-color: var(--weilin-prompt-ui-primary-color-hover);
}


#weilin_comfyui_tools_prompt_ui_div button {
  margin-left: 8px;
  padding: 6px 12px;
  border-radius: 4px;
  border: 1px solid var(--weilin-prompt-ui-border-color);
  cursor: pointer;
  background-color: var(--weilin-prompt-ui-button-bg);
  color: var(--weilin-prompt-ui-button-text);
}

#weilin_comfyui_tools_prompt_ui_div button:last-child {
  background: var(--weilin-prompt-ui-primary-color);
  color: white;
  border-color: var(--weilin-prompt-ui-primary-color);
}

.openai-settings {
  max-width: 800px;
  margin: 0 auto;
}

.config-list {
  margin-top: 20px;
}

.config-item {
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.config-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.config-actions button {
  margin-left: 5px;
  padding: 2px 8px;
}

.config-details {
  font-size: 0.9em;
  color: var(--weilin-prompt-ui-secondary-text);
}

.config-item {
  border: 1px solid var(--weilin-prompt-ui-border-color);
  border-radius: 4px;
  padding: 10px;
  margin-bottom: 10px;
}

.config-form {
  margin-top: 10px;
  padding: 10px;
  background-color: var(--weilin-prompt-ui-bg-light);
  border-radius: 4px;
}

.form-group {
  margin-bottom: 10px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 5px;
}

.form-actions {
  text-align: right;
  margin-top: 10px;
}

.add-button {
  margin-top: 20px;
  width: 100%;
  padding: 8px;
}

.start-panel-button.loading {
  position: relative;
  pointer-events: none;
  opacity: 0.8;
}

.start-panel-button.loading::after {
  content: "";
  position: absolute;
  width: 16px;
  height: 16px;
  top: 50%;
  left: 50%;
  margin: -8px 0 0 -8px;
  border: 2px solid #fff;
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>