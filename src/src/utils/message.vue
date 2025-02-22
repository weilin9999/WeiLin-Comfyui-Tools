<template>
  <div class="pop-message" :style="style[type]" v-show="visible">
      <i class="icon" :class="[style[type].icon]"></i>
      <span class="text">{{ str }}</span>
  </div>
</template>

<script>
import { onMounted, ref } from "vue";
export default {
  name: "popmessage",
  //    这个是传值方法，通过父级组件传入提示状态以及提示文本
  //    可以根据不同业务自定义更多的状态
  props: {
      type: {
          type: String,
          //    success 成功
          //    warn 警告
          //    error 错误
          default: "success",
      },
      str: {
          type: String,
          default: "登陆成功",
      },
  },
  setup() {
      //    定义一个对象，包含三种情况的样式，对象key就是类型字符串
      //    icon图标这一部分省略了，有需要的可以自己加入
      const style = {
          warn: {
              // icon: "icon-warning",
              color: "#E6A23C",
              backgroundColor: "rgb(253, 246, 236)",
              borderColor: "rgb(250, 236, 216)",
          },
          error: {
              // icon: "icon-shanchu",
              color: "#F56C6C",
              backgroundColor: "rgb(254, 240, 240)",
              borderColor: "rgb(253, 226, 226)",
          },
          success: {
              // icon: "icon-queren2",
              color: "#67C23A",
              backgroundColor: "rgb(240, 249, 235)",
              borderColor: "rgb(225, 243, 216)",
          },
      };

      const visible = ref(false);

      onMounted(() => {
          visible.value = true;
      });

      return { style, visible };
  },
};
</script>

<style scoped>
.pop-message {
  display: flex;
  align-items: center;
  padding: 16px 24px;
  border-radius: 8px;
  position: fixed;
  top: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: calc(9999 * 9999 * 1000 * 9999);
  transition: opacity 0.5s ease, transform 0.5s ease;
  opacity: 1; /* 初始透明度 */
  transform: translateY(0); /* 初始位置 */
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* 添加阴影 */
}

.pop-message.success {
  background-color: #67C23A; /* 成功背景色 */
  color: #fff; /* 字体颜色 */
}

.pop-message.warn {
  background-color: #E6A23C; /* 警告背景色 */
  color: #fff; /* 字体颜色 */
}

.pop-message.error {
  background-color: #F56C6C; /* 错误背景色 */
  color: #fff; /* 字体颜色 */
}

.icon {
  margin-right: 12px; /* 图标与文本之间的间距 */
  font-size: 20px; /* 图标大小 */
}

.text {
  flex: 1; /* 文本占据剩余空间 */
  font-size: 16px; /* 文本大小 */
}
</style>