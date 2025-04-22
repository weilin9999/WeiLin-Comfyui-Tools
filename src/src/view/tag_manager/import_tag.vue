<template>
    <Dialog v-model="dialogVisible" :title="t('importDialog.title')">
        <div class="settings-content">
            <!-- 加载遮罩层 -->
            <div v-if="loading" class="loading-overlay">
                <div class="loading-spinner"></div>
            </div>
            <div class="info-links">
                <div class="info-link-item">
                    <span class="info-link-label">{{ t('importDialog.tips1') }}</span>
                    <a href="https://www.bilibili.com/list/288025756/?sid=4690314&spm_id_from=333.1387.0.0&oid=114342431298474&bvid=BV1txdfYxE7X"
                        target="_blank" class="info-link">
                        {{ t('importDialog.tips1text') }}
                    </a>
                </div>
                <div class="info-link-item">
                    <span class="info-link-label">{{ t('importDialog.tips2') }}</span>
                    <a href="https://github.com/weilin9999/WeiLin-Comfyui-Tools-Prompt" target="_blank"
                        class="info-link">
                        {{ t('importDialog.tips2text') }}
                    </a>
                </div>
                <div class="info-link-item">
                    <span class="info-link-label">{{ t('importDialog.tips3') }}</span>
                    <a href="https://weilin9999.github.io/WeiLin-Share-Prompt-Web/#/" target="_blank" class="info-link">
                        {{ t('importDialog.tips3text') }}
                    </a>
                </div>
            </div>
            <div style="margin-bottom: 16px;">
                <button @click="cleanAll" class="upload-btn">{{ t('importDialog.cleanAll') }}</button>
                <button style="margin-left: 10px;" @click="triggerFileUpload" class="upload-btn">{{
                    t('importDialog.uploadSQL') }}</button>
                <button style="margin-left: 10px;" @click="openSelectGroup">{{ t('importDialog.selectGroup') }}</button>
                <button style="margin-left: 10px;" @click="exportSQL">{{ t('importDialog.dumpSQL') }}</button>
                <button style="margin-left: 10px;" @click="exportOnlyTagSQL">{{ t('importDialog.dumpOnlySQL')
                    }}</button>

                <input style="width: 300px;margin-left: 10px;" v-model="outPutName"
                    :placeholder="t('importDialog.settingOutputName')" />

                <input type="file" ref="fileInput" @change="handleFileUpload" accept=".sql" style="display: none;" />
                <input type="file" ref="jsonFileInput" @change="handleJSONUpload" accept=".json"
                    style="display: none;" />
                <input type="file" ref="txtFileInput" @change="handleTXTUpload" accept=".txt" style="display: none;" />
                <input type="file" ref="yamlFileInput" @change="handleYAMLUpload" accept=".yaml,.yml"
                    style="display: none;" />
            </div>
            <div style="margin-bottom: 16px;">
                <input  v-model="groupName" :placeholder="t('importDialog.pleaseMainCeb')" />
                <button  @click="generateGroupSQL">{{ t('importDialog.setMainCeb') }}</button>
                <input style="width: 300px;margin-left: 10px;" v-model="mainClassUUID"
                    :placeholder="t('importDialog.pleaseMainCebUuid')" />
            </div>
            <div style="margin-bottom: 16px;">
                <input v-model="subGroupName"
                    :placeholder="t('importDialog.pleaseSubGroup')" />
                <button @click="generateSubGroupSQL">{{ t('importDialog.setSubCeb')
                    }}</button>
                <input style="width: 300px;margin-left: 10px" v-model="subGroupUUID"
                    :placeholder="t('importDialog.pleaseSubGroupUuid')" />
            </div>
            <div style="margin-bottom: 16px;">
                <input v-model="tag" placeholder="Tag" />
                <input v-model="chinese" :placeholder="t('importDialog.translater')" />
                <button @click="generateSQL">{{ t('importDialog.add') }}</button>
                <button style="margin-left: 10px;" @click="triggerJSONUpload" class="upload-btn">{{
                    t('importDialog.fromJSONImput') }}</button>
                <button style="margin-left: 10px;" @click="triggerTXTUpload" class="upload-btn">{{
                    t('importDialog.fromTxtInput') }}</button>
                <button style="margin-left: 10px;" @click="triggerYAMLUpload" class="upload-btn">{{
                    t('importDialog.fromYmalInput') }}</button>
            </div>
            <div class="data-container">
                <div v-if="groupSql">
                    <h3>{{ parseSQL(groupSql).text }}</h3>
                    <div v-if="subGroupSql">
                        <h4>{{ parseSQL(subGroupSql).text }}</h4>
                        <div class="tag-group-container">
                            <div v-for="(tag, index) in tagGroups" :key="index"
                                style="display: flex;flex-direction: column;align-items: center;">
                                <p>{{ parseSQL(tag).text }} - {{ parseSQL(tag).desc }}</p>
                                <div style="display: flex;align-items: center;">
                                    <div v-if="editingIndex === index">
                                        <input v-model="editText" placeholder="Tag" />
                                        <input v-model="editDesc" :placeholder="t('importDialog.translater')" />
                                        <button @click="confirmEdit(index)">{{ t('importDialog.sureYes') }}</button>
                                        <button style="margin-left: 10px;" @click="cancelEdit">{{
                                            t('importDialog.cancel') }}</button>
                                    </div>
                                    <button v-else @click="startEdit(index)">{{ t('importDialog.edit') }}</button>
                                    <button style="margin-left: 10px;" @click="deleteTag(index)">{{
                                        t('importDialog.delete') }}</button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <template #footer>
            <button @click="dialogVisible = false">{{ t('promptBox.settings.close') }}</button>
            <button @click="sureToImportTags">{{ t('importDialog.sure') }}</button>
        </template>
    </Dialog>
    <TagGroupSelectDialog ref="tagGroupSelectDialogItem" @sureSelect="sureToSelectInfo" />
