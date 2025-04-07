<template>
  <div id="weilin_comfyui_tools_prompt_ui_div">
    <!-- 提示词窗口 -->
    <DraggableWindow name="promptBox" v-if="windows.prompt.visible" :title="promptManager === 'prompt' ? t('promptBox.windowTitle') : t('promptBox.windowTitleGlobal')"
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
      <LoraManager :loraManager="loraManager" />
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
      :position="windows.ai_window.position" :size="windows.ai_window.size" :z-index="windowManager.getZIndex('ai_window')"
      @update:position="updatePosition('ai_window', $event)" @update:size="updateSize('ai_window', $event)"
      @active="windowManager.setActiveWindow('ai_window')" @close="closeWindow('ai_window')">
      <AiWindow />
    </DraggableWindow>

    <!-- 节点列表快捷窗口 -->
    <DraggableWindow name="nodeListWindow" v-if="windows.node_list_window.visible" 
    :title="t('nodeListWindow.windowTitle')"
      :position="windows.node_list_window.position" :size="windows.node_list_window.size"
      :z-index="windowManager.getZIndex('node_list_window')"
      @update:position="updatePosition('node_list_window', $event)"
      @update:size="updateSize('node_list_window', $event)"
      @active="windowManager.setActiveWindow('node_list_window')"
      @close="closeWindow('node_list_window')">
      <NodeListWindow />
    </DraggableWindow>

    <!-- 云仓库窗口 -->
    <DraggableWindow name="cloudWindow" v-if="windows.cloud_window.visible" 
    :title="t('cloudWindow.windowTitle')"
      :position="windows.cloud_window.position" :size="windows.cloud_window.size"
      :z-index="windowManager.getZIndex('cloud_window')"
      @update:position="updatePosition('cloud_window', $event)"
      @update:size="updateSize('cloud_window', $event)"
      @active="windowManager.setActiveWindow('cloud_window')"
      @close="closeWindow('cloud_window')">
      <CloudWindow />
    </DraggableWindow>

    <!-- 悬浮球 -->
    <FloatingBall v-if="isFloatingBallEnabled">WeiLin</FloatingBall>

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
import { translatorApi } from '@/api/translator'
import { tagsApi } from '@/api/tags'

const tagStore = useTagStore();

const isFloatingBallEnabled = ref(localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true');
if(!localStorage.getItem('weilin_prompt_ui_floatingBallEnabled')) {
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

// 默认窗口配置
const DEFAULT_WINDOWS = {
  prompt: {
    visible: false,
    position: { x: 100, y: 100 },
    size: { width: 600, height: 500 }
  },
  tag: {
    visible: false,
    position: { x: 150, y: 150 },
    size: { width: 800, height: 600 }
  },
  lora: {
    visible: false,
    position: { x: 200, y: 200 },
    size: { width: 800, height: 600 }
  },
  history: {
    visible: false,
    position: { x: 300, y: 300 },
    size: { width: 800, height: 600 }
  },
  ai_window: {
    visible: false,
    position: { x: 400, y: 400 },
    size: { width: 800, height: 600 }
  },
  node_list_window: {
    visible: false,
    position: { x: 100, y: 100 },
    size: { width: 300, height: 600 }
  },
  cloud_window: {
    visible: false,
    position: { x: 100, y: 100 },
    size: { width: 800, height: 600 }
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
            ...parsedState[key]
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
    windowManager.registerWindow(windowName)
  })
  initTheme()
  // 添加消息监听
  window.addEventListener('message', handleMessage)

  getTagsData();
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
        position: { x: 150, y: 150 },
        size: { width: 800, height: 600 }
    }
  }

  const DEFAULT_GOL_WINDOWS = {
    prompt: {
      visible: false,
      position: { x: 100, y: 100 },
      size: { width: 600, height: 400 }
    },
    tag: {
      visible: false,
      position: { x: 150, y: 150 },
      size: { width: 800, height: 600 }
    },
    lora: {
      visible: false,
      position: { x: 200, y: 200 },
      size: { width: 800, height: 600 }
    },
    history: {
      visible: false,
      position: { x: 300, y: 300 },
      size: { width: 800, height: 600 }
    },
    ai_window: {
      visible: false,
      position: { x: 400, y: 400 },
      size: { width: 800, height: 600 }
    },
    node_list_window: {
      visible: false,
      position: { x: 100, y: 100 },
      size: { width: 400, height: 800 }
    },
    cloud_window: {
      visible: false,
      position: { x: 100, y: 100 },
      size: { width: 800, height: 600 }
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

// 处理消息
const handleMessage = (event) => {
  if (event.data.type === 'weilin_prompt_ui_openTagManager') {
    tagManager.value = 'manager'
    windows.value.tag.visible = true
    windowManager.setActiveWindow('tag')
  }else if (event.data.type === 'weilin_prompt_ui_openTagManager_prompt') {
    tagManager.value = 'prompt'
    windows.value.tag.visible = true
    windowManager.setActiveWindow('tag')
  } else if (event.data.type === 'weilin_prompt_ui_openPromptBox') {
    // 按钮点击打开promptBox

    thisEditPromptId.value = event.data.id
    promptManager.value = 'prompt'
    windows.value.prompt.visible = true
    hasPromptLoraStack.value = false
    if(event.data.node === "WeiLinPromptUI"){
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
  }else if (event.data.type === 'weilin_prompt_ui_floating_ball_setting') {
    isFloatingBallEnabled.value = localStorage.getItem('weilin_prompt_ui_floatingBallEnabled') === 'true';
  }else if (event.data.type === 'weilin_prompt_ui_restore_window') {
    restoreWindowsToDefault();
  }else if (event.data.type === 'weilin_prompt_ui_open_cloud_window') {
    windows.value.cloud_window.visible = true
    windowManager.setActiveWindow('cloud_window')
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
</style>
