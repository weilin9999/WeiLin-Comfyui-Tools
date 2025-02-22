<template>
    <div class="ai-chat-window">
        <!-- 历史对话侧边栏 -->
        <div class="history-sidebar">
            <button class="new-chat-btn" @click="startNewChat">{{ t('aiWindow.newChat') }}</button>
            <div class="history-list">
                <div v-for="(chat, index) in chatHistory" :key="index" class="history-item"
                    :class="{ active: currentChatIndex === index }" @click="switchChat(index)">
                    <span v-if="!isRenaming || currentChatIndex !== index">
                        {{ chat?.title || t('aiWindow.chatName') + ` ${index + 1}` }}
                    </span>
                    <input v-else v-model="renameInput" @keyup.enter="confirmRename(index)" @blur="confirmRename(index)"
                        @keyup.esc="cancelRename" class="rename-input" />
                    <div class="item-actions">
                        <button class="rename-btn" @click.stop="startRename(index)">✎</button>
                        <button class="delete-btn" v-if="!isRenaming" @click.stop="deleteChat(index)">×</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- 聊天主界面 -->
        <div class="chat-main">
            <div class="message-list">
                <div v-for="(message, index) in currentChat.messages" :key="index" class="message"
                    :class="message.role">
                    <div class="message-content">
                        <pre>{{ message.content }}</pre>
                    </div>
                </div>
                <div v-if="isLoading" class="message assistant">
                    <div class="message-content">
                        <pre>{{ t('aiWindow.thinking') }}</pre>
                    </div>
                </div>
            </div>

            <!-- 输入框 -->
            <div class="input-area">
                <textarea class="ai-chat-textarea" v-model="inputMessage" :placeholder="t('aiWindow.inputMessage')"
                    @keydown.enter.exact.prevent="sendMessage"></textarea>
                <button class="ai-chat-btn" @click="sendMessage" :disabled="isLoading">
                    {{ t('aiWindow.send') }}
                </button>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import { baseUrl } from '@/api/request'
import { openaiApi } from '@/api/openai'
import message from "@/utils/message"
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
// 聊天历史数据
const chatHistory = ref([]);
const currentChatIndex = ref(-1);
const inputMessage = ref('');
const isLoading = ref(false);

const openAiSetting = ref({})
// 在 data 部分添加
const isRenaming = ref(false);
const renameInput = ref('');

// 修改 startRename 方法
const startRename = (index) => {
  if (!chatHistory.value[index]) return; // 确保 chat 存在
  isRenaming.value = true;
  renameInput.value = chatHistory.value[index]?.title || `对话 ${index + 1}`;
  currentChatIndex.value = index;
};

// 修改 confirmRename 方法
const confirmRename = (index) => {
  if (!chatHistory.value[index]) return; // 确保 chat 存在
  if (renameInput.value.trim()) {
    chatHistory.value[index].title = renameInput.value.trim();
    saveChatHistory();
  }
  isRenaming.value = false;
};

const cancelRename = () => {
    isRenaming.value = false;
};

const getOpenAiSetting = () => {
    openaiApi.getOpenAiSetting().then(res => {
        openAiSetting.value = res.data
    }).catch(err => {
        message({ type: "warn", str: 'message.networkError' });
    })
}

onMounted(() => {
    getOpenAiSetting()
})

// 当前聊天
const currentChat = computed(() => {
    return chatHistory.value[currentChatIndex.value] || { messages: [] };
});

// 切换对话
const switchChat = (index) => {
    currentChatIndex.value = index;
};

// 在 startNewChat 中添加
const startNewChat = () => {
    isLoading.value = true;
    const newChat = {
        title: `对话 ${chatHistory.value.length + 1}`,
        messages: [],
        createdAt: new Date().toISOString()
    };
    chatHistory.value.push(newChat);
    currentChatIndex.value = chatHistory.value.length - 1;
    saveChatHistory();
    isLoading.value = false;
    return newChat;
};

// 从 localStorage 加载对话历史
const loadChatHistory = () => {
    const savedHistory = localStorage.getItem('aiChatHistory');
    if (savedHistory) {
        chatHistory.value = JSON.parse(savedHistory);
    }
};

// 保存对话历史到 localStorage
const saveChatHistory = () => {
    localStorage.setItem('aiChatHistory', JSON.stringify(chatHistory.value));
};

// 在组件挂载时加载历史记录
onMounted(() => {
    getOpenAiSetting();
    loadChatHistory();
});

// 修改后的 sendMessage 方法
const sendMessage = async () => {
    if (!inputMessage.value.trim() || isLoading.value) return;

    // 如果没有对话或未选择对话，自动创建新对话
    if (chatHistory.value.length === 0 || currentChatIndex.value === -1) {
        startNewChat();
    }

    const userMessage = {
        role: 'user',
        content: inputMessage.value,
        timestamp: new Date().toISOString()
    };

    // 先保存用户消息
    currentChat.value.messages.push(userMessage);
    saveChatHistory();

    // 清空输入框
    inputMessage.value = '';

    // 准备 AI 回复
    const assistantMessage = {
        role: 'assistant',
        content: '',
        timestamp: new Date().toISOString()
    };

    // 添加占位消息
    currentChat.value.messages.push(assistantMessage);
    saveChatHistory();

    isLoading.value = true;

    try {
        await streamResponse(
            { messages: currentChat.value.messages },
            (data) => {
                // 更新最后一条消息（AI 的回复）
                const lastMessage = currentChat.value.messages[currentChat.value.messages.length - 1];
                lastMessage.content += data.content;
                saveChatHistory();
            },
            (error) => {
                console.error('Error:', error);
                // 更新错误信息
                const lastMessage = currentChat.value.messages[currentChat.value.messages.length - 1];
                lastMessage.content = '抱歉，出错了，请稍后再试。';
                saveChatHistory();
            },
            () => {
                isLoading.value = false;
                saveChatHistory();
            }
        );
    } catch (error) {
        console.error('Error:', error);
        isLoading.value = false;
        // 更新错误信息
        const lastMessage = currentChat.value.messages[currentChat.value.messages.length - 1];
        lastMessage.content = '请求失败，请检查网络连接。';
        saveChatHistory();
    }
};

