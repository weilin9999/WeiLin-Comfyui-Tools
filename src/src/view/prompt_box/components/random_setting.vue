<template>
    <DraggableWindow v-if="isOpen" :title="t('randomUtils.title')" :position="windows.randomRuleSetting.position"
        :size="windows.randomRuleSetting.size" :z-index="windowManager.getZIndex('randomRuleSetting')"
        @update:position="updatePosition('randomRuleSetting', $event)"
        @update:size="updateSize('randomRuleSetting', $event)"
        @active="windowManager.setActiveWindow('randomRuleSetting')" @close="closeWindow('randomRuleSetting')">
        <template #default>
            <div class="random-rule-container">
                <!-- 规则模板设置 -->
                <div class="settings-section template-section">
                    <div class="section-header">
                        <h3>{{ t('randomUtils.ruleTemplates') }}</h3>
                    </div>
                    <div class="template-controls">
                        <div class="template-select-group">
                            <div class="template-select-with-apply">
                                <select v-model="selectedTemplate" @change="changeSelectTemplate"
                                    class="form-select template-select">
                                    <option value="">{{ t('randomUtils.selectTemplate') }}</option>
                                    <option v-for="(template, index) in templates" :key="index"
                                        :value="template.path_name">
                                        {{ template.file_name }}
                                    </option>
                                </select>
                                <button class="apply-template-btn" @click="applyTemplate" :disabled="!selectedTemplate">
                                    {{ t('randomUtils.applyTemplate') }}
                                </button>
                            </div>
                            <div class="template-bottom-buttons">
                                <button class="new-template-btn" @click="saveAsNewTemplate">
                                    {{ t('randomUtils.newTemplate') }}
                                </button>
                                <button class="edit-template-btn" @click="editTemplateName"
                                    :disabled="!selectedTemplate">
                                    {{ t('randomUtils.editTemplate') }}
                                </button>
                                <button class="delete-template-btn" @click="deleteTemplate"
                                    :disabled="!selectedTemplate">
                                    {{ t('randomUtils.deleteTemplate') }}
                                </button>
                            </div>
                        </div>
                        <div class="template-name-input" v-if="showTemplateNameInput">
                            <input type="text" v-model="newTemplateName" class="form-input"
                                :placeholder="t('randomUtils.templateNamePlaceholder')" />
                            <div class="template-actions">
                                <button class="save-template-btn" @click="confirmSaveTemplate">
                                    {{ t('randomUtils.save') }}
                                </button>
                                <button class="cancel-template-btn" @click="cancelSaveTemplate">
                                    {{ t('randomUtils.cancel') }}
                                </button>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- 设置内容区域 - 仅当选择了模板时显示 -->
                <div v-if="selectedTemplate && loadingFinish">
                    <!-- 规则列表 -->
                    <div class="settings-section">
                        <div class="section-header">
                            <h3>{{ t('randomUtils.rules') }}</h3>
                            <button class="add-rule-btn" @click="addRule">
                                <span>+</span> {{ t('randomUtils.addRule') }}
                            </button>
                        </div>
                        <div class="rules-reminder">
                            <p>{{ t('randomUtils.rulesReminder') }}</p>
                        </div>

                        <div class="rules-list">
                            <div v-for="(rule, index) in settings.rules" :key="index" class="rule-item">
                                <div class="rule-header">
                                    <h4>{{ t('randomUtils.rule') }} #{{ index + 1 }}</h4>
                                    <button class="delete-rule-btn" @click="deleteRule(index)">×</button>
                                </div>
                                <div class="rule-content">
                                    <div class="form-group">
                                        <label>{{ t('randomUtils.range') }}</label>
                                        <div class="range-inputs">
                                            <input type="number" v-model.number="rule.range.min" min="1"
                                                class="form-input range-input" />
                                            <span>-</span>
                                            <input type="number" v-model.number="rule.range.max" min="1"
                                                class="form-input range-input" />
                                        </div>
                                    </div>
                                    <div class="form-group">
                                        <label>{{ t('randomUtils.tagType') }}</label>
                                        <select v-model="rule.type" class="form-select">
                                            <option value="category">{{ t('randomUtils.category') }}</option>
                                            <option value="specific">{{ t('randomUtils.specificTags') }}</option>
                                        </select>
                                    </div>

                                    <!-- 分类选择 -->
                                    <div v-if="rule.type === 'category'" class="form-group">
                                        <!-- 已选择分类显示区域 -->
                                        <div class="selected-categories-container">
                                            <div class="selected-categories-header">
                                                <span>{{ t('importDialog.selectedCategories') }}</span>
                                            </div>
                                            <div class="selected-categories-content">
                                                <!-- 一级分类（没有子分类的选择） -->
                                                <div class="selected-category-section"
                                                    v-if="primaryCategories(rule.tagGroupList).length > 0">
                                                    <div class="section-title">{{ t('importDialog.primaryCategories') }}
                                                    </div>
                                                    <div class="selected-items">
                                                        <div v-for="(item, index) in primaryCategories(rule.tagGroupList)"
                                                            :key="'primary-' + index" class="selected-item">
                                                            <span class="category-name">{{ item.group.name }}</span>
                                                        </div>
                                                    </div>
                                                </div>

                                                <!-- 二级分类（有子分类的选择） -->
                                                <div class="selected-category-section"
                                                    v-if="subCategories(rule.tagGroupList).length > 0">
                                                    <div class="section-title">{{ t('importDialog.subCategories') }}
                                                    </div>
                                                    <div class="selected-items">
                                                        <div v-for="(item, index) in subCategories(rule.tagGroupList)"
                                                            :key="'sub-' + index" class="selected-item">
                                                            <span class="category-name">{{ item.group.name }}</span>
                                                            <span class="separator">></span>
                                                            <span class="subcategory-name">{{ item.sub.name }}</span>
                                                        </div>
                                                    </div>
                                                </div>

                                                <!-- 没有选择任何分类时显示 -->
                                                <div v-if="!rule.tagGroupList || rule.tagGroupList.length === 0"
                                                    class="no-selected">
                                                    {{ t('importDialog.noSelectedCategories') }}
                                                </div>
                                            </div>
                                        </div>
                                        <button class="add-tag-btn" @click="selectTagGroup(index,rule.tagGroupList)">
                                            {{ t('randomUtils.selectTagGroup') }}
                                        </button>
                                    </div>

                                    <!-- 特定标签选择 -->
                                    <div v-if="rule.type === 'specific'" class="form-group">
                                        <label>{{ t('randomUtils.specificTags') }}</label>
                                        <div class="tags-input-container">
                                            <div v-for="(tag, tagIndex) in rule.specificTags" :key="tagIndex"
                                                class="tag-chip">
                                                {{ tag }}
                                                <button class="remove-tag-btn"
                                                    @click="removeTag(rule, tagIndex)">×</button>
                                            </div>
                                            <input type="text" v-model="rule.tagInput"
                                                @keydown.enter.prevent="addTag(rule)" class="tag-input"
                                                :placeholder="t('randomUtils.addTagPlaceholder')" />
                                        </div>
                                        <button class="add-tag-btn" @click="addTag(rule)">
                                            {{ t('randomUtils.addTag') }}
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
            <!-- 保存按钮 -->
            <div class="actions-section">
                <button class="save-btn" @click="saveSettings" :disabled="!selectedTemplate">{{ t('common.save')
                    }}</button>
                <!-- <button class="test-btn" @click="testRandomTags" :disabled="!selectedTemplate">{{
                    t('randomUtils.testRandom') }}</button> -->
            </div>
        </template>
    </DraggableWindow>
    <TagGroupSelect ref="tagGroupSelectItem" @sureSelect="sureSelectThis" />
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useI18n } from 'vue-i18n'
import DraggableWindow from '@/components/DraggableWindow.vue'
import { windowManager } from '@/utils/windowManager'
import message from "@/utils/message";
import TagGroupSelect from "./tag_group_select.vue"
import { randomTagApi } from '@/api/random_tag'

