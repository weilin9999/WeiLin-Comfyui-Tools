import { app } from '../../scripts/app.js'
// 提示词 Node

// localStorage.setItem("weilin_prompt_ui_onfirst", 0);

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0,
      v = c == 'x' ? r : (r & 0x3 | 0x8);
    return v.toString(16);
  });
}

let localLanguage = "打开提示词编辑器"
let localOpenLoraLanguage = "打开Lora堆"

function getBrowserLanguage() {
  // 获取浏览器语言
  const language = navigator.language || navigator.userLanguage;
  // 判断语言类型
  if (language.startsWith('zh')) {
    localLanguage = "打开提示词编辑器"
    localOpenLoraLanguage = "打开Lora堆"
  } else if (language.startsWith('en')) {
    localLanguage = "Open Prompt UI"
    localOpenLoraLanguage = "Open Lora Stack"
  } else {
    localLanguage = "Open Prompt UI"
    localOpenLoraLanguage = "Open Lora Stack"
  }
}

let globalNodeList = []

let global_randomID = generateUUID(); // 随机种子ID

function updateNodeTitleBySeed(seed, newTitle) {
  // 使用 find 方法查找目标节点
  const targetNode = globalNodeList.find(node => node.seed === seed);
  if (targetNode) {
    // 如果找到目标节点，修改其 title
    targetNode.title = newTitle;
  }
}

function updateNodeIdBySeed(seed, newId) {
  const targetNode = globalNodeList.find(node => node.seed === seed);
  if (targetNode) {
    targetNode.id = newId;
  }
}

function updateNodeTextBySeed(seed, newText) {
  const targetNode = globalNodeList.find(node => node.seed === seed);
  if (targetNode) {
    targetNode.text = newText;
  }
}

// 根据seed删除元素
function removeNodeBySeed(seed) {
  const index = globalNodeList.findIndex(node => node.seed === seed);
  if (index !== -1) {
    globalNodeList.splice(index, 1);
  }
}
function initWindow() {
  var script = document.createElement('script');
  // 设置 script 元素的属性
  script.src = './weilin/prompt_ui/webjs'; // 注意确保这里的路径是正确的，并且服务器正在运行。
  script.type = 'text/javascript';
  script.async = true;
  document.head.appendChild(script);

  // 创建一个新的 link 元素
  var link = document.createElement('link');
  // 设置 link 元素的属性
  link.rel = 'stylesheet';
  link.type = 'text/css';
  link.href = './weilin/prompt_ui/file/style.css'; // 确保这里的路径是正确的，并且服务器正在运行。
  document.head.appendChild(link);

  // loraStack 脚本载入
  var script = document.createElement('script');
  // 设置 script 元素的属性
  script.src = './weilin/prompt_ui/file/lora_stack.js'; // 注意确保这里的路径是正确的，并且服务器正在运行。
  script.type = 'text/javascript';
  script.async = true;
  document.head.appendChild(script);
  // 创建一个新的 link 元素
  var link = document.createElement('link');
  // 设置 link 元素的属性
  link.rel = 'stylesheet';
  link.type = 'text/css';
  link.href = './weilin/prompt_ui/file/lora_stack.css'; // 确保这里的路径是正确的，并且服务器正在运行。
  document.head.appendChild(link);
}
initWindow()

