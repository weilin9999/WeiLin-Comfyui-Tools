<div align="center">
  
### [🇨🇳 简体中文](README.md) | [🇺🇸 English](README_EN.md)

</div>

# Special Attention!

Official QQ group: `1018231382`

# Notice!

This plugin is still in beta testing, please do not try it boldly! If you want to use it, please join the official QQ group for details!

## Companion Usage Instructions - Migrating Old Plugin Prompt Words to the New Plugin
The plugin has a dedicated independent backend panel that can convert your old version prompt words to those of the new version plugin and allows for portable offline modification of Tags. Project entry: [WeiLin-Comfyui-Tools-panel](https://github.com/weilin9999/WeiLin-Comfyui-Tools-panel)

# Author Statement

Due to limited personal time, the frequency of updating plug-ins will not be very high, occasionally free may update once, each update as far as possible to meet the proposed needs, generally no big BUG basically update frequency is not high, 2~5 a month, thank you for your use and support of this plug-in. You can submit an Issue or you can submit your Request to help update this plugin.

# Version update introduction

> Last updated: 2025-03-03

> 0.0.18 Public Beta Version Introduction: If you want to use this plugin, please be sure to join our official QQ group (1018231382)! 
>
>1. Add a new node list (opened in the floating ball), which can quickly open all the nodes of this node without the need to enlarge the nodes to find them

<details>
<summary>Click here for more updates from the past</summary>

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