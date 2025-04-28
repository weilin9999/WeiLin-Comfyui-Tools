// Global variables
window.weilinGlobalSelectedLoras = [];


// window.addEventListener('message', handleWindowMessage);

// Open Lora Manager
function openLoraManager(event) {
    const seedThis = event.getAttribute("data-seed");
    const seed = seedThis;
    // console.log(seed)
    window.postMessage({
        type: 'weilin_prompt_ui_openLoraManager_addLora_stack_node',
        seed: seed
    }, '*');
}

// Handle window messages
function handleWindowMessage(event) {
    if (event.data.type === 'weilin_prompt_ui_node_lora_stack_update_lora_stack') {
        const seed = event.data.seed;
        renderAllLoras(seed)
    }
}

// Add a new Lora
function addLora(seed, lora) {
    // Check if already exists
    if (!window.weilinGlobalSelectedLoras[seed].some(item => item.name === lora.name)) {
        const newLora = {
            name: lora.name,
            weight: 1,
            text_encoder_weight: 1,
            hidden: false,
            ...lora
        };
        window.weilinGlobalSelectedLoras[seed].push(newLora);
        renderLoraItem(seed, window.weilinGlobalSelectedLoras[seed].length - 1, newLora);
        updateLoraStackInfoToWindows(seed);
    }
}

// Remove a Lora
function removeLora(seed, index) {
    if (index > -1) {
        // console.log(index)
        window.weilinGlobalSelectedLoras[seed].splice(index, 1);
        const itemToRemove = document.getElementById(`lora-item-${seed}-${index}`);
        if (itemToRemove) {
            itemToRemove.remove();
        }
        updateLoraStackInfoToWindows(seed);
    }
}

// Toggle Lora visibility
function toggleHideLora(seed, index) {
    if (index > -1) {
        const lora = window.weilinGlobalSelectedLoras[seed][index];
        lora.hidden = !lora.hidden;
        const loraItem = document.getElementById(`lora-item-${seed}-${index}`);
        if (loraItem) {
            loraItem.classList.toggle('hidden-lora', lora.hidden);
            const hideBtn = loraItem.querySelector('.hide-btn');
            if (hideBtn) {
                hideBtn.innerHTML = `
                    ${getHideButtonContent(lora.hidden)}
                    ${lora.hidden ? (getSystemLanguage() === 'zh' ? '显示Lora' : 'Show Lora') : (getSystemLanguage() === 'zh' ? '隐藏Lora' : 'Hide Lora')}
                `;
            }
        }
        updateLoraStackInfoToWindows(seed);
    }
}

// 在文件顶部添加语言检测函数
function getSystemLanguage() {
    const lang = navigator.language || navigator.userLanguage;
    return lang.startsWith('zh') ? 'zh' : 'en';
}

// Render a Lora item
function renderLoraItem(seed, index, lora) {
    const loraListContainer = document.getElementById('loraListContainer_' + seed);


    const loraItem = document.createElement('div');
    loraItem.className = `lora-item ${lora.hidden ? 'hidden-lora' : ''}`;
    loraItem.id = `lora-item-${seed}-${index}`;

    loraItem.innerHTML = `
    <div class="lora-info">
        <div class="lora-header-item">
            <span class="lora-name" title="${lora.name}">${lora.name}</span>
            <div class="lora-actions">
                <button class="look-on-btn" title="${getSystemLanguage() === 'zh' ? '查看Lora' : 'Look on Lora'}">
                    <svg viewBox="0 0 1024 1024" width="14" height="14">
                        <path d="M576.5 930.2H163.1c-52.9 0-96-43.1-96-96v-672c0-52.9 43.1-96 96-96h672c52.9 0 96 43.1 96 96V577c0 17.7-14.3 32-32 32s-32-14.3-32-32V162.2c0-17.6-14.4-32-32-32h-672c-17.6 0-32 14.4-32 32v672c0 17.6 14.4 32 32 32h413.4c17.7 0 32 14.3 32 32s-14.3 32-32 32z" p-id="3466"></path>
                        <path d="M692.4 322.3H245.7c-17.7 0-32-14.3-32-32s14.3-32 32-32h446.7c17.7 0 32 14.3 32 32s-14.3 32-32 32zM388.5 530.2H245.7c-17.7 0-32-14.3-32-32s14.3-32 32-32h142.7c17.7 0 32 14.3 32 32 0.1 17.6-14.3 32-31.9 32zM388.5 738H245.7c-17.7 0-32-14.3-32-32s14.3-32 32-32h142.7c17.7 0 32 14.3 32 32 0.1 17.7-14.3 32-31.9 32z" p-id="3467"></path>
                        <path d="M624.1 792.5c-94.8 0-172-77.2-172-172s77.2-172 172-172 172 77.2 172 172-77.1 172-172 172z m0-280c-59.6 0-108 48.4-108 108s48.4 108 108 108 108-48.4 108-108-48.4-108-108-108z" p-id="3468"></path>
                        <path d="M820.8 864.2L710.5 753.9c-12.5-12.5-12.5-32.8 0-45.3s32.8-12.5 45.3 0L866 818.9c12.5 12.5 12.5 32.8 0 45.3s-32.7 12.5-45.2 0z" p-id="3469"></path>
                    </svg>
                </button>
                <button class="remove-btn" title="${getSystemLanguage() === 'zh' ? '移除Lora' : 'Remove Lora'}">
                    <svg viewBox="0 0 24 24" width="14" height="14">
                        <path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
                    </svg>
                </button>
            </div>
        </div>
        <div class="lora-weights">
            <div class="weight-item">
                <label>${getSystemLanguage() === 'zh' ? '模型权重' : 'Model Weight'}</label>
                <input id="model-weight-${seed}-${index}" type="number" class="lora-weight" step="0.1" value="${lora.weight}">
            </div>
            <div class="weight-item">
                <label>${getSystemLanguage() === 'zh' ? '文本编码器权重' : 'Text Encoder Weight'}</label>
                <input id="text-encoder-weight-${seed}-${index}" type="number" class="lora-weight" step="0.1" value="${lora.text_encoder_weight}">
            </div>
        </div>
        <div class="lora-footer">
            <button class="hide-btn" title="${lora.hidden ? (getSystemLanguage() === 'zh' ? '显示Lora' : 'Show Lora') : (getSystemLanguage() === 'zh' ? '隐藏Lora' : 'Hide Lora')}">
                ${getHideButtonContent(lora.hidden)}
                ${lora.hidden ? (getSystemLanguage() === 'zh' ? '显示Lora' : 'Show Lora') : (getSystemLanguage() === 'zh' ? '隐藏Lora' : 'Hide Lora')}
            </button>
        </div>
    </div>
    `;

    // Add event listeners
    loraItem.querySelector('.look-on-btn').addEventListener('click', () => lookOnLora(lora.lora));
    loraItem.querySelector('.remove-btn').addEventListener('click', () => removeLora(seed, index));
    loraItem.querySelector('.hide-btn').addEventListener('click', () => toggleHideLora(seed, index));

    // Add input change listeners
    const weightInputs = loraItem.querySelectorAll('.lora-weight');
    weightInputs.forEach(input => {
        input.addEventListener('change', (e) => {
            const lora = window.weilinGlobalSelectedLoras[seed][index];
            if (lora) {
                if (input.id.startsWith('model-weight')) {
                    lora.weight = parseFloat(e.target.value);
                } else if (input.id.startsWith('text-encoder-weight')) {
                    lora.text_encoder_weight = parseFloat(e.target.value);
                }
                updateLoraStackInfoToWindows(seed);
            }
        });
    });

    loraListContainer.appendChild(loraItem);
}

