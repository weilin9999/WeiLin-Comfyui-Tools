import { version } from "../../utils/version.js"
export default {
    promptBox: {
        placeholder: 'Please enter text...',
        delete: 'Delete',
        newline: 'New Line',
        tab: 'Tab',
        windowTitle: "WeiLin Prompt UI Window "+ version,
        windowTitleGlobal: "WeiLin Global Prompt UI Window "+ version,
        translate: 'Translate',
        translatePlaceholder: 'Please enter the text to be translated',
        weight: 'Weight',
        weightPlaceholder: 'Please enter the weight',
        addBracket: 'Add Bracket',
        removeLayer: 'Remove Bracket',
        oneClickTranslate: 'One Click Translate Untranslated Phrases',
        hiddenHint: "Double-click to show",
        tagTips: "Double-click the left mouse button to mask the Tag<br>click the Tag to edit<br>and drag the Tag to drag",
        settings: {
            title: 'Settings',
            cancel: 'Cancel',
            save: 'Save',
            translator: 'Translator',
            sourceLanguage: 'Source Language',
            targetLanguage: 'Target Language',
            chinese_simplified: 'Chinese Simplified',
            english: 'English',
            close: 'Close',
            auto_detect: 'Auto Detect',
            setting_floating_ball: 'Setting Floating Ball',
            setting_prompt_box: 'Setting Prompt Box',
            enablePromptCommaShow: 'Show Prompt Comma',
            floatingBallCount: 'Floating Ball Count',
            floatingBallCountPlaceholder: 'Please enter the number of floating balls',
            floatingBallSize: 'Floating Ball Size',
            floatingBallSizePlaceholder: 'Please enter the size of the floating ball',
            enableFloatingBall: 'Enable Floating Ball',
            enableCommaConversion: 'Enable Comma Conversion',
            enablePeriodConversion: 'Enable Period Conversion',
            enableBracketConversion: 'Enable Bracket Conversion',
            enableAngleBracketConversion: 'Enable Angle Bracket Conversion',
            enableUnderscoreToBracket: 'Enable Underscore to Bracket',
            setting_openai_box: 'OpenAI Settings',
            openai_api_key: 'API Key',
            openai_api_key_placeholder: 'Please enter API Key',
            openai_api_key_save: 'Save',
            openaiSettings: 'OpenAI Settings',
            openaiSettings_api_key: 'API Key',
            openaiSettings_api_key_placeholder: 'Please enter API Key',
            openaiSettings_api_key_save: 'Save',
            openai_base_url: 'Base URL',
            openai_base_url_placeholder: 'Please enter Base URL',
            openai_model: 'Model',
            openai_model_placeholder: 'Please enter Model',
            not_set: 'Not Set',
            edit: 'Edit',
            delete: 'Delete',
            selectedOpenaiConfig: 'Selected OpenAI Config',
            addNewConfig: 'Add New Config',
            setting_sponsor_me: 'Sponsor Me',
            sponsorMe: 'Sponsor Me',
            sponsorMeTip: 'Sponsor Me, Support Me to Continue Development',
            sponsorMeLink: 'Unique Sponsor Link https://afdian.com/a/weilin9999',
            setting_start_panel: 'Start Panel',
            startPanel: 'Start Panel',
            startPanelTip: 'Click Start Panel, after successful startup, the panel page will be automatically opened',
            selectTranslater: 'select translater',
            selectOptionNetworkTranslater :'Three party online translation',
            selectOptionPythonTranslater :'Translation Library Translation',
            apply: 'Apply',
            selectOptionNetworkTranslaterTitle: 'Three party network translation settings',
            selectOptionPythonTranslaterTitle: 'Translation library settings',
            selectOptionNetworkTranslaterInfo: 'The third-party tool used is (only for online translation)',
            selectOptionPythonTranslaterInfo: 'The translation package used is translators',
            install: 'Install',
            nowTranlaterPackageState: 'now transtler package state:',
            tranlaterPackageStateTrue: 'installed',
            tranlaterPackageStateFlase: 'not installed',
            installed: 'is installed ....',
            installTranslaterPackageInfo: 'Currently installing translation library, please do not close the window! Wait for installation to complete',
            translaterSetting: "Translation Settings",
            chooseTranslaterSetting: "Choose a translation service:",
            translaterLangSourceSetting: "Translation language:",
            translaterLangTargeSetting: "Translation target language:",
            saveTranslaterSetting: "Save Settings",
            testTranslaterTitle: "Test translation",
            inputTestTranslater: "Enter translation content:",
            outPutTestTranslater: "Translation result:",
            testingTranslater: "Test translation",
            inputTestTranslaterPlaceholder: "Please enter the content to be translated",
            outPutTestTranslaterPlaceholder: "The translation result will be displayed here",
            errorPrompt: "Read the prompt node failed",
        },
    },
    controls: {
        language: 'Language',
        settings: 'Settings',
        switchTheme: 'Switch Theme',
        darkMode: 'Dark Mode',
        lightMode: 'Light Mode',
        tagManager: 'Tag Manager',
        loraStack: 'Lora Stack',
        loraManager: 'Lora Manager',
        history: 'History',
        addLora: 'Add Lora',
        removeLora: 'Remove Lora',
        lookOnLora: 'Look On Lora',
        aiChat: 'AI Chat',
        github: "Github Home",
        shareCloudData: 'Share Cloud Data',
    },
    theme: {
        toggle: 'Switch Theme'
    },
    lora: {
        "title": "Lora Information",
        rawTitle: "LoraRaw",
        "file": "File",
        "hash": "Hash",
        "civitai": "Civitai",
        "viewOnCivitai": "View on Civitai",
        "fetchFromCivitai": "Fetch from Civitai",
        "modelNotFound": "Model not found",
        "modelNotFoundTip": "The model was not found on Civitai. It might be private or deleted",
        "name": "Name",
        "nameTip": "Display name of the model",
        "type": "Type",
        "baseModel": "Base Model",
        "trainedWords": "Trained Words",
        "trainedWordsTip": "Keywords used in model training, click to select for copying",
        "selectedWords": "{count} words selected",
        "strengthMin": "Min Strength",
        "strengthMinTip": "Recommended minimum strength value",
        "strengthMax": "Max Strength",
        "strengthMaxTip": "Recommended maximum strength value",
        "promptWords": "Prompt Words",
        "promptWordsTip": "Recommended prompt words when using this model",
        "loraWorks": "Lora Prompt Words",
        "strWeight": "Text Strength Weight",
        hideLora: "Hidden Lora",
        showLora: "Show Lora",
        baseModel: "Base Model",
        skipClip: "Clip Skip",
        seeLoraRaw: "LoraRaw",
    },
    common: {
        confirmDelete: "Confirm Delete",
        delete: "Delete",
        cancel: "Cancel",
        confirm: "Confirm",
        edit: "Edit",
        save: "Save",
        "refresh": "Refresh",
        "copy": "Copy",
        "copySuccess": "Copied successfully",
        "copyFailed": "Copy failed",
        "windowSize":"Adjust window size",
        "showMore": "show more",
        "showLess": "show less",
    },
    nodeListWindow:{
        "windowTitle": "Node List",
        "openPromptUI": "Open Prompt UI",
    },
    tagManager: {
        "deletePrimaryCategoryConfirm": "Are you sure you want to delete category {name}?",
        "deleteGroupConfirm": "Are you sure you want to delete group {name}?",
        "deleteTagConfirm": "Are you sure you want to delete tag {name}?",
        "windowTitle": "Tag Manager",
        "categories": "Categories",
        "groups": "Groups",
        "selectCategory": "Please select a category",
        "selectGroup": "Please select a group",
        "addPrimaryCategory": "Add Category",
        "addGroup": "Add Group",
        "editPrimaryCategory": "Edit Category",
        "editGroup": "Edit Group",
        "editTag": "Edit Tag",
        "categoryName": "Category Name",
        "categoryNamePlaceholder": "Enter category name",
        "categoryNameRequired": "Category name is required",
        "groupName": "Group Name",
        "groupNamePlaceholder": "Enter group name",
        "groupNameRequired": "Group name is required",
        "addTag": "Add Tag",
        "text": "Tag Description",
        "textPlaceholder": "Enter tag Description",
        "description": "Tag",
        "descriptionPlaceholder": "Enter tag",
        "textRequired": "Tag and Tag description cannot be empty",
        "backgroundColor": "Background Color",
        "colorPickerTitle": "Select Color",
        "opacity": "Opacity",
        "searchPlaceholder": "Search tags...",
        "noResults": "No results found",
        "searchInCategory": "in category",
        "searchInTag": "in tag",
        "save": "Save",
        "cancel": "Cancel",
        "confirm": "Confirm",
        "delete": "Delete",
        "addSubCategory": "Add Sub-category",
        "editSubCategory": "Edit Sub-category",
        "subCategoryName": "Sub-category Name",
        "subCategoryNamePlaceholder": "Enter sub-category name",
        "subCategoryNameRequired": "Sub-category name is required",
        "deleteConfirmTitle": "Confirm Delete",
        "deleteConfirmMessage": "This action will permanently delete this {type}. Continue?",
        "deleteSuccess": "Deleted successfully",
        "deleteFailed": "Delete failed",
        "saveSuccess": "Saved successfully",
        "saveFailed": "Save failed",
        "colorPickerAlpha": "Opacity",
        "colorPickerHex": "Hex Color Value",
        "colorPreview": "Color Preview",
        "dragToSort": "Drag to Sort",
        "searchTags": "Search Tags",
        "noTagsFound": "No tags found",
        "noGroupsFound": "No groups found",
        "noCategoriesFound": "No categories found",
        "refresh": "Refresh",
        "refreshing": "Refreshing...",
        "refreshSuccess": "Refresh successful",
        "refreshFailed": "Refresh failed",
        "search": "Search",
        "searching": "Searching...",
        "searchResult": "Search Result",
        "searchInPath": "Located in: {path}",
        "category": "Category",
        "group": "Group",
        "tag": "Tag",
        "resultType": {
            "category": "Category",
            "group": "Group",
            "tag": "Tag"
        },
        "hasDeleteAction": "Batch Delete",
        "deleteSelected": "Delete Selected",
        "confirmDeleteSelected": "Are you sure you want to delete the selected tags?",
        "cancelDelete": "Cancel Delete",
        "moveTag": "Move Tag",
        "targetTag": "Target Tag",
        "movePosition": "Move Position",
        "moveBefore": "Move Before",
        "moveAfter": "Move After",
        "editTag": "Edit Tag",
        "deleteTag": "Delete Tag",
        "editGroupMode": "Edit Group Mode",
        "exitEditMode": "Exit Edit Mode",
        "autoAddSearchTag": "Auto Add Search Tag With Prompt",
    },
    loraManager: {
        windowTitle: "Lora Manager",
        modelWeight: "Model Weight",
        textEncoderWeight: "Text Encoder Weight",
        all: "All",
        refresh: "Refresh",
        cacheAll: "Cache all Lora information",
        searchPlaceholder: "Search Lora...",
        noResults: "No results found",
        prevPage: "prev page",
        nextPage: "next page",
        loadingMore: "Loadding more ...",
        noMoreData: "No more data",
    },
    "message": {
        "copySuccess": "Copy successful",
        "copyFailed": "Copy failed",
        "saveSuccess": "Save successful",
        "saveFailed": "Save failed",
        "deleteSuccess": "Delete successful",
        "deleteFailed": "Delete failed",
        "operationSuccess": "Operation successful",
        "operationFailed": "Operation failed",
        "networkError": "Network error",
        "unknownError": "Unknown error",
        "refreshSuccess": "Refresh successful",
        "refreshFailed": "Refresh failed",
        "loadingData": "Loading data...",
        "dataLoaded": "Data loaded",
        "editSuccess": "Edit successful",
        "editFailed": "Edit failed",
        "addSuccess": "Add successful",
        "addFailed": "Add failed",
        "addFavoriteSuccess": "Added to favorites",
        "addFavoriteIsExist": "Added to favorites",
        "error": "Error",
        "moveSuccess": "Move successful",
        "moveFailed": "Move failed",
        "setLanguageSuccess": "Set language successful",
        "setLanguageFailed": "Set language failed",
        "startPanelSuccess": "Start panel successful",
        "startPanelFailed": "Start panel failed",
        "isLoading": "Loading...",
        "loaddingPrc": "Execution progress {name}%",
        "loaddingSuccess": "All loaded successfully",
        "noFinishKuo": "The parentheses are incomplete. Please check the input",
        "getTranslaterFail": "Get translator failed",
        "applyTranslaterFail": "Apply translator failed",
        "applyToTranslaterFail": "Switching to a translation library requires installing a translation library. Please install the translation library first and then apply the settings",
        "applyTranslaterSuccess": "Apply translator successful",
        tranlaterPackageInstallFail: 'Waiting for installation timeout, please check the background installation status. If the installation is successful, click install again to verify',
        tranlaterPackageInstallSuccess: 'Successfully installed translation package',
        translaterTestFail: "Translation failed, please try using another translation service",
        "installPackageSuccess": "Successfully installed translation package",
        "installPackageFail": "Failed to install translation package, please check the background installation status",
        loadFailed: "load failed",
    },
    cloudWindow:{
        "windowTitle": "Share Cloud Window",
        back: 'Back',
        currentPath: 'Current Path',
        tagDatabase: 'Tag Database',
        danbooruDatabase: 'Danbooru Database',
        open: "Open Folder",
        installed: 'Installed',
        install: 'Install',
         installing: 'Installing...'
    },
    history: {
        "title": "History",
        "search_placeholder": "Search history...",
        "windowTitle": "History",
        "search": "Search",
        "favorites": "Favorites",
        "history": "History",
        "refresh": "Refresh",
        "refresh_history": "Refresh history",
        "refresh_favorites": "Refresh favorites",
        "add_to_favorites": "Add to favorites",
        "delete_history": "Delete history",
        "use_item": "Use",
        "add_new": "Add new",
        "bulk_delete": "Bulk delete",
        "deleteHistoryConfirm": "Are you sure you want to delete history {name}?",
        "deleteFavoriteConfirm": "Are you sure you want to delete favorite {name}?",
        "confirmDeleteSelected": "Are you sure you want to delete selected information?",
        "cancel_delete": "Cancel delete",
        "sure_delete": "Sure delete",
        "deleteSelected": "Delete selected",
        "dialog": {
            "add_tag": "Add favorite",
            "edit_tag": "Edit favorite",
            "name": "Name",
            "name_placeholder": "Please enter name",
            "tag": "Tag",
            "tag_placeholder": "Please enter tag",
            "background_color": "Background color",
            "background_color_placeholder": "Please select background color",
            "edit_favorite": "Edit favorite",
            "delete_favorite": "Delete favorite",
        },
        "edit_favorite": "Edit favorite",
        "delete_favorite": "Delete favorite",
        "use_favorite": "Use favorite"
    },
    floatingBall: {
        "promptBox": "open Global Prompt Box",
        "tagManager": "open Tag Manager",
        "loraManager": "open Lora Manager",
        "aiWindow": "open AI Chat",
        "restoreWindow": "reset all windows",
        "openNodeListWindow": "open Node List",
        tranToWeb: "Image to Web Utils",
    },
    aiWindow: {
        "windowTitle": "AI Chat Window",
        "newChat": "New Chat",
        "chatName": "Chat",
        "thinking": "Thinking...",
        "send": "Send",
        "inputMessage": "Enter your message..."
    },
    translaterService: {
        "niutrans": "niutrans",
        "mymemory": "mymemory",
        "alibaba": "alibaba",
        "baidu": "baidu",
        "modernmt": "modernmt",
        "volcengine": "volcengine",
        "iciba": "iciba",
        "iflytek": "iflytek",
        "google": "google",
        "bing": "bing",
        "lingvanex": "lingvanex",
        "yandex": "yandex",
        "itranslate": "itranslate",
        "systran": "systran",
        "argos": "argos",
        "apertium": "apertium",
        "reverso": "reverso",
        "deepl": "deepl",
        "cloudtranslation": "cloudtranslation",
        "qqtransmart": "qqtransmart",
        "translatecom": "translatecom",
        "sogou": "sogou",
        "tilde": "tilde",
        "caiyun": "caiyun",
        "qqfanyi": "qqfanyi",
        "translateme": "translateme",
        "papago": "papago",
        "mirai": "mirai",
        "youdao": "youdao",
        "iflyrec": "iflyrec",
        "hujiang": "hujiang",
        "yeekit": "yeekit",
        "languagewire": "languagewire",
        "elia": "elia",
        "judic": "judic",
        "mglip": "mglip",
        "utibet": "utibet"
    },
    translaterLanguage:{
        "english": "english",
        "chinese": "chinese",
        "arabic": "arabic",
        "russian": "russian",
        "french": "french",
        "german": "german",
        "spanish": "spanish",
        "portuguese": "portuguese",
        "italian": "italian",
        "japanese": "japanese",
        "korean": "korean",
        "greek": "greek",
        "dutch": "dutch",
        "hindi": "hindi",
        "turkish": "turkish",
        "malay": "malay",
        "thai": "thai",
        "vietnamese": "vietnamese",
        "indonesian": "indonesian",
        "hebrew": "hebrew",
        "polish": "polish",
        "mongolian": "mongolian",
        "czech": "czech",
        "hungarian": "hungarian",
        "estonian": "estonian",
        "bulgarian": "bulgarian",
        "danish": "danish",
        "finnish": "finnish",
        "romanian": "romanian",
        "swedish": "swedish",
        "slovenian": "slovenian",
        "persian/farsi": "persian/farsi",
        "bosnian": "bosnian",
        "serbian": "serbian",
        "fijian": "fijian",
        "filipino": "filipino",
        "haitiancreole": "haitiancreole",
        "catalan": "catalan",
        "croatian": "croatian",
        "latvian": "latvian",
        "lithuanian": "lithuanian",
        "urdu": "urdu",
        "ukrainian": "ukrainian",
        "welsh": "welsh",
        "tahiti": "tahiti",
        "tongan": "tongan",
        "swahili": "swahili",
        "samoan": "samoan",
        "slovak": "slovak",
        "afrikaans": "afrikaans",
        "norwegian": "norwegian",
        "bengali": "bengali",
        "malagasy": "malagasy",
        "maltese": "maltese",
        "queretaro otomi": "queretaro otomi",
        "klingon/tlhingan hol": "klingon/tlhingan hol",
        "gujarati": "gujarati",
        "tamil": "tamil",
        "telugu": "telugu",
        "punjabi": "punjabi",
        "amharic": "amharic",
        "azerbaijani": "azerbaijani",
        "bashkir": "bashkir",
        "belarusian": "belarusian",
        "cebuano": "cebuano",
        "chuvash": "chuvash",
        "esperanto": "esperanto",
        "basque": "basque",
        "irish": "irish"
    },
    utils: {
        tranToWeb: 'Image to HTML',
        dropOrPasteImage: 'Drop or paste image here',
        downloadHtml: 'Download HTML',
        copyHtml: 'Copy HTML',
        copySuccess: 'HTML copied to clipboard',
        copyFailed: 'Failed to copy HTML',
        clear: 'Clear'
    }
} 