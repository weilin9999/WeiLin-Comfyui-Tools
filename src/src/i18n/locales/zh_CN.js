import { version } from "../../utils/version.js"
export default {
    promptBox: {
        placeholder: '请输入文本...',
        delete: '删除',
        newline: '换行',
        tab: '制表符',
        windowTitle: "WeiLin提示词UI窗口 "+version,
        windowTitleGlobal: "WeiLin全局提示词UI窗口 "+version,
        translate: '翻译',
        translatePlaceholder: '请输入要翻译的文本',
        weight: '权重',
        weightPlaceholder: '请输入权重',
        addBracket: '添加括号',
        removeLayer: '减去括号',
        oneClickTranslate: '一键翻译未翻译的词组',
        settings: {
            title: '设置',
            cancel: '取消',
            save: '保存',
            translator: '翻译设置',
            sourceLanguage: '源语言',
            targetLanguage: '目标语言',
            chinese_simplified: '简体中文',
            english: '英语',
            close: '关闭',
            auto_detect: '自动检测',
            setting_floating_ball: '悬浮球设置',
            setting_prompt_box: '提示词设置',
            enablePromptCommaShow: '显示提示词逗号',
            floatingBallCount: '悬浮球数量',
            floatingBallCountPlaceholder: '请输入悬浮球数量',
            floatingBallSize: '悬浮球大小',
            floatingBallSizePlaceholder: '请输入悬浮球大小',
            enableFloatingBall: '启用悬浮球',
            enableCommaConversion: '启用逗号转换，全角逗号转为半角逗号',
            enablePeriodConversion: '启用句号转换，全角句号转为半角句号',
            enableBracketConversion: '启用括号转换，全角括号转为半角括号',
            enableAngleBracketConversion: '启用尖括号转换，全角尖括号转为半角尖括号',
            enableUnderscoreToBracket: '启用下划线转换，下划线转换为空格',
            setting_openai_box: 'OpenAI设置',
            openai_api_key: 'API Key',
            openai_api_key_placeholder: '请输入API Key',
            openai_api_key_save: '保存',
            openaiSettings: 'OpenAI设置',
            openai_base_url: 'Base URL',
            openai_base_url_placeholder: '请输入Base URL',
            openai_model: '模型',
            openai_model_placeholder: '请输入模型',
            not_set: '未设置',
            edit: '编辑',
            delete: '删除',
            selectedOpenaiConfig: '当前选择的OpenAI配置',
            addNewConfig: '添加OpenAI配置',
            setting_sponsor_me: '赞助我',
            sponsorMe: '赞助我',
            sponsorMeTip: '赞助我，支持我继续开发',
            sponsorMeLink: '唯一赞助链接 https://afdian.com/a/weilin9999',
            setting_start_panel: '启动面板',
            startPanel: '启动面板',
            startPanelTip: '点击启动面板，启动成功后会自动打开面板页面',
            selectTranslater: '选择翻译器',
            selectOptionNetworkTranslater :'三方网络翻译',
            selectOptionPythonTranslater :'翻译库翻译',
            apply: '应用',
            selectOptionNetworkTranslaterTitle: '三方网络翻译设置',
            selectOptionPythonTranslaterTitle: '翻译库设置',
            selectOptionNetworkTranslaterInfo: '使用的三方工具是（仅网络翻译）',
            selectOptionPythonTranslaterInfo: '使用的翻译包为translators',
            install: '安装',
            nowTranlaterPackageState: '当前翻译包状态：',
            tranlaterPackageStateTrue: '已安装',
            tranlaterPackageStateFlase: '未安装',
            installed: '正在安装中...',
            installTranslaterPackageInfo: '当前正在安装翻译库中，请不要关闭窗口！等待安装完成',
            translaterSetting: "翻译设置",
            chooseTranslaterSetting: "选择翻译服务：",
            translaterLangSourceSetting: "翻译语言：",
            translaterLangTargeSetting: "翻译目标语言：",
            saveTranslaterSetting: "保存设置",
            testTranslaterTitle: "测试翻译",
            inputTestTranslater: "输入翻译内容：",
            outPutTestTranslater: "翻译结果：",
            testingTranslater: "测试翻译",
            inputTestTranslaterPlaceholder: "请输入要翻译的内容",
            outPutTestTranslaterPlaceholder: "翻译结果将显示在这里",
        },
    },
    controls: {
        language: '语言',
        settings: '设置',
        switchTheme: '切换主题',
        darkMode: '夜间模式',
        lightMode: '日间模式',
        tagManager: '标签管理',
        loraStack: 'Lora堆',
        loraManager: 'Lora管理',
        history: '历史记录',
        addLora: '添加Lora',
        removeLora: '移除Lora',
        lookOnLora: '查看Lora',
        aiChat: 'AI对话',
        github: "Github主页",
        shareCloudData: '共享云数据',
    },
    theme: {
        toggle: '切换主题'
    },
    common: {
        "confirmDelete": "确认删除",
        "delete": "删除",
        "cancel": "取消",
        "confirm": "确定",
        "edit": "编辑",
        "save": "保存",
        "refresh": "刷新",
        "copy": "复制",
        "copySuccess": "复制成功",
        "copyFailed": "复制失败",
        "windowSize":"调节窗口大小",
        "showMore": "显示更多",
        "showLess": "收起"
    },
    cloudWindow:{
        "windowTitle": "共享云仓库",
        back: '返回上一级',
        currentPath: '当前路径',
        tagDatabase: 'Tag 数据库',
        danbooruDatabase: 'Danbooru 数据库',
        open: "打开文件夹",
        installed: '已安装',
        install: '安装',
        installing: '正在安装...'
    },
    nodeListWindow:{
        "windowTitle": "节点列表",
        "openPromptUI": "打开提示词编辑器",
    },
    lora: {
        "title": "Lora 信息",
        "file": "文件",
        "hash": "Hash值",
        "civitai": "Civitai",
        "viewOnCivitai": "在 Civitai 上查看",
        "fetchFromCivitai": "从 Civitai 获取信息",
        "modelNotFound": "模型未找到",
        "modelNotFoundTip": "该模型在 Civitai 上未找到，可能是私有模型或已被删除",
        "name": "名称",
        "nameTip": "模型的显示名称",
        "type": "类型",
        "baseModel": "基础模型",
        "trainedWords": "训练词",
        "trainedWordsTip": "模型训练时使用的关键词，点击可选择复制",
        "selectedWords": "已选择 {count} 个词",
        "strengthMin": "最小强度",
        "strengthMinTip": "推荐的最小强度值",
        "strengthMax": "最大强度",
        "strengthMaxTip": "推荐的最大强度值",
        "promptWords": "提示词",
        "promptWordsTip": "使用该模型时的推荐提示词",
        "loraWorks": "Lora提示词",
        "strWeight": "文本强度权重",
    },
    tagManager: {
        "deletePrimaryCategoryConfirm": "确定要删除分类 {name} 吗？",
        "deleteGroupConfirm": "确定要删除分组 {name} 吗？",
        "deleteTagConfirm": "确定要删除标签 {name} 吗？",
        "windowTitle": "标签管理器",
        "categories": "分类管理",
        "groups": "分组管理",
        "selectCategory": "请选择分类",
        "selectGroup": "请选择分组",
        "addPrimaryCategory": "添加分类",
        "addGroup": "添加分组",
        "editPrimaryCategory": "编辑分类",
        "editGroup": "编辑分组",
        "editTag": "编辑标签",
        "categoryName": "分类名称",
        "categoryNamePlaceholder": "请输入分类名称",
        "categoryNameRequired": "分类名称不能为空",
        "groupName": "分组名称",
        "groupNamePlaceholder": "请输入分组名称",
        "groupNameRequired": "分组名称不能为空",
        "addTag": "添加Tag",
        "text": "Tag描述",
        "textPlaceholder": "请输入Tag描述",
        "description": "Tag",
        "descriptionPlaceholder": "请输入Tag",
        "textRequired": "Tag和Tag描述不能为空",
        "backgroundColor": "背景颜色",
        "colorPickerTitle": "选择颜色",
        "opacity": "透明度",
        "searchPlaceholder": "搜索Tag...",
        "noResults": "未找到相关结果",
        "searchInCategory": "在分类中",
        "searchInTag": "在Tag中",
        "save": "保存",
        "cancel": "取消",
        "confirm": "确定",
        "delete": "删除",
        "addSubCategory": "添加子分类",
        "editSubCategory": "编辑子分类",
        "subCategoryName": "子分类名称",
        "subCategoryNamePlaceholder": "请输入子分类名称",
        "subCategoryNameRequired": "子分类名称不能为空",
        "deleteConfirmTitle": "确认删除",
        "deleteConfirmMessage": "此操作将永久删除该{type}，是否继续？",
        "deleteSuccess": "删除成功",
        "deleteFailed": "删除失败",
        "saveSuccess": "保存成功",
        "saveFailed": "保存失败",
        "colorPickerAlpha": "透明度",
        "colorPickerHex": "十六进制颜色值",
        "colorPreview": "颜色预览",
        "dragToSort": "拖动排序",
        "searchTags": "搜索标签",
        "noTagsFound": "未找到标签",
        "noGroupsFound": "未找到分组",
        "noCategoriesFound": "未找到分类",
        "refresh": "刷新",
        "refreshing": "刷新中...",
        "refreshSuccess": "刷新成功",
        "refreshFailed": "刷新失败",
        "search": "搜索",
        "searching": "搜索中...",
        "searchResult": "搜索结果",
        "searchInPath": "位于: {path}",
        "category": "分类",
        "group": "分组",
        "tag": "标签",
        "resultType": {
            "category": "分类",
            "group": "分组",
            "tag": "标签"
        },
        "hasDeleteAction": "批量删除",
        "deleteSelected": "删除选中",
        "confirmDeleteSelected": "确定要删除选中标签吗？",
        "cancelDelete": "取消删除",
        "moveTag": "移动标签",
        "targetTag": "目标标签",
        "movePosition": "移动位置",
        "moveBefore": "移动到目标标签之前",
        "moveAfter": "移动到目标标签之后",
        "editTag": "编辑标签",
        "deleteTag": "删除标签",
        "editGroupMode": "编辑模式",
        "exitEditMode": "退出编辑模式",
        "autoAddSearchTag": "搜索的Tag自动添加到提示词中",
    },
    loraManager: {
        windowTitle: "Lora管理",
        modelWeight: "模型权重",
        textEncoderWeight: "文本权重",
        all: "全部",
        refresh: "刷新",
        cacheAll: "缓存全部Lora信息",
        searchPlaceholder: "搜索Lora...",
    },
    "message": {
        "copySuccess": "复制成功",
        "copyFailed": "复制失败",
        "saveSuccess": "保存成功",
        "saveFailed": "保存失败",
        "deleteSuccess": "删除成功",
        "deleteFailed": "删除失败",
        "operationSuccess": "操作成功",
        "operationFailed": "操作失败",
        "networkError": "网络错误",
        "unknownError": "未知错误",
        "refreshSuccess": "刷新成功",
        "refreshFailed": "刷新失败",
        "loadingData": "加载数据中...",
        "dataLoaded": "数据加载完成",
        "editSuccess": "编辑成功",
        "editFailed": "编辑失败",
        "addSuccess": "添加成功",
        "addFailed": "添加失败",
        "addFavoriteSuccess": "已添加到收藏夹",
        "addFavoriteIsExist": "已添加到收藏夹",
        "error": "错误",
        "editNameExist": "名称已存在",
        "moveSuccess": "移动成功",
        "moveFailed": "移动失败",
        "setLanguageSuccess": "设置语言成功",
        "setLanguageFailed": "设置语言失败",
        "startPanelSuccess": "启动面板成功",
        "startPanelFailed": "启动面板失败",
        "isLoading": "已在执行中请等待",
        "loaddingPrc": "执行进度 {name}%",
        "loaddingSuccess": "已全部加载成功",
        "noFinishKuo": "括号不完整，请检查输入",
        "getTranslaterFail": "获取翻译设置失败",
        "applyTranslaterFail": "应用翻译设置失败",
        "applyToTranslaterFail": "切换翻译库翻译需要安装翻译库，请先安装翻译库再应用设置",
        "applyTranslaterSuccess": "应用翻译设置成功",
        tranlaterPackageInstallFail: '等待安装超时，请查看后台安装情况，若安装成功再次点击安装即可验证',
        tranlaterPackageInstallSuccess: '安装翻译包成功',
        translaterTestFail: "翻译失败，请使用其它的翻译服务进行尝试",
        "installPackageSuccess": "安装共享数据成功！",
        "installPackageFail": "安装共享数据失败，请查看后台错误"
    },
    history: {
        "title": "历史记录",
        "search_placeholder": "搜索历史记录...",
        "search": "搜索",
        "windowTitle": "历史记录",
        "favorites": "收藏夹",
        "history": "历史记录",
        "refresh": "刷新",
        "refresh_history": "刷新历史记录",
        "refresh_favorites": "刷新收藏夹",
        "add_to_favorites": "添加到收藏夹",
        "delete_history": "删除历史记录",
        "use_item": "使用",
        "add_new": "添加收藏",
        "bulk_delete": "批量删除",
        "deleteHistoryConfirm": "确定要删除历史记录 {name} 吗？",
        "deleteFavoriteConfirm": "确定要删除收藏夹 {name} 吗？",
        "confirmDeleteSelected": "确定要删除选中的信息吗？",
        "cancel_delete": "取消删除",
        "sure_delete": "确定删除",
        "deleteSelected": "删除选中",
        "dialog": {
            "add_tag": "添加收藏",
            "edit_tag": "编辑收藏",
            "name": "名称",
            "name_placeholder": "请输入名称",
            "tag": "标签",
            "tag_placeholder": "请输入标签",
            "background_color": "背景颜色",
            "background_color_placeholder": "请选择背景颜色",
            "edit_favorite": "编辑收藏",
            "delete_favorite": "删除收藏",
        },
        "edit_favorite": "编辑收藏",
        "delete_favorite": "删除收藏",
        "use_favorite": "使用收藏"
    },
    floatingBall: {
        "promptBox": "打开全局提示词",
        "tagManager": "打开标签管理",
        "loraManager": "打开Lora管理",
        "aiWindow": "打开AI对话",
        "restoreWindow": "重置所有窗口",
        "openNodeListWindow": "打开节点列表",
    },
    aiWindow: {
        "windowTitle": "AI对话窗口",
        "newChat": "新建对话",
        "chatName": "对话",
        "thinking": "思考中...",
        "send": "发送",
        "inputMessage": "输入你的消息..."
    },
    translaterService: {
        "niutrans": "小牛翻译",
        "mymemory": "MyMemory",
        "alibaba": "阿里巴巴翻译",
        "baidu": "百度翻译",
        "modernmt": "ModernMT",
        "volcengine": "火山翻译",
        "iciba": "金山词霸",
        "iflytek": "科大讯飞翻译",
        "google": "谷歌翻译",
        "bing": "必应翻译",
        "lingvanex": "Lingvanex",
        "yandex": "Yandex翻译",
        "itranslate": "iTranslate",
        "systran": "SYSTRAN",
        "argos": "Argos翻译",
        "apertium": "Apertium",
        "reverso": "Reverso翻译",
        "deepl": "DeepL翻译",
        "cloudtranslation": "云翻译",
        "qqtransmart": "腾讯翻译君",
        "translatecom": "Translate.com",
        "sogou": "搜狗翻译",
        "tilde": "Tilde翻译",
        "caiyun": "彩云小译",
        "qqfanyi": "腾讯翻译",
        "translateme": "TranslateMe",
        "papago": "Papago翻译",
        "mirai": "未来翻译",
        "youdao": "有道翻译",
        "iflyrec": "讯飞听见翻译",
        "hujiang": "沪江翻译",
        "yeekit": "译库翻译",
        "languagewire": "LanguageWire",
        "elia": "Elia翻译",
        "judic": "Judic翻译",
        "mglip": "蒙古语翻译",
        "utibet": "藏语翻译"
    },
    translaterLanguage: {
        "english": "英语",
        "chinese": "中文",
        "arabic": "阿拉伯语",
        "russian": "俄语",
        "french": "法语",
        "german": "德语",
        "spanish": "西班牙语",
        "portuguese": "葡萄牙语",
        "italian": "意大利语",
        "japanese": "日语",
        "korean": "韩语",
        "greek": "希腊语",
        "dutch": "荷兰语",
        "hindi": "印地语",
        "turkish": "土耳其语",
        "malay": "马来语",
        "thai": "泰语",
        "vietnamese": "越南语",
        "indonesian": "印度尼西亚语",
        "hebrew": "希伯来语",
        "polish": "波兰语",
        "mongolian": "蒙古语",
        "czech": "捷克语",
        "hungarian": "匈牙利语",
        "estonian": "爱沙尼亚语",
        "bulgarian": "保加利亚语",
        "danish": "丹麦语",
        "finnish": "芬兰语",
        "romanian": "罗马尼亚语",
        "swedish": "瑞典语",
        "slovenian": "斯洛文尼亚语",
        "persian/farsi": "波斯语/波斯语",
        "bosnian": "波斯尼亚语",
        "serbian": "塞尔维亚语",
        "fijian": "斐济语",
        "filipino": "菲律宾语",
        "haitiancreole": "海地克里奥尔语",
        "catalan": "加泰罗尼亚语",
        "croatian": "克罗地亚语",
        "latvian": "拉脱维亚语",
        "lithuanian": "立陶宛语",
        "urdu": "乌尔都语",
        "ukrainian": "乌克兰语",
        "welsh": "威尔士语",
        "tahiti": "塔希提语",
        "tongan": "汤加语",
        "swahili": "斯瓦希里语",
        "samoan": "萨摩亚语",
        "slovak": "斯洛伐克语",
        "afrikaans": "南非荷兰语",
        "norwegian": "挪威语",
        "bengali": "孟加拉语",
        "malagasy": "马达加斯加语",
        "maltese": "马耳他语",
        "queretaro otomi": "克雷塔罗奥托米语",
        "klingon/tlhingan hol": "克林贡语",
        "gujarati": "古吉拉特语",
        "tamil": "泰米尔语",
        "telugu": "泰卢固语",
        "punjabi": "旁遮普语",
        "amharic": "阿姆哈拉语",
        "azerbaijani": "阿塞拜疆语",
        "bashkir": "巴什基尔语",
        "belarusian": "白俄罗斯语",
        "cebuano": "宿务语",
        "chuvash": "楚瓦什语",
        "esperanto": "世界语",
        "basque": "巴斯克语",
        "irish": "爱尔兰语"
    }
} 