const emit = defineEmits(['close', 'update', 'generateRandomTags'])
const { t } = useI18n()
const isOpen = ref(false)

const tagGroupSelectItem = ref(null)
const STORAGE_PREFIX = 'weilin_tools_'
const loadingFinish = ref(false)
const promptMode = ref('')
const nodeLocalTemplateId = ref('')

// 默认窗口配置
const DEFAULT_WINDOWS = {
    randomRuleSetting: {
        visible: false,
        position: { x: 150, y: 150 },
        size: { width: 800, height: 600 }
    }
}

// 默认设置
const DEFAULT_SETTINGS = {
    file_name: 'new_random_template',
    rules: [
        {
            range: { min: 1, max: 3 },
            type: 'category',
            categoryId: 1,
            specificTags: [],
            tagGroupList: [],
            tagInput: ''
        },
        {
            range: { min: 4, max: 6 },
            type: 'category',
            categoryId: 2,
            specificTags: [],
            tagGroupList: [],
            tagInput: ''
        }
    ]
}

// 设置状态
const settings = ref({})
// console.log(settings)

// 从 localStorage 加载设置
async function loadSettings() {
    try {
        if (promptMode.value == "prompt_global") {
            await randomTagApi.getRandomTemplateApple().then(async (res) => {
                // console.log(res);
                if (res.data == "") {
                    settings.value = DEFAULT_SETTINGS
                } else {
                    await randomTagApi.getTemplateData(res.data).then(async (resData) => {
                        selectedTemplate.value = res.data // 选中新创建的模板
                        settings.value = resData.data
                        loadingFinish.value = true
                    }).catch(err => {
                        console.error('加载模板失败:', err)
                        message({ type: "warn", str: 'randomUtils.errorLoadingTemplate' });
                    })
                }
            }).catch((err) => {
                console.error(err);
                message({ type: "warn", str: 'message.networkError' });
            });
        } else {
            if (nodeLocalTemplateId.value == "") {
                settings.value = DEFAULT_SETTINGS
            } else {
                await randomTagApi.getTemplateData(nodeLocalTemplateId.value).then(async (resData) => {
                    selectedTemplate.value = nodeLocalTemplateId.value // 选中新创建的模板
                    settings.value = resData.data
                    loadingFinish.value = true
                }).catch(err => {
                    console.error('加载模板失败:', err)
                    message({ type: "warn", str: 'randomUtils.errorLoadingTemplate' });
                })
            }
        }
    } catch (error) {
        message({ type: "warn", str: 'message.networkError' });
        console.error('Error loading random tag settings:', error)
    }
}

