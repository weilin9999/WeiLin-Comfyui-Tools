<template>
    <div class="cloud-manager">
        <!-- 顶部工具栏 -->
        <div class="toolbar">
            <button class="refresh-btn" @click="refreshTree">
                <svg viewBox="0 0 24 24" width="16" height="16" class="tag-icon">
                    <path
                        d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
                </svg>
            </button>

            <button class="database-btn" @click="openTagDatabase">
                <svg viewBox="0 0 24 24" width="16" height="16" class="tag-icon">
                    <path
                        d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z" />
                </svg>
                <span>{{ t('cloudWindow.tagDatabase') }}</span>
            </button>

            <button class="database-btn" @click="openDanbooruDatabase">
                <svg viewBox="0 0 24 24" width="16" height="16" class="tag-icon">
                    <path
                        d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm0 16H5V5h14v14zm-8-2h2v-4h4v-2h-4V7h-2v4H7v2h4v4z" />
                </svg>
                <span>{{ t('cloudWindow.danbooruDatabase') }}</span>
            </button>

            <div class="current-path">
                <span>{{ t('cloudWindow.currentPath') }}: {{ mainPath == 'tags' ? t('cloudWindow.tagDatabase') :
                t('cloudWindow.danbooruDatabase') }}</span>
            </div>
        </div>

        <!-- 文件列表 -->
        <div class="file-list">
            <button v-if="currentPath !== 'tags' && currentPath !== 'danbooru'" class="back-btn" @click="goBack">
                <svg viewBox="0 0 24 24" width="16" height="16" class="tag-icon">
                    <path d="M20 11H7.83l5.59-5.59L12 4l-8 8 8 8 1.41-1.41L7.83 13H20v-2z" />
                </svg>
                {{ t('cloudWindow.back') }}
            </button>
            <div v-for="item in fileList" :key="item.path" class="file-item">
                <div class="file-info">
                    <span class="file-name">{{ item.name }}</span>
                    <span class="file-type">{{ item.type == 'dir' ? '文件夹' : item.type == 'file' ? '文件' : '其它未知文件' }}</span>
                </div>
                <div class="file-actions">
                    <button v-if="item.type === 'dir'" @click="openDirectory(item.path)" class="open-btn">
                        {{ t('cloudWindow.open') }}
                    </button>
                    <div v-else-if="item.type === 'file'" class="install-container">
                        <span v-if="isPackageInstalled(item.path)" class="installed-badge">
                            {{ t('cloudWindow.installed') }}
                        </span>
                        <button v-else 
                                @click="installPackage(item.path)" 
                                class="install-btn"
                                :disabled="item.isInstalling">
                            {{ item.isInstalling ? t('cloudWindow.installing') : t('cloudWindow.install') }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { cloudApi } from '@/api/cloud'
import message from '@/utils/message'

const { t } = useI18n()
const fileList = ref([])
const currentPath = ref('tags')
const mainPath = ref('tags')
const installedPackages = ref([])

// 获取文件树
const getTree = async (path) => {
    try {
        const res = await cloudApi.getTreeFromCloud(path)
        fileList.value = res.data
    } catch (error) {
        console.error('获取文件树失败:', error)
        message({ type: "warn", str: 'message.networkError' });
    }
}

// 获取已安装的包
const getInstalledPackages = async () => {
    try {
        const res = await cloudApi.getLocalInstallPackage()
        installedPackages.value = res.data || []
    } catch (error) {
        console.error('获取已安装包列表失败:', error)
        message({ type: "warn", str: 'message.networkError' });
    }
}

// 检查包是否已安装
const isPackageInstalled = (path) => {
    // console.log(installedPackages.value)
    return installedPackages.value.some(pkg => pkg === path)
}

// 安装包
const installPackage = async (path) => {
    try {
        const item = fileList.value.find(item => item.path === path)
        if (item) {
            item.isInstalling = true
            await cloudApi.installSelectPackage(mainPath.value,[path]).then(() => {
                getInstalledPackages()
                message({ type: "success", str:'message.installPackageSuccess' })
            })
        }
    } catch (error) {
        console.error('安装包失败:', error)
        message({ type: "warn", str: 'message.installPackageFail' });
    }finally {
        const item = fileList.value.find(item => item.path === path)
        if (item) {
            item.isInstalling = false
        }
    }
}

const goBack = () => {
    const pathParts = currentPath.value.split('/')
    if (pathParts.length > 1) {
        currentPath.value = pathParts.slice(0, -1).join('/')
        getTree(currentPath.value)
    }
}

// 刷新文件树
const refreshTree = () => {
    getTree(currentPath.value)
    getInstalledPackages()
}

// 打开目录
const openDirectory = (path) => {
    currentPath.value = path
    getTree(path)
}

const openTagDatabase = () => {
    mainPath.value = 'tags'
    currentPath.value = 'tags'
    getTree(currentPath.value)
}

const openDanbooruDatabase = () => {
    mainPath.value = 'danbooru'
    currentPath.value = 'danbooru'
    getTree(currentPath.value)
}

onMounted(() => {
    getTree(currentPath.value)
    getInstalledPackages()
})
</script>

<style scoped>
.cloud-manager {
    padding: 16px;
}


.file-list {
    max-height: 500px;
}

.file-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px;
    border-bottom: 1px solid #eee;
}

.file-info {
    display: flex;
    flex-direction: column;
}

.file-name {
    font-weight: bold;
}

.file-type {
    color: #666;
    font-size: 0.8em;
}

.open-btn {
    padding: 4px 8px;
    background: var(--weilin-prompt-ui-secondary-bg);
    color: var(--weilin-prompt-ui-primary-text);
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.refresh-btn {
    background: none;
    border: none;
    cursor: pointer;
    padding: 4px;
}

.toolbar {
    display: flex;
    gap: 8px;
    margin-bottom: 16px;
}

.database-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background: var(--weilin-prompt-ui-secondary-bg);
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    color: var(--weilin-prompt-ui-primary-text);
    border-radius: 4px;
    cursor: pointer;
    color: var(--text-color);
}

.database-btn:hover {
    background-color: var(--weilin-prompt-ui-primary-color);
}

.tag-icon {
    width: 20px;
    height: 20px;
    fill: var(--weilin-prompt-ui-icon-color);
}

.current-path {
    margin-left: auto;
    padding: 4px 8px;
    background-color: var(--weilin-prompt-ui-secondary-bg);
    border-radius: 4px;
    color: var(--weilin-prompt-ui-primary-text);
}

.back-btn {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 8px;
    width: 100%;
    background-color: var(--weilin-prompt-ui-secondary-bg);
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    color: var(--weilin-prompt-ui-primary-text);
    cursor: pointer;
    margin-bottom: 8px;
}

.back-btn:hover {
    background-color: var(--weilin-prompt-ui-primary-color);
}

.file-actions {
    display: flex;
    gap: 8px;
}

.install-container {
    display: flex;
    align-items: center;
}

.installed-badge {
    padding: 4px 8px;
    background-color: var(--weilin-prompt-ui-success-color, #4caf50);
    color: white;
    border-radius: 4px;
    font-size: 0.8em;
}

.install-btn {
    padding: 4px 8px;
    background: var(--weilin-prompt-ui-primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

.install-btn:hover {
    opacity: 0.9;
}
</style>