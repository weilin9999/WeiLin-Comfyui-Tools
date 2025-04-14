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

app.registerExtension({
  name: "weilin.prompt_ui_node",

  async init() {
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

  },
  async setup() { },

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

            // 创建全局MutationObserver监听元素移除
            const observer = new MutationObserver((mutationsList) => {
              for (const mutation of mutationsList) {
                if (mutation.type === 'childList') {
                  for (const node of mutation.removedNodes) {
                    if (node === thisInputElement || node.contains(thisInputElement)) {
                      // console.log('Element removed!');
                      // 元素被销毁 事件发送更新元素
                      removeNodeBySeed(thisNodeSeed);
                      window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
                      // 停止监听
                      observer.disconnect();
                    }
                  }
                }
              }
            });

            // 使用document作为观察目标
            observer.observe(document, { childList: true, subtree: true });

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
          }
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

            updateNodeTextBySeed(thisNodeSeed, nodeTextAreaList[0].value);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')

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
            }
            if (nodeData.name === "WeiLinPromptUI" || nodeData.name === "WeiLinPromptUIOnlyLoraStack") {
              if (jsonReponse.temp_lora && jsonReponse.temp_lora != "") {
                nodeTextAreaList[3].value = JSON.stringify(jsonReponse.temp_lora);
              }
            }
          }


        }, false);

        return r;
      };
    }
  },
});


//from melmass
// https://github.com/kijai/ComfyUI-KJNodes/blob/main/web/js/spline_editor.js
export function hideWidgetForGood(node, widget, suffix = '') {
  widget.origType = widget.type
  widget.origComputeSize = widget.computeSize
  widget.origSerializeValue = widget.serializeValue
  widget.computeSize = () => [0, -4] // -4 is due to the gap litegraph adds between widgets automatically
  widget.type = "converted-widget" + suffix

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