</template>

<script setup>
import Dialog from '@/components/Dialog.vue'
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import { uuidv7 } from "uuidv7";
import message from '@/utils/message'
import TagGroupSelectDialog from "./tag_group_select.vue";
import yaml from 'js-yaml';
import { tagsApi } from '@/api/tags'

const { t } = useI18n()

const dialogVisible = ref(false)


const tag = ref('')
const chinese = ref('')
const sql = ref('')
const groupSql = ref('')
const subGroupSql = ref('')
const groupName = ref('')
const subGroupName = ref('')
const mainClassUUID = ref('')
const subGroupUUID = ref('')
const tagGroups = ref([])
const editingIndex = ref(-1)
const editText = ref('')
const editDesc = ref('')
const fileInput = ref(null)
const jsonFileInput = ref(null)
const txtFileInput = ref(null)
const isSelectGroup = ref(false)
const outPutName = ref('')

// 在script setup部分添加ref和函数
const yamlFileInput = ref(null)

function triggerYAMLUpload() {
    if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
        message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
        return
    }
    yamlFileInput.value.click();
}


function cleanAll() {
    tag.value = ''
    chinese.value = ''
    sql.value = ''
    groupSql.value = ''
    subGroupSql.value = ''
    groupName.value = ''
    subGroupName.value = ''
    mainClassUUID.value = ''
    subGroupUUID.value = ''
    tagGroups.value = []
    editingIndex.value = -1
    editText.value = ''
    editDesc.value = ''
    isSelectGroup.value = false
}

function handleTXTUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            const lines = content.split('\n').filter(line => line.trim());
            let i = 0;
            lines.forEach(line => {
                const [text, desc] = line.split(',');
                if (text && desc) {
                    const escapedText = text.trim().replace(/'/g, "''");
                    const escapedDesc = desc.trim().replace(/'/g, "''");
                    const result = uuidv7();
                    i = i + 1;
                    const time = parseInt(new Date().getTime() / 1000) + i;
                    const sql = `INSERT OR REPLACE INTO "tag_tags" ("text", "desc", "color", "create_time", "g_uuid", "t_uuid") VALUES ('${escapedText}', '${escapedDesc}', 'rgba(255, 123, 2, .4)', ${time}, '${subGroupUUID.value}', '${result}');`
                    tagGroups.value.push(sql);
                }
            });
        };
        reader.readAsText(file);
    }
}

function handleJSONUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const jsonData = JSON.parse(e.target.result);
                let i = 0;
                Object.entries(jsonData).forEach(([text, desc]) => {
                    const escapedText = text.replace(/'/g, "''");
                    const escapedDesc = desc.replace(/'/g, "''");
                    const result = uuidv7();
                    i = i + 1;
                    const time = parseInt(new Date().getTime() / 1000) + i;
                    const sql = `INSERT OR REPLACE INTO "tag_tags" ("text", "desc", "color", "create_time", "g_uuid", "t_uuid") VALUES ('${escapedText}', '${escapedDesc}', 'rgba(255, 123, 2, .4)', ${time}, '${subGroupUUID.value}', '${result}');`
                    tagGroups.value.push(sql);
                });
            } catch (error) {
                message({ type: "warn", str: 'message.jsonErrorMesg' });
            }
        };
        reader.readAsText(file);
    }
}

function handleYAMLUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            try {
                const yamlData = yaml.load(e.target.result);
                let i = 0;
                Object.entries(yamlData).forEach(([text, desc]) => {
                    const escapedText = text.replace(/'/g, "''");
                    const escapedDesc = String(desc).replace(/'/g, "''");
                    const result = uuidv7();
                    i = i + 1;
                    const time = parseInt(new Date().getTime() / 1000) + i;
                    const sql = `INSERT OR REPLACE INTO "tag_tags" ("text", "desc", "color", "create_time", "g_uuid", "t_uuid") VALUES ('${escapedText}', '${escapedDesc}', 'rgba(255, 123, 2, .4)', ${time}, '${subGroupUUID.value}', '${result}');`
                    tagGroups.value.push(sql);
                });
            } catch (error) {
                message({ type: "warn", str: 'message.yamlErrorMesg' });
            }
        };
        reader.readAsText(file);
    }
    event.target.value = '';
}

function handleFileUpload(event) {
    cleanAll();
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            const sqlStatements = content.split(';').filter(s => s.trim());
            sqlStatements.forEach(statement => {
                if ((statement.includes('tag_groups') || statement.includes('tag_subgroups')) && statement.includes('p_uuid')) {
                    if (statement.includes('g_uuid')) {
                        // 处理二级分类
                        subGroupSql.value = statement + ';';
                        // 提取g_uuid，使用更灵活的正则表达式
                        const valuesPart = statement.split("VALUES")[1].trim();
                        const lastValue = valuesPart.match(/,\s*'([^']+)'\)$/);
                        if (lastValue) subGroupUUID.value = lastValue[1];
                        const nameMatch = statement.match(/VALUES\s*\([^'"]*['"]([^'"]+)['"]/);
                        if (nameMatch) subGroupName.value = nameMatch[1].replace(/''/g, "'");
                    } else {
                        // 处理一级分类
                        groupSql.value = statement + ';';
                        // 提取p_uuid，使用更灵活的正则表达式
                        const valuesPart = statement.split('VALUES')[1].trim();
                        const lastValue = valuesPart.match(/,\s*'([^']+)'\)$/);
                        if (lastValue) mainClassUUID.value = lastValue[1];
                        const nameMatch = statement.match(/VALUES\s*\([^'"]*['"]([^'"]+)['"]/);
                        if (nameMatch) groupName.value = nameMatch[1].replace(/''/g, "'");
                    }
                } else if (statement.includes('tag_tags')) {
                    tagGroups.value.push(statement + ';');
                }
            });
        };
        reader.readAsText(file);
    }
    event.target.value = '';
}

function triggerTXTUpload() {
    if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
        message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
        return
    }
    txtFileInput.value.click();
}

function triggerJSONUpload() {
    if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
        message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
        return
    }
    jsonFileInput.value.click();
}

function triggerFileUpload() {
    fileInput.value.click();
}

