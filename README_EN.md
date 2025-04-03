<div align="center">
  
### [🇨🇳 简体中文](README.md) | [🇺🇸 English](README_EN.md)

</div>

# Special Attention!

Official QQ group: `1018231382`

# Notice!

This plugin is still in beta testing, please do not try it boldly! If you want to use it, please join the official QQ group for details!

## Companion Usage Instructions - Migrating Old Plugin Prompt Words to the New Plugin
The plugin has a dedicated independent backend panel that can convert your old version prompt words to those of the new version plugin and allows for portable offline modification of Tags. Project entry: [WeiLin-Comfyui-Tools-panel](https://github.com/weilin9999/WeiLin-Comfyui-Tools-panel)

## plugin for cloud Tag and Danbooru database repository
Warehouse location: [WeiLin-Comfyui-Tools-Prompt](https://github.com/weilin9999/WeiLin-Comfyui-Tools-Prompt), if you are interested can look at the work together

# Author Statement

Due to limited personal time, the frequency of updating plug-ins will not be very high, occasionally free may update once, each update as far as possible to meet the proposed needs, generally no big BUG basically update frequency is not high, 2~5 a month, thank you for your use and support of this plug-in. You can submit an Issue or you can submit your Request to help update this plugin.

# Version update introduction

> Last updated: 2025-04-03

> 0.0.32 Public Beta Version Introduction: If you want to use this plugin, please be sure to join our official QQ group (1018231382)! 
>
> 1. **Fix the issue again - the issue has been resolved** Fix old data migration will not move in its own added data, You can go to the directory ```user_data_old``` and change the name of the data file to ```userdatas_zh_CN.db``` and then go back to the folder ```user_data``` and delete all the files in the folder. Then paste the change name ```userdatas_zh_CN.db``` into this folder and start Comfyui to migrate the data again!
>

<details>
<summary>Click here for more updates from the past</summary>

> 0.0.31 Public Beta Version  2025-04-02
> 1. Add newline display, and Tag display will follow newline after newline
>
> 2. Fix the problem that the old data migration will not move the data you add into it. You can go to the directory ```user_data_old``` and change the name of the data file to ```userdatas_zh_CN.db``` and then return to the folder ```user_data``` and delete all the files in the folder. Then paste the change name ```userdatas_zh_CN.db``` into this folder and start Comfyui to migrate the data again!
>

> 0.0.30 Public Beta Version 2025-04-01
>
> 1. Fix the Tag moving issue when editing
>
> 2. Added Cloud warehouse! You can use the cloud warehouse to dynamically get prompt words or update Danbooru, open in the UI "Share Cloud data"!
>
> 3. Optimize performance issues
>
> 4. Fixed some known bugs

> 0.0.28 Public Beta Version 2025-03-31
>
> 1. Modified the new database pull method has been disclosed to the warehouse: [WeiLin-Comfyui-Tools-Prompt](https://github.com/weilin9999/WeiLin-Comfyui-Tools-Prompt), interested partners can check how to add your own tag or danbooru
>
> 2. Optimized the automatic completion function

> 0.0.27 Public Beta Version 2025-03-30
>
> 1. The search Tag is highlighted, and you can choose to automatically add the search Tag to the prompt words
>
> 2. Modify the prompt words in Lora detail page to add the function of hiding and expanding
>
> 3. Modify the Tag editing operation nowhere method and add an edit mode selection

> 0.0.26 Public Beta Version 2025-03-27
>
> 1. Modified the default prompt words to automatically add commas
>
> 2. Modify the test translation error prompt to avoid misleading
>
> 3. Hide the Lora box to make the node cleaner

> 0.0.24 2025-03-25 Public Beta Version
>
> 1. The translation library function has been added in the UI settings. You can replace the third-party translation with the translation library function. To use it, simply install the translation library by clicking "Install". It is convenient to use and has a complete translation function. -- v0.0.23 2025-03-24 
>
> 2. New Node: Lora is not loaded. The absence of the Lora information box for this node can reduce the node size -- v0.0.23 2025-03-24 
>
> 3. Fixed the issue where history records were not being saved and the problem of the names of favorites not being displayed -- v0.0.23 2025-03-24 
>
> 4. Fixed the issue where the last item in the Lora stack was not being deleted -- v0.0.23 2025-03-24 
>
> 5. Optimized the issue of translation timeout or local data acquisition timeout caused by too many tags -- v0.0.23 2025-03-24 
>
> 6. Fixed the issue where the floating ball would jump -- v0.0.23 2025-03-24 
>
> 7. Adjustment: The minimum size of the floating ball is set to 6, the upper limit of the size is 999999, and the maximum number of floating balls is adjusted to 100 -- v0.0.23 2025-03-24 
>
> 8. Fixed the issue where the plugin was not functioning properly in Comfyui version v0.3.27 -- v0.0.24 2025-03-25

> 0.0.20 2025-03-18 Public Beta Version
>
>1. Fix bug.

> 0.0.19 2025-03-17 Public Beta Version
>
>1. Split the prompt words of the node and the text of Lora to make it more intuitive.
>
>2. Added the function of searching for Lora, enabling users to find the Lora they want more quickly.

> 0.0.18 Public Beta Version 2025-03-03
>
>1. Add a new node list (opened in the floating ball), which can quickly open all the nodes of this node without the need to enlarge the nodes to find them

> 0.0.17 Public Beta Version 2025-02-22
>
> 1.Fix the bug where adding weights would delete other types of parentheses.

> 0.0.16 2025-02-14 Public beta version introduction If you want to use this plugin, please be sure to join our official QQ group (1018231382)!
>
>1. Node modification, adding clip node output
>
>2. Node modification, added string content input merging
>
>3. Fixed known bugs
>
>4. Modified the addition and subtraction of parentheses in the control bar of Tag


> 0.0.13 Public beta version introduction If you want to use this plug-in please be sure to enter our official QQ group (1018231382)!
>
> 1. Fixed known bugs
>
> 2. New Features -Lora supports one-click caching of all Lora files
>
> 3. New feature - Support to load the corresponding Lora prompt words at the same time when loading Lora (need to set the prompt words for Lora to take effect!)

> 0.0.12 Public beta version introduction
>
> 1. Fixed known bugs

> 0.0.0.3 Beta Version Introduction
>
> 1. Updated AI dialogue function
>
> 2. Updated Danbooru word library to 2024-11-30
>
> 3. All tags and word libraries are written into the database, we no longer use json files to store our tags and word libraries, because there is too much data to retrieve too slowly
>
> 4. Performance optimization

> 0.0.0.1 Version Introduction (Due to my work, I have time to update the plug-in, forgive me! Thank you very much for your support of this plugin!)
>
> 1. Upload Version 0.0.0.1

</details>

# Summary

This project allows you to quickly use the prompt word tool in ComfyUI. If you are interested in this project, please award a Star!

# How to Participate in Development? 

#### Main Project Structure 

```
WeiLin-Comfyui-Tools
├── README.md - Chinese documentation
├── README_EN.md - English documentation
├── __init__.py - Main entry point of the plugin
├── app - Business code of the plugin (API, database operations, etc.) │   ├── __init__.py
│   └── server - Service entry point │       ├── __pycache__
│       ├── ai_translator - AI settings business layer
│       ├── dao - data layer operations
│       ├── fast_autocomplete - autocomplete function business layer
│       ├── history - history record business layer
│       ├── prompt_api - prompt word business layer
│       ├── prompt_server.py - API exposure entry
│       ├── translate - local/offline translation Tag business layer
│       └── user_init - user settings initialization business layer
├── dist - compiled front-end files
├── init.json - file for saving AI service keys
├── install_request.py - automatic installation function
├── js_node - JS business code for comfyui
├── lora_userdatas - local data for user Lora
├── pyproject.toml - repository file for comfyui
├── requirements.txt - file for checking third-party library installation
├── src - front-end source code
├── tags_templete - template for user database files (Tags and Danbooru, if modification is needed, please use the background panel provided with the plugin)
└── user_data - database files used by users (no modification required) 
```


#### Front-end Source Code Instructions
The front-end framework is Vue3 + Javascript, and yarn is used to manage dependencies. When using it, please first execute `yarn install` to install the dependencies. To compile, use `yarn run build`, which will automatically package it into the `dist` directory of the plugin. 

#### Submit Code
Please clone the complete repository code. Before submitting the code, please test it once and then submit it. After my review and confirmation, the code can be merged.