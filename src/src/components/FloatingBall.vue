<template>
    <!-- 悬浮球 -->
    <div class="weilin_prompt_ui_floating-ball" :style="ballStyle[i - 1]" @mouseenter="handleMouseEnter(i - 1)"
        @mouseleave="handleMouseLeave(i - 1)" @mousedown="startDrag($event, i - 1)" @mouseup="stopDrag($event, i - 1)"
        v-for="i in savedFloatingBallCount" :key="'floating-ball-' + i">
        <div class="weilin_prompt_ui_ball-content" @click="handleClick">
            <slot></slot>
        </div>
        <!-- 目录 -->
        <div v-if="showMenu[i - 1]" class="weilin_prompt_ui_menu-container">
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item1')">{{ t('floatingBall.promptBox')
                }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item2')">{{
                t('floatingBall.tagManager') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item3')">{{
                t('floatingBall.loraManager') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item4')">{{
                t('floatingBall.aiWindow') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item6')">{{
            t('floatingBall.openNodeListWindow') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item5')">{{
                t('floatingBall.restoreWindow') }}</div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue';
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
// 新增悬浮球设置相关状态
const savedFloatingBallCount = ref(parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallCount')) || 1);
const savedFloatingBallSize = ref(parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallSize')) || 66);
// 如果悬浮球设置小于1或小于66，则设置为1和66
if (savedFloatingBallCount.value < 1 || savedFloatingBallSize.value < 66) {
    savedFloatingBallCount.value = 1;
    savedFloatingBallSize.value = 66;
    localStorage.setItem('weilin_prompt_ui_floatingBallCount', savedFloatingBallCount.value);
    localStorage.setItem('weilin_prompt_ui_floatingBallSize', savedFloatingBallSize.value);
}
if (!localStorage.getItem('weilin_prompt_ui_floatingBallCount')) {
    localStorage.setItem('weilin_prompt_ui_floatingBallCount', savedFloatingBallCount.value);
}
if (!localStorage.getItem('weilin_prompt_ui_floatingBallSize')) {
    localStorage.setItem('weilin_prompt_ui_floatingBallSize', savedFloatingBallSize.value);
}
// 悬浮球的位置
const ballPosition = ref([]);
const isDragging = ref([]);
const showMenu = ref([]); // 控制目录显示
// 悬浮球的样式
const ballStyle = ref([]);

// 初始化
for (let i = 0; i < savedFloatingBallCount.value; i++) {
    showMenu.value[i] = false;
    isDragging.value[i] = false;
    ballPosition.value[i] = {
        x: 20 + i * (savedFloatingBallSize.value + 10), // 增加间距
        y: window.innerHeight - 100,
        width: savedFloatingBallSize.value + 'px',
        height: savedFloatingBallSize.value + 'px'
    };
    ballStyle.value[i] = {
        left: `${ballPosition.value[i].x}px`,
        top: `${ballPosition.value[i].y}px`,
        width: `${savedFloatingBallSize.value}px`,
        height: `${savedFloatingBallSize.value}px`,
    }
}

// 开始拖拽
const startDrag = (event, i) => {
    isDragging.value[i] = true;
    document.addEventListener('mousemove', (e) => onDrag(e, i));
    document.addEventListener('mouseup', (e) => stopDrag(e, i));
};

// 拖拽中
const onDrag = (event, i) => {
    if (isDragging.value[i]) {
        ballPosition.value[i].x = event.clientX - savedFloatingBallSize.value / 2; // 减去球半径
        ballPosition.value[i].y = event.clientY - savedFloatingBallSize.value / 2; // 减去球半径
        ballStyle.value[i] = {
            left: `${ballPosition.value[i].x}px`,
            top: `${ballPosition.value[i].y}px`,
            width: `${savedFloatingBallSize.value}px`,
            height: `${savedFloatingBallSize.value}px`,
        };
    }
};

// 停止拖拽
const stopDrag = (event, i) => {
    isDragging.value[i] = false;
    document.removeEventListener('mousemove', (e) => onDrag(e, i));
    document.removeEventListener('mouseup', (e) => stopDrag(e, i));
};

// 点击悬浮球
const handleClick = () => {

};

// 处理目录项点击
const handleMenuItemClick = (item) => {
    switch (item) {
        case 'item1':
            window.parent.postMessage({
                type: 'weilin_prompt_ui_open_global_prompt_box'
            }, '*')
            break;
        case 'item2':
            window.parent.postMessage({
                type: 'weilin_prompt_ui_open_global_tag_manager'
            }, '*')
            break;
        case 'item3':
            window.parent.postMessage({
                type: 'weilin_prompt_ui_open_global_lora_manager'
            }, '*')
            break;
        case 'item4':
            window.parent.postMessage({ type: 'weilin_prompt_ui_openAiWindow' }, '*')
            break;
        case 'item5':
            window.parent.postMessage({ type: 'weilin_prompt_ui_restore_window' }, '*')
            break;
        case 'item6':
            window.parent.postMessage({ type: 'weilin_prompt_ui_open_node_list_window' }, '*')
            break;
    }
};

// 监听悬浮球设置
const handleMessage = (event) => {
    if (event.data.type === 'weilin_prompt_ui_floating_ball_setting') {
        savedFloatingBallCount.value = parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallCount')) || 1;
        savedFloatingBallSize.value = parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallSize')) || 66;

        // 重新初始化悬浮球
        showMenu.value = [];
        isDragging.value = [];
        ballPosition.value = [];
        ballStyle.value = [];

        for (let i = 0; i < savedFloatingBallCount.value; i++) {
            showMenu.value[i] = false;
            isDragging.value[i] = false;
            ballPosition.value[i] = {
                x: 20 + i * (savedFloatingBallSize.value + 10),
                y: window.innerHeight - 100,
                width: savedFloatingBallSize.value + 'px',
                height: savedFloatingBallSize.value + 'px'
            };
            ballStyle.value[i] = {
                left: `${ballPosition.value[i].x}px`,
                top: `${ballPosition.value[i].y}px`,
                width: `${savedFloatingBallSize.value}px`,
                height: `${savedFloatingBallSize.value}px`,
            }
        }
    }
}

// 监听鼠标进入悬浮球区域
const handleMouseEnter = (i) => {
    showMenu.value[i] = true;
};

// 监听鼠标离开悬浮球区域
const handleMouseLeave = (i) => {
    showMenu.value[i] = false;
};

onMounted(() => {
    // 添加消息监听
    window.addEventListener('message', handleMessage)
})

// 组件卸载时移除事件监听
onUnmounted(() => {
    // 移除消息监听
    window.removeEventListener('message', handleMessage)
    document.removeEventListener('mousemove', onDrag);
    document.removeEventListener('mouseup', stopDrag);
});
</script>

<style scoped>
.weilin_prompt_ui_floating-ball {
    background: linear-gradient(135deg, #6a11cb, #2575fc);
    /* 添加渐变色 */
    border-radius: 50%;
    cursor: pointer;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    display: flex;
    align-items: center;
    justify-content: center;
    left: 220px;
    bottom: 220px;
    transform: scale(1);
    font-size: 24px;
    position: fixed;
    z-index: calc(9999 * 9999 * 100 * 9999);
    user-select: none;
}

.weilin_prompt_ui_floating-ball:hover {
    transform: scale(1.1);
    /* 悬浮时放大 */
    box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
    /* 悬浮时阴影加深 */
}

.weilin_prompt_ui_ball-content {
    color: white;
    /* 文字颜色改为白色 */
    font-size: 16px;
    user-select: none;
}

.weilin_prompt_ui_menu-container {
    position: absolute;
    top: -230px;
    /* 目录在悬浮球上方 */
    left: 50%;
    max-height: 260px;
    width: 120px;
    transform: translateX(-50%);
    background-color: var(--p-menubar-submenu-background);
    /* 使用主题背景色 */
    border: 1px solid var(--p-menubar-submenu-border-color);
    /* 使用边框颜色 */
    border-radius: 8px;
    box-shadow: 0 4px 12px var(--weilin-prompt-ui-shadow-color);
    padding: 8px 0;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.weilin_prompt_ui_menu-item {
    padding: 8px 16px;
    cursor: pointer;
    transition: background-color 0.2s ease;
    font-size: 12px;
}

.weilin_prompt_ui_menu-item:hover {
    color: var(--p-menubar-item-focus-color);
    background-color: var(--p-menubar-item-focus-background);
    /* 使用悬停背景色 */
}
</style>