// 修改删除对话方法
const deleteChat = (index) => {
    chatHistory.value.splice(index, 1);
    if (currentChatIndex.value === index) {
        currentChatIndex.value = Math.max(0, index - 1);
    }
    saveChatHistory();
};

// 流式响应处理
const streamResponse = async (data, onMessage, onError, onComplete) => {
    try {
        const response = await fetch(openAiSetting.value.base_url + '/chat/completions', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${openAiSetting.value.api_key}` // 替换为你的 OpenAI API Key
            },
            body: JSON.stringify({
                model: openAiSetting.value.model, // 或 "gpt-4"
                messages: data.messages,
                stream: true
            }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) {
                onComplete();
                break;
            }

            buffer += decoder.decode(value, { stream: true });

            // 处理 OpenAI 的流式响应格式
            const lines = buffer.split('\n');
            buffer = lines.pop(); // 最后一行可能不完整

            for (const line of lines) {
                if (line.trim() === '') continue;
                if (line === 'data: [DONE]') {
                    onComplete();
                    return;
                }

                try {
                    const json = line.replace(/^data: /, '');
                    const parsed = JSON.parse(json);
                    const content = parsed.choices[0]?.delta?.content || '';
                    if (content) {
                        onMessage({ content });
                    }
                } catch (e) {
                    console.error('Failed to parse message:', line);
                }
            }
        }
    } catch (error) {
        onError(error);
    }
};
</script>

<style scoped>
.ai-chat-window {
    display: flex;
    height: 100%;
    background: var(--weilin-prompt-ui-primary-bg);
    color: var(--weilin-prompt-ui-primary-text);
}

.history-sidebar {
    width: 250px;
    border-right: 1px solid var(--weilin-prompt-ui-border-color);
    padding: 16px;
    background: var(--weilin-prompt-ui-secondary-bg);
}

.new-chat-btn {
    width: 100%;
    padding: 8px 16px;
    margin-bottom: 16px;
    background: var(--weilin-prompt-ui-primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.new-chat-btn:hover {
    background: var(--weilin-prompt-ui-primary-color-hover);
}

.history-list {
    overflow-y: auto;
    height: calc(100% - 60px);
}

.history-item {
    position: relative;
    padding: 8px 12px;
    margin-bottom: 8px;
    border-radius: 4px;
    cursor: pointer;
    background: var(--weilin-prompt-ui-secondary-bg);
    transition: background 0.3s ease;
}

.history-item:hover {
    background: var(--weilin-prompt-ui-hover-bg-color);
}

.history-item.active {
    background: var(--weilin-prompt-ui-primary-color);
    color: white;
}

.rename-input {
    width: 100%;
    padding: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-primary-text);
}

.item-actions {
    position: absolute;
    right: 8px;
    top: 50%;
    transform: translateY(-50%);
    display: none;
}

.history-item:hover .item-actions {
    display: flex;
    gap: 4px;
}

.rename-btn,
.delete-btn {
    background: none;
    border: none;
    padding: 4px;
    cursor: pointer;
    color: var(--weilin-prompt-ui-secondary-text);
    transition: color 0.2s;
}

.rename-btn:hover {
    color: var(--weilin-prompt-ui-warning-color);
}

.delete-btn:hover {
    color: var(--weilin-prompt-ui-warning-color);
}

.chat-main {
    flex: 1;
    display: flex;
    flex-direction: column;
    padding: 16px;
}

.message-list {
    flex: 1;
    overflow-y: auto;
    margin-bottom: 16px;
}

.message {
    margin-bottom: 16px;
    padding: 12px 16px;
    border-radius: 8px;
    max-width: 80%;
    width: fit-content;
}

.message.user {
    margin-left: auto;
    background: var(--weilin-prompt-ui-primary-color);
    color: white;
}

.message.assistant {
    margin-right: auto;
    background: var(--weilin-prompt-ui-secondary-bg);
    border: 1px solid var(--weilin-prompt-ui-border-color);
}

.message-content pre {
    margin: 0;
    white-space: pre-wrap;
    word-wrap: break-word;
    font-family: inherit;
}

.input-area {
    display: flex;
    gap: 8px;
    padding: 16px;
    background: var(--weilin-prompt-ui-secondary-bg);
    border-radius: 8px;
}

.ai-chat-textarea {
    flex: 1;
    padding: 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-primary-text);
    resize: none;
}

.ai-chat-btn {
    padding: 12px 24px;
    background: var(--weilin-prompt-ui-primary-color);
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background 0.3s ease;
}

.ai-chat-btn:hover {
    background: var(--weilin-prompt-ui-primary-color-hover);
}

.ai-chat-btn:disabled {
    background: var(--weilin-prompt-ui-secondary-bg);
    cursor: not-allowed;
    opacity: 0.7;
}
</style>