// 保存设置到 localStorage
function saveSettings() {
    try {
        // 使用settings中的数据
        const templateData = JSON.parse(JSON.stringify(settings.value));

        // 移除每个规则中的tagInput字段
        if (templateData.rules) {
            templateData.rules.forEach(rule => {
                delete rule.tagInput
            })
        }

        // 更新模板信息
        randomTagApi.updateTemplateData(selectedTemplate.value, templateData).then(async (res) => {
            await randomTagApi.getTemplateData(res.path_name).then(async (resData) => {
                settings.value = resData.data
                message({ type: "success", str: 'randomUtils.templateSaved' });
            }).catch(err => {
                console.error('加载模板失败:', err)
                message({ type: "warn", str: 'randomUtils.errorLoadingTemplate' });
            })
        }).catch(err => {
            console.error('更新模板失败:', err)
            message({ type: "warn", str: 'randomUtils.errorSavingTemplate' });
        })

    } catch (error) {
        console.error('Error saving random tag settings:', error)
        message({ type: "warn", str: 'randomUtils.errorSavingSettings' });
    }
}

// 添加新规则
function addRule() {
    settings.value.rules.push({
        range: {
            min: settings.value.rules.length > 0
                ? settings.value.rules[settings.value.rules.length - 1].range.max + 1
                : 1,
            max: settings.value.rules.length > 0
                ? settings.value.rules[settings.value.rules.length - 1].range.max + 3
                : 3
        },
        type: 'category',
        categoryId: 1,
        specificTags: [],
        tagGroupList: [],
        tagInput: ''
    })
}

// 删除规则
function deleteRule(index) {
    settings.value.rules.splice(index, 1)
}

// 添加标签
function addTag(rule) {
    if (rule.tagInput && rule.tagInput.trim()) {
        rule.specificTags.push(rule.tagInput.trim())
        rule.tagInput = ''
    }
}

// 移除标签
function removeTag(rule, tagIndex) {
    rule.specificTags.splice(tagIndex, 1)
}

// 测试随机标签生成
function testRandomTags() {
    const randomTags = generateRandomTags()
    message.success(`${t('randomUtils.generatedTags')}: ${randomTags.join(', ')}`)
}

// 生成随机标签
function generateRandomTags() {
    // 这里是简化的实现，实际应用中需要根据真实标签数据生成
    const result = []
}

