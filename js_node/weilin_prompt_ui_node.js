import { app } from '../../scripts/app.js'

// 提示词 Node

// localStorage.setItem("weilin_prompt_ui_onfirst", 0);

function generateUUID() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
      var r = Math.random() * 16 | 0,
          v = c == 'x' ? r : (r & 0x3 | 0x8);
      return v.toString(16);
  });
}

let localLanguage = "打开提示词编辑器"

function getBrowserLanguage() {
  // 获取浏览器语言
  const language = navigator.language || navigator.userLanguage;
  // 判断语言类型
  if (language.startsWith('zh')) {
    localLanguage = "打开提示词编辑器"
  } else if (language.startsWith('en')) {
    localLanguage = "Open Prompt UI"
  } else {
    localLanguage = "Open Prompt UI"
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
      nodeData.name === "WeiLinPromptUI"
    ) {
      // console.log(nodeData)
      // Create node
      const onNodeCreated = nodeType.prototype.onNodeCreated;
      nodeType.prototype.onNodeCreated = async function () {
        const r = onNodeCreated ? onNodeCreated.apply(this, arguments) : undefined;

        const thisNodeName = nodeData.name // 存储当前的节点名称
        let nodeTextAreaList = [] // 按顺序载入element，name="positive" || "lora_str"
        const thisNodeSeed = generateUUID(); // 随机唯一种子ID

        for (let index = 0; index < this.widgets.length; index++) {
          const widgetItem = this.widgets[index];
          if (widgetItem.name == "positive"){
            let thisInputElement = widgetItem.element
            // thisInputElement.readOnly = true
            nodeTextAreaList[0] = thisInputElement
          }else if (widgetItem.name == "lora_str"){
            let thisInputElement = widgetItem.element
            // thisInputElement.readOnly = true
            nodeTextAreaList[1] = thisInputElement
          }
        }
        // console.log(this)

        globalNodeList.push({ seed: thisNodeSeed, text: nodeTextAreaList[0].value,id: this.id })

        const textarea = nodeTextAreaList[0];

        textarea.addEventListener('input', (event) => {
          const newValue = event.target.value;
          updateNodeTextBySeed(newValue);
          window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
        });


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
          updateNodeIdBySeed(thisNodeSeed, newId);
          window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
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
          updateNodeTitleBySeed(thisNodeSeed, newTitle);
          window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
        }

        // console.log(thisNodeSeed)

        //console.log(globalNodeList)

        let randomID = ""
        
        randomID = generateUUID();

        this.addWidget("button", localLanguage, '', ($e) => {
          // console.log(thisNodeName)
          // 发送消息给父窗口
          // console.log(global_randomID)
          randomID = generateUUID();
          // console.log("register====>",randomID)
          let jsonData = {
            prompt: nodeTextAreaList[0].value,
            lora: [],
          }
          if (nodeTextAreaList[1].value.length > 0){
            jsonData.lora = JSON.parse(nodeTextAreaList[1].value);
          }
          const data = JSON.stringify(jsonData)
          window.parent.postMessage({ type: 'weilin_prompt_ui_openPromptBox', id: randomID, prompt: data }, '*')
        });

        window.addEventListener('message', event => {
          // console.log(e)
          if (event.data.type === 'weilin_prompt_ui_prompt_update_prompt_' + randomID) {
            const jsonReponse = JSON.parse(event.data.data)
            nodeTextAreaList[0].value = jsonReponse.prompt;
            nodeTextAreaList[1].value = JSON.stringify(jsonReponse.lora);
            // console.log(nodeTextAreaList)
            updateNodeTextBySeed(thisNodeSeed, event.data.data);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
          }else if (event.data.type === 'weilin_prompt_ui_prompt_get_node_list_info') {
            updateNodeTextBySeed(thisNodeSeed, nodeTextAreaList[0].value);
            window.parent.postMessage({ type: 'weilin_prompt_ui_update_node_list_info', nodeList: globalNodeList }, '*')
          }else if( event.data.type === "weilin_prompt_ui_prompt_open_node_wit_seed" && event.data.seed === thisNodeSeed){
            randomID = generateUUID();
            // console.log("register====>",randomID)
            let jsonData = {
              prompt: nodeTextAreaList[0].value,
              lora: [],
            }
            if (nodeTextAreaList[1].value.length > 0){
              jsonData.lora = JSON.parse(nodeTextAreaList[1].value);
            }
            const data = JSON.stringify(jsonData)
            window.parent.postMessage({ type: 'weilin_prompt_ui_openPromptBox', id: randomID, prompt: data }, '*')
          }
        }, false);

        return r;
      };
    }
  },
});