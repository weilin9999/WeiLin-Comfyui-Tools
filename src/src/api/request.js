import axios from 'axios'

export const baseUrl = '/weilin/prompt_ui/api'

// 创建 axios 实例
const request = axios.create({
  baseURL: baseUrl, // 基础URL，根据实际情况修改
  timeout: 30000,  // 请求超时时间
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  config => {
    // 在这里可以添加token等认证信息
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  response => {
    return response.data
  },
  error => {
    return Promise.reject(error)
  }
)

export default request 