// 从 localStorage 获取窗口状态
const getInitialWindowState = () => {
    try {
        const savedState = localStorage.getItem(`${STORAGE_PREFIX}randomRuleSettingState`)
        if (savedState) {
            const parsedState = JSON.parse(savedState)

            // 检查并补充缺失的窗口配置
            const mergedState = { ...DEFAULT_WINDOWS }

            // 将保存的状态合并到默认配置中
            if (parsedState.randomRuleSetting) {
                mergedState.randomRuleSetting = {
                    ...DEFAULT_WINDOWS.randomRuleSetting,  // 默认值
                    ...parsedState.randomRuleSetting       // 保存的值
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
        localStorage.setItem(`${STORAGE_PREFIX}randomRuleSettingState`, JSON.stringify(newState))
    } catch (error) {
        console.error('Error saving window states:', error)
    }
}, { deep: true })


// 关闭窗口
const closeWindow = (windowName) => {
    isOpen.value = false
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

// 打开窗口
const open = (mode) => {
    isOpen.value = true
    // console.log(mode)
    promptMode.value = mode
    windowManager.registerWindow('randomRuleSetting')
    nextTick(() => {
        windowManager.setActiveWindow('randomRuleSetting')
        if (mode == "prompt_global") {
            loadTemplates(1)
        } else {
            getNodeTagTemplateIdAndReGet()
        }
    })
}


const selectTagGroup = (index,data) => {
    tagGroupSelectItem.value.open(index,data)
}

// 对外暴露生成随机标签的方法
const getRandomTags = () => {
    return generateRandomTags()
}

// 计算属性：获取一级分类（没有子分类的选择）
const primaryCategories = (data) => {
    if (!data || !Array.isArray(data) || data.length <= 0) return [];
    return data.filter(item => !item.sub);
};

// 计算属性：获取二级分类（有子分类的选择）
const subCategories = (data) => {
    if (!data || !Array.isArray(data) || data.length <= 0) return [];
    return data.filter(item => item.sub);
};


const sureSelectThis = (data) => {
    // 确保 data.data 是一个数组，并且具有正确的结构
    if (data && data.data && Array.isArray(data.data)) {
        settings.value.rules[data.index].tagGroupList = data.data;
    } else {
        // 初始化为空数组
        settings.value.rules[data.index].tagGroupList = [];
    }
}


// 规则模板相关
const templates = ref([])
const selectedTemplate = ref('')
const newTemplateName = ref('')
const showTemplateNameInput = ref(false)
const isEditingTemplate = ref(false) // 新增：是否正在编辑模板

// 加载规则模板
async function loadTemplates(loadSetting = 0) {

    try {
        await randomTagApi.getTemplateList().then((res) => {
            // console.log(res);
            templates.value = res.data
            if (loadSetting == 1) {
                loadSettings()
            }
        }).catch((err) => {
            console.error(err);
            message({ type: "warn", str: 'message.networkError' });
        });

    } catch (error) {
        message({ type: "warn", str: 'message.networkError' });
        console.error('RandomTemplate获取列表失败:', error)
    }

    // try {
    //     const savedTemplates = localStorage.getItem(`${STORAGE_PREFIX}ruleTemplates`)
    //     if (savedTemplates) {
    //         templates.value = JSON.parse(savedTemplates)
    //     }
    // } catch (error) {
    //     console.error('Error loading rule templates:', error)
    //     templates.value = []
    // }
}

// 显示保存模板输入框
function saveAsNewTemplate() {
    showTemplateNameInput.value = true
    newTemplateName.value = ''
}

// 取消保存模板
function cancelSaveTemplate() {
    showTemplateNameInput.value = false
    newTemplateName.value = ''
}

// 应用模板
function applyTemplate() {
    if (!selectedTemplate.value) {
        message.warm(t('randomUtils.pleaseChooseTemplate'))
        return
    }
    if (promptMode.value == "prompt_global") {
        // 获取选中的模板
        randomTagApi.updateRandomTemplateApple(selectedTemplate.value).then(res => {
            message({ type: "success", str: 'randomUtils.templateApplied' });
        }).catch(err => {
            console.error('获取模板失败:', err)
            message({ type: "warn", str: 'randomUtils.errorApplyingTemplate' });
        })
    } else {
        window.postMessage({
            type: 'weilin_prompt_ui_prompt_inner_update_node_tag_template_id',
            data: selectedTemplate.value
        }, '*')
        message({ type: "success", str: 'randomUtils.templateApplied' });
    }

}


// 删除模板
function deleteTemplate() {
    if (!selectedTemplate.value) return

    // 确认删除
    randomTagApi.deleteTemplateData(selectedTemplate.value).then(() => {
        message({ type: "success", str: 'randomUtils.templateDeleted' });
        loadTemplates() // 重新加载模板列表
        selectedTemplate.value = '' // 清空选择
    }).catch(err => {
        console.error('删除模板失败:', err)
        message({ type: "warn", str: 'randomUtils.errorDeletingTemplate' });
    })
}

// 编辑模板名称
function editTemplateName() {
    if (!selectedTemplate.value) return

    const template = templates.value.find(t => t.path_name === selectedTemplate.value)
    if (!template) return

    // 显示编辑界面并设置当前模板名称
    showTemplateNameInput.value = true
    newTemplateName.value = template.file_name
    isEditingTemplate.value = true
}

// 修改确认保存模板函数
function confirmSaveTemplate() {
    if (!newTemplateName.value.trim()) {
        message({ type: "warn", str: 'randomUtils.templateNameRequired' });
        return
    }

    // 更新当前设置的文件名
    settings.value.file_name = newTemplateName.value.trim();

    if (isEditingTemplate.value) {
        // 编辑现有模板
        const template = templates.value.find(t => t.path_name === selectedTemplate.value)
        if (template) {
            template.file_name = newTemplateName.value.trim()

            // 使用settings中的数据
            const templateData = JSON.parse(JSON.stringify(settings.value))

            // 移除每个规则中的tagInput字段
            if (templateData.rules) {
                templateData.rules.forEach(rule => {
                    delete rule.tagInput
                })
            }

            // 调用API保存新模板
            randomTagApi.updateTemplateData(template.path_name, templateData).then(async (res) => {
                message({ type: "success", str: 'randomUtils.templateSaved' });
                await loadTemplates().then(async () => {
                    await randomTagApi.getTemplateData(res.path_name).then(async (resData) => {
                        selectedTemplate.value = res.path_name // 选中新创建的模板
                        settings.value = resData.data
                        message({ type: "success", str: 'randomUtils.templateSaved' });
                    }).catch(err => {
                        console.error('加载模板失败:', err)
                        message({ type: "warn", str: 'randomUtils.errorLoadingTemplate' });
                    })
                }) // 重新加载模板列表
            }).catch(err => {
                console.error('保存模板失败:', err)
                message({ type: "warn", str: 'randomUtils.errorSavingTemplate' });
            })
        }
    } else {
        // 创建新模板 - 使用settings中的数据
        settings.value = DEFAULT_SETTINGS
        settings.value.file_name = newTemplateName.value.trim();
        const templateData = JSON.parse(JSON.stringify(settings.value))

        // 移除每个规则中的tagInput字段
        if (templateData.rules) {
            templateData.rules.forEach(rule => {
                delete rule.tagInput
            })
        }

        // 调用API保存新模板
        randomTagApi.saveTemplateData(templateData).then(async (res) => {
            await loadTemplates().then(async () => {
                await randomTagApi.getTemplateData(res.path_name).then(async (resData) => {
                    selectedTemplate.value = res.path_name // 选中新创建的模板
                    settings.value = resData.data
                    message({ type: "success", str: 'randomUtils.templateSaved' });
                }).catch(err => {
                    console.error('加载模板失败:', err)
                    message({ type: "warn", str: 'randomUtils.errorLoadingTemplate' });
                })
            }) // 重新加载模板列表
        }).catch(err => {
            console.error('保存模板失败:', err)
            message({ type: "warn", str: 'randomUtils.errorSavingTemplate' });
        })
    }

    // 重置UI状态
    showTemplateNameInput.value = false
    newTemplateName.value = ''
    isEditingTemplate.value = false
}


const changeSelectTemplate = async (event) => {
    // console.log(event.target.value);
    if (event.target.value == "") {
        return
    }
    try {
        await randomTagApi.getTemplateData(event.target.value).then(async (res) => {
            selectedTemplate.value = res.path_name // 选中新创建的模板
            settings.value = res.data
            loadingFinish.value = true
        }).catch(err => {
            console.error('加载模板失败:', err)
            message({ type: "warn", str: 'randomUtils.errorLoadingTemplate' });
        })
    } catch (error) {
        message({ type: "warn", str: 'message.networkError' });
        console.error('Error loading random tag settings:', error)
    }

}

const getNodeTagTemplateIdAndReGet = () => {
    window.postMessage({
        type: 'weilin_prompt_ui_prompt_inner_get_node_tag_template_id'
    }, '*')
}


// 处理消息
const handleMessage = (event) => {
    if (event.data.type === 'weilin_prompt_ui_prompt_inner_get_node_tag_template_id_response') {
        // console.log(event.data.data)
        nodeLocalTemplateId.value = event.data.data
        // 继续执行
        loadTemplates(1)
    }
}


// 组件挂载时注册所有窗口
onMounted(() => {
    // 添加消息监听
    window.addEventListener('message', handleMessage)
})
// 组件卸载时注销所有窗口
onUnmounted(() => {
    windowManager.unregisterWindow('randomRuleSetting')
    // 移除消息监听
    window.removeEventListener('message', handleMessage)
})

defineExpose({
    open,
    getRandomTags
})
</script>
<style scoped>
.random-rule-container {
    padding: 16px;
    height: calc(100% - 55px);
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    gap: 20px;
}

.settings-section {
    background-color: var(--weilin-prompt-ui-secondary-bg);
    border-radius: 8px;
    padding: 16px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    color: var(--weilin-prompt-ui-primary-text);
}

.section-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 16px;
    color: var(--weilin-prompt-ui-primary-text);
}

.form-group {
    margin-bottom: 16px;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    font-weight: 500;
    color: var(--weilin-prompt-ui-primary-text);
}

.form-input,
.form-select {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background-color: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-input-text);
}

.range-inputs {
    display: flex;
    align-items: center;
    gap: 8px;
}

.range-input {
    width: 80px;
}

.rules-list {
    display: flex;
    flex-direction: column;
    gap: 16px;
}

.rule-item {
    background-color: var(--weilin-prompt-ui-primary-bg);
    border-radius: 6px;
    padding: 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
}

.rule-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
    color: var(--weilin-prompt-ui-primary-text);
}

