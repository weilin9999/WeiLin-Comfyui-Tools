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

let global_randomID = generateUUID(); // 随机种子ID

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
        let nodeTextAreaList = []
        for (let index = 0; index < this.widgets.length; index++) {
          const element = this.widgets[index];
          let thisInputElement = element.element
          // thisInputElement.readOnly = true
          nodeTextAreaList[0] = thisInputElement
        }

        let randomID = ""
        this.addWidget("button", "打开可视化PromptUI", '', ($e) => {
          // console.log(thisNodeName)
          // 发送消息给父窗口
          // console.log(global_randomID)
          randomID = generateUUID();
          // console.log("register====>",randomID)
          window.parent.postMessage({ type: 'weilin_prompt_ui_openPromptBox', id: randomID, prompt: nodeTextAreaList[0].value }, '*')
        });

        window.addEventListener('message', event => {
          // console.log(e)
          if (event.data.type === 'weilin_prompt_ui_prompt_update_prompt_' + randomID) {
            nodeTextAreaList[0].value = event.data.data
            // console.log(nodeTextAreaList)
          }
        }, false);

        return r;
      };
    }
  },
});