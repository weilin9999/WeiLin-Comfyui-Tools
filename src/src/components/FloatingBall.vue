<template>
    <!-- 悬浮球 -->
    <div class="weilin_prompt_ui_floating-ball" :style="computedBallStyle[i - 1]" @mouseenter="handleMouseEnter(i - 1)"
        @mouseleave="handleMouseLeave(i - 1)" @mousedown="startDrag($event, i - 1)" @mouseup="stopDrag($event, i - 1)"
        v-for="i in savedFloatingBallCount" :key="'floating-ball-' + i">
        <div class="weilin_prompt_ui_ball-content" @click="handleClick">
            {{ ballSkinType === 'default' ? 'WeiLin' : '' }}
        </div>
        <!-- 目录 -->
        <div v-if="showMenu[i - 1]" class="weilin_prompt_ui_menu-container" @mousedown.stop>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item1')">{{ t('floatingBall.promptBox')
            }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item2')">{{
                t('floatingBall.tagManager') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item3')">{{
                t('floatingBall.loraManager') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item4')">{{ t('floatingBall.aiWindow')
            }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item6')">{{
                t('floatingBall.openNodeListWindow') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item7')">{{ t('floatingBall.tranToWeb')
            }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item8')">{{
                t('floatingBall.openSetting') }}</div>
            <div class="weilin_prompt_ui_menu-item" @click="handleMenuItemClick('item5')">{{
                t('floatingBall.restoreWindow') }}</div>
        </div>
    </div>

    <tranToWeb ref="tranToWebRef" />
    <SettingDialog ref="settingDialog" />

</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue';
import { useI18n } from 'vue-i18n'
import tranToWeb from './tranToWeb.vue';
import SettingDialog from '../view/prompt_box/components/setting_dialog.vue'

