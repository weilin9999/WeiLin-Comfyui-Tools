<template>
  <div id="weilin_comfyui_tools_prompt_ui_div">
    <!-- 提示词窗口 -->
    <DraggableWindow name="promptBox" v-if="windows.prompt.visible"
      :title="promptManager === 'prompt' ? t('promptBox.windowTitle') : t('promptBox.windowTitleGlobal')"
      :position="windows.prompt.position" :size="windows.prompt.size" :z-index="windowManager.getZIndex('prompt')"
      @update:position="updatePosition('prompt', $event)" @update:size="updateSize('prompt', $event)"
      @active="windowManager.setActiveWindow('prompt')" @close="closeWindow('prompt')">
      <PromptBox :promptManager="promptManager" :hasPromptLoraStack="hasPromptLoraStack" ref="promptBoxRef" />
    </DraggableWindow>

    <!-- Tag管理窗口 -->
    <DraggableWindow name="tagManager" v-if="windows.tag.visible" :title="t('tagManager.windowTitle')"
      :position="windows.tag.position" :size="windows.tag.size" :z-index="windowManager.getZIndex('tag')"
      @update:position="updatePosition('tag', $event)" @update:size="updateSize('tag', $event)"
      @active="windowManager.setActiveWindow('tag')" @close="closeWindow('tag')">
      <TagManager :tagManager="tagManager" />
    </DraggableWindow>

    <!-- Lora管理窗口 -->
    <DraggableWindow name="loraManager" v-if="windows.lora.visible" :title="t('loraManager.windowTitle')"
      :position="windows.lora.position" :size="windows.lora.size" :z-index="windowManager.getZIndex('lora')"
      @update:position="updatePosition('lora', $event)" @update:size="updateSize('lora', $event)"
      @active="windowManager.setActiveWindow('lora')" @close="closeWindow('lora')">
      <LoraManager :loraManager="loraManager" ref="loraManagerRef" />
    </DraggableWindow>

    <!-- 历史记录窗口  -->
    <DraggableWindow name="historyManager" v-if="windows.history.visible" :title="t('history.windowTitle')"
      :position="windows.history.position" :size="windows.history.size" :z-index="windowManager.getZIndex('history')"
      @update:position="updatePosition('history', $event)" @update:size="updateSize('history', $event)"
      @active="windowManager.setActiveWindow('history')" @close="closeWindow('history')">
      <HistoryManager />
    </DraggableWindow>

    <!-- AI窗口 -->
    <DraggableWindow name="aiWindow" v-if="windows.ai_window.visible" :title="t('aiWindow.windowTitle')"
      :position="windows.ai_window.position" :size="windows.ai_window.size"
      :z-index="windowManager.getZIndex('ai_window')" @update:position="updatePosition('ai_window', $event)"
      @update:size="updateSize('ai_window', $event)" @active="windowManager.setActiveWindow('ai_window')"
      @close="closeWindow('ai_window')">
      <AiWindow />
    </DraggableWindow>

    <!-- 节点列表快捷窗口 -->
    <DraggableWindow name="nodeListWindow" v-if="windows.node_list_window.visible"
      :title="t('nodeListWindow.windowTitle')" :position="windows.node_list_window.position"
      :size="windows.node_list_window.size" :z-index="windowManager.getZIndex('node_list_window')"
      @update:position="updatePosition('node_list_window', $event)"
      @update:size="updateSize('node_list_window', $event)" @active="windowManager.setActiveWindow('node_list_window')"
      @close="closeWindow('node_list_window')">
      <NodeListWindow />
    </DraggableWindow>

    <!-- 云仓库窗口 -->
    <DraggableWindow name="cloudWindow" v-if="windows.cloud_window.visible" :title="t('cloudWindow.windowTitle')"
      :position="windows.cloud_window.position" :size="windows.cloud_window.size"
      :z-index="windowManager.getZIndex('cloud_window')" @update:position="updatePosition('cloud_window', $event)"
      @update:size="updateSize('cloud_window', $event)" @active="windowManager.setActiveWindow('cloud_window')"
      @close="closeWindow('cloud_window')">
      <CloudWindow />
    </DraggableWindow>

    <!-- Lora堆窗口 -->
    <DraggableWindow name="loraStackWindow" v-if="windows.lora_stack_window.visible" :title="t('controls.loraStack')"
      :position="windows.lora_stack_window.position" :size="windows.lora_stack_window.size"
      :z-index="windowManager.getZIndex('lora_stack_window')"
      @update:position="updatePosition('lora_stack_window', $event)"
      @update:size="updateSize('lora_stack_window', $event)"
      @active="windowManager.setActiveWindow('lora_stack_window')" @close="closeWindow('lora_stack_window')">
      <LoraStackWindow ref="loraStackRef" />
    </DraggableWindow>

    <!-- 悬浮球 -->
    <FloatingBall v-if="isFloatingBallEnabled"></FloatingBall>
    <loraDetail ref="loraDetailLoraStackRef" />

    <!-- 版本更新提示 -->
    <div v-if="showVersionUpdate" class="version-update-notification">
      <div class="version-update-content">
        <span>{{ versionUpdateMessage }}</span>
        <div class="version-update-actions">
          <button class="goto-github-btn" @click="goToGitHub">前往GitHub</button>
          <button class="close-version-update" @click="closeVersionUpdate">×</button>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import DraggableWindow from '@/components/DraggableWindow.vue'
