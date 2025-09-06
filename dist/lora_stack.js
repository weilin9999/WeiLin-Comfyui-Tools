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
       // Ensure defaults are 1 and override any incoming 0.5
       const newLora = {
           ...lora,
           name: lora.name,
           weight: 1,
           text_encoder_weight: 1,
           hidden: false,
       };
       window.weilinGlobalSelectedLoras[seed].push(newLora);
       renderAllLoras(seed);
       updateLoraStackInfoToWindows(seed);
   }
}

// Remove a Lora
function removeLora(seed, index) {
   if (index > -1) {
       // console.log(index)
       window.weilinGlobalSelectedLoras[seed].splice(index, 1);
       renderAllLoras(seed);
       updateLoraStackInfoToWindows(seed);
   }
}

// Toggle Lora visibility
function toggleHideLora(seed, index) {
   if (index > -1) {
       const lora = window.weilinGlobalSelectedLoras[seed][index];
       lora.hidden = !lora.hidden;
       updateLoraStackInfoToWindows(seed);
   }
}

// 语言检测函数
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
   
   // 添加拖动属性
   loraItem.setAttribute('draggable', 'true');
   loraItem.setAttribute('data-index', index.toString());

   const displayName = lora.display_name || lora.name || lora.lora;

   loraItem.innerHTML = `
   <div class="lora-info">
       <div class="lora-header-item">
           <span class="lora-name" title="${displayName}">${displayName}</span>
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
       <div class="lora-weights compact">
           <div class="weight-item">
               <label>${getSystemLanguage() === 'zh' ? '模型权重' : 'Model Weight'}</label>
               <input id="model-weight-${seed}-${index}" type="number" class="lora-weight" step="0.1" value="${lora.weight}">
           </div>
           <div class="weight-item">
               <label>${getSystemLanguage() === 'zh' ? '文本编码器权重' : 'Text Encoder Weight'}</label>
               <input id="text-encoder-weight-${seed}-${index}" type="number" class="lora-weight" step="0.1" value="${lora.text_encoder_weight}">
           </div>
           <div class="weight-item toggle-item" title="${getSystemLanguage() === 'zh' ? '启用/禁用 Lora' : 'Enable/Disable Lora'}">
               <label class="switch">
                   <input type="checkbox" id="visible-toggle-${seed}-${index}" ${lora.hidden ? '' : 'checked'}>
                   <span class="slider round"></span>
               </label>
           </div>
       </div>
   </div>
   `;

   // 添加拖动事件监听器
   loraItem.addEventListener('dragstart', (e) => handleDragStart(e, seed, index));
