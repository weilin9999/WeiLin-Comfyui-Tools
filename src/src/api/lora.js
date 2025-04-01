import request from './request'

// Lora相关接口
export const loraApi = {
  // 获取Lora列表
  getLoraList: async (params) => {
    return await request({
      url: '/get_lora_list',
      method: 'get',
      params
    })
  },

  // 获取Lora全部列表
  getAllLoraList: async (params) => {
    return await request({
      url: '/get_lora_load_all',
      method: 'get',
      params
    })
  },

  // 获取执行进度
  getAllLoraStatus: async (params) => {
    return await request({
      url: '/get_lora_load_status',
      method: 'get',
      params
    })
  },

  // 获取Lora详情
  getLoraDetail: async (params) => {
    return await request({
      url: '/lorainfo/api/loras/info',
      method: 'get',
      params
    })
  },

  // 获取Lora信息C站获取
  getLoraRefresh: async (params) => {
    return await request({
      url: '/lorainfo/api/loras/info/refresh',
      method: 'get',
      params
    })
  },

  // 上传Lora图片
  postUplaodImg: async (image,path,fileName) => {
    const body = new FormData();
    body.append("image", image);
    body.append("path", path);
    body.append("fileName", fileName);
    return await request({
        url: "/lorainfo/api/loras/set/img",
        method: 'post',
        data: body,
        headers: {'Content-Type': 'multipart/form-data'}
      })
  },

  // 保存Lora信息
  postLoraSave: async (file,json) => {
    const body = new FormData();
    body.append("json", JSON.stringify(json));
    return await request({
        url: "/lorainfo/api/loras/info?file="+file,
        method: 'post',
        data: body,
        headers: {'Content-Type': 'multipart/form-data'}
      })
}
} 