.rule-header h4 {
    margin: 0;
    color: var(--weilin-prompt-ui-primary-text);
}

.add-rule-btn,
.add-tag-btn {
    background-color: var(--weilin-prompt-ui-primary-color);
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 6px 12px;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 4px;
    transition: background-color 0.3s;
}

.add-rule-btn:hover,
.add-tag-btn:hover {
    background-color: var(--weilin-prompt-ui-primary-color-hover);
}

.delete-rule-btn,
.remove-tag-btn {
    background-color: transparent;
    color: var(--weilin-prompt-ui-danger-color);
    border: none;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
}

.delete-rule-btn:hover,
.remove-tag-btn:hover {
    color: var(--weilin-prompt-ui-danger-color-hover);
}

.tags-input-container {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    padding: 8px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background-color: var(--weilin-prompt-ui-input-bg);
    min-height: 40px;
    margin-bottom: 8px;
}

.tag-chip {
    display: flex;
    align-items: center;
    gap: 4px;
    padding: 4px 8px;
    background-color: var(--weilin-prompt-ui-tag-bg);
    color: var(--weilin-prompt-ui-tag-text);
    border-radius: 16px;
    font-size: 14px;
}

.tag-input {
    flex: 1;
    min-width: 100px;
    border: none;
    outline: none;
    background: transparent;
    color: var(--weilin-prompt-ui-input-text);
}

