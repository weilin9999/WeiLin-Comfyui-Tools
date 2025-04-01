import request from './request'

export const cloudApi = {
    // 获取云仓库列表
    getTreeFromCloud: async (path) => {
        return await request({
            url: '/cloud/get/tree',
            method: 'post',
            data: { path: path }
        })
    },
    getLocalInstallPackage: async () => {
        return await request({
            url: '/cloud/get/local/package',
            method: 'post',
            data: {  }
        })
    },
    installSelectPackage: async (path,paths) => {
        return await request({
            url: '/cloud/download/file',
            method: 'post',
            timeout: 0,
            data: { paths: paths, path: path }
        })
    },
}