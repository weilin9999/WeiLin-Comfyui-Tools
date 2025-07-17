import { createApp } from 'vue'
import App from './App.vue' 
import './style.css' 
import '@/styles/theme.css' 
import VueClipboard from 'vue-clipboard3'
import { createPinia } from 'pinia'
import i18n, { initI18n } from './i18n'
import { version } from "./utils/version.js" 
import '@/styles/vue3-json-viewer.css'   // ✅ 修正的样式导入路径 [1]()
 
const { toClipboard } = VueClipboard()
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'
 
document.addEventListener('DOMContentLoaded',  async () => { // 改用 async 函数
    const div = document.createElement('div') 
    div.id  = 'weilin_comfyui_tools_prompt_ui_div'
    document.body.appendChild(div) 
   
    const pinia = createPinia()
    pinia.use(piniaPluginPersistedstate) 
   
    const app = createApp(App)
    app.use(pinia) 
    app.use(i18n) 
    
    try {
      // 关键修复：确保 initI18n 返回 Promise
      await initI18n()  // [1]() 异步操作必须用 await 处理
      
      app.config.globalProperties.$copyText  = toClipboard
      app.mount(div) 
      
      console.log("WeiLin  Prompt UI is running - version " + version)
      console.log("WeiLin  节点插件已运行 - 版本 " + version)
    } catch (error) {
      console.error(" 初始化失败:", error)
      // 降级处理：即使失败也挂载应用 
      app.mount(div)  
    }
  })