import PromptBox from './view/prompt_box/prompt_index.vue'
import TagManager from './view/tag_manager/tag_index.vue'
import LoraManager from './view/lora_manager/lora_index.vue'
import HistoryManager from './view/history_manager/history_index.vue'
import { windowManager } from '@/utils/windowManager'
import FloatingBall from '@/components/FloatingBall.vue';
import { useTagStore } from '@/stores/tagStore';
import AiWindow from '@/view/ai_window/ai_window.vue'
import NodeListWindow from '@/view/node_list/index.vue'
import CloudWindow from '@/view/cloud/index.vue'
import LoraStackWindow from '@/view/lora_manager/lora_stack.vue'
import { translatorApi } from '@/api/translator'
import { tagsApi } from '@/api/tags'
import loraDetail from '@/view/lora_manager/lora_detail.vue'
import { version as localVersion } from './utils/version'

const tagStore = useTagStore();

const isFloatingBallEnabled = ref(localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true');
if (!localStorage.getItem('weilin_prompt_ui_floatingBallEnabled')) {
  localStorage.setItem('weilin_prompt_ui_floatingBallEnabled', 'true');
  isFloatingBallEnabled.value = true
}

const { t } = useI18n()

const thisEditPromptId = ref("")
const STORAGE_PREFIX = 'weilin_tools_'
const loraManager = ref('look')
const tagManager = ref('manager')
const promptManager = ref('prompt_global')
const hasPromptLoraStack = ref(false)
const THEME_KEY = `${STORAGE_PREFIX}theme`
// 获取主题设置
const isDark = ref(localStorage.getItem(THEME_KEY) === 'dark')
// 全局提示词
const globalPrompt = ref('')

// 检查版本更新
const showVersionUpdate = ref(false);
const versionUpdateMessage = ref('');
const versionUpdateTimer = ref(null);
// 关闭版本更新提示
const closeVersionUpdate = () => {
  showVersionUpdate.value = false;
  if (versionUpdateTimer.value) {
    clearTimeout(versionUpdateTimer.value);
    versionUpdateTimer.value = null;
  }
};
// 跳转到GitHub
const goToGitHub = () => {
  window.open('https://github.com/weilin9999/WeiLin-Comfyui-Tools', '_blank');
  closeVersionUpdate();
};

// 默认窗口配置
const DEFAULT_WINDOWS = {
  prompt: {
    visible: false,
    is_default_close: false,
    position: { x: 100, y: 100 },
    size: { width: 600, height: 500 }
  },
  tag: {
    visible: false,
    is_default_close: false,
    position: { x: 150, y: 150 },
    size: { width: 800, height: 600 }
  },
  lora: {
    visible: false,
    is_default_close: false,
    position: { x: 200, y: 200 },
    size: { width: 800, height: 600 }
  },
  history: {
    visible: false,
    is_default_close: false,
    position: { x: 300, y: 300 },
    size: { width: 800, height: 600 }
  },
  ai_window: {
    visible: false,
    is_default_close: false,
    position: { x: 400, y: 400 },
    size: { width: 800, height: 600 }
  },
  node_list_window: {
    visible: false,
    is_default_close: false,
    position: { x: 100, y: 100 },
    size: { width: 300, height: 600 }
  },
  cloud_window: {
    visible: false,
    is_default_close: false,
    position: { x: 100, y: 100 },
    size: { width: 800, height: 600 }
  },
  lora_stack_window: {
    visible: false,
    is_default_close: true,
    position: { x: 100, y: 100 },
    size: { width: 300, height: 600 }
  }
}

// 从 localStorage 获取窗口状态
const getInitialWindowState = () => {
  try {
    const savedState = localStorage.getItem(`${STORAGE_PREFIX}windowStates`)
    if (savedState) {
      const parsedState = JSON.parse(savedState)
      const mergedState = { ...DEFAULT_WINDOWS }

      // 将保存的状态合并到默认配置中
      for (const key in parsedState) {
        if (key in mergedState) {
          mergedState[key] = {
            ...DEFAULT_WINDOWS[key],
            ...parsedState[key],
            // 如果is_default_close为true，则强制visible为false
            visible: parsedState[key].is_default_close ? false : parsedState[key].visible
          }
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
    localStorage.setItem(`${STORAGE_PREFIX}windowStates`, JSON.stringify(newState))
  } catch (error) {
    console.error('Error saving window states:', error)
  }
}, { deep: true })

// 组件挂载时注册所有窗口
onMounted(() => {
  Object.keys(windows.value).forEach(windowName => {
    // console.log(windowName)
    windowManager.registerWindow(windowName)
  })

  initTheme()
  // 添加消息监听
  window.addEventListener('message', handleMessage)

  // getTagsData();

  // 检查版本更新
  checkForUpdates();

})

// 初始化主题
const initTheme = () => {
  let savedTheme = localStorage.getItem(THEME_KEY)
  if (!savedTheme) {
    localStorage.setItem(THEME_KEY, 'dark')
    savedTheme = 'dark'
    isDark.value = true
  }
  isDark.value = savedTheme === 'dark'
  // 初始化主题
  const container = document.getElementById('weilin_comfyui_tools_prompt_ui_div')
  if (container) {
    // console.log(isDark.value)
    container.setAttribute('data-theme', isDark.value ? 'dark' : 'light')
  }
}

// 组件卸载时注销所有窗口
onUnmounted(() => {
  Object.keys(windows.value).forEach(windowName => {
    windowManager.unregisterWindow(windowName)
  })

  // 移除消息监听
  window.removeEventListener('message', handleMessage)

  // 清除版本更新定时器
  if (versionUpdateTimer.value) {
    clearTimeout(versionUpdateTimer.value);
    versionUpdateTimer.value = null;
  }
})

// 关闭窗口
const closeWindow = (windowName) => {
  if (windowName === 'prompt') {
    thisEditPromptId.value = ''
  }
  windows.value[windowName].visible = false
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


// 复原所有窗口到默认位置和大小
const restoreWindowsToDefault = () => {
  const LORA_DETAIL_WINDOWS = {
    loraDetail: {
      visible: false,
      is_default_close: false,
      position: { x: 150, y: 150 },
      size: { width: 800, height: 600 }
    }
  }

  const DEFAULT_GOL_WINDOWS = {
    prompt: {
      visible: false,
      is_default_close: false,
      position: { x: 100, y: 100 },
      size: { width: 600, height: 400 }
    },
    tag: {
      visible: false,
      is_default_close: false,
      position: { x: 150, y: 150 },
      size: { width: 800, height: 600 }
    },
    lora: {
      visible: false,
      is_default_close: false,
      position: { x: 200, y: 200 },
      size: { width: 800, height: 600 }
    },
    history: {
      visible: false,
      is_default_close: false,
      position: { x: 300, y: 300 },
      size: { width: 800, height: 600 }
    },
    ai_window: {
      visible: false,
      is_default_close: false,
      position: { x: 400, y: 400 },
      size: { width: 800, height: 600 }
    },
    node_list_window: {
      visible: false,
      is_default_close: false,
      position: { x: 100, y: 100 },
      size: { width: 400, height: 800 }
    },
    cloud_window: {
      visible: false,
      is_default_close: false,
      position: { x: 100, y: 100 },
      size: { width: 800, height: 600 }
    },
    lora_stack_window: {
      visible: false,
      is_default_close: true,
      position: { x: 100, y: 100 },
      size: { width: 300, height: 600 }
    }
  }


  localStorage.setItem(`${STORAGE_PREFIX}windowStates`, JSON.stringify(DEFAULT_GOL_WINDOWS))
  localStorage.setItem(`${STORAGE_PREFIX}loraDetailState`, JSON.stringify(LORA_DETAIL_WINDOWS))

  windows.value = getInitialWindowState()
};

const getTranslaterSetting = () => {
  translatorApi.getTranslateSetting().then(res => {
    // console.log(res)
    localStorage.setItem('weilin_prompt_ui_translater_setting', res.data);
  }).catch(err => {
    message({ type: "warn", str: 'message.getTranslaterFail' });
  })
};

getTranslaterSetting()

const promptBoxRef = ref()
const loraStackRef = ref()
const loraManagerRef = ref()
const loraDetailLoraStackRef = ref()

// 处理消息
const handleMessage = (event) => {
  if (event.data.type === 'weilin_prompt_ui_openTagManager') {
    tagManager.value = 'manager'
    windows.value.tag.visible = true
    windowManager.setActiveWindow('tag')
  } else if (event.data.type === 'weilin_prompt_ui_openTagManager_prompt') {
    tagManager.value = 'prompt'
    windows.value.tag.visible = true
    windowManager.setActiveWindow('tag')
  } else if (event.data.type === 'weilin_prompt_ui_openPromptBox') {
    // 按钮点击打开promptBox

    thisEditPromptId.value = event.data.id
    promptManager.value = 'prompt'
    windows.value.prompt.visible = true
    hasPromptLoraStack.value = false
    if (event.data.node === "WeiLinPromptUI") {
      hasPromptLoraStack.value = true
    }
    nextTick(() => {
      promptBoxRef.value.setPromptText(event.data.prompt)
    })
    windowManager.setActiveWindow('prompt')

  } else if (event.data.type === 'weilin_prompt_ui_openLoraManager') {
    loraManager.value = 'look'
    windows.value.lora.visible = true
    windowManager.setActiveWindow('lora')
  } else if (event.data.type === 'weilin_prompt_ui_openLoraManager_addLora') {
    loraManager.value = 'addLora'
    windows.value.lora.visible = true
    nextTick(() => {
      loraManagerRef.value.openSetSeed(0, "")
    })
    windowManager.setActiveWindow('lora')
  } else if (event.data.type === 'weilin_prompt_ui_openLoraManager_addLora_stack') {
    loraManager.value = 'addLora'
    windows.value.lora.visible = true
    nextTick(() => {
      loraManagerRef.value.openSetSeed(1, event.data.seed)
    })
    windowManager.setActiveWindow('lora')
  } else if (event.data.type === 'weilin_prompt_ui_openLoraManager_addLora_stack_node') {
    loraManager.value = 'addLora'
    windows.value.lora.visible = true
    nextTick(() => {
      loraManagerRef.value.openSetSeed(2, event.data.seed)
    })
    windowManager.setActiveWindow('lora')
  } else if (event.data.type === 'weilin_prompt_ui_openHistoryManager') {
    windows.value.history.visible = true
    windowManager.setActiveWindow('history')
  } else if (event.data.type === 'weilin_prompt_ui_openAiWindow') {
    windows.value.ai_window.visible = true
    windowManager.setActiveWindow('ai_window')
  } else if (event.data.type === 'weilin_prompt_ui_open_node_list_window') {
    windows.value.node_list_window.visible = true
    windowManager.setActiveWindow('node_list_window')

  } else if (event.data.type === 'weilin_prompt_ui_prompt_finish_prompt') {
    window.postMessage({
      type: 'weilin_prompt_ui_prompt_update_prompt_' + thisEditPromptId.value,
      data: event.data.data
    }, '*')
  } else if (event.data.type === 'weilin_prompt_ui_open_global_prompt_box') {
    promptManager.value = 'prompt_global'
    thisEditPromptId.value = "global"
    windows.value.prompt.visible = true
    hasPromptLoraStack.value = false
    nextTick(() => {
      promptBoxRef.value.setPromptText(globalPrompt.value)
    })
    windowManager.setActiveWindow('prompt')
  } else if (event.data.type === 'weilin_prompt_ui_open_global_tag_manager') {
    tagManager.value = 'manager'
    windows.value.tag.visible = true
    windowManager.setActiveWindow('tag')
  } else if (event.data.type === 'weilin_prompt_ui_open_global_lora_manager') {
    loraManager.value = 'look'
    windows.value.lora.visible = true
    windowManager.setActiveWindow('lora')
  } else if (event.data.type === 'weilin_prompt_ui_prompt_update_prompt_global') {
    globalPrompt.value = event.data.data
  } else if (event.data.type === 'weilin_prompt_ui_floating_ball_setting') {
    isFloatingBallEnabled.value = localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true';
  } else if (event.data.type === 'weilin_prompt_ui_restore_window') {
    restoreWindowsToDefault();
  } else if (event.data.type === 'weilin_prompt_ui_open_cloud_window') {
    windows.value.cloud_window.visible = true
    windowManager.setActiveWindow('cloud_window')
  } else if (event.data.type === 'weilin_prompt_ui_open_node_lora_stack_window') {
    windows.value.lora_stack_window.visible = true
    nextTick(() => {
      loraStackRef.value.initLoraStack(event.data.prompt, event.data.seed)
    })
    windowManager.setActiveWindow('lora_stack_window')
  } else if (event.data.type === "weilin_prompt_ui_openLoraDetail") {
    loraDetailLoraStackRef.value.open({ name: event.data.lora })
  }
}


const getTagsData = async () => {
  try {
    const res = await tagsApi.getTagsList()
    tagStore.setCategories(res.data);
  } catch (error) {
    console.error('获取标签列表失败:', error)
  }
}

// 检查版本更新
const checkForUpdates = async () => {
  try {
    const response = await fetch('https://raw.githubusercontent.com/weilin9999/WeiLin-Comfyui-Tools/refs/heads/main/src/src/utils/version.js');
    if (!response.ok) {
      console.error('获取版本信息失败:', response.status);
      return;
    }

    const text = await response.text();
    // 使用正则表达式提取版本号
    const versionMatch = text.match(/export const version = "([^"]+)"/);

    if (versionMatch && versionMatch[1]) {
      const remoteVersion = versionMatch[1];
      console.info(`WeiLin-Comfyui-Tools GitHub版本： ${remoteVersion}`);
      // 比较版本号
      if (remoteVersion !== localVersion) {
        // 显示更新提示
        versionUpdateMessage.value = `WeiLin-Comfyui-Tools 发现新版本 ${remoteVersion}，当前版本 ${localVersion}`;
        showVersionUpdate.value = true;

        // 10秒后自动关闭
        if (versionUpdateTimer.value) {
          clearTimeout(versionUpdateTimer.value);
        }
        versionUpdateTimer.value = setTimeout(() => {
          showVersionUpdate.value = false;
          versionUpdateTimer.value = null;
        }, 10000);

        console.info(`WeiLin-Comfyui-Tools 发现新版本 ${remoteVersion}，当前版本 ${localVersion} GitHub链接：https://github.com/weilin9999/WeiLin-Comfyui-Tools`);
      }
    }
  } catch (error) {
    console.error('WeiLin-Comfyui-Tools 检查更新失败:', error);
  }
};

</script>

<style scoped>
.main-container {
  width: 100%;
  height: 100%;
}

/* 确保所有对话框都在窗口之上 */
:deep(.dialog-overlay) {
  z-index: 9999 !important;
}


/* 版本更新提示样式 */
.version-update-notification {
  position: fixed;
  right: 10px;
  bottom: 10px;
  z-index: 9999;
  background-color: var(--primary-color, #4caf50);
  color: white;
  padding: 10px 15px;
  border-radius: 4px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  max-width: 350px;
  animation: slideIn 0.3s ease-out;
}

.version-update-content {
  display: flex;
  flex-direction: column;
}

.version-update-actions {
  display: flex;
  justify-content: flex-end;
  margin-top: 10px;
}

.goto-github-btn {
  background-color: white;
  color: var(--primary-color, #4caf50);
  border: none;
  border-radius: 4px;
  padding: 5px 10px;
  margin-right: 10px;
  cursor: pointer;
  font-weight: bold;
}

.close-version-update {
  background: none;
  border: none;
  color: white;
  font-size: 18px;
  cursor: pointer;
  padding: 0 5px;
}

@keyframes slideIn {
  from {
    transform: translateY(100%);
    opacity: 0;
  }

  to {
    transform: translateY(0);
    opacity: 1;
  }
}
</style>