.actions-section {
    height: 55px;
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 10px;
    border-top: 1px solid var(--weilin-prompt-ui-border-color);
}

.save-btn,
.test-btn {
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s;
}

.save-btn {
    background-color: var(--weilin-prompt-ui-primary-color);
    color: white;
    border: none;
}

.save-btn:hover {
    background-color: var(--weilin-prompt-ui-primary-color-hover);
}

.test-btn {
    background-color: var(--weilin-prompt-ui-button-bg);
    color: var(--weilin-prompt-ui-button-text);
    border: 1px solid var(--weilin-prompt-ui-border-color);
}

.test-btn:hover {
    background-color: var(--weilin-prompt-ui-button-hover);
}

/* 分类选择相关样式 */
.selected-categories-container {
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    margin-bottom: 12px;
    overflow: hidden;
}

.selected-categories-header {
    background-color: var(--weilin-prompt-ui-header-bg);
    padding: 8px 12px;
    font-weight: 500;
    color: var(--weilin-prompt-ui-primary-text);
    border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.selected-categories-content {
    padding: 12px;
    max-height: 200px;
    overflow-y: auto;
    background-color: var(--weilin-prompt-ui-primary-bg);
}

.selected-category-section {
    margin-bottom: 12px;
}

.section-title {
    font-size: 14px;
    font-weight: 500;
    margin-bottom: 8px;
    color: var(--weilin-prompt-ui-secondary-text);
}

.selected-items {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
}

.selected-item {
    display: flex;
    align-items: center;
    padding: 4px 8px;
    background-color: var(--weilin-prompt-ui-tag-bg);
    color: var(--weilin-prompt-ui-tag-text);
    border-radius: 4px;
    font-size: 14px;
}

.separator {
    margin: 0 4px;
    color: var(--weilin-prompt-ui-secondary-text);
}

.no-selected {
    color: var(--weilin-prompt-ui-secondary-text);
    font-style: italic;
    padding: 8px 0;
}

/* 滚动条样式 */
.selected-categories-content::-webkit-scrollbar {
    width: 6px;
}

.selected-categories-content::-webkit-scrollbar-track {
    background: var(--weilin-prompt-ui-scrollbar-track);
}

.selected-categories-content::-webkit-scrollbar-thumb {
    background: var(--weilin-prompt-ui-scrollbar-thumb);
    border-radius: 3px;
}

.selected-categories-content::-webkit-scrollbar-thumb:hover {
    background: var(--weilin-prompt-ui-scrollbar-thumb-hover);
}

/* 模板相关样式 */
.template-section {
    margin-bottom: 16px;
}

.template-controls {
    display: flex;
    flex-direction: column;
    gap: 12px;
}

.template-select-group {
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.template-buttons {
    display: flex;
    gap: 8px;
}

.template-select {
    width: 100%;
}

.apply-template-btn,
.edit-template-btn,
.delete-template-btn {
    padding: 6px 12px;
    border-radius: 4px;
    cursor: pointer;
    border: none;
    transition: background-color 0.3s;
}

.apply-template-btn {
    background-color: var(--weilin-prompt-ui-primary-color);
    color: white;
    flex: 1;
}

.apply-template-btn:hover {
    background-color: var(--weilin-prompt-ui-primary-color-hover);
}

.edit-template-btn {
    background-color: var(--weilin-prompt-ui-secondary-color);
    color: white;
    flex: 1;
}

.edit-template-btn:hover {
    background-color: var(--weilin-prompt-ui-secondary-color-hover);
}

.delete-template-btn {
    background-color: var(--weilin-prompt-ui-danger-color);
    color: white;
    flex: 1;
}

.delete-template-btn:hover {
    background-color: var(--weilin-prompt-ui-danger-color-hover);
}

.apply-template-btn:disabled,
.edit-template-btn:disabled,
.delete-template-btn:disabled {
    background-color: var(--weilin-prompt-ui-disabled-bg);
    color: var(--weilin-prompt-ui-disabled-text);
    cursor: not-allowed;
}


/* 新增样式 */
.template-select-with-apply {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.template-select-with-apply .template-select {
    flex: 9;
    margin-right: 10px;
}

.template-bottom-buttons {
    display: flex;
    justify-content: space-between;
    margin-top: 10px;
}

.template-bottom-buttons button {
    flex: 1;
    margin: 0 5px;
}

.template-bottom-buttons button:first-child {
    margin-left: 0;
}

.template-bottom-buttons button:last-child {
    margin-right: 0;
}

/* 按钮样式 */
.new-template-btn,
.edit-template-btn,
.delete-template-btn {
    padding: 5px 10px;
    border-radius: 4px;
    font-size: 0.9em;
    cursor: pointer;
}

.new-template-btn {
    background-color: #4caf50;
    color: white;
    border: none;
}

.edit-template-btn {
    background-color: #2196f3;
    color: white;
    border: none;
}

.delete-template-btn {
    background-color: #f44336;
    color: white;
    border: none;
}

button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.rules-reminder {
    margin-bottom: 10px;
    padding: 8px 12px;
    background-color: #fff7e6;
    border-left: 4px solid #ffbb33;
    border-radius: 4px;
}

.rules-reminder p {
    margin: 0;
    font-size: 0.9em;
    color: #996600;
}
</style>