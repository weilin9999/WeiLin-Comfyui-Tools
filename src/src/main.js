import { createApp } from 'vue'
import App from './App.vue'
import './style.css'
import '@/styles/theme.css'
import VueClipboard from 'vue-clipboard3'
import { createPinia } from 'pinia'; // 导入 Pinia
import i18n, { initI18n } from './i18n'

const {toClipboard} = VueClipboard()

const div = document.createElement('div')
div.id  = 'weilin_comfyui_tools_prompt_ui_div'  
const body=document.querySelector('body')
body.appendChild(div)
const app = createApp(App)
app.use(createPinia())
app.use(i18n)
// 在 pinia 初始化后调用
initI18n()
app.config.globalProperties.$copyText  = toClipboard
app.mount(div)

console.log("WeiLin Prompt UI is running")