app.registerExtension({
  name: "weilin.prompt_ui_node",
  async init() {},
  async setup() {},
  async beforeRegisterNodeDef(nodeType, nodeData, app) {
    // console.log(app)
    if (
      nodeData.name === "WeiLinPromptUI" ||
      nodeData.name === "WeiLinPromptUIWithoutLora" ||
      nodeData.name === "WeiLinPromptUIOnlyLoraStack"
    ) {
      // console.log(nodeData)
      // Create node
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

        const thisNodeName = nodeData.name // 存储当前的节点名称
        let nodeTextAreaList = [] // 按顺序载入element，name="positive" || "lora_str" || "temp_str"
        const thisNodeSeed = generateUUID(); // 随机唯一种子ID

        if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIWithoutLora") {
          hideWidgetForGood(this, this.widgets.find(w => w.name === "temp_str"))
          hideWidgetForGood(this, this.widgets.find(w => w.name === "random_template"))
        }
        if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIOnlyLoraStack") {
          hideWidgetForGood(this, this.widgets.find(w => w.name === "lora_str"))
          hideWidgetForGood(this, this.widgets.find(w => w.name === "temp_lora_str"))
        }

        for (let index = 0; index < this.widgets.length; index++) {
          const widgetItem = this.widgets[index];
          if (widgetItem.name == "positive") {
            let thisInputElement = widgetItem.element
            // thisInputElement.readOnly = true
            nodeTextAreaList[0] = thisInputElement
          } else if (widgetItem.name == "lora_str") {
            let thisInputElement = widgetItem.element
            thisInputElement.readOnly = true
            nodeTextAreaList[1] = thisInputElement
          } else if (widgetItem.name == "temp_str") {
            let thisInputElement = widgetItem.element
            thisInputElement.readOnly = true
            nodeTextAreaList[2] = thisInputElement
          } else if (widgetItem.name == "temp_lora_str") {
            let thisInputElement = widgetItem.element
            thisInputElement.readOnly = true
            nodeTextAreaList[3] = thisInputElement
          } else if (widgetItem.name == "random_template") {
            let thisInputElement = widgetItem.element
            thisInputElement.readOnly = true
            nodeTextAreaList[4] = thisInputElement
          }
        }

        // Lora Stack 创建可视化节点
        if (nodeData.name === "WeiLinPromptUIOnlyLoraStack") {
          await createLoraStackWidget(this, thisNodeSeed,nodeTextAreaList[3]);
        }

        // console.log(this)

        if (nodeData.name === "WeiLinPromptUI" ||
          nodeData.name === "WeiLinPromptUIWithoutLora") {
          globalNodeList.push({ seed: thisNodeSeed, text: nodeTextAreaList[0].value, id: this.id })

          const textarea = nodeTextAreaList[0];

          textarea.addEventListener('input', (event) => {
            const newValue = event.target.value;
            updateNodeTextBySeed(newValue);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
          });
        }

        // 监听节点ID
        let currentThisId = this.id
        Object.defineProperty(this, 'id', {
          get() {
            return currentThisId;
          },
          set(newValue) {
            currentThisId = newValue;
            onTisIdChange(newValue);
          },
          enumerable: true,
          configurable: true
        });

        function onTisIdChange(newId) {
          // console.log(newId)
          if (nodeData.name === "WeiLinPromptUI" ||
            nodeData.name === "WeiLinPromptUIWithoutLora") {
            updateNodeIdBySeed(thisNodeSeed, newId);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
          }
        }

        // 监听 this.title 的变化
        let currentTitle = this.title; // 缓存当前值
        Object.defineProperty(this, 'title', {
          get() {
            return currentTitle;
          },
          set(newValue) {
            // console.log(`this.title changed from ${currentTitle} to ${newValue}`);
            currentTitle = newValue;
            // 触发回调，返回新的 this.title 数据
            onTitleChange(newValue);
          },
          enumerable: true,
          configurable: true
        });

        // 监听 this.title 变化的回调函数
        function onTitleChange(newTitle) {
          // console.log("New this.title:", newTitle);
          // 在这里可以处理新的 this.title 数据
          // 例如，将新的 this.title 传递给其他逻辑
          if (nodeData.name === "WeiLinPromptUI" ||
            nodeData.name === "WeiLinPromptUIWithoutLora") {
            updateNodeTitleBySeed(thisNodeSeed, newTitle);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
          }
        }

        // 保存原有的onRemoved函数
        const originalOnRemoved = this.onRemoved;
        // 节点被删除事件
        this.onRemoved = () => {
          // 调用原有的onRemoved函数
          if (originalOnRemoved) {
            originalOnRemoved.apply(this);
          }
          
          // 元素被销毁 事件发送更新元素
          if (nodeData.name === "WeiLinPromptUI" ||
            nodeData.name === "WeiLinPromptUIWithoutLora") {
            removeNodeBySeed(thisNodeSeed);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
          }
        }

        // console.log(thisNodeSeed)

        //console.log(globalNodeList)

        let randomID = ""

        randomID = generateUUID();

        if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIWithoutLora") {
          // 节点按钮点击事件
          this.addWidget("button", localLanguage, '', ($e) => {
            // console.log(thisNodeName)
            // 发送消息给父窗口
            // console.log(global_randomID)
            randomID = generateUUID();
            // console.log("register====>",randomID)
            let jsonData = {
              prompt: nodeTextAreaList[0].value,
              lora: [],
              temp_prompt: {},
              temp_lora: {},
            }
            if (nodeData.name === "WeiLinPromptUI" && nodeTextAreaList[1].value.length > 0) {
              jsonData.lora = JSON.parse(nodeTextAreaList[1].value);
            }

            if (nodeTextAreaList[2].value.length > 0) {
              jsonData.temp_prompt = JSON.parse(nodeTextAreaList[2].value)
            }

            if (nodeData.name === "WeiLinPromptUI" && nodeTextAreaList[3].value.length > 0) {
              jsonData.temp_lora = JSON.parse(nodeTextAreaList[3].value)
            }

            const data = JSON.stringify(jsonData)
            window.parent.postMessage({ type: 'weilin_prompt_ui_openPromptBox', id: randomID, prompt: data, node: nodeData.name }, '*')
          });
        }

        if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIOnlyLoraStack") {
          // 节点按钮点击事件
          this.addWidget("button", localOpenLoraLanguage, '', ($e) => {
            // console.log(thisNodeName)
            // 发送消息给父窗口
            // console.log(global_randomID)
            randomID = generateUUID();
            // console.log("register====>",randomID)
            let jsonData = {
              lora: [],
              temp_lora: {},
            }
            if (nodeTextAreaList[1].value.length > 0) {
              jsonData.lora = JSON.parse(nodeTextAreaList[1].value);
            }

            if (nodeTextAreaList[3].value.length > 0) {
              jsonData.temp_lora = JSON.parse(nodeTextAreaList[3].value)
            }

            const data = JSON.stringify(jsonData)
            window.parent.postMessage({ type: 'weilin_prompt_ui_open_node_lora_stack_window', seed: randomID, prompt: data, node: nodeData.name }, '*')
          });
        }


        window.addEventListener('message', event => {
          // console.log(e)
          if (event.data.type === 'weilin_prompt_ui_prompt_update_prompt_' + randomID) {
            // 接收到更新提示词内容消息

            const jsonReponse = JSON.parse(event.data.data)
            // console.log(jsonReponse)
            nodeTextAreaList[0].value = jsonReponse.prompt;

            if (nodeData.name === "WeiLinPromptUI") {
              // console.log(jsonReponse.lora.length)
              if (jsonReponse.lora && jsonReponse.lora.length > 0 && jsonReponse.lora != "") {
                nodeTextAreaList[1].value = JSON.stringify(jsonReponse.lora);
              } else {
                nodeTextAreaList[1].value = "";
              }
            }

            if (jsonReponse.temp_prompt && jsonReponse.temp_prompt != "") {
              nodeTextAreaList[2].value = JSON.stringify(jsonReponse.temp_prompt);
            }

            if (nodeData.name === "WeiLinPromptUI") {
              if (jsonReponse.temp_lora && jsonReponse.temp_lora != "") {
                nodeTextAreaList[3].value = JSON.stringify(jsonReponse.temp_lora);
              }
            }


            // console.log(nodeTextAreaList)
            updateNodeTextBySeed(thisNodeSeed, jsonReponse.prompt);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')

          } else if (event.data.type === 'weilin_prompt_ui_prompt_get_node_list_info') {
            // 获取节点导航信息
            if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIWithoutLora") {
              updateNodeTextBySeed(thisNodeSeed, nodeTextAreaList[0].value);
              window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
            }

          } else if (event.data.type === "weilin_prompt_ui_prompt_open_node_wit_seed" && event.data.seed === thisNodeSeed) {
            // 节点导航打开节点UI按钮

            randomID = generateUUID();
            // console.log("register====>",randomID)
            let jsonData = {
              prompt: nodeTextAreaList[0].value,
              lora: [],
              temp_prompt: {},
              temp_lora: {},
            }
            if (nodeData.name === "WeiLinPromptUI" && nodeTextAreaList[1].value.length > 0) {
              jsonData.lora = JSON.parse(nodeTextAreaList[1].value);
            }
            if (nodeTextAreaList[2].value.length > 0) {
              jsonData.temp_prompt = JSON.parse(nodeTextAreaList[2].value)
            }
            if (nodeData.name === "WeiLinPromptUI" && nodeTextAreaList[3].value.length > 0) {
              jsonData.temp_lora = JSON.parse(nodeTextAreaList[3].value)
            }

            const data = JSON.stringify(jsonData)
            window.parent.postMessage({ type: 'weilin_prompt_ui_openPromptBox', id: randomID, prompt: data, node: nodeData.name }, '*')
          
          } else if (event.data.type === 'weilin_prompt_ui_prompt_finish_lora_stack_' + randomID) {
            // 接收到更新LoraStack内容消息
            const jsonReponse = JSON.parse(event.data.data)
            // console.log(jsonReponse)
            if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIOnlyLoraStack") {
              // console.log(jsonReponse.lora.length)
              if (jsonReponse.lora && jsonReponse.lora.length > 0 && jsonReponse.lora != "") {
                nodeTextAreaList[1].value = JSON.stringify(jsonReponse.lora);
              } else {
                nodeTextAreaList[1].value = "";
              }

              if (jsonReponse.temp_lora && jsonReponse.temp_lora != "") {
                nodeTextAreaList[3].value = JSON.stringify(jsonReponse.temp_lora);
              }else{
                nodeTextAreaList[3].value = "";
              }

              if (nodeTextAreaList[3].value.length > 0) {
                window.weilinGlobalSelectedLoras[thisNodeSeed] = JSON.parse(nodeTextAreaList[3].value)
              }else {
                window.weilinGlobalSelectedLoras[thisNodeSeed]= []
              }
              renderAllLoras(thisNodeSeed)
            }
          
          }else if (event.data.type === "weilin_prompt_ui_prompt_node_finish_lora_stack_" + thisNodeSeed) {
            // 接收到更新LoraStack内容消息
            const jsonReponse = JSON.parse(event.data.data)
            if (nodeData.name === "WeiLinPromptUIOnlyLoraStack") {
              if (jsonReponse.lora && jsonReponse.lora.length > 0 && jsonReponse.lora != "") {
                nodeTextAreaList[1].value = JSON.stringify(jsonReponse.lora);
              } else {
                nodeTextAreaList[1].value = "";
              }
              if (jsonReponse.temp_lora && jsonReponse.temp_lora != "") {
                nodeTextAreaList[3].value = JSON.stringify(jsonReponse.temp_lora);
              }else{
                nodeTextAreaList[3].value = "";
              }
            }
          }else if (event.data.type === "weilin_prompt_ui_selectLora_stack_node_"+thisNodeSeed) {
            addLora(thisNodeSeed,event.data.lora)
          }else if (event.data.type === "weilin_prompt_ui_update_template_"+randomID) {
            nodeTextAreaList[4].value = event.data.data
          }else if (event.data.type === "weilin_prompt_ui_get_template_"+randomID) {
            window.parent.postMessage({ type: 'weilin_prompt_ui_get_template_response', id: randomID, data: nodeTextAreaList[4].value }, '*')
          }else if (event.data.type === "weilin_prompt_ui_get_template_go_random_"+randomID) {
            window.parent.postMessage({ type: 'weilin_prompt_ui_get_template_go_random_response', id: randomID, data: nodeTextAreaList[4].value }, '*')
          }

        }, false);

        return r;
      };

      // When the node is executed we will be sent the input text, display this in the widget
			const onExecuted = nodeType.prototype.onExecuted;
			nodeType.prototype.onExecuted = function (message) {
				onExecuted?.apply(this, arguments);
        const positiveWidget = this.widgets.find(w => w.name === "positive");
        if (positiveWidget && message.positive) {
          positiveWidget.element.value = message.positive;
          // 触发input事件以更新全局状态
          const event = new Event('input', { bubbles: true });
          positiveWidget.element.dispatchEvent(event);
        }
        // console.log(message.positive)
			};
    }
  },
});