function exportSQL() {
    const sqlContent = [groupSql.value, subGroupSql.value, ...tagGroups.value].join('\n');
    const blob = new Blob([sqlContent], { type: 'text/sql' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    if (outPutName.value.length <= 0) {
        const time = parseInt(new Date().getTime() / 1000);
        link.download = 'export_' + time + '.sql';
    } else {
        link.download = outPutName.value + '.sql';
    }
    link.click();
}

const exportOnlyTagSQL = () => {
    const sqlContent = [...tagGroups.value].join('\n');
    const blob = new Blob([sqlContent], { type: 'text/sql' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    if (outPutName.value.length <= 0) {
        const time = parseInt(new Date().getTime() / 1000);
        link.download = 'export_tags_' + time + '.sql';
    } else {
        link.download = outPutName.value + '.sql';
    }
    link.click();
}

function parseSQL(sql) {
    const textMatch = sql.match(/VALUES\s*\([^']*'([^']+)'/);
    const descMatch = sql.match(/VALUES\s*\([^']*'[^']*'\s*,\s*'([^']+)'/);
    return {
        text: textMatch ? textMatch[1].replace(/''/g, "'") : '',
        desc: descMatch ? descMatch[1].replace(/''/g, "'") : ''
    }
}

function deleteTag(index) {
    tagGroups.value.splice(index, 1);
}

function startEdit(index) {
    const tag = tagGroups.value[index];
    const parsed = parseSQL(tag);
    editText.value = parsed.text;
    editDesc.value = parsed.desc;
    editingIndex.value = index;
}

function confirmEdit(index) {
    const escapedText = editText.value.replace(/'/g, "''");
    const escapedDesc = editDesc.value.replace(/'/g, "''");
    tagGroups.value[index] = tagGroups.value[index].replace(/(VALUES\s*\([^']*')([^']+)'/, `$1${escapedText}'`).replace(/(VALUES\s*\([^']*'[^']*'\s*,\s*')([^']+)'/, `$1${escapedDesc}'`);
    editingIndex.value = -1;
}

function cancelEdit() {
    editingIndex.value = -1;
}

function generateSQL() {
    if (!subGroupUUID.value) {
        message({ type: "warn", str: 'message.pleaseAddSub' });
        return
    }
    const escapedTag = tag.value.replace(/'/g, "''")
    const escapedChinese = chinese.value.replace(/'/g, "''")
    const result = uuidv7();
    const time = parseInt(new Date().getTime() / 1000);
    sql.value = `INSERT OR REPLACE INTO "tag_tags" ("text", "desc", "color", "create_time", "g_uuid", "t_uuid") VALUES ('${escapedTag}', '${escapedChinese}', 'rgba(255, 123, 2, .4)', ${time}, '${subGroupUUID.value}', '${result}');`
    tagGroups.value.push(sql.value)
}

function generateGroupSQL() {
    if (groupName.value.length <= 0) {
        message({ type: "warn", str: 'importDialog.pleaseAddGroupName' });
        return
    }
    const escapedGroupName = groupName.value.replace(/'/g, "''")
    if (mainClassUUID.value.length <= 0) {
        mainClassUUID.value = uuidv7();
    }
    const time = parseInt(new Date().getTime() / 1000);
    groupSql.value = `INSERT OR REPLACE INTO "tag_groups" ("name", "color", "create_time", "p_uuid") VALUES ('${escapedGroupName}', 'rgba(255, 123, 2, .4)', ${time}, '${mainClassUUID.value}');`
}

function generateSubGroupSQL() {
    if (subGroupName.value.length <= 0) {
        message({ type: "warn", str: 'importDialog.pleaseAddSubGroupName' });
        return
    }
    if (!mainClassUUID.value) {
        message({ type: "warn", str: 'message.pleaseAddMainCeb' });
        return
    }
    const escapedSubGroupName = subGroupName.value.replace(/'/g, "''")
    if (subGroupUUID.value.length <= 0) {
        subGroupUUID.value = uuidv7();
    }
    const time = parseInt(new Date().getTime() / 1000);
    subGroupSql.value = `INSERT OR REPLACE INTO "tag_subgroups" ("name", "color", "create_time", "p_uuid", "g_uuid") VALUES ('${escapedSubGroupName}', 'rgba(255, 123, 2, .4)', ${time}, '${mainClassUUID.value}', '${subGroupUUID.value}');`
}

const tagGroupSelectDialogItem = ref(null)
const openSelectGroup = () => {
    tagGroupSelectDialogItem.value.open()
}

const sureToSelectInfo = (info) => {
    isSelectGroup.value = true
    groupName.value = info.group.name
    subGroupName.value = info.sub.name
    mainClassUUID.value = info.group.p_uuid
    subGroupUUID.value = info.sub.g_uuid
    const escapedGroupName = info.group.name.replace(/'/g, "''")
    const escapedSubGroupName = info.sub.name.replace(/'/g, "''")
    groupSql.value = `INSERT OR REPLACE INTO "tag_groups" ("name", "color", "create_time", "p_uuid") VALUES ('${escapedGroupName}', '${info.group.color}', ${info.group.create_time}, '${info.group.p_uuid}');`
    subGroupSql.value = `INSERT OR REPLACE INTO "tag_subgroups" ("name", "color", "create_time", "p_uuid", "g_uuid") VALUES ('${escapedSubGroupName}', '${info.sub.color}', ${info.sub.create_time}, '${info.group.p_uuid}', '${info.sub.g_uuid}');`
    // console.log(info)
}

const loading = ref(false)

const runSQLToServer = async (sql) => {
    loading.value = true
    try {
        await tagsApi.runSQLToServer(sql).then(res => {
            if (res.code != 200) {
                message({ type: "warn", str: res.message });
                return
            } else {
                getTagsList()
                message({ type: "success", str: 'importDialog.successImport' });
            }
        }).catch(err => {
            console.error(err)
            message({ type: "warn", str: 'importDialog.importFail' });
        })
    } catch (err) {
        console.error(err)
        message({ type: "warn", str: 'importDialog.importFail' });
    } finally {
        loading.value = false
    }
}

// 获取标签列表
const getTagsList = () => {
    window.postMessage({
        type: 'weilin_prompt_ui_tag_manager_refresh'
    }, '*')
}

const sureToImportTags = async () => {
    if (isSelectGroup.value) {
        if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
            message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
            return
        }
        const sqlContent = [...tagGroups.value]
        // console.log(sqlContent)
        await runSQLToServer(sqlContent)
    } else {
        if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
            message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
            return
        }
        const sqlContent = [groupSql.value, subGroupSql.value, ...tagGroups.value]
        await runSQLToServer(sqlContent)
        // console.log(sqlContent)
    }
}

watch(groupSql, (newVal, oldVal) => {
  if (!newVal || newVal === oldVal) return;
  // 提取 p_uuid（最后一个单引号包裹的内容）
  const newPUuid = newVal.match(/'([^']+)'\s*\)\s*;?$/)?.[1];
  const oldPUuid = oldVal?.match(/'([^']+)'\s*\)\s*;?$/)?.[1];

  if (newPUuid && oldPUuid && subGroupSql.value) {
    // 只替换原有 oldPUuid 为 newPUuid
    subGroupSql.value = subGroupSql.value.replace(
      new RegExp(`'${oldPUuid}'`, 'g'),
      `'${newPUuid}'`
    );
  }
});


watch(subGroupSql, (newVal, oldVal) => {
  if (!newVal || newVal === oldVal) return;
  // 提取 g_uuid（最后一个单引号包裹的内容）
  const newGUuid = newVal.match(/'([^']+)'\s*\)\s*;?$/)?.[1];
  const oldGUuid = oldVal?.match(/'([^']+)'\s*\)\s*;?$/)?.[1];
  if (newGUuid && oldGUuid && tagGroups.value.length > 0) {
    // 只替换原有 oldGUuid 为 newGUuid
    tagGroups.value = tagGroups.value.map(sql =>
      sql.replace(new RegExp(`'${oldGUuid}'`, 'g'), `'${newGUuid}'`)
    );
  }
});

defineExpose({
    open: () => {
        dialogVisible.value = true
    }
})
</script>

<style scoped>
.settings-content {
    display: flex;
    flex-direction: column;
    min-width: 600px;
    background-color: var(--weilin-prompt-ui-primary-bg);
    color: var(--weilin-prompt-ui-primary-text);
    padding-bottom: 20px;
    box-sizing: border-box;
}

input {
    padding: 8px;
    margin-right: 8px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-primary-text);
}

input:focus {
    outline: none;
    border-color: var(--weilin-prompt-ui-primary-color);
    box-shadow: 0 0 0 2px var(--weilin-prompt-ui-primary-color-fade);
}


button {
    padding: 8px 16px;
    background-color: #2196f3;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #1976d2;
}

button:disabled {
    background-color: #8d8f91;
}

.data-container {
    margin-top: 24px;
    padding: 16px;
    color: var(--weilin-prompt-ui-primary-bg);
    color: var(--weilin-prompt-ui-primary-text);
    border-radius: 4px;
    height: 500px;
}

.tag-group-container {
    height: 430px;
    overflow-y: auto;
}

h3,
h4 {
    margin: 8px 0;
    text-align: center;
}

p {
    margin: 4px 0;
    text-align: center;
}

.loading-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.loading-spinner {
    width: 40px;
    height: 40px;
    border: 4px solid #f3f3f3;
    border-top: 4px solid #3498db;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}

.info-links {
    margin-bottom: 16px;
    padding: 12px;
    background-color: var(--weilin-prompt-ui-secondary-bg);
    border-radius: 8px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
}

.info-link-item {
    display: flex;
    align-items: center;
    margin: 6px 0;
    font-size: 14px;
}

.info-link-label {
    color: var(--weilin-prompt-ui-secondary-text);
    min-width: 80px;
    font-weight: 500;
}

.info-link {
    color: var(--weilin-prompt-ui-primary-color);
    text-decoration: none;
    transition: color 0.2s;
}

.info-link:hover {
    color: var(--weilin-prompt-ui-primary-color-hover);
    text-decoration: underline;
}
</style>