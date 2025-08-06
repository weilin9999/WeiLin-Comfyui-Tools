<template>
    <!-- 加载遮罩层 -->
    <div v-if="loading" class="loading-overlay">
        <div class="loading-spinner"></div>
    </div>
    <Dialog v-model="dialogVisible" :title="t('danbooruManager.importBatchTitle')">
        <div class="settings-content">
            <div style="margin-bottom: 16px;">
                <button @click="cleanAll" class="upload-btn">{{ t('importDialog.cleanAll') }}</button>
                <button style="margin-left: 10px;" @click="exportSQL">{{ t('importDialog.dumpSQL') }}</button>

                <input style="width: 300px;margin-left: 10px;" v-model="outPutName"
                    :placeholder="t('importDialog.settingOutputName')" />

                <input type="file" ref="fileInput" @change="handleFileUpload" accept=".sql" style="display: none;" />
                <input type="file" ref="danbooruTxtFileInput" @change="handleDanbooruTXTUpload" accept=".txt,.csv"
                    style="display: none;" />
            </div>
            <div style="margin-bottom: 16px;">
                <input v-model="tag" placeholder="Tag" />
                <input v-model="chinese" :placeholder="t('importDialog.translater')" />
                <input v-model="hot" :placeholder="t('danbooruManager.hot')" type="number" />
                <input v-model="aliases" :placeholder="t('danbooruManager.aliases')" type="number" />
                <button @click="generateDanbooruSQL">{{ t('importDialog.add') }}</button>
                <button style="margin-left: 10px;" @click="triggerDanbooruTXTUpload" class="upload-btn">{{
                    t('danbooruManager.import') }}</button>
            </div>
            <div class="data-container">
                <div v-if="groupSql">
                    <h3>{{ parseSQL(groupSql).text }}</h3>
                    <div v-if="subGroupSql">
                        <h4>{{ parseSQL(subGroupSql).text }}</h4>
                        <div class="tag-group-container">
                            <div v-for="(tag, index) in tagGroups" :key="index"
                                style="display: flex;flex-direction: column;align-items: center;">
                                <p v-if="isDanbooruFormat(tag)">{{ parseDanbooruSQL(tag).tag }} - {{
                                    parseDanbooruSQL(tag).translate }} ({{ t('danbooruManager.hot') }}: {{
                                    parseDanbooruSQL(tag).hot }}, {{ t('danbooruManager.aliases') }}: {{
                                    parseDanbooruSQL(tag).aliases }})</p>
                                <p v-else>{{ parseSQL(tag).text }} - {{ parseSQL(tag).desc }}</p>
                                <div style="display: flex;align-items: center;">
                                    <div v-if="editingIndex === index">
                                        <input v-if="isDanbooruFormat(tag)" v-model="editText" placeholder="Tag" />
                                        <input v-else v-model="editText" placeholder="Tag" />
                                        <input v-if="isDanbooruFormat(tag)" v-model="editDesc"
                                            :placeholder="t('importDialog.translate')" />
                                        <input v-else v-model="editDesc" :placeholder="t('importDialog.translater')" />
                                        <input v-if="isDanbooruFormat(tag)" v-model="editHot"
                                            :placeholder="t('danbooruManager.hot')" type="number" />
                                        <input v-if="isDanbooruFormat(tag)" v-model="editAliases"
                                            :placeholder="t('danbooruManager.aliases')" type="number" />
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
                <div v-else-if="tagGroups.length > 0">
                    <h3>{{ t('danbooruManager.importTitle') }}</h3>
                    <div class="tag-group-container">
                        <div v-for="(tag, index) in tagGroups" :key="index"
                            style="display: flex;flex-direction: column;align-items: center;">
                            <p v-if="isDanbooruFormat(tag)">{{ parseDanbooruSQL(tag).tag }} - {{
                                parseDanbooruSQL(tag).translate }} (热度: {{ parseDanbooruSQL(tag).hot }}, 别名: {{
                                parseDanbooruSQL(tag).aliases }})</p>
                            <p v-else>{{ parseSQL(tag).text }} - {{ parseSQL(tag).desc }}</p>
                            <div style="display: flex;align-items: center;">
                                <div v-if="editingIndex === index">
                                    <input v-if="isDanbooruFormat(tag)" v-model="editText" placeholder="Tag" />
                                    <input v-else v-model="editText" placeholder="Tag" />
                                    <input v-if="isDanbooruFormat(tag)" v-model="editDesc"
                                        :placeholder="t('importDialog.translater')" />
                                    <input v-else v-model="editDesc" :placeholder="t('importDialog.translater')" />
                                    <input v-if="isDanbooruFormat(tag)" v-model="editHot"
                                        :placeholder="t('danbooruManager.hot')" type="number" />
                                    <input v-if="isDanbooruFormat(tag)" v-model="editAliases"
                                        :placeholder="t('danbooruManager.aliases')" type="number" />
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
        <template #footer>
            <button @click="dialogVisible = false">{{ t('promptBox.settings.close') }}</button>
            <button @click="sureToImportTags">{{ t('importDialog.sure') }}</button>
        </template>
    </Dialog>