// Get hide button content
function getHideButtonContent(hidden) {
    return hidden ?
        `<svg viewBox="0 0 24 24" width="14" height="14">
                <path d="M12 4.5C7 4.5 2.73 7.61 1 12c1.73 4.39 6 7.5 11 7.5s9.27-3.11 11-7.5c-1.73-4.39-6-7.5-11-7.5zM12 17c-2.76 0-5-2.24-5-5s2.24-5 5-5 5 2.24 5 5-2.24 5-5 5zm0-8c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z" />
            </svg>` :
        `<svg viewBox="0 0 24 24" width="14" height="14">
                <path  d="M12 7c2.76 0 5 2.24 5 5 0 .65-.13 1.26-.36 1.83l2.92 2.92c1.51-1.26 2.7-2.89 3.43-4.75-1.73-4.39-6-7.5-11-7.5-1.4 0-2.74.25-3.98.7l2.16 2.16C10.74 7.13 11.35 7 12 7zM2 4.27l2.28 2.28.46.46C3.08 8.3 1.78 10.02 1 12c1.73 4.39 6 7.5 11 7.5 1.55 0 3.03-.3 4.38-.84l.42.42L19.73 22 21 20.73 3.27 3 2 4.27zM7.53 9.8l1.55 1.55c-.05.21-.08.43-.08.65 0 1.66 1.34 3 3 3 .22 0 .44-.03.65-.08l1.55 1.55c-.67.33-1.41.53-2.2.53-2.76 0-5-2.24-5-5 0-.79.2-1.53.53-2.2zm4.31-.78l3.15 3.15.02-.16c0-1.66-1.34-3-3-3l-.17.01z" />
        </svg>`;
}

// Look on Lora
function lookOnLora(lora) {
    window.postMessage({
        type: 'weilin_prompt_ui_openLoraDetail',
        lora: lora
    }, '*');
}

// Initialize Lora Stack
function initLoraStack() {
    window.postMessage({
        type: 'weilin_prompt_ui_node_lora_stack_get_lora_info',
        seed: seed
    }, '*');
}

// Render all Lora items
function renderAllLoras(seed) {
    const loraListContainer = document.getElementById('loraListContainer_' + seed);
    loraListContainer.innerHTML = '';
    window.weilinGlobalSelectedLoras[seed].forEach((lora, index) => {
        renderLoraItem(seed, index, lora);
    });
}

// Update Lora stack info to windows
function updateLoraStackInfoToWindows(seed) {
    let putJson = {
        lora: "",
        temp_lora: window.weilinGlobalSelectedLoras[seed]
    };

    const tempLora = window.weilinGlobalSelectedLoras[seed].filter(lora => !lora.hidden);
    if (tempLora.length > 0) {
        putJson.lora = tempLora;
    }

    const jsonStr = JSON.stringify(putJson);
    window.postMessage({
        type: 'weilin_prompt_ui_prompt_node_finish_lora_stack_' + seed,
        data: jsonStr
    }, '*');
}
