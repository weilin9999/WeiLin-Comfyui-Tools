<template>
  <div class="weilin_prompt_ui_prompt-box">
    <!-- Lora栈 -->
    <LoraStack v-if="props.promptManager === 'prompt'" :is-open="loraOpen" :selected-loras="selectedLoras"
      @close="closeLora" />
    <!-- 主标签管理器（左侧边栏） -->
    <!-- <MainLabelManager ref="mainLabelManagerRef" :selected-id="selectedMainLabelId" @select="onSelectMainLabel" /> -->
    <MainLabelManager v-if="isLabelManagerVisible" ref="mainLabelManagerRef" :selected-id="selectedMainLabelId" @select="onSelectMainLabel" />
    <!-- 主要内容容器 -->
    <div :class="`${prefix}main-content`" :style="{ width: mainContentWidth }">
      <!-- 操作栏 -->
      <div class="center-container">

        <!-- <div class="action-item">
          <button class="tag-manager-btn" @click="toggleLabelManager" :title="t(isLabelManagerVisible ? 'controls.hideSidebar' : 'controls.showSidebar')">
            <svg class="sidebar-toggle-icon" :class="{ 'is-closed': !isLabelManagerVisible }" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24">
              <path fill="currentColor" d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
            </svg>
            <span class="action-text">{{ t('controls.sidebar') }}</span>
          </button>
        </div> -->
        <div class="action-item">
          <button 
            class="tag-manager-btn" 
            @click="toggleLabelManager" 
            :title="isLabelManagerVisible ? '收起标签栏' : '展开标签栏'">
            
            <svg 
              class="sidebar-toggle-icon" 
              :class="{ 'is-closed': !isLabelManagerVisible }" 
              xmlns="http://www.w3.org/2000/svg" 
              viewBox="0 0 24 24" 
              width="24" height="24">
              <path fill="currentColor" d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12z"/>
            </svg>
            
            <span class="action-text">
              {{ isLabelManagerVisible ? '收起标签栏' : '展开标签栏' }}
            </span>
          </button>
        </div>
        <div class="action-item">
          <button class="language-switch-btn" @click.stop="toggleLanguageSelector" ref="langBtnRef"
            :title="t('controls.language')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="translate-icon">
              <path
                d="M12.87 15.07l-2.54-2.51.03-.03c1.74-1.94 2.98-4.17 3.71-6.53H17V4h-7V2H8v2H1v1.99h11.17C11.5 7.92 10.44 9.75 9 11.35 8.07 10.32 7.3 9.19 6.69 8h-2c.73 1.63 1.73 3.17 2.98 4.56l-5.09 5.02L4 19l5-5 3.11 3.11.76-2.04zM18.5 10h-2L12 22h2l1.12-3h4.75L21 22h2l-4.5-12zm-2.62 7l1.62-4.33L19.12 17h-3.24z" />
            </svg>
            <span class="action-text">{{ t('controls.language') }}</span>
          </button>
          <Transition name="fade">
            <LanguageSwitcher v-if="showLanguageSelector" ref="languageSwitcherRef" @close="closeLanguageSelector" />
          </Transition>
        </div>

        <div class="action-item">
          <ThemeSwitch :title="t('controls.switchTheme')">
            <template #default="{ isDark }">
              <span class="action-text">{{ t(isDark ? 'controls.darkMode' : 'controls.lightMode') }}</span>
            </template>
          </ThemeSwitch>
        </div>

        <div class="action-item">
          <button class="settings-btn" @click="openSettings" :title="t('controls.settings')">
            <svg class="settings-icon" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M19.14 12.94c.04-.3.06-.61.06-.94 0-.32-.02-.64-.07-.94l2.03-1.58c.18-.14.23-.41.12-.61l-1.92-3.32c-.12-.22-.37-.29-.59-.22l-2.39.96c-.5-.38-1.03-.7-1.62-.94l-.36-2.54c-.04-.24-.24-.41-.48-.41h-3.84c-.24 0-.43.17-.47.41l-.36 2.54c-.59.24-1.13.57-1.62.94l-2.39-.96c-.22-.08-.47 0-.59.22L2.74 8.87c-.12.21-.08.47.12.61l2.03 1.58c-.05.3-.07.62-.07.94s.02.64.07.94l-2.03 1.58c-.18.14-.23.41-.12.61l1.92 3.32c.12.22.37.29.59.22l2.39-.96c.5.38 1.03.7 1.62.94l.36 2.54c.05.24.24.41.48.41h3.84c.24 0 .44-.17.47-.41l.36-2.54c.59-.24 1.13-.56 1.62-.94l2.39.96c.22.08.47 0 .59-.22l1.92-3.32c.12-.22.07-.47-.12-.61l-2.01-1.58zM12 15.6c-1.98 0-3.6-1.62-3.6-3.6s1.62-3.6 3.6-3.6 3.6 1.62 3.6 3.6-1.62 3.6-3.6 3.6z" />
            </svg>
            <span class="action-text">{{ t('controls.settings') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openTagManager" :title="t('controls.tagManager')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="tag-icon">
              <path
                d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z" />
            </svg>
            <span class="action-text">{{ t('controls.tagManager') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openDanbooruManager" :title="t('controls.danbooruManager')">
            <svg class="tag-icon" viewBox="0 0 24 24" width="24" height="24" xmlns="http://www.w3.org/2000/svg">
              <path
                d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z" />
            </svg>
            <span class="action-text">{{ t('controls.danbooruManager') }}</span>
          </button>
        </div>

        <div class="action-item" v-if="props.hasPromptLoraStack">
          <button class="tag-manager-btn" @click="toggleLora" :title="t('controls.loraStack')">
            <svg sxmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" class="tag-icon" width="24" height="24">
              <path
                d="M902.5 485.1c-59-17.5-113.8-3.4-155 27.7V365.1c0-45.2-36.9-82.1-82.1-82.1H511.2c31.1-41.2 45.2-96 27.7-155C522.2 71.6 475 26.1 418 12 303.4-16.5 200.9 69.4 200.9 179.3c0 39.1 13.5 74.7 35.3 103.7H82.1C36.9 283 0 319.9 0 365.1v113.1c0 25.5 27.9 38.8 49.5 25.3 38.8-24.3 87.8-33.6 139.4-19.5 57 15.6 103.4 62.5 118.4 119.7 30.1 115.5-56.2 219.4-166.8 219.4-33.5 0-64.7-9.6-91.1-26.2C27.8 783.4 0 796.8 0 822.2v113.2c0 45.2 36.9 82.1 82.1 82.1h583.3c45.2 0 82.1-36.9 82.1-82.1V787.7c29 21.9 64.6 35.3 103.7 35.3 109.9 0 195.8-102.5 167.3-217.1-14.1-56.9-59.7-104.1-116-120.8z">
              </path>
            </svg>
            <span class="action-text">{{ t('controls.loraStack') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openLoraManager" :title="t('controls.loraManager')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" class="tag-icon" width="24" height="24">
              <path
                d="M129 128h350v80H209v224h270v80H129V128zM129 895V576h768v319H129z m80-239v159h608V656H209zM730 356c19.882 0 36-16.118 36-36s-16.118-36-36-36-36 16.118-36 36 16.118 36 36 36z">
              </path>
              <path
                d="M578.517 214.386a32.002 32.002 0 0 0-16.01 27.731l0.058 155.918a31.998 31.998 0 0 0 16 27.701l135.156 78.033a32.002 32.002 0 0 0 31.99 0.006l135.058-77.909a32.002 32.002 0 0 0 16.01-27.731l-0.058-155.918a32 32 0 0 0-16-27.701l-135.157-78.033a31.998 31.998 0 0 0-31.989-0.005l-135.058 77.908z m67.002 58.058l84.033-48.591 84.181 48.715 0.034 95.24-84.034 48.591-84.18-48.714-0.034-95.241z">
              </path>
            </svg>
            <span class="action-text">{{ t('controls.loraManager') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openHistoryBox" :title="t('controls.history')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" class="tag-icon" width="24" height="24">
              <path
                d="M653.7 85.83c-235.05 0-426.29 191.25-426.29 426.3s191.24 426.3 426.29 426.3c235.06 0 426.3-191.25 426.3-426.3S888.76 85.83 653.7 85.83z m0 779.98c-195.01 0-353.67-158.65-353.67-353.68S458.69 158.45 653.7 158.45c195.02 0 353.68 158.65 353.68 353.68S848.72 865.81 653.7 865.81z">
              </path>
              <path
                d="M866.78 634.19L695.93 533.61V302.59c0-20.06-16.26-36.31-36.31-36.31s-36.31 16.26-36.31 36.31v253.66c0 17.06 11.8 31.26 27.66 35.16l178.98 105.36c17.28 10.17 39.54 4.41 49.71-12.87 10.17-17.28 4.4-39.54-12.88-49.71zM44.76 324.51h186.42c20.05 0 36.31-16.26 36.31-36.31s-16.26-36.31-36.31-36.31H44.76c-20.05 0-36.31 16.26-36.31 36.31s16.26 36.31 36.31 36.31zM231.18 703.25H44.76c-20.05 0-36.31 16.26-36.31 36.31s16.26 36.31 36.31 36.31h186.42c20.05 0 36.31-16.26 36.31-36.31s-16.25-36.31-36.31-36.31zM36.31 550.19h118.8c20.05 0 36.31-16.26 36.31-36.31s-16.26-36.31-36.31-36.31H36.31c-20.05 0-36.31 16.26-36.31 36.31 0 20.06 16.26 36.31 36.31 36.31z">
              </path>
            </svg>
            <span class="action-text">{{ t('controls.history') }}</span>
          </button>
        </div>

        <!-- 新增 AI 对话按钮 -->
        <div class="action-item">
          <button class="tag-manager-btn" @click="openAIChat" :title="t('controls.aiChat')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="tag-icon" width="24" height="24">
              <path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z" />
              <path d="M6 14h12v2H6zm0-3h12v2H6zm0-3h12v2H6z" />
            </svg>
            <span class="action-text">{{ t('controls.aiChat') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openGitHub" :title="t('controls.github')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="tag-icon" width="24" height="24">
              <path
                d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z" />
            </svg>
            <span class="action-text">{{ t('controls.github') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="shareCloudData" :title="t('controls.shareCloudData')">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" class="tag-icon" width="24" height="24">
              <path
                d="M19.35 10.04C18.67 6.59 15.64 4 12 4 9.11 4 6.6 5.64 5.35 8.04 2.34 8.36 0 10.91 0 14c0 3.31 2.69 6 6 6h13c2.76 0 5-2.24 5-5 0-2.64-2.05-4.78-4.65-4.96zM14 13v4h-4v-4H7l5-5 5 5h-3z" />
            </svg>
            <span class="action-text">{{ t('controls.shareCloudData') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openBilibili" :title="t('controls.tutorialVideo')">
            <svg t="1745234292993" class="tag-icon" viewBox="0 0 1024 1024" version="1.1"
              xmlns="http://www.w3.org/2000/svg" p-id="1496" width="128" height="128">
              <path
                d="M204.288 63.488c-8.704 8.192-16.896 20.48-18.944 26.624-3.584 11.776 12.8 62.464 20.48 62.464S235.52 176.128 235.52 184.32c0 16.384-17.92 26.112-47.104 26.112-34.816 0-104.448 27.648-128.512 51.2-9.216 8.704-26.112 33.792-37.888 56.32L0 358.4v469.504l21.504 40.448c24.576 47.616 35.84 59.392 82.944 84.992l40.96 22.528h722.944l40.96-19.968c51.712-24.576 72.704-45.056 95.744-94.72l17.92-38.4v-231.424l0.512-231.424-17.92-36.352c-9.216-20.48-28.16-47.104-42.496-59.904-31.232-30.208-86.528-54.272-122.368-54.272-54.272 0-65.024-22.528-26.624-57.856 20.48-18.432 23.04-25.088 23.04-45.568 0-19.968-3.584-28.16-16.896-41.984-9.216-9.216-22.528-16.896-29.696-16.896-11.776 0-34.304 9.216-40.448 16.896-1.536 1.536-35.84 35.328-75.776 74.24l-73.216 71.168-83.456-0.512c-45.568 0-88.064-2.56-93.696-4.608-5.632-2.56-38.4-31.232-72.704-65.024C249.856 40.448 235.008 32.256 204.288 63.488z m652.8 262.656c5.12 0.512 19.968 9.216 31.744 20.48l21.504 19.968 1.536 217.088c1.024 197.12 0.512 218.112-8.704 236.032-14.336 27.136-34.816 40.448-65.536 41.984-14.336 0.512-173.568 0.512-353.28 0l-326.144-1.536-45.056-45.056V373.248l20.992-22.528c15.872-17.92 25.6-23.552 41.984-25.088 16.384-1.024 634.88-0.512 680.96 0.512z"
                p-id="1497"></path>
              <path
                d="M279.04 502.272c-20.48 22.016-20.992 25.088-20.992 66.56 0 39.936 1.024 44.544 17.92 64 29.184 33.28 55.808 32.256 84.48-2.56 11.264-12.8 12.8-22.016 13.312-64 0-47.104-0.512-48.64-19.968-68.096-27.136-27.648-47.616-26.112-74.752 4.096z m393.216-3.584c-18.944 18.944-19.968 20.992-19.968 69.12 0 47.616 0.512 49.664 18.432 67.072 24.576 23.552 35.84 26.624 58.368 13.824 29.184-16.896 39.936-43.52 36.864-90.624-2.56-35.328-4.608-41.984-22.016-59.904-25.088-25.6-45.568-25.6-71.68 0.512z"
                p-id="1498"></path>
            </svg>
            <span class="action-text">{{ t('controls.tutorialVideo') }}</span>
          </button>
        </div>

        <div class="action-item">
          <button class="tag-manager-btn" @click="openSponsor" :title="t('controls.sponsor')">
            <svg t="1745823985128" class="tag-icon" viewBox="0 0 1322 1024" version="1.1"
              xmlns="http://www.w3.org/2000/svg" width="24" height="24">
              <path
                d="M495.899049 634.906371c-17.304811 0-31.251971 13.947161-31.251971 31.251971S478.594238 697.410314 495.899049 697.410314c17.304811 0 31.251971-13.947161 31.251971-31.251972 0-17.304811-13.947161-31.251971-31.251971-31.251971zM790.855671 728.662285c-17.304811 0-31.251971 13.947161-31.251972 31.251971s13.947161 31.251971 31.251972 31.251972 31.251971-13.947161 31.251971-31.251972c0-17.04653-13.947161-30.993691-31.251971-31.251971z">
              </path>
              <path
                d="M1262.99289 719.622459c-13.430599-8.264984-28.927445-13.430599-44.68257-14.980284 34.867902-84.974368 57.080047-196.293374-18.596215-306.837537-115.193217-168.657333-280.75118-256.73107-491.766556-260.863562-60.179416-1.291404-130.948343 1.549685-205.849762 4.649054-87.040614 3.35765-203.008673 8.006703-281.526023 1.549684 15.755126-8.523265 32.543375-16.788249 47.007098-23.761829 55.530362-27.119479 98.921529-48.04022 84.457807-85.232649-7.748423-21.695583-30.218848-33.059937-67.411277-34.09306C206.624604-1.755689 37.967271 43.443443 7.748423 119.636265c-17.04653 42.874605-19.887618 125.524447 152.902206 198.876182 71.027208 30.218848 271.969635 66.894715 349.453861 74.643138 17.563091 1.549685 34.867902 5.165615 51.397871 11.364353-17.821372 11.622634-35.901025 24.02011-54.238959 36.417586-31.768533-18.079653-83.941245-39.516955-122.683358-13.172318-14.463722 9.298107-23.503549 25.053233-24.02011 42.358044-0.516562 21.179022 12.397476 42.099763 26.861198 58.629731-57.080047 45.715694-103.312302 89.881703-119.84227 123.974762-18.337934 41.841482-25.828075 110.544163 8.523265 177.438879 43.391167 84.974368 138.955046 144.120661 284.625391 176.147474 190.352916 41.583202 354.619476 4.132492 463.355674-53.205835 60.437697-32.026814 103.570583-69.994085 124.233043-103.828864 6.457019 2.066246 12.914038 4.132492 19.629338 6.198738 9.298107 2.841088 18.596214 5.682177 27.37776 8.781546 28.669164 10.072949 60.695977 8.523265 85.232649-3.61593l1.291403-0.774843c17.821372-9.039826 31.510252-25.053233 37.708991-44.166009 15.238565-51.139589-29.444006-79.033911-56.563486-96.08044z m-811.776412-239.684541l-17.30481 12.655757c-5.165615-5.165615-9.814669-11.106072-13.430599-17.563091 6.7153-2.066246 18.337934 0.258281 30.735409 4.907334zM1262.99289 798.139808c-1.291404 3.874211-4.132492 6.97358-9.298107 9.814669-10.33123 5.165615-25.569795 5.423896-39.258675 0.774842-9.298107-3.35765-19.371057-6.457019-29.444006-9.556388-18.596214-5.682177-49.848186-15.238565-55.788643-22.470426-9.814669-12.914038-28.152602-15.755126-41.32492-5.940457s-15.755126 28.152602-5.940458 41.324921c3.615931 4.390773 7.490142 8.264984 12.139196 11.622634-44.940851 62.245662-242.267348 186.220424-521.468844 125.007885-125.782728-27.636041-210.498815-77.742507-244.850155-145.412065-24.794952-48.815063-19.112776-98.921529-7.231861-126.299289 34.09306-71.027208 280.75118-234.518925 438.30244-327.241716 13.947161-8.264984 18.596214-26.344637 10.33123-40.291798s-27.119479-19.629337-40.291797-10.33123c-12.655757 7.490142-55.788643 33.059937-111.060725 68.186119-18.596214-12.655757-50.881309-27.894322-102.537459-33.059936-81.874999-8.264984-270.936512-44.42429-332.149051-70.252366C139.471608 245.418993 40.033517 196.34565 61.987381 141.073568c5.165615-12.914038 29.185725-33.576498 81.100157-53.464116 35.384463-13.430599 72.318611-22.470426 109.769321-27.119479l-11.622634 5.682176c-35.384463 17.304811-73.868296 36.417586-99.954652 59.146293-1.807965-1.033123-3.615931-2.324527-5.165615-3.874211-10.847792-11.622634-29.185725-12.397476-41.06664-1.291404l-0.516562 0.516561c-11.880915 11.106072-12.139195 29.702287-1.033123 41.583202 10.589511 11.106072 26.086356 19.371057 45.715694 25.569795 0.774842 0.258281 1.291404 0.516562 2.066246 0.774842 68.702681 21.179022 190.611197 18.596214 362.367899 11.622634 74.126577-2.841088 144.120661-5.682177 202.492111-4.649054 193.710566 3.874211 339.122631 80.841876 444.75946 235.552049 64.828469 95.047318 41.583202 188.544951 4.390773 269.903388-4.649054-3.615931-9.039826-7.748423-12.655757-12.139195-10.33123-12.397476-28.669164-14.463722-41.324921-4.649054-12.655757 10.072949-14.722003 28.669164-4.649054 41.324921 5.940457 7.490142 36.675867 42.874605 74.643138 39.775236h2.066246c1.291404-0.258281 2.324527 0 3.615931-0.258281 25.828075-4.649054 42.358044-3.615931 57.596608 6.198738 20.40418 12.914038 30.218848 20.40418 28.410883 26.861199z">
              </path>
            </svg>
            <span class="action-text">{{ t('controls.sponsor') }}</span>
          </button>
        </div>



        <SettingDialog ref="settingDialog" />

      </div>

      <div style="position: relative;" ref="parentCneterBox">
        <!-- 输入框区域 -->
        <!-- 移除事件 @change="finishPromptPutItHistory" -->
        <textarea v-model="inputText" class="input-area" @input="handleInput" :placeholder="t('promptBox.placeholder')"
          @keydown="handleKeydown" @blur="onBlur" rows="6" ref="inputAreaRef" @mouseup="saveTextareaHeight"
          @resize="saveTextareaHeight"></textarea>

        <!-- 添加token计数器 -->
        <div class="update-label-bar">
          <div class="token-counter">{{ tokenCount }} tokens</div>
          <button :class="['update-label-btn', { 'is-dirty': unsavedChanges }]" :disabled="!selectedMainLabelId || !unsavedChanges" @click="updateSelectedLabel">
            更新标签
          </button>
        </div>

        <!-- 自动补全窗口 -->
        <div class="autocomplete-container" ref="autocompleteContainerRef" :style="{
          top: `${autocompletePosition.top}px`,
          left: `${adjustedAutocompletePosition.left}px`,
          display: showAutocomplete ? 'block' : 'none',
          width: `${saveAutoCompleteWidth}px`,
          maxHeight: `${saveAutoCompleteHeight}px`
        }">
          <button class="close-autocomplete-btn" @click.stop="closeAutocomplete">×</button>
          <div v-for="(item, index) in autocompleteResults" :key="index" class="autocomplete-item"
            :class="{ selected: index === selectedAutocompleteIndex }" @click.stop="selectAutocomplete(index, $event)"
            :ref="el => { if (el && index === selectedAutocompleteIndex) selectedItemRef = el }">
            <span class="tag">{{ item.text }}</span>
            <span class="desc">{{ item.desc }}</span>
          </div>
        </div>

      </div>

      <!--  中间小工具栏  -->
      <div class="prompt-input-translate-area">

        <!-- 添加翻译输入框 -->
        <input type="text" v-model="translateText" class="prompt-input-translate-area-textarea"
          @keyup.enter="finishTranslateEnter()" :placeholder="t('promptBox.translatePlaceholder')" />

        <!-- 添加翻译按钮 -->
        <button class="translate-btn" @click="oneClickTranslatePrompt" :title="t('promptBox.oneClickTranslate')">
          <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" class="token-item-icon" width="24"
            height="24">
            <path
              d="M677.676657 294.6142c19.165116 57.5433 44.715939 102.2992 89.431879 147.0551 38.322239-38.3622 63.873063-89.5118 83.038178-147.0551h-172.470057z m-421.56861 319.685h166.076358l-83.038179-223.7795-83.038179 223.7795z"
              p-id="2419"></path>
            <path
              d="M894.854661 0.504H128.353929C58.095158 0.504 0.607803 58.0473 0.607803 128.378v767.244c0 70.3307 57.487355 127.874 127.746126 127.874h766.500733c70.258771 0 127.746126-57.5433 127.746126-127.874V128.378c0-70.3307-51.101647-127.874-127.746126-127.874zM581.867062 825.2913c-12.771416 12.7874-25.550824 12.7874-38.322239 12.7874-6.3937 0-19.165116 0-25.550824-6.3937-6.3937-6.3937-12.779408 0-12.779408-6.3937s-6.385708-12.7874-12.771415-25.5748c-6.3937-12.7874-6.3937-19.1811-12.779408-31.9685l-25.542832-70.3307H230.557224L205.0064 767.748c-12.771416 25.5748-19.165116 44.7559-25.550824 57.5433-6.3937 12.7874-19.165116 12.7874-38.322239 12.7874-12.779408 0-25.550824-6.3937-38.330231-12.7874-12.771416-12.7874-19.157124-19.1811-19.157124-31.9685 0-6.3937 0-12.7874 6.385708-25.5748 6.3937-12.7874 6.3937-19.1811 12.771416-31.9685l140.525533-358.0472c6.3937-12.7874 6.3937-25.5748 12.779408-38.3622 6.385708-12.7874 12.771416-25.5748 19.157124-31.9685 6.3937-6.3937 12.779408-19.1811 25.550823-25.5748 12.779408-6.3937 25.550824-6.3937 38.330232-6.3937 12.771416 0 25.542832 0 38.322239 6.3937 12.771416 6.3937 19.165116 12.7874 25.550824 25.5748 6.385708 6.3937 12.771416 19.1811 19.157124 31.9685 6.3937 12.7874 12.779408 25.5748 19.165115 44.7559l140.525534 351.6535c12.771416 25.5748 19.165116 44.7559 19.165116 57.5433-6.3937 6.3937-12.779408 19.1811-19.165116 31.9685zM933.176901 575.937c-70.258771-25.5748-121.360418-57.5433-166.076358-95.9055-44.707947 44.7559-102.195302 76.7244-172.462065 95.9055l-19.157124-31.9685c70.258771-19.1811 127.746126-44.7559 172.462066-89.5118C703.22748 409.7008 664.905241 352.1575 652.125833 288.2205h-63.873063v-25.5748h172.470058c-12.7874-19.1811-25.558816-44.7559-38.330232-63.937l19.157124-6.3937c12.779408 19.1811 31.944524 44.7559 44.715939 70.3307h159.682658v31.9685h-63.873063c-19.157124 63.937-51.093655 121.4803-89.423887 159.8425 44.715939 38.3622 95.809594 70.3307 166.076358 89.5118l-25.550824 31.9685z"
              p-id="2420"></path>
          </svg>
          <span style="margin-left: 5px;" class="action-text">{{ t('promptBox.oneClickTranslate') }}</span>
        </button>

        <!-- 添加设置随机Tag规则按钮 -->
        <button class="translate-btn random-tag-settings-btn" @click="openRandomTagSettings"
          :title="t('promptBox.randomTagSettings')">
          <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" class="utils-item-icon" width="24"
            height="24">
            <path
              d="M512 409.6c-56.32 0-102.4 46.08-102.4 102.4s46.08 102.4 102.4 102.4 102.4-46.08 102.4-102.4-46.08-102.4-102.4-102.4z m0 153.6c-28.16 0-51.2-23.04-51.2-51.2s23.04-51.2 51.2-51.2 51.2 23.04 51.2 51.2-23.04 51.2-51.2 51.2z">
            </path>
            <path
              d="M512 204.8c-25.6 0-51.2 2.56-76.8 7.68l-15.36-61.44c-2.56-10.24-10.24-17.92-20.48-20.48-10.24-2.56-20.48 0-28.16 7.68l-76.8 76.8c-5.12 5.12-7.68 12.8-7.68 20.48s2.56 15.36 7.68 20.48l76.8 76.8c5.12 5.12 12.8 7.68 20.48 7.68 2.56 0 5.12 0 7.68-2.56 10.24-2.56 17.92-10.24 20.48-20.48l15.36-61.44c25.6-5.12 51.2-7.68 76.8-7.68 140.8 0 256 115.2 256 256s-115.2 256-256 256-256-115.2-256-256c0-25.6 2.56-51.2 7.68-76.8l61.44-15.36c10.24-2.56 17.92-10.24 20.48-20.48 2.56-10.24 0-20.48-7.68-28.16l-76.8-76.8c-5.12-5.12-12.8-7.68-20.48-7.68s-15.36 2.56-20.48 7.68l-76.8 76.8c-7.68 7.68-10.24 17.92-7.68 28.16 2.56 10.24 10.24 17.92 20.48 20.48l61.44 15.36c-5.12 25.6-7.68 51.2-7.68 76.8 0 168.96 138.24 307.2 307.2 307.2s307.2-138.24 307.2-307.2-138.24-307.2-307.2-307.2z">
            </path>
          </svg>
          <span class="action-text">{{ t('promptBox.randomTagSettings') }}</span>
        </button>

        <!-- 添加一键随机Tag按钮 -->
        <button class="translate-btn random-tag-btn" @click="oneClickRandomTag"
          :title="t('promptBox.oneClickRandomTag')">
          <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" class="utils-item-icon" width="24"
            height="24">
            <path
              d="M832 512c0-176-144-320-320-320S192 336 192 512s144 320 320 320 320-144 320-320z m-384 0c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m128-128c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m-256 0c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m128-128c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m256 256c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m-256 0c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m-128 128c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z m256 0c0-35.2 28.8-64 64-64s64 28.8 64 64-28.8 64-64 64-64-28.8-64-64z">
            </path>
          </svg>
          <span class="action-text">{{ t('promptBox.oneClickRandomTag') }}</span>
        </button>

      </div>

      <!-- 词组显示区域 -->
      <div class="tokens-container" v-if="tokens.length > 0">
        <template v-for="(token, index) in tokens" :key="'tag-item-'+index">
          <div class="token-item-box" :draggable="!token.isEditing" @dragstart="handleDragStart(index, $event)"
            @dragover.prevent="handleDragOver(index, $event)" @drop="handleDrop(index, $event)"
            @dblclick="toggleHidden(index)" :style="{ backgroundColor: token.color }">

            <!-- 换行标记 -->
            <div v-if="token.text === '\n'" class="newline-token">
              <span class="token-symbol" :title="t('promptBox.newline')">↵</span>
            </div>

            <!-- Tab标记 -->
            <div v-else-if="token.text === '\t'" class="token-item tab-token" @mouseenter="showControls(index, $event)"
              @mouseleave="handleMouseLeave(index)">
              <span class="token-symbol" :title="t('promptBox.tab')">→</span>
            </div>

            <!-- 为Lora标签添加特殊图标 -->
            <div v-else-if="token.isLoraTag" class="lora-tag-icon" :title="t('promptBox.loraTag')"
              @mouseenter="showControls(index, $event)" @mouseleave="handleMouseLeave(index)">
              <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="15" height="15">
                <path
                  d="M20.5 11H19V7c0-1.1-.9-2-2-2h-4V3.5C13 2.12 11.88 1 10.5 1S8 2.12 8 3.5V5H4c-1.1 0-1.99.9-1.99 2v3.8H3.5c1.49 0 2.7 1.21 2.7 2.7s-1.21 2.7-2.7 2.7H2V20c0 1.1.9 2 2 2h3.8v-1.5c0-1.49 1.21-2.7 2.7-2.7 1.49 0 2.7 1.21 2.7 2.7V22H17c1.1 0 2-.9 2-2v-4h1.5c1.38 0 2.5-1.12 2.5-2.5S21.88 11 20.5 11z" />
              </svg>
              <span style="margin-left: 5px;">{{ token.text }}</span>
            </div>

            <!-- 普通词组 -->
            <div v-else-if="token.text && !token.isLoraTag" class="token-item" @mouseenter="showControls(index, $event)"
              @mouseleave="handleMouseLeave(index)" :class="{
                'punctuation': token.isPunctuation
              }">
              <span v-if="!token.isEditing || token.isPunctuation"
                @click="!token.isPunctuation && startEditing(index)">{{
                  token.text }}</span>
              <input v-else-if="!token.isPunctuation" :value="token.text" @input="handleTokenEdit(index, $event)"
                @blur="finishEditing(index)" @keyup.enter="finishEditing(index)"
                :ref="el => { if (el) tokenInputRefs[index] = el }">
            </div>



            <!-- 翻译结果显示 -->
            <div class="translation-result" v-if="token.text !== '\n' && token.text !== '\t' && !token.isLoraTag">
              <div v-if="isTextTranslatable(token.text)" @click="translateFunction(token.text, token)"
                class="translate-button" :title="t('promptBox.translate')">
                <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg" class="token-item-icon" width="24"
                  height="24">
                  <path
                    d="M677.676657 294.6142c19.165116 57.5433 44.715939 102.2992 89.431879 147.0551 38.322239-38.3622 63.873063-89.5118 83.038178-147.0551h-172.470057z m-421.56861 319.685h166.076358l-83.038179-223.7795-83.038179 223.7795z"
                    p-id="2419"></path>
                  <path
                    d="M894.854661 0.504H128.353929C58.095158 0.504 0.607803 58.0473 0.607803 128.378v767.244c0 70.3307 57.487355 127.874 127.746126 127.874h766.500733c70.258771 0 127.746126-57.5433 127.746126-127.874V128.378c0-70.3307-51.101647-127.874-127.746126-127.874zM581.867062 825.2913c-12.771416 12.7874-25.550824 12.7874-38.322239 12.7874-6.3937 0-19.165116 0-25.550824-6.3937-6.3937-6.3937-12.779408 0-12.779408-6.3937s-6.385708-12.7874-12.771415-25.5748c-6.3937-12.7874-6.3937-19.1811-12.779408-31.9685l-25.542832-70.3307H230.557224L205.0064 767.748c-12.771416 25.5748-19.165116 44.7559-25.550824 57.5433-6.3937 12.7874-19.165116 12.7874-38.322239 12.7874-12.779408 0-25.550824-6.3937-38.330231-12.7874-12.771416-12.7874-19.157124-19.1811-19.157124-31.9685 0-6.3937 0-12.7874 6.385708-25.5748 6.3937-12.7874 6.3937-19.1811 12.771416-31.9685l140.525533-358.0472c6.3937-12.7874 6.3937-25.5748 12.779408-38.3622 6.385708-12.7874 12.771416-25.5748 19.157124-31.9685 6.3937-6.3937 12.779408-19.1811 25.550823-25.5748 12.779408-6.3937 25.550824-6.3937 38.330232-6.3937 12.771416 0 25.542832 0 38.322239 6.3937 12.771416 6.3937 19.165116 12.7874 25.550824 25.5748 6.385708 6.3937 12.771416 19.1811 19.157124 31.9685 6.3937 12.7874 12.779408 25.5748 19.165115 44.7559l140.525534 351.6535c12.771416 25.5748 19.165116 44.7559 19.165116 57.5433-6.3937 6.3937-12.779408 19.1811-19.165116 31.9685zM933.176901 575.937c-70.258771-25.5748-121.360418-57.5433-166.076358-95.9055-44.707947 44.7559-102.195302 76.7244-172.462065 95.9055l-19.157124-31.9685c70.258771-19.1811 127.746126-44.7559 172.462066-89.5118C703.22748 409.7008 664.905241 352.1575 652.125833 288.2205h-63.873063v-25.5748h172.470058c-12.7874-19.1811-25.558816-44.7559-38.330232-63.937l19.157124-6.3937c12.779408 19.1811 31.944524 44.7559 44.715939 70.3307h159.682658v31.9685h-63.873063c-19.157124 63.937-51.093655 121.4803-89.423887 159.8425 44.715939 38.3622 95.809594 70.3307 166.076358 89.5118l-25.550824 31.9685z"
                    p-id="2420"></path>
                </svg>
              </div>
              <span class="translated-text">{{ token.translate ? token.translate : '' }}</span>
            </div>
          </div>

          <!-- 在显示token的地方添加 -->
          <span v-if="token.isHidden" class="hidden-hint" :title="token.hiddenHint">
            <!-- 这里可以添加一个视觉提示图标 -->
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
          </span>

          <!-- 如果是 换行，插入换行占位元素 -->
          <div v-if="token.text === '\n'" class="line-break"></div>
        </template>

      </div>

      <!-- 添加悬浮提示框 -->
      <div v-if="showTagTipsBox" class="tag-tips-box" :style="tagTipsPosition">
        <div class="tag-tips-content">
          <p v-html="t('promptBox.tagTips')"></p>
        </div>
      </div>

      <!-- 控制栏容器 -->
      <div v-show="activeControls !== null && tokens[activeControls]" class="token-controls" :style="controlsPosition"
        @mouseenter="isOverControls = true" @mouseleave="handleControlsLeave">

        <!-- 普通Tag 添加权重输入框 -->
        <div class="weight-control" v-if="!tokens[activeControls]?.isLoraTag">
          <input type="number" v-model="weightValue" step="0.1" class="weight-input" @change="applyWeight">
          <span class="weight-label">{{ t('promptBox.weight') }}</span>
        </div>

        <!-- Lora标签的权重控制 -->
        <div class="lora-weight-controls" v-if="tokens[activeControls]?.isLoraTag">
          <div class="weight-control">
            <input type="number" v-model="loraModelWeight" step="0.1" class="weight-input" @change="applyLoraWeights">
            <span class="weight-label">{{ t('promptBox.modelWeight') }}</span>
          </div>
          <div class="weight-control">
            <input type="number" v-model="loraTextWeight" step="0.1" class="weight-input" @change="applyLoraWeights">
            <span class="weight-label">{{ t('promptBox.textWeight') }}</span>
          </div>
        </div>

        <button @click="handleDelete" class="delete-btn" :title="t('promptBox.delete')">
          <svg viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z" />
          </svg>
        </button>

        <div class="bracket-btn-group" v-if="!tokens[activeControls]?.isLoraTag">
          <div class="bracket-btn-container">
            <!-- 括号按钮 -->
            <div class="bracket-btn">
              ()
            </div>
            <!-- 加减号按钮组 -->
            <div class="vertical-btn-group">
              <button class="vertical-btn" @click="wrapWith('(')" :title="t('promptBox.addBracket')">
                +
              </button>
              <button class="vertical-btn" @click="removeLayer('(')" :title="t('promptBox.removeLayer')">
                -
              </button>
            </div>
          </div>

          <div class="bracket-btn-container">
            <div class="bracket-btn">
              []
            </div>
            <div class="vertical-btn-group">
              <button class="vertical-btn" @click="wrapWith('[')" :title="t('promptBox.addBracket')">
                +
              </button>
              <button class="vertical-btn" @click="removeLayer('[')" :title="t('promptBox.removeLayer')">
                -
              </button>
            </div>
          </div>

          <div class="bracket-btn-container">
            <div class="bracket-btn">
              {}
            </div>
            <div class="vertical-btn-group">
              <button class="vertical-btn" @click="wrapWith('{')" :title="t('promptBox.addBracket')">
                +
              </button>
              <button class="vertical-btn" @click="removeLayer('{')" :title="t('promptBox.removeLayer')">
                -
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Lora管理器容器 -->
      <div class="tag-manager-section">
        <div class="tag-manager-header" @click="toggleLoraManager">
          <div class="header-left">
            <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1024 1024" class="tag-icon" width="24" height="24">
              <path
                d="M129 128h350v80H209v224h270v80H129V128zM129 895V576h768v319H129z m80-239v159h608V656H209zM730 356c19.882 0 36-16.118 36-36s-16.118-36-36-36-36 16.118-36 36 16.118 36 36 36z">
              </path>
              <path
                d="M578.517 214.386a32.002 32.002 0 0 0-16.01 27.731l0.058 155.918a31.998 31.998 0 0 0 16 27.701l135.156 78.033a32.002 32.002 0 0 0 31.99 0.006l135.058-77.909a32.002 32.002 0 0 0 16.01-27.731l-0.058-155.918a32 32 0 0 0-16-27.701l-135.157-78.033a31.998 31.998 0 0 0-31.989-0.005l-135.058 77.908z m67.002 58.058l84.033-48.591 84.181 48.715 0.034 95.24-84.034 48.591-84.18-48.714-0.034-95.241z">
              </path>
            </svg>
            <span class="section-title">{{ t('controls.loraManager') }}</span>
          </div>
          <div class="header-right">
            <svg class="collapse-icon" :class="{ 'is-collapsed': !showLoraManager }" viewBox="0 0 24 24">
              <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z" />
            </svg>
          </div>
        </div>
        <div class="lora-manager-container" v-show="showLoraManager">
          <LoraManager :loraManager="'prompt_inner'" />
        </div>
      </div>

      <!-- 标签管理器容器 -->
      <div class="tag-manager-section">
        <div class="tag-manager-header" @click="toggleTagManager">
          <div class="header-left">
            <svg class="tag-icon" viewBox="0 0 24 24">
              <path
                d="M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z" />
            </svg>
            <span class="section-title">{{ t('controls.tagManager') }}</span>
          </div>
          <div class="header-right">
            <svg class="collapse-icon" :class="{ 'is-collapsed': !showTagManager }" viewBox="0 0 24 24">
              <path d="M7.41 15.41L12 10.83l4.59 4.58L18 14l-6-6-6 6z" />
            </svg>
          </div>
        </div>
        <div class="tag-manager-container" v-show="showTagManager">
          <TagManager />
        </div>
      </div>

    </div>
  </div>

  <RandomSetting ref="randomSettingItem" />
</template>

<script setup>
import { ref, watch, onBeforeUpdate, onMounted, onUnmounted, onBeforeUnmount, nextTick, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import LanguageSwitcher from '@/components/LanguageSwitcher.vue'
import SettingDialog from './components/setting_dialog.vue'
import ThemeSwitch from '@/components/ThemeSwitch.vue'
import TagManager from '@/view/tag_manager/tag_index.vue'  // 导入 TagManager 组件
import LoraStack from './components/lora_stack.vue'
import MainLabelManager from './components/main_label_manager.vue'
import translate from 'i18n-jsautotranslate'
import { translatorApi } from '@/api/translator'
import { historyApi } from '@/api/history'
import message from '@/utils/message'
import { autocompleteApi } from '@/api/autocomplete'
import LoraManager from "@/view/lora_manager/lora_index.vue"
import RandomSetting from './components/random_setting.vue'
import { randomTagApi } from '@/api/random_tag'
import pako from 'pako'

const randomSettingItem = ref(null)

const prefix = "weilin_prompt_ui_"
const { t } = useI18n()

const autocompleteContainerRef = ref()
const inputAreaRef = ref()
const autocompletePosition = ref({ top: 0, left: 0 })

// 在data或ref部分添加
const tokenCount = ref(0)

const props = defineProps({
  promptManager: {
    type: String,
    default: 'prompt_global'
  },
  hasPromptLoraStack: {
    type: Boolean,
    default: false
  },
})

const parentCneterBox = ref(null)

// 输入prompt信息
const inputText = ref('')
const tokens = ref([])
const tokenInputRefs = {}
const activeControls = ref(null)
const isOverControls = ref(false)
const controlsPosition = ref({
  top: '0px',
  left: '0px'
})
const showLanguageSelector = ref(false)
const settingDialog = ref(null)
const langBtnRef = ref(null)
const languageSwitcherRef = ref(null)

// Lora选择信息
const selectedLoras = ref([])
const loraOpen = ref(false)

// 添加自动补全相关的 ref
const showAutocomplete = ref(false);
const autocompleteResults = ref([]);
const selectedAutocompleteIndex = ref(0);
const selectedItemRef = ref(null);
const saveAutoCompleteWidth = ref(localStorage.getItem('weilin_prompt_ui_auto_box_width') || 450);
const saveAutoCompleteHeight = ref(localStorage.getItem('weilin_prompt_ui_auto_box_height') || 350);


const translateText = ref('')

// 在现有的ref声明部分添加
const showTagTipsBox = ref(false);
const tagTipsPosition = ref({
  top: '0px',
  left: '0px'
});


// 添加防抖相关的变量
const debounceTimeout = ref(null); // 用于存储 setTimeout 的 ID
const proceTimeout = ref(null);
const lastInputValue = ref(''); // 用于存储上一次的输入内容

// 在data或ref部分添加一个计数器用于生成唯一ID
const tokenIdCounter = ref(0);

// 控制左侧标签管理器是否可见的状态
const isLabelManagerVisible = ref(true);

// 用于本地存储的键名
const STORAGE_KEY_SIDEBAR_VISIBLE = 'weilin_prompt_ui_sidebar_visible';

// 切换标签管理器的显示状态
const toggleLabelManager = () => {
  isLabelManagerVisible.value = !isLabelManagerVisible.value;
};

// 监听状态变化并保存到 localStorage
watch(isLabelManagerVisible, (newValue) => {
  localStorage.setItem(STORAGE_KEY_SIDEBAR_VISIBLE, String(newValue));
});

// 组件挂载时，从 localStorage 读取并恢复状态
onMounted(() => {
  const savedState = localStorage.getItem(STORAGE_KEY_SIDEBAR_VISIBLE);
  // 默认值为 true (显示)，如果存储了 'false' 则为 false
  isLabelManagerVisible.value = savedState !== 'false';
  // ... 其他 onMounted 逻辑
});

// 生成唯一ID的函数
const generateUniqueId = () => {
  tokenIdCounter.value++;
  return `token_${tokenIdCounter.value}_${Date.now()}`;
};

const toggleLora = () => {
  loraOpen.value = !loraOpen.value
}

const closeLora = () => {
  loraOpen.value = false
}

// 左侧主标签管理器交互与主内容宽度计算
const mainLabelManagerRef = ref(null)
const selectedMainLabelId = ref(null)
const unsavedChanges = ref(false)
// 记录/恢复最后选中的主标签
const LAST_LABEL_KEY = `weilin_prompt_ui_last_main_label_id_${props.promptManager || 'default'}`
const MAIN_LABELS_STORAGE_KEY = 'weilin_prompt_ui_main_labels_v1'
// --- 修改 mainContentWidth 计算属性 ---
const mainContentWidth = computed(() => {
  // 根据 isLabelManagerVisible 决定左侧标签管理器的宽度
  const labelManagerWidth = isLabelManagerVisible.value ? 280 : 0; 
  const left = (loraOpen.value ? 300 : 0) + labelManagerWidth; // Lora(可变) + 主标签管理器(可变)
  return `calc(100% - ${left}px)`;
});
// const mainContentWidth = computed(() => {
//   const left = (loraOpen.value ? 300 : 0) + 280 // Lora(可变) + 主标签管理器(固定)
//   return `calc(100% - ${left}px)`
// })

let suppressUnsavedOnce = false
const onSelectMainLabel = (item) => {
  if (!item) {
    selectedMainLabelId.value = null
    inputText.value = ''
    nextTick(() => {
      if (inputAreaRef.value) {
        inputAreaRef.value.value = ''
        handleInput({ target: inputAreaRef.value })
      }
    })
    unsavedChanges.value = false
    return
  }
  selectedMainLabelId.value = item.id
  suppressUnsavedOnce = true
  inputText.value = item.content || ''
  nextTick(() => {
    if (inputAreaRef.value) {
      inputAreaRef.value.value = inputText.value
      // 模拟输入事件，触发 tokens 解析与渲染
      handleInput({ target: inputAreaRef.value })
    }
  })
  unsavedChanges.value = false
}

// 将输入框的变更回写到选中的主标签
// 仅做“有未保存变更”的标记，不再自动写回标签
watch(inputText, (v) => {
  if (suppressUnsavedOnce) { suppressUnsavedOnce = false; return }
  unsavedChanges.value = true
})

// 监听并持久化最后选中的主标签 ID
watch(selectedMainLabelId, (id) => {
  try { localStorage.setItem(LAST_LABEL_KEY, id || '') } catch {}
})

// 恢复最后一次选中的主标签
function restoreLastSelectedMainLabel() {
  try {
    const lastId = localStorage.getItem(LAST_LABEL_KEY)
    if (!lastId) return
    const raw = localStorage.getItem(MAIN_LABELS_STORAGE_KEY)
    const arr = raw ? JSON.parse(raw) : []
    const node = Array.isArray(arr) ? arr.find(x => x && x.id === lastId) : null
    if (!node) return
    selectedMainLabelId.value = lastId
    suppressUnsavedOnce = true
    inputText.value = node.content || ''
    nextTick(() => {
      if (inputAreaRef.value) {
        inputAreaRef.value.value = inputText.value
        handleInput({ target: inputAreaRef.value })
      }
    })
    unsavedChanges.value = false
  } catch {}
}

onMounted(() => {
  // 页面加载时尝试恢复上次的主标签选择
  restoreLastSelectedMainLabel()
  // 关闭页面前保存选中状态（兜底一次）
  const saveLast = () => { try { localStorage.setItem(LAST_LABEL_KEY, selectedMainLabelId.value || '') } catch {} }
  window.addEventListener('beforeunload', saveLast)
  onBeforeUnmount(() => window.removeEventListener('beforeunload', saveLast))
})

// 点击“更新标签”时才把文本写回当前标签
function updateSelectedLabel() {
  if (!selectedMainLabelId.value) return
  if (!mainLabelManagerRef.value?.updateSelectedContent) return
  mainLabelManagerRef.value.updateSelectedContent(inputText.value)
  unsavedChanges.value = false
}

const openSettings = () => {
  settingDialog.value.open()
}

// 在 script 中添加相关方法
const weightValue = ref(1);

const applyWeight = () => {
  if (activeControls.value === null) return;

  const token = tokens.value[activeControls.value];
  let text = token.text;

  // 检查括号是否完整
  if (!isBracketComplete(text)) {
    message({ type: "warn", str: 'message.noFinishKuo' });
    return;
  }

  // 辅助函数：检查是否只有一层圆括号
  const hasOnlySingleParentheses = (text) => {
    return text.startsWith('(') && text.endsWith(')') &&
      !text.slice(1, -1).includes('(') &&
      !text.slice(1, -1).includes(')') &&
      !text.slice(1, -1).includes('[') &&
      !text.slice(1, -1).includes(']') &&
      !text.slice(1, -1).includes('{') &&
      !text.slice(1, -1).includes('}') &&
      !text.slice(1, -1).includes('<') &&
      !text.slice(1, -1).includes('>');
  };

  // 辅助函数：查找最内层内容并更新权重
  const updateInnerContent = (text) => {
    // 匹配括号和权重的正则表达式
    const bracketRegex = /^([\(\[\{\<]*)(.*?)([\)\]\}\>]*)$/;
    const weightRegex = /(.*?)(?::[\d.]+)?$/;

    const match = text.match(bracketRegex);
    if (!match) return text;

    const [, openBrackets, content, closeBrackets] = match;

    // 如果内容中还有括号，递归处理
    if (/[\(\[\{\<].*[\)\]\}\>]/.test(content)) {
      return openBrackets + updateInnerContent(content) + closeBrackets;
    }

    // 处理最内层内容，移除现有权重
    const baseContent = content.replace(/:\d+(\.\d+)?$/, '');

    // 构建新内容
    if (weightValue.value === 1) {
      return openBrackets + baseContent + closeBrackets;
    } else {
      return openBrackets + baseContent + ':' + weightValue.value + closeBrackets;
    }
  };

  // 主要处理逻辑
  let newText = text;

  // 处理没有任何括号的情况
  if (!/[\(\[\{\<\)\]\}\>]/.test(text)) {
    // 移除现有权重
    const baseText = text.replace(/:\d+(\.\d+)?$/, '');
    if (weightValue.value === 1) {
      newText = baseText;
    } else {
      newText = `(${baseText}:${weightValue.value})`;
    }
  }
  // 处理只有一层圆括号的情况
  else if (weightValue.value === 1 && hasOnlySingleParentheses(text)) {
    // 移除括号和权重
    newText = text.slice(1, -1).replace(/:\d+(\.\d+)?$/, '');
  }
  // 处理其他情况（包括嵌套括号）
  else {
    newText = updateInnerContent(text);
  }

  tokens.value[activeControls.value].text = newText;
  updateInputText();
};


// Lora权重控制
const loraModelWeight = ref(0.5);
const loraTextWeight = ref(0.5);

// 当选择一个Lora标签时，解析其权重
watch(activeControls, (newVal) => {
  if (newVal !== null && tokens.value[newVal]?.isLoraTag) {
    // 解析Lora标签格式 <wlr:LoraName:weight1:weight2>
    const text = tokens.value[newVal].text;
    const match = text.match(/<wlr:([^:]+):([^:]+):([^>]+)>/);
    if (match) {
      loraModelWeight.value = parseFloat(match[2]);
      loraTextWeight.value = parseFloat(match[3]);
    }
  }
});

// 应用Lora权重
const applyLoraWeights = () => {
  if (activeControls.value !== null && tokens.value[activeControls.value]?.isLoraTag) {
    const token = tokens.value[activeControls.value];
    const match = token.text.match(/<wlr:([^:]+):([^:]+):([^>]+)>/);
    if (match) {
      const loraName = match[1];
      // 创建新的Lora标签文本
      const newText = `<wlr:${loraName}:${loraModelWeight.value}:${loraTextWeight.value}>`;
      // 更新token文本
      token.text = newText;
      // 更新输入文本
      updateInputText();
    }
  }
};


// 修改wrapWith函数
const wrapWith = (bracketType) => {
  if (activeControls.value === null) return;

  const token = tokens.value[activeControls.value];
  let text = token.text;

  // 定义括号对
  const bracketPair = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
  }[bracketType];

  text = `${bracketType}${text}${bracketPair}`;

  tokens.value[activeControls.value].text = text;

  finishPromptPutItHistory();
};

const removeLayer = (bracketType) => {
  if (activeControls.value === null) return;
  const token = tokens.value[activeControls.value];
  let text = token.text;

  // 移除最外层对应类型的括号
  const bracketPair = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
  };

  if (text.startsWith(bracketType) && text.endsWith(bracketPair[bracketType])) {
    text = text.slice(1, -1);
    tokens.value[activeControls.value].text = text;
    finishPromptPutItHistory();
  }
};

// 添加括号完整性检查函数
const isBracketComplete = (text) => {
  const stack = [];
  const bracketMap = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>'
  };

  for (let char of text) {
    if (bracketMap[char]) {
      stack.push(char);
    } else if (Object.values(bracketMap).includes(char)) {
      if (stack.length === 0 || bracketMap[stack.pop()] !== char) {
        return false;
      }
    }
  }

  return stack.length === 0;
};

const getClosingBracket = (bracketType) => {
  switch (bracketType) {
    case '(': return ')';
    case '[': return ']';
    case '{': return '}';
    default: return '';
  }
};


// 在更新前清除 refs
onBeforeUpdate(() => {
  for (const key in tokenInputRefs) {
    delete tokenInputRefs[key]
  }
})

// 添加判断是否为标点符号的函数
const isPunctuation = (char) => {
  // 匹配中文标点和英文标点
  return /[\u2000-\u206F\u3000-\u303F\uFF00-\uFFEF!-/:-@\[-`{-~]/.test(char);
};

// 添加判断是否为英文的函数
const isEnglish = (text) => {
  return /^[a-zA-Z]+$/.test(text);
};
// 添加选择分割方式的变量
const splitByPunctuation = ref(true); // 默认以标点符号分割
const replaceUnderscoreWithSpace = ref(false); // 默认不替换下划线

const isTextTranslatable = (text) => {
  // 匹配包含任何语言的字母或字符
  // 包括但不限于：中文、英文、日文、韩文、阿拉伯文、俄文等
  // 排除纯数字、标点符号和特殊符号
  return /[\p{L}]/u.test(text);
};

const extractText = (input) => {
  // 匹配任意字符序列，直到遇到冒号
  const match = input.match(/([^:]+):[\d.]+/);
  // 如果找到了匹配项，则返回第一个捕获组，否则返回原输入
  return match ? match[1] : input;
}

const replaceTagsWithDesc = (text, tagMap) => {
  // 确保 tagMap 是 Map 类型
  if (!(tagMap instanceof Map)) {
    throw new Error("tagMap 必须是 Map 类型");
  }

  // 将所有 tag 拼接成一个正则表达式
  const tagsPattern = Array.from(tagMap.keys())
    .map(tag => {
      // 确保 tag 是字符串
      const tagStr = typeof tag === 'string' ? tag : String(tag);
      // 转义正则表达式的特殊字符
      return tagStr.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
    })
    .join('|'); // 用 | 连接所有 tag

  // 创建全局不区分大小写的正则表达式
  const regex = new RegExp(tagsPattern, 'gi');

  // 使用 replace 和回调函数进行一次性替换
  return text.replace(regex, matchedTag => {
    // 查找对应的 desc
    const tagInfo = tagMap.get(matchedTag.toLowerCase()); // 假设不区分大小写
    return tagInfo ? tagInfo.desc : matchedTag; // 如果找不到 desc，返回原 tag
  });
};


let debounceTimer = null;
const calculateAutocompletePosition = async () => {
  if (debounceTimer) {
    clearTimeout(debounceTimer);
  }
  debounceTimer = setTimeout(async () => {
    if (!inputAreaRef.value) return;

    const textarea = inputAreaRef.value;
    const cursorPos = textarea.selectionStart;
    // console.log(textarea,cursorPos)

    // 确保自动补全窗口已经渲染
    await nextTick();

    // 创建镜像元素计算光标位置
    const text = textarea.value.substring(0, cursorPos);
    const mirror = document.createElement('div');
    mirror.style.position = 'absolute';
    mirror.style.top = '0';
    mirror.style.left = '0';
    mirror.style.visibility = 'hidden';
    mirror.style.whiteSpace = 'pre-wrap';
    mirror.style.wordWrap = 'break-word';
    mirror.style.width = window.getComputedStyle(textarea).width;
    mirror.style.font = window.getComputedStyle(textarea).font;
    mirror.style.padding = window.getComputedStyle(textarea).padding;

    const textNode = document.createTextNode(text);
    const cursorNode = document.createElement('span');
    cursorNode.textContent = '|';

    mirror.appendChild(textNode);
    mirror.appendChild(cursorNode);
    textarea.parentNode.appendChild(mirror);

    // 获取光标相对于父容器的位置
    const cursorRect = cursorNode.getBoundingClientRect();
    const parentRect = textarea.parentNode.getBoundingClientRect();

    // 计算初始位置
    let top = cursorRect.top - parentRect.top + cursorRect.height;
    let left = cursorRect.left - parentRect.left;

    // 等待DOM更新完成
    await nextTick();

    if (autocompleteContainerRef.value) {
      const autocompleteWidth = autocompleteContainerRef.value.offsetWidth;
      const textareaWidth = textarea.offsetWidth;
      const textareaLeft = textarea.getBoundingClientRect().left - parentRect.left;

      // 检查右边界
      if (left + autocompleteWidth > textareaLeft + textareaWidth) {
        left = textareaLeft + textareaWidth - autocompleteWidth;
      }

      // 检查左边界
      if (left < textareaLeft) {
        left = textareaLeft;
      }

      // 确保不会超出父容器
      left = Math.max(0, Math.min(left, parentRect.width - autocompleteWidth));
    }

    // 清理临时元素
    textarea.parentNode.removeChild(mirror);

    autocompletePosition.value = { top, left };
    debounceTimer = null;
  }, 50); // 50ms防抖
};

// 添加一个 ref 用于存储定时器
const historyTimer = ref(null);


// 处理输入事件
const handleInput = (event) => {
  if (!event?.target) return;

  if (!inputAreaRef.value) return

  // 获取原始输入值和光标位置
  const originalValue = event.target.value;
  const cursorPosition = event.target.selectionStart;
  const cursorEnd = event.target.selectionEnd;


  // 1. 首先处理格式转换
  const formatConversions = {
    comma: { enabled: localStorage.getItem('weilin_prompt_ui_comma_conversion') !== 'false', pattern: /，/g, replace: ',' },
    period: { enabled: localStorage.getItem('weilin_prompt_ui_period_conversion') !== 'false', pattern: /。/g, replace: '.' },
    bracket: {
      enabled: localStorage.getItem('weilin_prompt_ui_bracket_conversion') !== 'false', patterns: [
        { pattern: /【/g, replace: '[' },
        { pattern: /】/g, replace: ']' },
        { pattern: /（/g, replace: '(' },
        { pattern: /）/g, replace: ')' }
      ]
    },
    angleBracket: {
      enabled: localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion') !== 'false', patterns: [
        { pattern: /《/g, replace: '<' },
        { pattern: /》/g, replace: '>' }
      ]
    },
    underscore: { enabled: localStorage.getItem('weilin_prompt_ui_underscore_to_bracket') === 'true', pattern: /_/g, replace: ' ' }
  };

  // 记录每个替换操作前光标位置的字符
  let beforeCursor = originalValue.substring(0, cursorPosition);
  let processedValue = originalValue;

  // 应用所有转换
  Object.values(formatConversions).forEach(conversion => {
    if (conversion.enabled) {
      if (conversion.pattern) {
        // 处理单个模式的替换
        beforeCursor = beforeCursor.replace(conversion.pattern, conversion.replace);
        processedValue = processedValue.replace(conversion.pattern, conversion.replace);
      } else if (conversion.patterns) {
        // 处理多个模式的替换
        conversion.patterns.forEach(({ pattern, replace }) => {
          beforeCursor = beforeCursor.replace(pattern, replace);
          processedValue = processedValue.replace(pattern, replace);
        });
      }
    }
  });

  // 2. 直接更新输入框值
  inputText.value = processedValue;

  // 3. 立即计算并设置新的光标位置
  // 使用转换后的beforeCursor长度作为新的光标位置
  const newCursorPosition = beforeCursor.length;
  const selectionDiff = cursorEnd - cursorPosition;
  const newCursorEnd = newCursorPosition + selectionDiff;

  // 确保DOM更新后立即设置光标位置
  nextTick(() => {
    if (inputAreaRef.value) {
      inputAreaRef.value.setSelectionRange(newCursorPosition, newCursorEnd);
      // 确保输入框获得焦点
      inputAreaRef.value.focus();
    }
  });

  // 4. 精确获取当前输入内容用于补全
  const textBeforeCursor = processedValue.substring(0, newCursorPosition);

  // 查找当前输入的单词起始位置
  let wordStart = newCursorPosition;
  while (wordStart > 0 && !/[,\s]/.test(textBeforeCursor[wordStart - 1])) {
    wordStart--;
  }


  const currentWord = textBeforeCursor.substring(wordStart, newCursorPosition).trim();

  // 5. 防抖处理
  if (debounceTimeout.value) {
    clearTimeout(debounceTimeout.value);
  }

  debounceTimeout.value = setTimeout(() => {
    if (currentWord) {
      triggerAutocomplete(currentWord);
    }
    postMessageToWindowsPrompt();
  }, 300);

  // 计算token数量（简单实现，可根据实际分词算法调整）
  tokenCount.value = calculateTokens(inputText.value)
};


// 添加计算token的方法
const calculateTokens = (text) => {
  if (!text) return 0
  // 简单实现：按空格分词
  // 注意：实际的token计算应该使用与您模型匹配的分词器
  return text.trim().split(/\s+/).length
}

// 处理输入事件 ========== 主事件处理 ==========
const processInput = async () => {

  // 预设设置
  let isCommaConversionEnabled = localStorage.getItem('weilin_prompt_ui_comma_conversion') === 'true';
  let isPeriodConversionEnabled = localStorage.getItem('weilin_prompt_ui_period_conversion') === 'true';
  let isBracketConversionEnabled = localStorage.getItem('weilin_prompt_ui_bracket_conversion') === 'true';
  let isAngleBracketConversionEnabled = localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion') === 'true';
  let isUnderscoreToBracketEnabled = localStorage.getItem('weilin_prompt_ui_underscore_to_bracket') === 'true';

  if (!localStorage.getItem('weilin_prompt_ui_comma_conversion')) {
    localStorage.setItem('weilin_prompt_ui_comma_conversion', 'true')
    isCommaConversionEnabled = true
  }
  if (!localStorage.getItem('weilin_prompt_ui_period_conversion')) {
    localStorage.setItem('weilin_prompt_ui_period_conversion', 'true')
    isPeriodConversionEnabled = true
  }
  if (!localStorage.getItem('weilin_prompt_ui_bracket_conversion')) {
    localStorage.setItem('weilin_prompt_ui_bracket_conversion', 'true')
    isBracketConversionEnabled = true
  }
  if (!localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion')) {
    localStorage.setItem('weilin_prompt_ui_angle_bracket_conversion', 'true')
    isAngleBracketConversionEnabled = true
  }
  if (!localStorage.getItem('weilin_prompt_ui_underscore_to_bracket')) {
    localStorage.setItem('weilin_prompt_ui_underscore_to_bracket', 'false')
    isUnderscoreToBracketEnabled = false
  }


  if (isCommaConversionEnabled) {
    inputText.value = inputText.value.replace(/，/g, ',');
  }
  if (isPeriodConversionEnabled) {
    inputText.value = inputText.value.replace(/。/g, '.');
  }
  if (isBracketConversionEnabled) {
    inputText.value = inputText.value
      .replace(/【/g, '[')  // 中文左方括号
      .replace(/】/g, ']')  // 中文右方括号
      .replace(/（/g, '(')  // 中文左圆括号
      .replace(/）/g, ')'); // 中文右圆括号
  }
  if (isAngleBracketConversionEnabled) {
    // 替换中文书名号为英文尖括号
    inputText.value = inputText.value
      .replace(/《/g, '<')  // 中文左书名号
      .replace(/》/g, '>'); // 中文右书名号
  }

  if (isUnderscoreToBracketEnabled) {
    // 替换下划线为空格
    inputText.value = inputText.value.replace(/_/g, ' ');
  }

  // 处理文本分割
  const text = inputText.value;
  let segments = [];

  // 首先记录所有隐藏token的原始位置
  const hiddenTokensWithOriginalIndex = tokens.value
    .map((token, originalIndex) => ({
      token,
      originalIndex,  // 保存原始绝对位置
      currentIndex: originalIndex  // 初始时currentIndex与originalIndex相同
    }))
    .filter(({ token }) => token.isHidden);

  // 递归函数处理嵌套括号
  const parseNestedBrackets = (str, startIndex = 0) => {
    let segments = [];
    let i = startIndex;
    let buffer = '';
    let bracketStack = [];

    while (i < str.length) {
      const char = str[i];

      // 处理开括号
      // if ('([{<'.includes(char)) {
      //   // 检测前一个字符是否是逗号或空格，或者是否是字符串开头
      //   const prevChar = i > 0 ? str[i - 1] : '';
      //   const isValidStart = prevChar === '' || prevChar === ',' || prevChar === ' ';

      //   if (isValidStart) {
      //     if (bracketStack.length === 0 && buffer.trim()) {
      //       // 如果这是第一层括号且缓冲区不为空，按逗号分割并添加
      //       segments.push(...buffer.split(',').filter(Boolean).map(s => s.trim()));
      //       buffer = '';
      //     }
      //     bracketStack.push(char);
      //     buffer += char;
      //   } else {
      //     // 如果不是有效开始，按普通字符处理
      //     buffer += char;
      //   }
      // }
      // // 处理闭括号
      // else if (')]}>'.includes(char)) {
      //   const lastBracket = bracketStack[bracketStack.length - 1];
      //   if (('(' === lastBracket && ')' === char) ||
      //     ('[' === lastBracket && ']' === char) ||
      //     ('{' === lastBracket && '}' === char) ||
      //     ('<' === lastBracket && '>' === char)) {

      //     // 只有在存在对应的开括号时才进行后续检测
      //     if (bracketStack.length > 0) {
      //       // 检测后一个字符是否是逗号或空格，或者是否是字符串结尾
      //       const nextChar = i < str.length - 1 ? str[i + 1] : '';
      //       const isValidEnd = nextChar === '' || nextChar === ',' || nextChar === ' ';

      //       if (isValidEnd) {
      //         bracketStack.pop();
      //         buffer += char;

      //         // 如果括号全部匹配完成，添加整个括号内容
      //         if (bracketStack.length === 0) {
      //           segments.push(buffer.trim());
      //           buffer = '';
      //         }
      //       } else {
      //         // 如果不是有效结束，按普通字符处理
      //         buffer += char;
      //       }
      //     }
      //   }
      // }

      // 处理换行符
      if (char === '\n') {
        if (buffer.trim()) {
          segments.push(buffer.trim());
          buffer = '';
        }
        segments.push('\n');
        i++;
        continue;
      }

      // 处理普通字符   
      if (bracketStack.length === 0 && char === ',') {
        if (buffer.trim()) {
          segments.push(buffer.trim());
        }
        buffer = '';
      } else {
        buffer += char;
      }
      i++;
    }

    // 处理剩余的缓冲区内容
    if (buffer.trim()) {
      if (bracketStack.length === 0) {
        segments.push(...buffer.split(',').filter(Boolean).map(s => s.trim()));
      } else {
        segments.push(buffer.trim());
      }
    }

    return segments;
  };

  // 解析文本得到分段
  segments = parseNestedBrackets(text);

  // 处理每个片段
  const existingTokensMap = new Map();
  tokens.value.forEach((token, index) => {
    // 确保每个token都有唯一ID
    if (!token.id) {
      token.id = generateUniqueId();
    }
    existingTokensMap.set(index, token); // 使用索引作为key
  });

  const result = [];

  // 然后处理剩余的segments（新增的token）
  segments.forEach(segment => {
    if (segment === '\n') {
      // 保留换行符作为特殊token
      result.push({
        id: generateUniqueId(),
        text: '\n',
        translate: '',
        isPunctuation: false,
        isEditing: false,
        isHidden: false,
        color: ''
      });
    } else if (segment.trim()) {
      // 处理非空文本
      const trimmedSegment = segment.trim();
      // 检查是否是Lora标签格式 <wlr:LoraName:weight1:weight2>
      const isLoraTag = /^<wlr:[^:]+:\d+(\.\d+)?:\d+(\.\d+)?>$/.test(trimmedSegment);

      // 优先匹配非隐藏的token
      let matched = false;
      for (const [index, token] of existingTokensMap) {
        if (token.text === trimmedSegment && !token.isHidden && !result.includes(token)) {
          // 如果是已存在的token，确保更新其Lora标签状态
          if (isLoraTag && !token.isLoraTag) {
            token.isLoraTag = true;
          }
          result.push(token);
          existingTokensMap.delete(index);
          matched = true;
          break;
        }
      }

      // 如果没有匹配到非隐藏token，再尝试匹配隐藏token
      if (!matched) {
        for (const [index, token] of existingTokensMap) {
          if (token.text === trimmedSegment && !result.includes(token)) {
            // 如果是已存在的token，确保更新其Lora标签状态
            if (isLoraTag && !token.isLoraTag) {
              token.isLoraTag = true;
            }
            result.push(token);
            existingTokensMap.delete(index);
            matched = true;
            break;
          }
        }
      }

      if (!matched) {
        result.push({
          id: generateUniqueId(),
          text: trimmedSegment,
          translate: '',
          isPunctuation: false,
          isEditing: false,
          isHidden: false,
          color: '',
          isLoraTag: isLoraTag // 添加Lora标签标识
        });
      }
    }

  });

  // 使用ID来跟踪已处理的隐藏token
  const processedHiddenTokenIds = new Set();

  //重新插入隐藏token到它们原来的位置
  hiddenTokensWithOriginalIndex.forEach(({ token, originalIndex }) => {
    // 如果这个token已经处理过，跳过
    if (processedHiddenTokenIds.has(token.id)) {
      return;
    }

    // 标记这个token已经处理
    processedHiddenTokenIds.add(token.id);

    // 检查结果中是否已经包含这个隐藏token
    const alreadyExists = result.some(t => t.id === token.id);

    // 如果已经存在，不再添加
    if (alreadyExists) {
      return;
    }

    let insertIndex = originalIndex;

    // 确保插入位置有效
    while (insertIndex > result.length) {
      insertIndex--;
    }

    // 如果所有尝试都失败，插入到最后
    if (insertIndex < 0) {
      result.push(token);
    } else {
      result.splice(insertIndex, 0, token);
    }
  });

  tokens.value = result;

  // 更新输入文本，保持原有格式，但排除隐藏的tokens
  inputText.value = tokens.value.length > 0
    ? tokens.value.reduce((acc, token, index) => {
      // 如果token是隐藏的，不添加到输入文本中
      if (token.isHidden) {
        return acc;
      }

      // 如果是换行符，不加逗号
      if (token.text === '\n') {
        // 查找前一个非隐藏token
        const prevNonHiddenIndex = findPrevNonHiddenIndex(index);
        const prevToken = prevNonHiddenIndex !== -1 ? tokens.value[prevNonHiddenIndex] : null;

        // 直接返回换行符，不添加额外的逗号
        // 因为前一个token在处理时已经根据shouldAddComma添加了逗号
        return acc + token.text;
      }

      // 第一个非隐藏token不加逗号前缀
      if (acc === '') {
        // 查找下一个非隐藏token
        let nextNonHiddenIndex = index + 1;
        while (nextNonHiddenIndex < tokens.value.length && tokens.value[nextNonHiddenIndex]?.isHidden) {
          nextNonHiddenIndex++;
        }

        // 判断是否是最后一个非隐藏token或者下一个是换行符
        const isLastToken = nextNonHiddenIndex >= tokens.value.length;
        const nextToken = nextNonHiddenIndex < tokens.value.length ? tokens.value[nextNonHiddenIndex] : null;
        const shouldAddComma = isLastToken || (nextToken && nextToken.text === '\n');

        return token.text + (shouldAddComma ? ',' : '');
      }

      // 查找下一个非隐藏token
      let nextNonHiddenIndex = index + 1;
      while (nextNonHiddenIndex < tokens.value.length && tokens.value[nextNonHiddenIndex]?.isHidden) {
        nextNonHiddenIndex++;
      }

      // 判断是否是最后一个非隐藏token
      const isLastToken = nextNonHiddenIndex >= tokens.value.length;
      const nextToken = nextNonHiddenIndex < tokens.value.length ? tokens.value[nextNonHiddenIndex] : null;

      // 如果是换行符前或者最后一个token，则添加逗号
      const shouldAddComma = (nextToken && nextToken.text === '\n') || isLastToken;

      // 前一个token是换行符，不加逗号前缀
      const prevNonHiddenIndex = findPrevNonHiddenIndex(index);
      if (prevNonHiddenIndex !== -1 && tokens.value[prevNonHiddenIndex].text === '\n') {
        return acc + token.text + (shouldAddComma ? ',' : '');
      }

      // 其他情况加逗号和空格前缀
      return acc + ', ' + token.text + (shouldAddComma ? ',' : '');
    }, '') : '';


  // 处理历史记录
  if (proceTimeout.value) {
    clearTimeout(proceTimeout.value);
  }
  proceTimeout.value = setTimeout(() => {
    // console.log('处理历史记录');
    finishPromptPutItHistory();
  }, 1000);
  postMessageToWindowsPrompt();

  // 处理翻译
  const batchSize = 20; // 每批处理的数量
  let currentIndex = 0;

  while (currentIndex < tokens.value.length) {
    const endIndex = Math.min(currentIndex + batchSize, tokens.value.length);
    const promises = [];

    for (let i = currentIndex; i < endIndex; i++) {
      if (tokens.value[i].text.length > 0 && !tokens.value[i].translate) {
        let cleanedTrSegment = tokens.value[i].text;
        const text = extractText(cleanedTrSegment.trim());
        promises.push(
          translatorApi.getTranslateLocal(text).then(res => {
            const translate = res;
            tokens.value[i].translate = translate.translated.translate;
            tokens.value[i].color = translate.translated.color;
          })
        );
      }
    }

    await Promise.all(promises);
    currentIndex = endIndex;
  }

  // 处理翻译
  // for (let i = 0; i < tokens.value.length; i++) {
  //   if (tokens.value[i].text.length > 0 && !tokens.value[i].translate) {
  //     let cleanedTrSegment = tokens.value[i].text;
  //     const text = extractText(cleanedTrSegment.trim());
  //     translatorApi.getTranslateLocal(text).then(res => {
  //       const translate = res;
  //       tokens.value[i].translate = translate.translated.translate;
  //       tokens.value[i].color = translate.translated.color;
  //     });
  //   }
  // }

  // 计算token数量（简单实现，可根据实际分词算法调整）
  tokenCount.value = calculateTokens(inputText.value)
};

const oneClickTranslatePrompt = async () => {
  const batchSize = 20; // 每批处理的数量
  let currentIndex = 0;

  while (currentIndex < tokens.value.length) {
    const endIndex = Math.min(currentIndex + batchSize, tokens.value.length);
    const promises = [];

    for (let i = currentIndex; i < endIndex; i++) {
      const token = tokens.value[i];
      // 检查translate是否包含英文字符
      if (token.translate && /[a-zA-Z]/.test(token.translate)) {
        // 提取需要翻译的文本
        const textToTranslate = token.text;
        const promise = new Promise((resolve) => {

          if (localStorage.getItem('weilin_prompt_ui_translater_setting') == 'network') {
            translate.request.translateText(textToTranslate, function (data) {
              if (data.result > 0) {
                const translatedText = data.text.map(item => item.replace(/[\[\]“”]/g, '')).join(', ');
                tokens.value[i].translate = translatedText;
              }
              resolve();
            });
          } else {
            translatorApi.translaterText(textToTranslate).then(res => {
              // console.log(res)
              if (res.text.length > 0) {
                tokens.value[i].translate = res.text;
              }
              resolve();
            })
          }

        });
        promises.push(promise);
      }
    }

    // 等待当前批次完成
    await Promise.all(promises);
    currentIndex = endIndex;
  }
};


const tempInputText = ref('')

const finishPromptPutItHistory = () => {
  // console.log('finishPromptPutItHistory 被调用', new Error().stack);
  // 去除空格、换行和制表符
  const trimmedInput = inputText.value.replace(/[\s\t\n]+/g, '');
  if (selectedLoras.value.length > 0) {
    if (trimmedInput.length > 0) {
      const tempLora = selectedLoras.value.filter(lora => !lora.hidden);
      let putJson = {
        prompt: inputText.value,
        lora: "",
        temp_prompt: tokens.value,
        temp_lora: selectedLoras.value
      }
      if (tempLora.length > 0) {
        putJson.lora = tempLora
      }
      const jsonStr = JSON.stringify(putJson)
      if (tempInputText.value != jsonStr) {
        tempInputText.value = jsonStr
        historyApi.saveHistory({ tag: jsonStr })
      }
    }
  } else {
    if (tempInputText.value != inputText.value) {
      const putJson = {
        prompt: inputText.value,
        lora: "",
        temp_prompt: tokens.value,
        temp_lora: ""
      }
      const jsonStr = JSON.stringify(putJson)
      if (trimmedInput.length > 0) {
        historyApi.saveHistory({ tag: jsonStr })
      }
    }
  }
  postMessageToWindowsPrompt()
}

const postMessageToWindowsPrompt = () => {
  if (selectedLoras.value.length > 0) {
    tempInputText.value = inputText.value
    const tempLora = selectedLoras.value.filter(lora => !lora.hidden);
    let putJson = {
      prompt: inputText.value,
      lora: "",
      temp_prompt: tokens.value,
      temp_lora: selectedLoras.value
    }
    if (tempLora.length > 0) {
      putJson.lora = tempLora
    }
    const jsonStr = JSON.stringify(putJson)
    window.postMessage({
      type: 'weilin_prompt_ui_prompt_finish_prompt',
      data: jsonStr
    }, '*')
  } else {
    tempInputText.value = inputText.value
    const putJson = {
      prompt: inputText.value,
      lora: "",
      temp_prompt: tokens.value,
      temp_lora: ""
    }
    const jsonStr = JSON.stringify(putJson)
    window.postMessage({
      type: 'weilin_prompt_ui_prompt_finish_prompt',
      data: jsonStr
    }, '*')
  }
}


// 显示控制栏
const showControls = (index, event) => {
  // 清除任何现有的定时器
  if (hideTimeout.value) {
    clearTimeout(hideTimeout.value)
    hideTimeout.value = null
  }

  const rect = event.target.getBoundingClientRect()
  controlsPosition.value = {
    top: `${rect.top - 50}px`,
    left: `${rect.left + rect.width / 2}px`
  }
  activeControls.value = index

  // 检测并设置权重值
  const text = tokens.value[index].text;
  weightValue.value = findInnerWeight(text);

  tagTipsPosition.value = {
    top: `${rect.bottom + window.scrollY + rect.height + 10}px`,
    left: `${rect.left + rect.width / 2}px`
  };
  if (!tokens.value[index].isLoraTag) {
    showTagTipsBox.value = true;
  }
}


// 定义递归函数来查找最内层的权重
const findInnerWeight = (content) => {
  // 定义括号匹配正则表达式
  const bracketPairs = [
    { open: '(', close: ')' },
    { open: '[', close: ']' },
    { open: '{', close: '}' },
    { open: '<', close: '>' }
  ];

  // 查找最内层内容
  for (const pair of bracketPairs) {
    if (content.startsWith(pair.open) && content.endsWith(pair.close)) {
      // 递归查找内层内容
      return findInnerWeight(content.slice(1, -1));
    }
  }

  // 如果没有括号，直接匹配权重
  const weightMatch = content.match(/:(\d+(\.\d+)?)$/);
  return weightMatch ? parseFloat(weightMatch[1]) : 1;
};

const hideTimeout = ref(null)

// 处理鼠标离开词组
const handleMouseLeave = (index) => {
  // 清除现有的定时器
  if (hideTimeout.value) {
    clearTimeout(hideTimeout.value)
  }

  // 设置新的定时器
  hideTimeout.value = setTimeout(() => {
    if (!isOverControls.value) {
      hideControls()
    }
    hideTimeout.value = null
  }, 100)

  showTagTipsBox.value = false;
}

// 处理鼠标离开控制栏
const handleControlsLeave = () => {
  isOverControls.value = false
  handleMouseLeave(activeControls.value)
}

// 隐藏控制栏
const hideControls = () => {
  if (!isOverControls.value) {
    activeControls.value = null
  }
}

// 处理删除按钮点击
const handleDelete = () => {
  if (activeControls.value !== null) {
    const index = activeControls.value
    deleteToken(index)
    // 删除后立即隐藏控制栏
    activeControls.value = null
    isOverControls.value = false
  }
}

// 删除词组
const deleteToken = (index) => {
  const text = inputText.value
  let targetToken = tokens.value[index]
  let lastIndex = 0
  let tokenPos = -1

  // 查找要删除的词组位置
  for (let i = 0; i < index; i++) {
    let pos = text.indexOf(tokens.value[i].text, lastIndex)
    if (pos !== -1) {
      lastIndex = pos + tokens.value[i].text.length
    }
  }

  // 找到目标词组的位置
  if (targetToken.text === '\n' || targetToken.text === '\t') {
    for (let i = lastIndex; i < text.length; i++) {
      if (text[i] === targetToken.text) {
        tokenPos = i
        break
      }
    }
  } else {
    tokenPos = text.indexOf(targetToken.text, lastIndex)
  }

  if (tokenPos !== -1) {
    // 如果删除的是换行符，则替换为空格
    const replacement = targetToken.text === '\n' ? ' ' : ''
    const newText = text.substring(0, tokenPos) + replacement + text.substring(tokenPos + targetToken.text.length)
    inputText.value = newText
  }

  tokens.value.splice(index, 1)
  // 更新输入文本，保持原有格式，但排除隐藏的tokens
  inputText.value = tokens.value.length > 0
    ? tokens.value.reduce((acc, token, index) => {
      // 如果token是隐藏的，不添加到输入文本中
      if (token.isHidden) {
        return acc;
      }

      // 如果是换行符，不加逗号
      if (token.text === '\n') {
        // 查找前一个非隐藏token
        const prevNonHiddenIndex = findPrevNonHiddenIndex(index);
        const prevToken = prevNonHiddenIndex !== -1 ? tokens.value[prevNonHiddenIndex] : null;

        // 直接返回换行符，不添加额外的逗号
        // 因为前一个token在处理时已经根据shouldAddComma添加了逗号
        return acc + token.text;
      }

      // 第一个非隐藏token不加逗号前缀
      if (acc === '') {
        // 查找下一个非隐藏token
        let nextNonHiddenIndex = index + 1;
        while (nextNonHiddenIndex < tokens.value.length && tokens.value[nextNonHiddenIndex]?.isHidden) {
          nextNonHiddenIndex++;
        }

        // 判断是否是最后一个非隐藏token或者下一个是换行符
        const isLastToken = nextNonHiddenIndex >= tokens.value.length;
        const nextToken = nextNonHiddenIndex < tokens.value.length ? tokens.value[nextNonHiddenIndex] : null;
        const shouldAddComma = isLastToken || (nextToken && nextToken.text === '\n');

        return token.text + (shouldAddComma ? ',' : '');
      }

      // 查找下一个非隐藏token
      let nextNonHiddenIndex = index + 1;
      while (nextNonHiddenIndex < tokens.value.length && tokens.value[nextNonHiddenIndex]?.isHidden) {
        nextNonHiddenIndex++;
      }

      // 判断是否是最后一个非隐藏token
      const isLastToken = nextNonHiddenIndex >= tokens.value.length;
      const nextToken = nextNonHiddenIndex < tokens.value.length ? tokens.value[nextNonHiddenIndex] : null;

      // 如果是换行符前或者最后一个token，则添加逗号
      const shouldAddComma = (nextToken && nextToken.text === '\n') || isLastToken;

      // 前一个token是换行符，不加逗号前缀
      const prevNonHiddenIndex = findPrevNonHiddenIndex(index);
      if (prevNonHiddenIndex !== -1 && tokens.value[prevNonHiddenIndex].text === '\n') {
        return acc + token.text + (shouldAddComma ? ',' : '');
      }

      // 其他情况加逗号和空格前缀
      return acc + ', ' + token.text + (shouldAddComma ? ',' : '');
    }, '') : '';

  finishPromptPutItHistory()
}

// 处理词组编辑
const handleTokenEdit = (index, event) => {
  const text = inputText.value
  let lastIndex = 0
  let tokenPos = -1

  // 查找要编辑的词组位置
  for (let i = 0; i < index; i++) {
    let pos = text.indexOf(tokens.value[i].text, lastIndex)
    if (pos !== -1) {
      lastIndex = pos + tokens.value[i].text.length
    }
  }

  // 找到目标词组的原始位置
  const oldText = tokens.value[index].text
  tokenPos = text.indexOf(oldText, lastIndex)

  if (tokenPos !== -1) {
    // 更新输入框文本和词组文本
    const newValue = event.target.value
    const newText = text.substring(0, tokenPos) + newValue + text.substring(tokenPos + oldText.length)
    inputText.value = newText
    tokens.value[index] = {
      ...tokens.value[index],
      text: newValue
    }

    finishPromptPutItHistory()
  }
}

// 修改 startEditing 函数，添加对标点符号的处理
const startEditing = (index) => {
  // 如果是标点符号，不允许编辑
  if (tokens.value[index].isPunctuation) {
    return;
  }

  tokens.value[index].isEditing = true;
  setTimeout(() => {
    const input = tokenInputRefs[index];
    if (input) {
      input.focus();
      const len = input.value.length;
      input.setSelectionRange(len, len);
      adjustInputWidth(input);
      input.addEventListener('input', () => adjustInputWidth(input));
      finishPromptPutItHistory()
    }
  });
}

// 调整输入框宽度
const adjustInputWidth = (input) => {
  // 创建一个临时的 span 元素来计算文本宽度
  const span = document.createElement('span')
  span.style.visibility = 'hidden'
  span.style.position = 'absolute'
  span.style.whiteSpace = 'pre'
  // 复制输入框的样式
  const computedStyle = window.getComputedStyle(input)
  span.style.font = computedStyle.font
  span.style.fontSize = computedStyle.fontSize
  span.style.fontFamily = computedStyle.fontFamily
  span.style.padding = computedStyle.padding
  span.style.border = computedStyle.border
  span.textContent = input.value || input.placeholder || ''

  document.body.appendChild(span)
  // 设置输入框宽度，添加一些额外空间以防止文字紧贴边框
  const width = span.offsetWidth
  input.style.width = `${Math.max(width + 4, 20)}px`
  document.body.removeChild(span)
}

// 完成编辑
const finishEditing = (index) => {
  tokens.value[index].isEditing = false
}

// 删除 watch 监听器，因为我们现在使用直接的输入事件处理

// 监听词组的变化
watch(tokens, (newTokens) => {
  updateInputText()
}, { deep: true })

watch(selectedLoras, (newLoras) => {
  // console.log(newLoras)
  // finishPromptPutItHistory()
  finishPromptPutItHistory()
}, { deep: true })

// 切换语言选择器
const toggleLanguageSelector = () => {
  showLanguageSelector.value = !showLanguageSelector.value
  if (showLanguageSelector.value) {
    nextTick(() => {
      const btnRect = langBtnRef.value.getBoundingClientRect()
      languageSwitcherRef.value?.setPosition(btnRect)
    })
  }
}

// 关闭语言选择器
const closeLanguageSelector = () => {
  showLanguageSelector.value = false
}

// 处理点击外部
const handleClickOutside = (event) => {
  if (langBtnRef.value && !langBtnRef.value.contains(event.target) &&
    languageSwitcherRef.value && !languageSwitcherRef.value.$el.contains(event.target)) {
    closeLanguageSelector()
  }
  // 如果点击的不是补全窗口或输入框
  if (
    autocompleteContainerRef.value?.contains &&
    inputAreaRef.value?.contains &&
    !autocompleteContainerRef.value.contains(event.target) &&
    !inputAreaRef.value.contains(event.target)
  ) {
    showAutocomplete.value = false;
  }

}


// 打开标签管理器
const openTagManager = () => {
  // 发送消息给父窗口
  window.parent.postMessage({ type: 'weilin_prompt_ui_openTagManager_prompt' }, '*')
}

const openLoraManager = () => {
  // 发送消息给父窗口
  window.parent.postMessage({ type: 'weilin_prompt_ui_openLoraManager' }, '*')
}

const openHistoryBox = () => {
  // 发送消息给父窗口
  window.parent.postMessage({ type: 'weilin_prompt_ui_openHistoryManager' }, '*')
}

// 添加折叠状态控制
const showTagManager = ref(true)

// 切换标签管理器显示状态
const toggleTagManager = () => {
  showTagManager.value = !showTagManager.value
}

// 添加折叠状态控制
const showLoraManager = ref(false)

// 切换Lora管理器显示状态
const toggleLoraManager = () => {
  showLoraManager.value = !showLoraManager.value
}

const resizeObserver = ref(null)

const handleTextareaResize = () => {
  if (inputAreaRef.value) {
    const height = inputAreaRef.value.clientHeight
    localStorage.setItem('weilinPromptTextAreaHeight', height)
  }
}

const setupCursorTracking = () => {
  const textarea = inputAreaRef.value;
  if (!textarea) return;

  // 添加光标位置变化监听
  textarea.addEventListener('keyup', updateAutocompletePosition);
  textarea.addEventListener('click', updateAutocompletePosition);
  textarea.addEventListener('input', updateAutocompletePosition);
};

const updateAutocompletePosition = () => {
  if (showAutocomplete.value) {
    calculateAutocompletePosition();
  }
};

// 保存文本区域高度到localStorage
const saveTextareaHeight = () => {
  if (inputAreaRef.value) {
    const height = inputAreaRef.value.style.height || `${inputAreaRef.value.offsetHeight}px`;
    localStorage.setItem('weilinPromptTextAreaHeight', height);
  }
};

// 从localStorage恢复文本区域高度
const restoreTextareaHeight = () => {
  const savedHeight = localStorage.getItem('weilinPromptTextAreaHeight');
  if (savedHeight && inputAreaRef.value) {
    inputAreaRef.value.style.height = savedHeight;
  }
};

// 添加消息监听
onMounted(() => {
  document.addEventListener('click', handleClickOutside);
  window.addEventListener('message', handleMessage)
  initTranslate()
  setupCursorTracking()

  nextTick(() => {
    restoreTextareaHeight();
  });
})

onBeforeUnmount(() => {

})


// 组件卸载时清理事件监听
onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  if (historyTimer.value) {
    clearTimeout(historyTimer.value);
  }
  window.removeEventListener('message', handleMessage)
  const textarea = inputAreaRef.value;
  if (textarea) {
    textarea.removeEventListener('keyup', updateAutocompletePosition);
    textarea.removeEventListener('click', updateAutocompletePosition);
    textarea.removeEventListener('input', updateAutocompletePosition);
  }
})

// 处理消息
const handleMessage = (event) => {
  if (event.data.type === 'weilin_prompt_ui_insertTag') {
    // 在输入框末尾添加标签文本
    const currentText = inputText.value
    const tagText = event.data.tagText

    // 检查当前文本是否为空或是否以空格结尾
    if (currentText === '') {
      inputText.value = tagText
    } else if (currentText.endsWith(' ')) {
      inputText.value = currentText + ', ' + tagText + ',';
    } else {
      inputText.value = currentText + ', ' + tagText + ',';
    }

    lastInputValue.value = inputText.value; // 更新上一次的输入内容
    // 触发输入事件以更新词组
    processInput()
  } else if (event.data.type === 'weilin_prompt_ui_user_history_tag') {
    const tagText = event.data.tagText
    tempInputText.value = tagText
    setPromptText(tagText)
  } else if (event.data.type === 'weilin_prompt_ui_refresh_all_data') {

  } else if (event.data.type === 'weilin_prompt_ui_translate_setting') {
    initTranslate()
  } else if (event.data.type === 'weilin_prompt_ui_selectLora') {
    // console.log(event.data.lora)
    if (event.data.lora.loraWorks != undefined && event.data.lora.loraWorks.length > 0) {
      // 在输入框末尾添加标签文本
      const currentText = inputText.value
      const tagText = event.data.lora.loraWorks

      // 检查当前文本是否为空或是否以空格结尾
      if (currentText === '') {
        inputText.value = tagText
      } else if (currentText.endsWith(' ')) {
        inputText.value = currentText + ', ' + tagText + ',';
      } else {
        inputText.value = currentText + ', ' + tagText + ',';
      }

      lastInputValue.value = inputText.value; // 更新上一次的输入内容
      // 触发输入事件以更新词组
      processInput()
    }
  } else if (event.data.type === 'weilin_prompt_ui_prompt_inner_get_node_tag_template_id_go_random_response') {
    onClickLocalTemplateRandomTag(event.data.data)
  } else if (event.data.type === 'weilin_prompt_ui_addLoraTag_inner') {
    // console.log(event.data.lora)
    if (event.data.lora.loraWorks != undefined && event.data.lora.loraWorks.length > 0) {
      // 在输入框末尾添加标签文本
      const currentText = inputText.value
      const tagText = event.data.lora.tag + (event.data.lora.loraWorks === '' ? "" : ", " + event.data.lora.loraWorks)

      // 检查当前文本是否为空或是否以空格结尾
      if (currentText === '') {
        inputText.value = tagText
      } else if (currentText.endsWith(' ')) {
        inputText.value = currentText + ', ' + tagText + ',';
      } else {
        inputText.value = currentText + ', ' + tagText + ',';
      }

      lastInputValue.value = inputText.value; // 更新上一次的输入内容
      // 触发输入事件以更新词组
      processInput()
    } else {
      // 在输入框末尾添加标签文本
      const currentText = inputText.value
      const tagText = event.data.lora.tag

      // 检查当前文本是否为空或是否以空格结尾
      if (currentText === '') {
        inputText.value = tagText
      } else if (currentText.endsWith(' ')) {
        inputText.value = currentText + ', ' + tagText + ',';
      } else {
        inputText.value = currentText + ', ' + tagText + ',';
      }

      lastInputValue.value = inputText.value; // 更新上一次的输入内容
      // 触发输入事件以更新词组
      processInput()
    }
  }
}

const initTranslate = async () => {
  const savedSourceLanguage = localStorage.getItem('weilin_prompt_ui_sourceLanguage') || 'english';
  const savedTargetLanguage = localStorage.getItem('weilin_prompt_ui_targetLanguage') || 'chinese_simplified';
  if (!localStorage.getItem('weilin_prompt_ui_sourceLanguage')) {
    localStorage.setItem('weilin_prompt_ui_sourceLanguage', savedSourceLanguage);
  }
  if (!localStorage.getItem('weilin_prompt_ui_targetLanguage')) {
    localStorage.setItem('weilin_prompt_ui_targetLanguage', savedTargetLanguage);
  }
  if (savedSourceLanguage !== 'auto') {
    translate.language.setLocal(savedSourceLanguage);
  }
  translate.language.setDefaultTo(savedTargetLanguage);
  // console.log(res)
}

const translateFunction = (texts, token) => {
  if (localStorage.getItem('weilin_prompt_ui_translater_setting') == 'network') {
    translate.request.translateText(texts, function (data) {
      if (data.result > 0) {
        const translatedText = data.text.map(item => item.replace(/[\[\]“”]/g, '')).join(', ');
        token.translate = translatedText
      }
      //打印翻译结果
      // console.log(data);
    });
  } else {
    translatorApi.translaterText(texts).then(res => {
      // console.log(res)
      if (res.text.length > 0) {
        token.translate = res.text;
      }
    })
  }
}

const finishTranslateEnter = () => {

  if (localStorage.getItem('weilin_prompt_ui_translater_setting') == 'network') {
    const restran = translate.language.recognition(translateText.value)
    var obj = {
      from: restran.languageName,
      to: 'english',
      texts: [translateText.value]
    }

    translate.request.translateText(obj, function (data) {
      if (data.result > 0) {
        const translatedText = data.text.map(item => item.replace(/[\[\]“”]/g, '')).join(', ');
        tokens.value.push({
          text: translatedText,
          translate: translateText.value,
          isPunctuation: false,
          isEditing: false,
          isHidden: false,
          color: ''
        });
        translateText.value = ''
        updateInputText()
      }
      //打印翻译结果
      // console.log(data);
    });
  } else {
    translatorApi.translaterInputText(translateText.value).then(res => {
      // console.log(res)
      if (res.text.length > 0) {
        tokens.value.push({
          text: res.text,
          translate: translateText.value,
          isPunctuation: false,
          isEditing: false,
          isHidden: false,
          color: ''
        });
        translateText.value = ''
        updateInputText()
      }
    })
  }

}


// 自动补全功能

const onBlur = () => {
  // 添加延迟处理，避免与自动补全点击冲突
  setTimeout(() => {
    if (!showAutocomplete.value) {
      lastInputValue.value = inputText.value; // 更新上一次的输入内容
      processInput();
    }
  }, 100);
}

// 提取补全逻辑到单独的函数
const triggerAutocomplete = (inputValue) => {
  // 处理特殊格式
  let cleanedTrSegment = inputValue.replace(/[\[\](){}]/g, '').trim();
  const text = extractText(cleanedTrSegment)

  // 清除输入值的前后空格
  const trimmedInput = text.trim();

  // 如果输入为空，隐藏补全框
  if (!trimmedInput) {
    showAutocomplete.value = false;
    return;
  }

  // 如果输入过长，直接返回
  if (trimmedInput.length > 20) {
    showAutocomplete.value = false;
    return;
  }

  try {
    // 优化匹配逻辑
    const lowerInput = trimmedInput.toLowerCase();

    autocompleteApi.getAutocomplete(String(lowerInput)).then(async (res) => {
      autocompleteResults.value = res.data
      // 更新补全结果
      await calculateAutocompletePosition();
      setTimeout(() => {
        saveAutoCompleteWidth.value = localStorage.getItem('weilin_prompt_ui_auto_box_width') || 450
        saveAutoCompleteHeight.value = localStorage.getItem('weilin_prompt_ui_auto_box_height') || 350
        showAutocomplete.value = autocompleteResults.value.length > 0;
        selectedAutocompleteIndex.value = 0; // 重置选中索引
      }, 50)
    })

  } catch (error) {
    console.error('Autocomplete error:', error);
    showAutocomplete.value = false;
  }
};

// 处理键盘事件
const handleKeydown = (event) => {
  if (showAutocomplete.value) {
    if (event.key === 'ArrowDown') {
      event.preventDefault();
      selectedAutocompleteIndex.value = Math.min(selectedAutocompleteIndex.value + 1, autocompleteResults.value.length - 1);
      scrollToSelectedItem();
    } else if (event.key === 'ArrowUp') {
      event.preventDefault();
      selectedAutocompleteIndex.value = Math.max(selectedAutocompleteIndex.value - 1, 0);
      scrollToSelectedItem();
    } else if (event.key === 'Tab' || event.key === 'Enter') {
      event.preventDefault();
      selectAutocomplete(selectedAutocompleteIndex.value, null, true);
    } else if (event.key === 'Escape') {
      event.preventDefault();
      closeAutocomplete();
    }
  }
};

// 添加滚动到选中项的函数
const scrollToSelectedItem = () => {
  nextTick(() => {
    if (selectedItemRef.value && autocompleteContainerRef.value) {
      const container = autocompleteContainerRef.value;
      const selectedItem = selectedItemRef.value;

      // 获取容器和选中项的位置信息
      const containerRect = container.getBoundingClientRect();
      const selectedRect = selectedItem.getBoundingClientRect();

      // 判断选中项是否在可视区域内
      const isAbove = selectedRect.top < containerRect.top;
      const isBelow = selectedRect.bottom > containerRect.bottom;

      if (isAbove) {
        // 如果选中项在可视区域上方，滚动到顶部
        container.scrollTop = container.scrollTop + (selectedRect.top - containerRect.top);
      } else if (isBelow) {
        // 如果选中项在可视区域下方，滚动到底部
        container.scrollTop = container.scrollTop + (selectedRect.bottom - containerRect.bottom);
      }
    }
  });
};

// 计算调整后的自动补全位置
const adjustedAutocompletePosition = computed(() => {
  if (!parentCneterBox.value) return { left: autocompletePosition.value.left };

  const parentWidth = parentCneterBox.value.offsetWidth;
  saveAutoCompleteWidth.value = localStorage.getItem('weilin_prompt_ui_auto_box_width') || 450
  const autocompleteWidth = saveAutoCompleteWidth.value;
  let left = autocompletePosition.value.left;

  // 检查是否会超出右侧边界
  if (left + autocompleteWidth > parentWidth) {
    // 将窗口贴在右侧边界
    left = parentWidth - autocompleteWidth;
  }

  // 确保不会超出左侧边界
  if (left < 0) {
    left = 0;
  }

  return { left };
});


const selectAutocomplete = (index, event) => {
  // 如果有event参数，阻止默认行为和事件冒泡
  if (event) {
    event.preventDefault();
    event.stopPropagation();
  }

  if (!autocompleteResults.value[index]) return;

  showAutocomplete.value = false;

  // 获取当前输入框的选区位置
  const cursorPosition = inputAreaRef.value.selectionStart;
  const cursorEnd = inputAreaRef.value.selectionEnd;

  // 获取当前输入文本
  const currentText = inputText.value;

  // 处理补全文本格式转换
  let tagText = autocompleteResults.value[index].text;

  // 应用所有格式转换
  if (localStorage.getItem('weilin_prompt_ui_comma_conversion') !== 'false') {
    tagText = tagText.replace(/，/g, ',');
  }
  if (localStorage.getItem('weilin_prompt_ui_period_conversion') !== 'false') {
    tagText = tagText.replace(/。/g, '.');
  }
  if (localStorage.getItem('weilin_prompt_ui_bracket_conversion') !== 'false') {
    tagText = tagText
      .replace(/【/g, '[')
      .replace(/】/g, ']')
      .replace(/（/g, '(')
      .replace(/）/g, ')');
  }
  if (localStorage.getItem('weilin_prompt_ui_angle_bracket_conversion') !== 'false') {
    tagText = tagText
      .replace(/《/g, '<')
      .replace(/》/g, '>');
  }
  if (localStorage.getItem('weilin_prompt_ui_underscore_to_bracket') === 'true') {
    tagText = tagText.replace(/_/g, ' ');
  }

  // 确定要替换的范围
  let replaceStart = cursorPosition;
  let replaceEnd = cursorEnd;

  // 向前查找单词边界
  while (replaceStart > 0 &&
    !/[,\s]/.test(currentText[replaceStart - 1])) {
    replaceStart--;
  }

  // 向后查找单词边界
  while (false && replaceEnd < currentText.length &&
    !/[,\s]/.test(currentText[replaceEnd])) {
    replaceEnd++;
  }

  // 执行替换
  let newText =
    currentText.substring(0, replaceStart) +
    tagText +
    currentText.substring(replaceEnd);

  // 如果右侧不是分隔符，在新 tag 与右侧之间补上分隔符，避免覆盖后续 tag
  if (currentText[replaceEnd] && !(/[\,\s]/.test(currentText[replaceEnd]))) {
    newText = currentText.substring(0, replaceStart) + tagText + ', ' + currentText.substring(replaceEnd);
  }

  // 计算新光标位置
  const separatorAdded = currentText[replaceEnd] && !(/[\,\s]/.test(currentText[replaceEnd]));
  const newCursorPosition = replaceStart + tagText.length + (separatorAdded ? 2 : 0);

  // 更新输入文本
  inputText.value = newText;
  lastInputValue.value = newText;

  // 触发输入处理
  processInput();

  // 恢复光标位置
  nextTick(() => {
    if (inputAreaRef.value) {
      inputAreaRef.value.selectionStart = newCursorPosition;
      inputAreaRef.value.selectionEnd = newCursorPosition;
    }
  });
};

// 关闭补全窗口
const closeAutocomplete = () => {
  showAutocomplete.value = false;
};

const setPromptText = (text) => {
  // console.log(text)
  if (text.length > 0) {
    try {
      const jsonStr = JSON.parse(text)

      inputText.value = jsonStr.prompt
      lastInputValue.value = inputText.value; // 更新上一次的输入内容

      if (jsonStr.lora && jsonStr.lora != "") {
        selectedLoras.value = jsonStr.lora
      }

      if (jsonStr.temp_prompt && jsonStr.temp_prompt != "") {
        // console.log(jsonStr.temp_prompt)
        const tempDataJson = jsonStr.temp_prompt
        // console.log(tempDataJson)
        let isOldVersion = false
        if (tempDataJson.tokens && tempDataJson.tokens.length > 0 && tempDataJson.tokens != "") {
          tokens.value = tempDataJson.tokens
          isOldVersion = true
        }
        if (tempDataJson.lora && tempDataJson.lora.length > 0 && tempDataJson.lora != "") {
          selectedLoras.value = tempDataJson.lora
          isOldVersion = true
        }

        if (!isOldVersion && tempDataJson.length > 0 && tempDataJson != "") {
          tokens.value = tempDataJson
        }

      }

      if (jsonStr.temp_lora && jsonStr.temp_lora.length > 0 && jsonStr.temp_lora != "") {
        const tempDataJson = jsonStr.temp_lora
        selectedLoras.value = tempDataJson
      }

      processInput()
    } catch (error) {
      // console.log('读取数据错误：', error)
      message({ type: "warn", str: 'promptBox.settings.errorPrompt' });
    }
  }
}

const dragStartIndex = ref(null);

const handleDragStart = (index, event) => {
  dragStartIndex.value = index;
  event.dataTransfer.effectAllowed = 'move';
};

const handleDragOver = (index, event) => {
  event.preventDefault();
  if (dragStartIndex.value !== null && dragStartIndex.value !== index) {
    const draggedItem = tokens.value[dragStartIndex.value];
    const newTokens = [...tokens.value];
    newTokens.splice(dragStartIndex.value, 1);
    newTokens.splice(index, 0, draggedItem);
    tokens.value = newTokens;
    dragStartIndex.value = index;
    updateInputText();
  }
};

const handleDrop = (index, event) => {
  event.preventDefault();
  dragStartIndex.value = null;
  updateInputText();
};

const updateInputText = () => {
  // 更新输入文本，保持原有格式，但排除隐藏的tokens
  inputText.value = tokens.value.length > 0
    ? tokens.value.reduce((acc, token, index) => {
      // 如果token是隐藏的，不添加到输入文本中
      if (token.isHidden) {
        return acc;
      }

      // 如果是换行符，不加逗号
      if (token.text === '\n') {
        // 查找前一个非隐藏token
        const prevNonHiddenIndex = findPrevNonHiddenIndex(index);
        const prevToken = prevNonHiddenIndex !== -1 ? tokens.value[prevNonHiddenIndex] : null;

        // 直接返回换行符，不添加额外的逗号
        // 因为前一个token在处理时已经根据shouldAddComma添加了逗号
        return acc + token.text;
      }

      // 第一个非隐藏token不加逗号前缀
      if (acc === '') {
        // 查找下一个非隐藏token
        let nextNonHiddenIndex = index + 1;
        while (nextNonHiddenIndex < tokens.value.length && tokens.value[nextNonHiddenIndex]?.isHidden) {
          nextNonHiddenIndex++;
        }

        // 判断是否是最后一个非隐藏token或者下一个是换行符
        const isLastToken = nextNonHiddenIndex >= tokens.value.length;
        const nextToken = nextNonHiddenIndex < tokens.value.length ? tokens.value[nextNonHiddenIndex] : null;
        const shouldAddComma = isLastToken || (nextToken && nextToken.text === '\n');

        return token.text + (shouldAddComma ? ',' : '');
      }

      // 查找下一个非隐藏token
      let nextNonHiddenIndex = index + 1;
      while (nextNonHiddenIndex < tokens.value.length && tokens.value[nextNonHiddenIndex]?.isHidden) {
        nextNonHiddenIndex++;
      }

      // 判断是否是最后一个非隐藏token
      const isLastToken = nextNonHiddenIndex >= tokens.value.length;
      const nextToken = nextNonHiddenIndex < tokens.value.length ? tokens.value[nextNonHiddenIndex] : null;

      // 如果是换行符前或者最后一个token，则添加逗号
      const shouldAddComma = (nextToken && nextToken.text === '\n') || isLastToken;

      // 前一个token是换行符，不加逗号前缀
      const prevNonHiddenIndex = findPrevNonHiddenIndex(index);
      if (prevNonHiddenIndex !== -1 && tokens.value[prevNonHiddenIndex].text === '\n') {
        return acc + token.text + (shouldAddComma ? ',' : '');
      }

      // 其他情况加逗号和空格前缀
      return acc + ', ' + token.text + (shouldAddComma ? ',' : '');
    }, '') : '';

  postMessageToWindowsPrompt()
};

// AI对话
const openAIChat = () => {
  window.parent.postMessage({ type: 'weilin_prompt_ui_openAiWindow' }, '*')
}

const openGitHub = () => {
  window.open('https://github.com/weilin9999/WeiLin-Comfyui-Tools', '_blank')
}

const shareCloudData = () => {
  window.parent.postMessage({ type: 'weilin_prompt_ui_open_cloud_window' }, '*')
}

const openDanbooruManager = () => {
  window.parent.postMessage({ type: 'weilin_prompt_ui_open_danbooru_manager_window' }, '*')
}

const openSponsor = () => {
  window.open('https://afdian.com/a/weilin9999', '_blank')
}

// 添加一个辅助函数来查找前一个非隐藏的token索引
const findPrevNonHiddenIndex = (currentIndex) => {
  for (let i = currentIndex - 1; i >= 0; i--) {
    if (!tokens.value[i].isHidden) {
      return i;
    }
  }
  return -1;
};

// 添加toggleHidden方法
const toggleHidden = (index) => {
  if (index >= 0 && index < tokens.value.length) {
    // 不允许隐藏换行符
    if (tokens.value[index].text === '\n' || tokens.value[index].text === '\t') {
      return;
    }

    // 切换隐藏状态
    tokens.value[index].isHidden = !tokens.value[index].isHidden;

    // 添加/移除隐藏提示
    if (tokens.value[index].isHidden) {
      tokens.value[index].hiddenHint = t('promptBox.hiddenHint'); // 使用国际化提示
    } else {
      tokens.value[index].hiddenHint = '';
    }

    // 更新输入文本，排除隐藏的tokens
    updateInputText();
  }
};

const openBilibili = () => {
  window.open('https://www.bilibili.com/list/288025756/?sid=4690314&spm_id_from=333.1387.0.0&oid=114342431298474&bvid=BV1txdfYxE7X', '_blank');
};

// 一键随机Tag方法
const oneClickRandomTag = async () => {
  if (props.promptManager == "prompt_global") {
    try {
      await randomTagApi.goRandomTemplate().then((res) => {
        if (res.code === 200) {
          // console.log(res.random_tags)
          inputText.value = res.random_tags
          nextTick(() => {
            // 触发输入处理
            processInput();
          })
        } else {
          message({ type: "warn", str: res.info });
        }
      }).catch((err) => {
        console.error(err);
        message({ type: "warn", str: 'message.networkError' });
      });
    } catch (error) {
      message({ type: "warn", str: 'message.networkError' });
      console.error('Error loading random tag settings:', error)
    }
  } else {
    window.postMessage({
      type: 'weilin_prompt_ui_prompt_inner_get_node_tag_template_id_gorandom'
    }, '*')
  }

};

const onClickLocalTemplateRandomTag = async (name) => {
  try {
    await randomTagApi.goRandomTemplatePath(name).then((res) => {
      if (res.code === 200) {
        // console.log(res.random_tags)
        inputText.value = res.random_tags
        nextTick(() => {
          // 触发输入处理
          processInput();
        })
      } else {
        message({ type: "warn", str: res.info });
      }
    }).catch((err) => {
      console.error(err);
      message({ type: "warn", str: 'message.networkError' });
    });
  } catch (error) {
    message({ type: "warn", str: 'message.networkError' });
    console.error('Error loading random tag settings:', error)
  }
}

/**
 * 从短码反向解析出原始路径
 * 
 * @param {string} shortcode - 短码
 * @returns {string} - 原始文件路径
 */
const shortcodeToPath = (shortcode) => {
  try {
    // 还原 Base64 编码中被替换的字符
    let base64Str = shortcode.replace(/-/g, '+').replace(/_/g, '/');

    // 添加回可能被移除的填充字符
    const padding = 4 - (base64Str.length % 4);
    if (padding < 4) {
      base64Str += '='.repeat(padding);
    }

    // 解码 Base64
    const binaryStr = atob(base64Str);

    // 将二进制字符串转换为 Uint8Array
    const bytes = new Uint8Array(binaryStr.length);
    for (let i = 0; i < binaryStr.length; i++) {
      bytes[i] = binaryStr.charCodeAt(i);
    }

    // 解压缩
    const decompressed = pako.inflate(bytes);

    // 将 Uint8Array 转换为字符串
    const decoder = new TextDecoder('utf-8');
    const path = decoder.decode(decompressed);

    return path;
  } catch (error) {
    console.error('解析短码时出错:', error);
    return '';
  }
};

// 打开随机Tag设置对话框
const openRandomTagSettings = () => {
  randomSettingItem.value.open(props.promptManager)
};

defineExpose({
  setPromptText
})
</script>

<style scoped>
@import "./prompt_index.css";
</style>