const { t } = useI18n()
// 新增悬浮球设置相关状态
const savedFloatingBallCount = ref(parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallCount')) || 1);
const savedFloatingBallSize = ref(parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallSize')) || 66);
const savedFloatingBallHeight = ref(localStorage.getItem('weilin_prompt_ui_floatingBallHeightSize') || savedFloatingBallSize.value);

// 新增悬浮球样式相关状态
const ballSkinType = ref(localStorage.getItem('weilin_prompt_ui_ballSkinType') || 'default');
const customSkinUrl = ref(localStorage.getItem('weilin_prompt_ui_customSkinUrl') || '');
const bgType = ref(localStorage.getItem('weilin_prompt_ui_bgType') || 'gradient');
const gradientColor1 = ref(localStorage.getItem('weilin_prompt_ui_gradientColor1') || '#6a11cb');
const gradientColor2 = ref(localStorage.getItem('weilin_prompt_ui_gradientColor2') || '#2575fc');
const ballBorderRadius = ref(localStorage.getItem('weilin_prompt_ui_ballBorderRadius') || 50);

// 如果悬浮球设置小于1或小于66，则设置为1和66
if (savedFloatingBallCount.value < 1) {
    savedFloatingBallCount.value = 1;
    localStorage.setItem('weilin_prompt_ui_floatingBallCount', savedFloatingBallCount.value);
}
if (savedFloatingBallSize.value < 5) {
    savedFloatingBallSize.value = 66;
    localStorage.setItem('weilin_prompt_ui_floatingBallSize', savedFloatingBallSize.value);
}
if (savedFloatingBallHeight.value < 5) {
    savedFloatingBallHeight.value = 66;
    localStorage.setItem('weilin_prompt_ui_floatingBallHeightSize', savedFloatingBallHeight.value);
}

if (!localStorage.getItem('weilin_prompt_ui_floatingBallCount')) {
    localStorage.setItem('weilin_prompt_ui_floatingBallCount', savedFloatingBallCount.value);
}

if (!localStorage.getItem('weilin_prompt_ui_floatingBallSize')) {
    localStorage.setItem('weilin_prompt_ui_floatingBallSize', savedFloatingBallSize.value);
}

if (!localStorage.getItem('weilin_prompt_ui_floatingBallHeightSize')) {
    localStorage.setItem('weilin_prompt_ui_floatingBallHeightSize', savedFloatingBallSize.value);
}

// 悬浮球的位置
const ballPosition = ref([]);
const isDragging = ref([]);
const showMenu = ref([]); // 控制目录显示
// 悬浮球的样式
const ballStyle = ref([]);
const settingDialog = ref(null)


// 计算悬浮球样式
const computedBallStyle = computed(() => {
    return ballStyle.value.map(style => {
        const newStyle = { ...style };

        // 背景设置
        if (ballSkinType.value === 'custom' && customSkinUrl.value) {
            newStyle.backgroundImage = `url(${customSkinUrl.value})`;
            newStyle.backgroundSize = 'contain';  // 改为contain保持比例
            newStyle.backgroundRepeat = 'no-repeat';
            newStyle.backgroundPosition = 'center';
            newStyle.imageRendering = 'optimizeQuality';  // 优化渲染质量
        } else if (bgType.value === 'gradient') {
            newStyle.background = `linear-gradient(135deg, ${gradientColor1.value}, ${gradientColor2.value})`;
        } else {
            newStyle.background = 'transparent';
        }

        // 圆角设置
        newStyle.borderRadius = `${ballBorderRadius.value}%`;

        return newStyle;
    });
});

// 初始化
for (let i = 0; i < savedFloatingBallCount.value; i++) {
    showMenu.value[i] = false;
    isDragging.value[i] = false;

    const viewportWidth = window.innerWidth;
    const viewportHeight = window.innerHeight;
    const ballSize = savedFloatingBallSize.value;
    const ballHeight = savedFloatingBallHeight.value; // 使用设置的高度或默认大小
    const spacing = 10; // 球之间的间距

    // 计算每行能放多少个球
    const ballsPerRow = Math.floor(viewportWidth / (ballSize + spacing));

    // 计算当前球的行和列
    const row = Math.floor(i / ballsPerRow);
    const col = i % ballsPerRow;

    // 计算初始位置
    let x = 20 + col * (ballSize + spacing);
    let y = viewportHeight - 100 - row * (ballHeight + spacing);

    // 边界检查
    x = Math.max(0, x);
    x = Math.min(x, viewportWidth - ballSize);
    y = Math.max(0, y);
    y = Math.min(y, viewportHeight - ballHeight);

    ballPosition.value[i] = {
        x: x,
        y: y,
        width: ballSize + 'px',
        height: ballHeight + 'px'
    };

    ballStyle.value[i] = {
        left: `${ballPosition.value[i].x}px`,
        top: `${ballPosition.value[i].y}px`,
        width: `${ballSize}px`,
        height: `${ballHeight}px`,
    }
}

// 开始拖拽
const startDrag = (event, i) => {
    // 判断点击是否在悬浮球本体或其直接子元素上
    const target = event.target;
    if (target.closest('.weilin_prompt_ui_floating-ball')) {
        isDragging.value[i] = true;
        document.addEventListener('mousemove', (e) => onDrag(e, i));
        document.addEventListener('mouseup', (e) => stopDrag(e, i));
    }
};

// 拖拽中
const onDrag = (event, i) => {
    if (isDragging.value[i]) {
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        const ballSize = savedFloatingBallSize.value;
        const ballHeight = savedFloatingBallHeight.value; // 新增高度变量

        // 计算新位置并确保不超出边界
        let newX = event.clientX - ballSize / 2;
        let newY = event.clientY - ballHeight / 2; // 使用ballHeight计算Y位置

        // 确保左侧不超出边界
        newX = Math.max(0, newX);
        // 确保右侧不超出边界
        newX = Math.min(newX, viewportWidth - ballSize);
        // 确保顶部不超出边界
        newY = Math.max(0, newY);
        // 确保底部不超出边界
        newY = Math.min(newY, viewportHeight - ballHeight);

        ballPosition.value[i] = {
            x: newX,
            y: newY,
            width: ballSize + 'px',
            height: ballHeight + 'px' // 使用设置的高度
        };

        ballStyle.value[i] = {
            left: `${ballPosition.value[i].x}px`,
            top: `${ballPosition.value[i].y}px`,
            width: `${ballSize}px`,
            height: `${ballHeight}px`, // 使用设置的高度
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
        case 'item7':
            openTranToWebDialog()
            break;
        case 'item8':
            settingDialog.value.open()
            break;
    }
};

const tranToWebRef = ref()
const openTranToWebDialog = () => {
    tranToWebRef.value.open()
}

// 监听悬浮球设置
const handleMessage = (event) => {
    if (event.data.type === 'weilin_prompt_ui_floating_ball_setting') {
        savedFloatingBallCount.value = parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallCount')) || 1;
        savedFloatingBallSize.value = parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallSize')) || 66;
        savedFloatingBallHeight.value = parseInt(localStorage.getItem('weilin_prompt_ui_floatingBallHeightSize')) || savedFloatingBallSize.value;
        ballSkinType.value = localStorage.getItem('weilin_prompt_ui_ballSkinType') || 'default';
        customSkinUrl.value = localStorage.getItem('weilin_prompt_ui_customSkinUrl') || '';
        bgType.value = localStorage.getItem('weilin_prompt_ui_bgType') || 'gradient';
        gradientColor1.value = localStorage.getItem('weilin_prompt_ui_gradientColor1') || '#6a11cb';
        gradientColor2.value = localStorage.getItem('weilin_prompt_ui_gradientColor2') || '#2575fc';
        ballBorderRadius.value = localStorage.getItem('weilin_prompt_ui_ballBorderRadius') || 50;

        // 重新初始化悬浮球
        showMenu.value = [];
        isDragging.value = [];
        ballPosition.value = [];
        ballStyle.value = [];

        for (let i = 0; i < savedFloatingBallCount.value; i++) {
            showMenu.value[i] = false;
            isDragging.value[i] = false;

            const viewportWidth = window.innerWidth;
            const viewportHeight = window.innerHeight;
            const ballSize = savedFloatingBallSize.value;
            const ballHeight = savedFloatingBallHeight.value; // 使用设置的高度或默认大小
            const spacing = 10; // 球之间的间距

            // 计算每行能放多少个球
            const ballsPerRow = Math.floor(viewportWidth / (ballSize + spacing));

            // 计算当前球的行和列
            const row = Math.floor(i / ballsPerRow);
            const col = i % ballsPerRow;

            // 计算初始位置
            let x = 20 + col * (ballSize + spacing);
            let y = viewportHeight - 100 - row * (ballHeight + spacing);

            // 边界检查
            x = Math.max(0, x);
            x = Math.min(x, viewportWidth - ballSize);
            y = Math.max(0, y);
            y = Math.min(y, viewportHeight - ballHeight);

            ballPosition.value[i] = {
                x: x,
                y: y,
                width: ballSize + 'px',
                height: ballHeight + 'px'
            };

            ballStyle.value[i] = {
                left: `${ballPosition.value[i].x}px`,
                top: `${ballPosition.value[i].y}px`,
                width: `${ballSize}px`,
                height: `${ballHeight}px`,
                // 优化后的样式判断逻辑
                ...(ballSkinType.value === 'custom' && customSkinUrl.value
                    ? {
                        backgroundImage: `url(${customSkinUrl.value})`,
                        backgroundSize: 'cover',
                        backgroundRepeat: 'no-repeat',
                        backgroundPosition: 'center'
                    }
                    : bgType.value === 'gradient'
                        ? { background: `linear-gradient(135deg, ${gradientColor1.value}, ${gradientColor2.value})` }
                        : { background: 'transparent' }
                ),
                borderRadius: `${ballBorderRadius.value}%`
            };
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
    /* background: linear-gradient(135deg, #6a11cb, #2575fc); */
    /* 添加渐变色 */
    /* border-radius: 50%; */
    cursor: pointer;
    /* box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2); */
    display: flex;
    align-items: center;
    justify-content: center;
    transform: scale(1);
    font-size: 24px;
    position: fixed;
    z-index: calc(9999 * 9999 * 100 * 9999);
    user-select: none;
    /* transition: all 0.1s; */
}

.weilin_prompt_ui_floating-ball:hover {
    /* transform: scale(1.1); */
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
    top: -320px;
    /* 目录在悬浮球上方 */
    left: 50%;
    max-height: 330px;
    width: 120px;
    transform: translateX(-50%);
    background-color: var(--weilin-prompt-ui-primary-bg);
    /* 使用主题背景色 */
    border: 1px solid var(--weilin-prompt-ui-border-color);
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
    color: var(--weilin-prompt-ui-tag-text);
}

.weilin_prompt_ui_menu-item:hover {
    color: var(--weilin-prompt-ui-tag-text);
    background-color: var(--weilin-prompt-ui-tag-hover);
    /* 使用悬停背景色 */
}
</style>