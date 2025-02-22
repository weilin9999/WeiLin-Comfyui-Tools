//      引入创建虚拟节点和渲染方法
import { createVNode, render } from "vue";
import tip from "./message.vue";
import i18n from '@/i18n'

//      定义一个div容器
const div = document.createElement("div");
//      将定义的容器添加到dom上
document.body.appendChild(div);
//      定义定时器：一定时间后清除
let timer = null;

const message = ({ str, type, name = "" }) => {
  //      调用创建虚拟节点方法
  //      第一个参数为要创建的虚拟节点即编写好的vue组件
  //      第二个参数为props的参数

  let translatedMessage =  i18n.global.t(str)
  if (name.length > 0) {
    translatedMessage =  i18n.global.t(str, { name })
  }
  const vnode = createVNode(tip, { str: translatedMessage, type });
  //      调用渲染方法：将虚拟节点渲染到dom中
  render(vnode, div);
  //      开启定时器，若原先存在则先进行清除
  timer&&clearTimeout(timer);
  timer = setTimeout(() => {
    render(null, div);
  }, 2000);
};

export default message