//    loraItem.addEventListener('dragover', handleDragOver);
//    loraItem.addEventListener('drop', (e) => handleDrop(e, seed));
   loraItem.addEventListener('dragend', handleDragEnd);

   // Add event listeners
   loraItem.querySelector('.look-on-btn').addEventListener('click', () => lookOnLora(lora.lora));
   loraItem.querySelector('.remove-btn').addEventListener('click', () => removeLora(seed, index));

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

   // If display name is missing, try to fetch it from server and update UI
   if (!lora.display_name && lora.lora) {
       try {
           fetch(`/weilin/prompt_ui/api/lorainfo/api/loras/info?file=${encodeURIComponent(lora.lora)}`)
               .then(r => r.json())
               .then(data => {
                   const info = data && (data.data || data);
                   if (info && info.name) {
                       lora.display_name = info.name;
                       const nameEl = loraItem.querySelector('.lora-name');
                       if (nameEl) {
                           nameEl.textContent = info.name;
                           nameEl.setAttribute('title', info.name);
                       }
                       updateLoraStackInfoToWindows(seed);
                   }
               })
               .catch(() => { /* ignore network errors */ });
       } catch (e) { /* ignore */ }
   }

   // Bind visibility toggle switch
   const visToggle = loraItem.querySelector(`#visible-toggle-${seed}-${index}`);
   if (visToggle) {
       visToggle.addEventListener('change', (e) => {
           const loraRef = window.weilinGlobalSelectedLoras[seed][index];
           if (loraRef) {
               loraRef.hidden = !e.target.checked;
               renderAllLoras(seed);
               updateLoraStackInfoToWindows(seed);
           }
       });
   }
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
    if (!loraListContainer) {
        return;
    }
    loraListContainer.innerHTML = '';
    
    // 移除旧的容器事件监听器（避免重复绑定）
    loraListContainer.removeEventListener('dragover', handleContainerDragOver);
    loraListContainer.removeEventListener('drop', handleContainerDrop);
    
    // 在容器上绑定拖放事件
    loraListContainer.addEventListener('dragover', (e) => handleContainerDragOver(e, seed));
    loraListContainer.addEventListener('drop', (e) => handleContainerDrop(e, seed));
    
    const list = window.weilinGlobalSelectedLoras[seed] || [];
    list.forEach((lora, index) => {
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

let draggedIndex = null;
let placeholder = null;
let insertIndex = null;

function handleDragStart(e, seed, index) {
    draggedIndex = index;
    e.target.classList.add('dragging');
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/html', e.target.outerHTML);
}

function handleDragOver(e) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    
    let target = e.target;
    while (target && !target.classList.contains('lora-item')) {
        target = target.parentElement;
    }
    
    if (!target || target.classList.contains('dragging')) return;
    
    const container = target.parentElement;
    const rect = target.getBoundingClientRect();
    const mouseY = e.clientY;
    const elementMiddle = rect.top + rect.height / 2;
    
    // 简化索引计算：直接基于DOM顺序
    const allItems = Array.from(container.querySelectorAll('.lora-item:not(.dragging)'));
    const targetIndex = allItems.indexOf(target);
    
    let newInsertIndex;
    if (mouseY < elementMiddle) {
        newInsertIndex = targetIndex;
    } else {
        newInsertIndex = targetIndex + 1;
    }
    
    if (newInsertIndex === insertIndex) return;
    
    insertIndex = newInsertIndex;
    
    removePlaceholderAndShifts();
    createPlaceholder();
    
    // 在DOM中插入占位框
    if (insertIndex >= allItems.length) {
        container.appendChild(placeholder);
    } else {
        container.insertBefore(placeholder, allItems[insertIndex]);
    }
}

function createPlaceholder() {
    placeholder = document.createElement('div');
    placeholder.className = 'lora-placeholder';
    placeholder.innerHTML = '放置位置';
}

function removePlaceholderAndShifts() {
    // 移除占位框
    if (placeholder && placeholder.parentElement) {
        placeholder.parentElement.removeChild(placeholder);
    }
    
    // 移除所有位移效果
    document.querySelectorAll('.lora-item').forEach(item => {
        item.classList.remove('shift-down');
    });
}

function addShiftEffects(container, insertPos) {
    // 这个函数可以添加让开位置的动画效果
    // 暂时简化处理，主要依靠占位框显示插入位置
}

function handleDrop(e, seed) {
    e.preventDefault();
    
    if (draggedIndex !== null && insertIndex !== null) {
        const list = window.weilinGlobalSelectedLoras[seed];
        if (draggedIndex >= 0 && draggedIndex < list.length) {
            const draggedItem = list[draggedIndex];
            
            // 先移除被拖动的元素
            list.splice(draggedIndex, 1);
            
            // 计算实际插入位置
            let finalIndex = insertIndex;
            if (insertIndex > draggedIndex) {
                finalIndex--;
            }
            
            // 插入到新位置
            list.splice(finalIndex, 0, draggedItem);
            
            renderAllLoras(seed);
            updateLoraStackInfoToWindows(seed);
        }
    }
    
    // 清理
    removePlaceholderAndShifts();
    draggedIndex = null;
    insertIndex = null;
    placeholder = null;
}

function handleDragEnd(e) {
    e.target.classList.remove('dragging');
    removePlaceholderAndShifts();
    draggedIndex = null;
    insertIndex = null;
}

function handleContainerDragOver(e, seed) {
    e.preventDefault();
    e.dataTransfer.dropEffect = 'move';
    
    const container = e.currentTarget;
    const mouseY = e.clientY;
    
    // 找到最近的 lora-item
    const allItems = Array.from(container.querySelectorAll('.lora-item:not(.dragging)'));
    let targetItem = null;
    let insertPosition = allItems.length; // 默认插入到最后
    
    for (let i = 0; i < allItems.length; i++) {
        const item = allItems[i];
        const rect = item.getBoundingClientRect();
        const itemMiddle = rect.top + rect.height / 2;
        
        if (mouseY < itemMiddle) {
            targetItem = item;
            insertPosition = i;
            break;
        }
    }
    
    if (insertPosition === insertIndex) return;
    
    insertIndex = insertPosition;
    
    removePlaceholderAndShifts();
    createPlaceholder();
    
    // 插入占位框
    if (insertIndex >= allItems.length) {
        container.appendChild(placeholder);
    } else {
        container.insertBefore(placeholder, allItems[insertIndex]);
    }
}

function handleContainerDrop(e, seed) {
    e.preventDefault();
    
    if (draggedIndex !== null && placeholder && placeholder.parentElement) {
        const container = placeholder.parentElement;
        
        // 计算占位框前面有多少个非拖动的lora-item
        let actualInsertIndex = 0;
        let currentNode = placeholder.previousElementSibling;
        
        while (currentNode) {
            if (currentNode.classList.contains('lora-item') && !currentNode.classList.contains('dragging')) {
                actualInsertIndex++;
            }
            currentNode = currentNode.previousElementSibling;
        }
        
        const list = window.weilinGlobalSelectedLoras[seed];
        if (draggedIndex >= 0 && draggedIndex < list.length) {
            const draggedItem = list[draggedIndex];
            list.splice(draggedIndex, 1);
            list.splice(actualInsertIndex, 0, draggedItem);
            
            renderAllLoras(seed);
            updateLoraStackInfoToWindows(seed);
        }
    }
    
    removePlaceholderAndShifts();
    insertIndex = null;
}