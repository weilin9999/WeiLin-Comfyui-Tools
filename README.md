<div align="center">
  
### [🇨🇳 简体中文](README.md) | [🇺🇸 English](README_EN.md)

</div>

# 特别关注！

官方 QQ 群：`1018231382`

# 注意！

本插件还是在内测中，请不要大胆尝鲜！如果要使用请进官方 QQ 群了解详情！

## 配套使用说明 - 旧插件提示词迁移到新插件
插件有专门的独立后台面板，可以把你的旧版的提示词转换成新版本插件的提示词以及便携式的离线修改Tag，项目入口 [WeiLin-Comfyui-Tools-panel
](https://github.com/weilin9999/WeiLin-Comfyui-Tools-panel)

# 作者声明

由于个人时间有限，更新插件的频率并不会很高，偶尔有空或许会更新一次，每次更新尽量满足所提出的需求，一般没有大的 BUG 基本上更新频率不高，一个月 2~5 更，感谢你对本插件的使用与支持，有需求可以提交 Issue 或者你可以提交你的 Request 帮助本插件更新。

# 版本更新介绍

> 最新更新：2025-02-22

> 0.0.17 公测版本介绍 如果你要使用本插件请务必进我们的官方 QQ 群（1018231382）！
>
> 1.修复权重添加会删除其它括号类型的BUG


<details>
<summary>点击查看往期更多更新内容</summary>

> 0.0.16 2025-02-14 公测版本介绍
>
> 1.节点修改，新增了clip节点输出
>
> 2.节点修改，新增了string内容输入合并
>
> 3.修复了已知BUG
>
> 4.修改了Tag的控制栏的括号加减问题


> 0.0.15 公测版本介绍
>
> 1.节点修改，新增了clip节点输出
>
> 2.节点修改，新增了string内容输入合并


> 0.0.13 公测版本介绍
>
> 1.修复了已知 BUG
>
> 2.新增功能-Lora 支持一键缓存所有 Lora 文件
>
> 3.新增功能-支持加载 Lora 的时候同时加载对应的 Lora 提示词（需要给 Lora 设置提示词才可生效！）

> 0.0.12 公测版本介绍
>
> 1.修复了已知 BUG

> 0.0.0.3 内测版本介绍
>
> 1.更新了 AI 对话功能
>
> 2.更新了 Danbooru 词库到 2024-11-30
>
> 3.将所有 tag 和词库都写入到数据库中，我们不再使用 json 文件来存储我们的 tag 和词库，因为数据太多检索起来太慢了
>
> 4.优化了性能

> 0.0.0.1 版本介绍 （由于本人工作原因空闲时间才有时间更新插件，见谅！在此非常感谢大家对本插件的支持！）
>
> 1. 上传插件 0.0.0.1 版本

</details>

# 概要说明

本项目可以让你在 ComfyUI 中快捷的使用提示词工具
如果你对本项目有兴趣赏一个 Star 吧！

# 如何参与开发？

#### 项目主要结构
```
WeiLin-Comfyui-Tools 
├── README.md - 中文文档
├── README_EN.md - 英文文档
├── __init__.py - 插件主入口
├── app - 插件的业务代码（API、数据库操作等）
│   ├── __init__.py
│   └── server - 服务入口
│       ├── __pycache__
│       ├── ai_translator - AI设置业务层
│       ├── dao - 数据层操作
│       ├── fast_autocomplete - 补全功能业务层
│       ├── history - 历史记录业务层
│       ├── prompt_api - 提示词业务层
│       ├── prompt_server.py - API暴露入口
│       ├── translate - 本地/离线翻译Tag业务层
│       └── user_init - 用户设置初始化业务层
├── dist - 前端编译后的文件
├── init.json - AI服务的Key保存文件
├── install_request.py - 自动安装功能
├── js_node - comfyui的JS业务代码
├── lora_userdatas - 用户Lora的本地数据
├── pyproject.toml - comfyui的仓库文件
├── requirements.txt - 安装三方库检测文件
├── src - 前端源码
├── tags_templete 用户数据库文件模板 （Tag和Danbooru，如果需要修改请前往插件配套的后台面板使用）
└── user_data 用户使用的数据库文件（不需要修改）
```

#### 前端源码说明
前端框架是Vue3+Javascript，yarn管理依赖包，使用时请先执行`yarn install`安装依赖包，编译请使用`yarn run build`，会自动打包到插件的`dist`目录中

#### 提交代码
请克隆完整的仓库代码，提交代码时请测试一遍随后提交代码，等待我的审核确认后即可合并代码