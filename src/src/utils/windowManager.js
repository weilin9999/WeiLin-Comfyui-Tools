import { ref } from 'vue'

const baseZIndex = 100
const activeWindow = ref('')
const windowZIndexes = ref({})

export const windowManager = {
  // 设置活动窗口
  setActiveWindow(windowName) {
    if (activeWindow.value !== windowName) {
      activeWindow.value = windowName
      // 更新所有窗口的 z-index
      Object.keys(windowZIndexes.value).forEach(key => {
        windowZIndexes.value[key] = baseZIndex
      })
      // 设置当前窗口为最高层
      windowZIndexes.value[windowName] = baseZIndex + 10
    }
  },

  // 获取窗口的 z-index
  getZIndex(windowName) {
    if (!windowZIndexes.value[windowName]) {
      windowZIndexes.value[windowName] = baseZIndex
    }
    return windowZIndexes.value[windowName]
  },

  // 注册窗口
  registerWindow(windowName) {
    if (!windowZIndexes.value[windowName]) {
      windowZIndexes.value[windowName] = baseZIndex
    }
  },

  // 注销窗口
  unregisterWindow(windowName) {
    delete windowZIndexes.value[windowName]
  }
} 