</template>

<script setup>
import Dialog from '@/components/Dialog.vue'
import { ref, watch } from 'vue'
import { useI18n } from 'vue-i18n'
import message from '@/utils/message'
import { danbooruApi } from "@/api/danbooru";

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
const txtFileInput = ref(null)
const danbooruTxtFileInput = ref(null)
const isSelectGroup = ref(false)
const outPutName = ref('')
const hot = ref(0)
const aliases = ref(0)

function cleanAll() {
    tag.value = ''
    chinese.value = ''
    hot.value = 0
    aliases.value = 0
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

function handleDanbooruTXTUpload(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            const content = e.target.result;
            const lines = content.split('\n').filter(line => line.trim());
            let index = 1;

            lines.forEach(line => {
                const parts = line.split(',');
                if (parts.length >= 2) {
                    let tag, aliases, hot, translate;

                    if (parts.length === 2) {
                        // 只有两个参数：tag, translate
                        tag = parts[0].trim();
                        translate = parts[1].trim();
                        aliases = 0;
                        hot = 0;
                    } else if (parts.length >= 3) {
                        // 三个或更多参数：tag, aliases, hot, translate
                        tag = parts[0].trim();
                        aliases = parseInt(parts[1].trim()) || 0;
                        hot = parseInt(parts[2].trim()) || 0;

                        // 获取最后一个参数，将剩余的部分重新组合
                        const remainingParts = parts.slice(3);
                        translate = remainingParts.join(',').trim();

                        // 去除双引号
                        translate = translate.replace(/^"(.*)"$/, '$1');
                    }

                    // 转义单引号
                    const escapedTag = tag.replace(/'/g, "''");
                    const escapedTranslate = translate.replace(/'/g, "''");

                    const sql = `INSERT INTO "danbooru_tag" ("tag", "color_id", "translate", "hot", "aliases") VALUES ('${escapedTag}', '', '${escapedTranslate}', ${hot}, ${aliases});`;
                    tagGroups.value.push(sql);
                    index++;
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

function triggerDanbooruTXTUpload() {
    danbooruTxtFileInput.value.click();
}


function exportSQL() {
    // 根据数据格式选择导出内容
    let sqlContent;
    if (tagGroups.value.length > 0 && isDanbooruFormat(tagGroups.value[0])) {
        // danbooru格式只导出标签数据
        sqlContent = [...tagGroups.value].join('\n');
    } else {
        // 原有格式导出所有数据
        sqlContent = [groupSql.value, subGroupSql.value, ...tagGroups.value].join('\n');
    }

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

function parseSQL(sql) {
    const textMatch = sql.match(/VALUES\s*\([^']*'([^']+)'/);
    const descMatch = sql.match(/VALUES\s*\([^']*'[^']*'\s*,\s*'([^']+)'/);
    return {
        text: textMatch ? textMatch[1].replace(/''/g, "'") : '',
        desc: descMatch ? descMatch[1].replace(/''/g, "'") : ''
    }
}

function isDanbooruFormat(sql) {
    return sql.includes('danbooru_tag');
}

function parseDanbooruSQL(sql) {
    // 匹配当前生成的 danbooru_tag 表的 SQL 语句格式
    // INSERT INTO "danbooru_tag" ("tag", "color_id", "translate", "hot", "aliases") VALUES ('tag_name', '', 'translate_text', 123, 1);
    const match = sql.match(/VALUES\s*\(\s*'([^']+)'\s*,\s*'([^']*)'\s*,\s*'([^']*)'\s*,\s*(\d+)\s*,\s*(\d+)\s*\)/);

    if (match) {
        return {
            tag: match[1].replace(/''/g, "'"),
            color_id: match[2],
            translate: match[3].replace(/''/g, "'"),
            hot: parseInt(match[4]),
            aliases: parseInt(match[5])
        };
    }

    return {
        tag: '',
        color_id: '',
        translate: '',
        hot: 0,
        aliases: 0
    };
}

// ...existing code...

const editHot = ref(0)
const editAliases = ref(0)

// ...existing code...

function startEdit(index) {
    const tag = tagGroups.value[index];
    if (isDanbooruFormat(tag)) {
        const parsed = parseDanbooruSQL(tag);
        editText.value = parsed.tag;
        editDesc.value = parsed.translate;
        editHot.value = parsed.hot;
        editAliases.value = parsed.aliases;
    } else {
        const parsed = parseSQL(tag);
        editText.value = parsed.text;
        editDesc.value = parsed.desc;
    }
    editingIndex.value = index;
}

function confirmEdit(index) {
    const escapedText = editText.value.replace(/'/g, "''");
    const escapedDesc = editDesc.value.replace(/'/g, "''");

    if (isDanbooruFormat(tagGroups.value[index])) {
        // 更新 danbooru_tag 格式的 SQL
        const parsed = parseDanbooruSQL(tagGroups.value[index]);
        const hot = parseInt(editHot.value) || 0;
        const aliases = parseInt(editAliases.value) || 0;

        tagGroups.value[index] = `INSERT INTO "danbooru_tag" ("tag", "color_id", "translate", "hot", "aliases") VALUES ('${escapedText}', '${parsed.color_id}', '${escapedDesc}', ${hot}, ${aliases});`;
    } else {
        // 更新原有格式的 SQL
        tagGroups.value[index] = tagGroups.value[index].replace(/(VALUES\s*\([^']*')([^']+)'/, `$1${escapedText}'`).replace(/(VALUES\s*\([^']*'[^']*'\s*,\s*')([^']+)'/, `$1${escapedDesc}'`);
    }
    editingIndex.value = -1;
}

function cancelEdit() {
    editingIndex.value = -1;
    editText.value = '';
    editDesc.value = '';
    editHot.value = 0;
    editAliases.value = 0;
}

function deleteTag(index) {
    tagGroups.value.splice(index, 1);
}

function generateDanbooruSQL() {
    // 转义单引号
    const escapedTag = tag.value.replace(/'/g, "''");
    const escapedChinese = chinese.value.replace(/'/g, "''");
    const hotValue = parseInt(hot.value) || 0;
    const aliasesValue = parseInt(aliases.value) || 0;

    const sql = `INSERT INTO "danbooru_tag" ("tag", "color_id", "translate", "hot", "aliases") VALUES ('${escapedTag}', '', '${escapedChinese}', ${hotValue}, ${aliasesValue});`;
    tagGroups.value.push(sql);

    // 清空输入框
    tag.value = '';
    chinese.value = '';
    hot.value = 0;
    aliases.value = 0;
}

const loading = ref(false)

const runSQLToServer = async (sql) => {
    loading.value = true
    try {
        await danbooruApi.runSQLToServer(sql).then(res => {
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
    // 对于danbooru格式，不需要分组SQL
    if (tagGroups.value.length > 0 && isDanbooruFormat(tagGroups.value[0])) {
        const sqlContent = [...tagGroups.value]
        await runSQLToServer(sqlContent)
    } else {
        // 原有逻辑保持不变
        if (isSelectGroup.value) {
            if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
                message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
                return
            }
            const sqlContent = [...tagGroups.value]
            await runSQLToServer(sqlContent)
        } else {
            if (groupSql.value.length <= 0 || subGroupSql.value.length <= 0) {
                message({ type: "warn", str: 'importDialog.pleaseFullRequest' });
                return
            }
            const sqlContent = [groupSql.value, subGroupSql.value, ...tagGroups.value]
            await runSQLToServer(sqlContent)
        }
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
    z-index: 1099;
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