//from melmass
// https://github.com/kijai/ComfyUI-KJNodes/blob/main/web/js/spline_editor.js
function hideWidgetForGood(node, widget, suffix = '') {
  widget.origType = widget.type
  widget.origComputeSize = widget.computeSize
  widget.origSerializeValue = widget.serializeValue
  widget.computeSize = () => [0, -4] // -4 is due to the gap litegraph adds between widgets automatically
  widget.type = "converted-widget" + suffix

  widget.element.style.display = 'none'
  // widget.serializeValue = () => {
  //     // Prevent serializing the widget if we have no input linked
  //     const w = node.inputs?.find((i) => i.widget?.name === widget.name);
  //     if (w?.link == null) {
  //         return undefined;
  //     }
  //     return widget.origSerializeValue ? widget.origSerializeValue() : widget.value;
  // };

  // Hide any linked widgets, e.g. seed+seedControl
  if (widget.linkedWidgets) {
    for (const w of widget.linkedWidgets) {
      hideWidgetForGood(node, w, ':' + widget.name)
    }
  }
}

function createLoraStackWidget(node, seed, ptEl) {
  var element = document.createElement("div");
  const previewNode = node;
  const prSeed = seed;
  const prTempLoraEl = ptEl;


  var previewWidget = node.addDOMWidget("weilin_lora_stack", "lora_stack", element, {
    serialize: false,
    hideOnZoom: false,
    getValue() {
      return element.value;
    },
    setValue(v) {
      element.value = v;
    },
  });

  previewNode.onResize = function () {
    let [w, h] = previewNode.size;
    if (h < 300) h = 300;
    previewNode.size = [w, h];
  };


  previewWidget.value = { hidden: false, paused: false, params: {} }
  previewWidget.parentEl = document.createElement("div");
  previewWidget.parentEl.className = "lora-stack";
  element.appendChild(previewWidget.parentEl);

  const lang = navigator.language || navigator.userLanguage;
  const localLang = lang.startsWith('zh') ? 'zh' : 'en';
  previewWidget.contentEl = document.createElement("div");
  previewWidget.contentEl.innerHTML = `
    <div class="lora-header">
        <div class="header-actions">
            <button class="add-btn" onclick="openLoraManager(this)" id="addLoraBtn" data-seed="`+prSeed+`" title="${localLang === 'zh' ? '添加Lora' : 'Add Lora' }">
                <svg viewBox="0 0 24 24" width="16" height="16">
                    <path d="M19 13h-6v6h-2v-6H5v-2h6V5h2v6h6v2z" />
                </svg>
            </button>
        </div>
    </div>
    <div class="lora-body">
        <div class="lora-list" id="loraListContainer_`+prSeed+`">
            <!-- Lora items will be added here dynamically -->
        </div>
    </div>
  `
  previewWidget.contentEl.className = "lora-content"
  previewWidget.parentEl.appendChild(previewWidget.contentEl)

  setTimeout(() => {
    if (prTempLoraEl.value.length > 0) {
      window.weilinGlobalSelectedLoras[seed] = JSON.parse(prTempLoraEl.value)
    }else {
      window.weilinGlobalSelectedLoras[seed]= []
    }
    renderAllLoras(seed)
    // console.log(window.weilinGlobalSelectedLoras)
  },300)

  // console.log(node)
}
