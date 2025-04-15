<template>
    <div class="container">
        <h1>{{ currentTab === 'history' ? t('history.title') : t('history.favorites') }}</h1>
        <div class="tab-container">
            <button :class="{ active: currentTab === 'history' }" @click="currentTab = 'history'" class="tab-button">
                {{ t('history.history') }}
            </button>
            <button :class="{ active: currentTab === 'favorites' }" @click="currentTab = 'favorites'"
                class="tab-button">
                {{ t('history.favorites') }}
            </button>
        </div>
        <div v-if="currentTab === 'history'">
            <div class="search-container">
                <button class="refresh-btn" @click="refreshHistory">
                    <svg viewBox="0 0 24 24" width="16" height="16" class="refresh-icon">
                        <path
                            d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
                    </svg>
                </button>
                <input type="text" v-model="searchQuery" :placeholder="t('history.search_placeholder')"
                    @input="filterHistory" class="search-input" />
                <input type="checkbox" v-if="isDeleteBatch" v-model="selectAllTags" :value="1" class="tag-checkbox"
                    @change="selectAllTagsChange" />
                <button v-if="!isDeleteBatch" class="bulk-delete-btn" @click="bulkDelete"
                    :title="t('history.bulk_delete')">
                    <svg viewBox="0 0 1024 1024" width="16" height="16" class="delete-favorite-icon">
                        <path
                            d="M907.618072 232.742353 744.713682 232.742353 744.713682 116.382952c0-12.852708-10.419786-23.272495-23.272495-23.272495L302.556765 93.110457c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 116.360425L116.380904 232.743377c-12.852708 0-23.272495 10.419786-23.272495 23.272495s10.418762 23.272495 23.272495 23.272495l791.237168 0c12.852708 0 23.272495-10.419786 23.272495-23.272495S920.469756 232.742353 907.618072 232.742353zM325.829259 139.654423l372.340458 0 0 93.08793L325.829259 232.742353 325.829259 139.654423zM791.257647 372.362985c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 488.712146L256.012799 884.347625 256.012799 395.635479c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 511.983617c0 12.852708 10.418762 23.272495 23.272495 23.272495l558.516318 0c12.852708 0 23.272495-10.419786 23.272495-23.272495L814.529118 395.635479C814.529118 382.782771 804.110355 372.362985 791.257647 372.362985zM442.189684 767.987201l0-372.351721c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.418762 23.272495 23.272495 23.272495S442.189684 780.839909 442.189684 767.987201zM628.353257 767.987201l0-372.351721c0-12.852708-10.419786-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.419786 23.272495 23.272495 23.272495S628.353257 780.839909 628.353257 767.987201z">
                        </path>
                    </svg>
                </button>
                <button v-if="isDeleteBatch" class="bulk-delete-btn" @click="sureDelete"
                    :title="t('history.sure_delete')" :disabled="selectedTags.length === 0">
                    <svg viewBox="0 0 1024 1024" width="16" height="16" class="delete-favorite-icon">
                        <path
                            d="M392.533333 806.4L85.333333 503.466667l59.733334-59.733334 247.466666 247.466667L866.133333 213.333333l59.733334 59.733334L392.533333 806.4z">
                        </path>
                    </svg>
                </button>
                <button v-if="isDeleteBatch" class="bulk-delete-btn" @click="cancelDelete"
                    :title="t('history.cancel_delete')">
                    <svg viewBox="0 0 1024 1024" width="16" height="16" class="delete-favorite-icon">
                        <path
                            d="M794.8 794.8c-14 14-36.9 14-50.9 0L229.2 280.1c-14-14-14-36.9 0-50.9s36.9-14 50.9 0L794.9 744c13.9 13.9 13.9 36.8-0.1 50.8z">
                        </path>
                        <path
                            d="M794.8 229.2c14 14 14 36.9 0 50.9L280.1 794.8c-14 14-36.9 14-50.9 0s-14-36.9 0-50.9L744 229.1c13.9-13.9 36.8-13.9 50.8 0.1z">
                        </path>
                    </svg>
                </button>
            </div>
            <ul class="history-list">
                <li v-for="item in filteredHistory" :key="item.id_index" class="history-item">
                    <span>{{ item.tag }}</span>
                    <div class="action-buttons">
                        <button @click="addToFavorites(item)" class="favorite-btn"
                            :title="t('history.add_to_favorites')">
                            <svg viewBox="0 0 24 24" width="24" height="24" class="favorite-icon">
                                <path
                                    d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z" />
                            </svg>
                        </button>
                        <button @click="deleteHistory(item)" class="delete-favorite-btn"
                            :title="t('history.delete_history')">
                            <svg viewBox="0 0 1024 1024" width="24" height="24" class="delete-favorite-icon">
                                <path
                                    d="M907.618072 232.742353 744.713682 232.742353 744.713682 116.382952c0-12.852708-10.419786-23.272495-23.272495-23.272495L302.556765 93.110457c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 116.360425L116.380904 232.743377c-12.852708 0-23.272495 10.419786-23.272495 23.272495s10.418762 23.272495 23.272495 23.272495l791.237168 0c12.852708 0 23.272495-10.419786 23.272495-23.272495S920.469756 232.742353 907.618072 232.742353zM325.829259 139.654423l372.340458 0 0 93.08793L325.829259 232.742353 325.829259 139.654423zM791.257647 372.362985c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 488.712146L256.012799 884.347625 256.012799 395.635479c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 511.983617c0 12.852708 10.418762 23.272495 23.272495 23.272495l558.516318 0c12.852708 0 23.272495-10.419786 23.272495-23.272495L814.529118 395.635479C814.529118 382.782771 804.110355 372.362985 791.257647 372.362985zM442.189684 767.987201l0-372.351721c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.418762 23.272495 23.272495 23.272495S442.189684 780.839909 442.189684 767.987201zM628.353257 767.987201l0-372.351721c0-12.852708-10.419786-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.419786 23.272495 23.272495 23.272495S628.353257 780.839909 628.353257 767.987201z">
                                </path>
                            </svg>
                        </button>
                        <button @click="useItem(item)" class="use-btn" :title="t('history.use_item')">
                            <svg viewBox="0 0 1024 1024" width="24" height="24" class="use-icon">
                                <path
                                    d="M915.515273 142.819385 98.213046 458.199122c-46.058539 17.772838-44.90475 43.601756 2.348455 57.622994l197.477685 58.594874 80.292024 238.91085c10.51184 31.277988 37.972822 37.873693 61.462483 14.603752l103.584447-102.611545 204.475018 149.840224c26.565749 19.467242 53.878547 9.222132 61.049613-23.090076l149.210699-672.34491C965.264096 147.505054 946.218922 130.971848 915.515273 142.819385zM791.141174 294.834331l-348.61988 310.610267c-6.268679 5.58499-11.941557 16.652774-12.812263 24.846818l-15.390659 144.697741c-1.728128 16.24808-7.330491 16.918483-12.497501 1.344894l-67.457277-203.338603c-2.638691-7.954906 0.975968-17.705389 8.022355-21.931178l442.114555-265.181253C812.67481 268.984974 815.674251 272.975713 791.141174 294.834331z"
                                    p-id="18085"></path>
                            </svg>
                        </button>
                        <input type="checkbox" v-if="isDeleteBatch" v-model="selectedTags" :value="item.id_index"
                            class="tag-checkbox" />
                    </div>
                </li>
            </ul>
        </div>
        <div v-else>
            <div class="search-container">
                <button class="refresh-btn" @click="refreshFavorites">
                    <svg viewBox="0 0 24 24" width="16" height="16" class="refresh-icon">
                        <path
                            d="M17.65 6.35C16.2 4.9 14.21 4 12 4c-4.42 0-7.99 3.58-7.99 8s3.57 8 7.99 8c3.73 0 6.84-2.55 7.73-6h-2.08c-.82 2.33-3.04 4-5.65 4-3.31 0-6-2.69-6-6s2.69-6 6-6c1.66 0 3.14.69 4.22 1.78L13 11h7V4l-2.35 2.35z" />
                    </svg>
                </button>
                <input type="text" v-model="searchQuery" :placeholder="t('history.search_placeholder')"
                    @input="filterFavorites" class="search-input" />
                
                <input type="checkbox" v-if="isDeleteBatch" v-model="selectAllTags" :value="1" class="tag-checkbox"
                    @change="selectAllTagsChange" />
                
                <button class="add-his-btn" @click="showAddTagDialog" :title="t('history.add_new')">
                    <svg viewBox="0 0 24 24" width="16" height="16" class="add-icon">
                        <path d="M19 11h-6V5c0-.55-.45-1-1-1s-1 .45-1 1v6H5c-.55 0-1 .45-1 1s.45 1 1 1h6v6c0 .55.45 1 1 1s1-.45 1-1v-6h6c.55 0 1-.45 1-1s-.45-1-1-1z"/>
                    </svg>
                </button>
                <button v-if="!isDeleteBatch" class="bulk-delete-btn" @click="bulkDelete"
                    :title="t('history.bulk_delete')">
                    <svg viewBox="0 0 1024 1024" width="16" height="16" class="delete-favorite-icon">
                        <path
                            d="M907.618072 232.742353 744.713682 232.742353 744.713682 116.382952c0-12.852708-10.419786-23.272495-23.272495-23.272495L302.556765 93.110457c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 116.360425L116.380904 232.743377c-12.852708 0-23.272495 10.419786-23.272495 23.272495s10.418762 23.272495 23.272495 23.272495l791.237168 0c12.852708 0 23.272495-10.419786 23.272495-23.272495S920.469756 232.742353 907.618072 232.742353zM325.829259 139.654423l372.340458 0 0 93.08793L325.829259 232.742353 325.829259 139.654423zM791.257647 372.362985c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 488.712146L256.012799 884.347625 256.012799 395.635479c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 511.983617c0 12.852708 10.418762 23.272495 23.272495 23.272495l558.516318 0c12.852708 0 23.272495-10.419786 23.272495-23.272495L814.529118 395.635479C814.529118 382.782771 804.110355 372.362985 791.257647 372.362985zM442.189684 767.987201l0-372.351721c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.418762 23.272495 23.272495 23.272495S442.189684 780.839909 442.189684 767.987201zM628.353257 767.987201l0-372.351721c0-12.852708-10.419786-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.419786 23.272495 23.272495 23.272495S628.353257 780.839909 628.353257 767.987201z">
                        </path>
                    </svg>
                </button>
                <button v-if="isDeleteBatch" class="bulk-delete-btn" @click="sureDeleteFavorite"
                    :title="t('history.sure_delete')" :disabled="selectedTags.length === 0">
                    <svg viewBox="0 0 1024 1024" width="16" height="16" class="delete-favorite-icon">
                        <path
                            d="M392.533333 806.4L85.333333 503.466667l59.733334-59.733334 247.466666 247.466667L866.133333 213.333333l59.733334 59.733334L392.533333 806.4z">
                        </path>
                    </svg>
                </button>
                <button v-if="isDeleteBatch" class="bulk-delete-btn" @click="cancelDelete"
                    :title="t('history.cancel_delete')">
                    <svg viewBox="0 0 1024 1024" width="16" height="16" class="delete-favorite-icon">
                        <path
                            d="M794.8 794.8c-14 14-36.9 14-50.9 0L229.2 280.1c-14-14-14-36.9 0-50.9s36.9-14 50.9 0L794.9 744c13.9 13.9 13.9 36.8-0.1 50.8z">
                        </path>
                        <path
                            d="M794.8 229.2c14 14 14 36.9 0 50.9L280.1 794.8c-14 14-36.9 14-50.9 0s-14-36.9 0-50.9L744 229.1c13.9-13.9 36.8-13.9 50.8 0.1z">
                        </path>
                    </svg>
                </button>
            </div>
            <ul class="history-list">
                <li v-for="item in filteredFavorites" :key="item.id_index" class="history-item">
                    <div class="favor-name-box" :style="{ backgroundColor: item.color || 'transparent' }" >
                        <span class="favor-name"v-if="item.name.length > 0" >{{ item.name }}</span>
                    </div>
                    <span>{{ item.tag }}</span>
                    <div class="action-buttons">
                        <button @click="editTag(item)" class="delete-favorite-btn" :title="t('history.edit_favorite')">
                            <svg viewBox="0 0 1024 1024" width="24" height="24" class="delete-favorite-icon">
                                <path
                                    d="M200.59 626.48v129.5h129.5l381.93-381.93-129.5-129.5-381.93 381.93z m611.56-352.57c13.45-13.41 13.48-35.18 0.07-48.62l-0.07-0.07-80.81-80.81c-13.41-13.45-35.18-13.48-48.62-0.07l-0.07 0.07-63.19 63.19 129.5 129.5 63.19-63.19zM131.52 824.96h759.71c23.02 0 34.53 11.51 34.53 34.53 0 23.02-11.51 34.53-34.53 34.53H131.52c-23.02 0-34.53-11.51-34.53-34.53 0-23.02 11.51-34.53 34.53-34.53z"
                                    p-id="2346"></path>
                            </svg>
                        </button>
                        <button @click="deleteFavorite(item)" class="delete-favorite-btn"
                            :title="t('history.delete_favorite')">
                            <svg viewBox="0 0 1024 1024" width="24" height="24" class="delete-favorite-icon">
                                <path
                                    d="M907.618072 232.742353 744.713682 232.742353 744.713682 116.382952c0-12.852708-10.419786-23.272495-23.272495-23.272495L302.556765 93.110457c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 116.360425L116.380904 232.743377c-12.852708 0-23.272495 10.419786-23.272495 23.272495s10.418762 23.272495 23.272495 23.272495l791.237168 0c12.852708 0 23.272495-10.419786 23.272495-23.272495S920.469756 232.742353 907.618072 232.742353zM325.829259 139.654423l372.340458 0 0 93.08793L325.829259 232.742353 325.829259 139.654423zM791.257647 372.362985c-12.852708 0-23.272495 10.418762-23.272495 23.272495l0 488.712146L256.012799 884.347625 256.012799 395.635479c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 511.983617c0 12.852708 10.418762 23.272495 23.272495 23.272495l558.516318 0c12.852708 0 23.272495-10.419786 23.272495-23.272495L814.529118 395.635479C814.529118 382.782771 804.110355 372.362985 791.257647 372.362985zM442.189684 767.987201l0-372.351721c0-12.852708-10.418762-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.418762 23.272495 23.272495 23.272495S442.189684 780.839909 442.189684 767.987201zM628.353257 767.987201l0-372.351721c0-12.852708-10.419786-23.272495-23.272495-23.272495s-23.272495 10.418762-23.272495 23.272495l0 372.351721c0 12.852708 10.419786 23.272495 23.272495 23.272495S628.353257 780.839909 628.353257 767.987201z">
                                </path>
                            </svg>
                        </button>
                        <button @click="useItem(item)" class="use-btn" :title="t('history.use_favorite')">
                            <svg viewBox="0 0 1024 1024" width="24" height="24" class="use-icon">
                                <path
                                    d="M915.515273 142.819385 98.213046 458.199122c-46.058539 17.772838-44.90475 43.601756 2.348455 57.622994l197.477685 58.594874 80.292024 238.91085c10.51184 31.277988 37.972822 37.873693 61.462483 14.603752l103.584447-102.611545 204.475018 149.840224c26.565749 19.467242 53.878547 9.222132 61.049613-23.090076l149.210699-672.34491C965.264096 147.505054 946.218922 130.971848 915.515273 142.819385zM791.141174 294.834331l-348.61988 310.610267c-6.268679 5.58499-11.941557 16.652774-12.812263 24.846818l-15.390659 144.697741c-1.728128 16.24808-7.330491 16.918483-12.497501 1.344894l-67.457277-203.338603c-2.638691-7.954906 0.975968-17.705389 8.022355-21.931178l442.114555-265.181253C812.67481 268.984974 815.674251 272.975713 791.141174 294.834331z"
                                    p-id="18085"></path>
                            </svg>
                        </button>
                        <input type="checkbox" v-if="isDeleteBatch" v-model="selectedTags" :value="item.id_index"
                            class="tag-checkbox" />
                    </div>
                </li>
            </ul>
        </div>

        <!-- 标签对话框 -->
        <div v-if="showTagDialog" class="dialog-overlay">
            <div class="dialog-content" @mousedown.stop>
                <div class="dialog-header">
                    <h2>{{ isEditingTag ? t('history.dialog.edit_tag') : t('history.dialog.add_tag') }}</h2>
                    <button class="close-btn" @click="closeTagDialog">×</button>
                </div>
                <div class="dialog-body">
                    <div class="form-group">
                        <label>{{ t('history.dialog.name') }}</label>
                        <input type="text" v-model="currentTag.name"
                            :placeholder="t('history.dialog.name_placeholder')">
                    </div>
                    <div class="form-group">
                        <label>{{ t('history.dialog.tag') }}</label>
                        <textarea v-model="currentTag.tag" :placeholder="t('history.dialog.tag_placeholder')" rows="4">
                        </textarea>
                    </div>
                    <div class="form-group">
                        <label>{{ t('history.dialog.background_color') }}</label>
                        <div class="color-picker">
                            <div class="color-preview" :style="{ backgroundColor: previewColor }">
                            </div>
                            <div class="color-controls">
                                <input type="color" v-model="colorPickerState.hex" @input="updateColor"
                                    class="color-input">
                                <div class="alpha-control">
                                    <input type="range" v-model.number="colorPickerState.alpha" min="0" max="100"
                                        @input="updateColor" class="alpha-slider">
                                    <span class="alpha-value">{{ colorPickerState.alpha }}%</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="dialog-footer">
                    <button class="cancel-btn" @click="closeTagDialog">{{ t('common.cancel') }}</button>
                    <button class="confirm-btn" @click="saveTag">{{ t('common.confirm') }}</button>
                </div>
            </div>
        </div>

        <!-- 确认删除对话框 -->
        <div v-if="showDeleteDialog" class="dialog-overlay">
            <div class="dialog-content confirm-dialog" @mousedown.stop>
                <div class="dialog-header">
                    <h2>{{ t('common.confirmDelete') }}</h2>
                    <button class="close-btn" @click="closeDeleteDialog">×</button>
                </div>
                <div class="dialog-body">
                    <p class="confirm-message">{{ deleteConfirmMessage }}</p>
                </div>
                <div class="dialog-footer">
                    <button class="cancel-btn" @click="closeDeleteDialog">{{ t('common.cancel') }}</button>
                    <button class="delete-btn" @click="confirmDelete">{{ t('common.delete') }}</button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { historyApi } from "@/api/history";
import message from "@/utils/message";
import { useI18n } from 'vue-i18n'

const { t } = useI18n()
const searchQuery = ref('');
const history = ref([]); // 存储历史记录
const filteredHistory = ref([]); // 存储过滤后的历史记录
const favorites = ref([]); // 存储收藏夹记录
const filteredFavorites = ref([]); // 存储过滤后的收藏夹记录
const currentTab = ref('history'); // 当前选中的标签
const selectedTags = ref([]);
const showTagDialog = ref(false)
const showDeleteDialog = ref(false)
const isEditingTag = ref(false)
const colorPickerState = ref({
    hex: 'rgba(255, 123, 2, .4)',
    alpha: 100
})
const currentTag = ref({
    name: '',
    tag: '',
    color: 'rgba(255, 123, 2, .4)'
})

const isDeleteBatch = ref(false)
const selectAllTags = ref(0)

// 改进的 RGBA 解析函数
const parseRgba = (rgba) => {
    if (!rgba || rgba === 'transparent') {
        return { hex: '#FFFFFF', alpha: 0 }
    }

    const match = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/)
    if (match) {
        const [, r, g, b, a] = match
        const hex = '#' + [r, g, b].map(x => {
            const hex = parseInt(x).toString(16)
            return hex.length === 1 ? '0' + hex : hex
        }).join('')

        return {
            hex: hex,
            alpha: Math.round((a || 1) * 100)
        }
    }
    return { hex: '#FFFFFF', alpha: 0 }
}

// 初始化颜色选择器
const initColorPicker = (color) => {
    const { hex, alpha } = parseRgba(color)
    colorPickerState.value = { hex, alpha }
}

// 显示添加标签对话框
const showAddTagDialog = () => {
    isEditingTag.value = false
    currentTag.value = {
        id: '',
        name: '',
        tag: '',
        backgroundColor: 'transparent' // 设置默认颜色
    }
    // 初始化颜色选择器
    initColorPicker('transparent')
    showTagDialog.value = true
}

const rgbaToColorPickerState = (rgba) => {
    const match = rgba.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)(?:,\s*([0-9.]+))?\)/);
    if (match) {
        const [, r, g, b, a] = match;
        const hex = `#${((1 << 24) + (parseInt(r) << 16) + (parseInt(g) << 8) + parseInt(b)).toString(16).slice(1)}`;
        const alpha = a ? Math.round(parseFloat(a) * 100) : 100; // 将 alpha 转换为百分比
        return { hex, alpha };
    }
    return { hex: '#FF7B02', alpha: 50 }; // 默认值
};

// 编辑标签
const editTag = (tag) => {
    isEditingTag.value = true
    currentTag.value = { ...tag }
    colorPickerState.value = rgbaToColorPickerState(tag.color)
    showTagDialog.value = true
}


// 更新颜色（统一处理分类和标签）
const updateColor = () => {
  const color = hexToRgba(colorPickerState.value.hex, colorPickerState.value.alpha)
  currentTag.value.color = color
}


// 关闭标签对话框
const closeTagDialog = () => {
    showTagDialog.value = false
    currentTag.value = {
        name: '',
        tag: '',
        color: 'rgba(255, 123, 2, .4)'
    }
    isEditingTag.value = false
}

const deleteType = ref('')
const itemToDelete = ref(null)
const deleteConfirmMessage = computed(() => {
    if (!itemToDelete.value) return ''

    switch (deleteType.value) {
        case 'history':
            return t('history.deleteHistoryConfirm', { name: itemToDelete.value.tag })
        case 'favorite':
            return t('history.deleteFavoriteConfirm', { name: itemToDelete.value.tag })
        case 'deleteSelected':
            return t('history.confirmDeleteSelected')
        case 'deleteSelectedFavorite':
            return t('history.confirmDeleteSelected')
        default:
            return ''
    }
})

const deleteHistory = (history) => {
    deleteType.value = 'history'
    itemToDelete.value = history
    showDeleteDialog.value = true
}

const deleteFavorite = (favorite) => {
    deleteType.value = 'favorite'
    itemToDelete.value = favorite
    showDeleteDialog.value = true
}

const sureDelete = () => {
    isDeleteBatch.value = false
    selectAllTags.value = 0
    deleteType.value = 'deleteSelected'
    itemToDelete.value = selectedTags.value
    showDeleteDialog.value = true
}

const sureDeleteFavorite = () => {
    isDeleteBatch.value = false
    selectAllTags.value = 0
    deleteType.value = 'deleteSelectedFavorite'
    itemToDelete.value = selectedTags.value
    showDeleteDialog.value = true
}

// 确认删除
const confirmDelete = async () => {
    try {
        switch (deleteType.value) {
            case 'history':
                historyApi
                    .deleteHistory(itemToDelete.value.id_index)
                    .then((res) => {
                        fetchHistory()
                        message({ type: "success", str: 'message.deleteSuccess' });
                    })
                    .catch((err) => {
                        message({ type: "warn", str: 'message.networkError' });
                    });
                break

            case 'favorite':
                historyApi
                    .deleteFavorite(itemToDelete.value.id_index)
                    .then((res) => {
                        fetchFavorites()
                        window.postMessage({
                            type: 'weilin_prompt_ui_refresh_all_data',
                        }, '*')
                        message({ type: "success", str: 'message.deleteSuccess' });
                    })
                    .catch((err) => {
                        message({ type: "warn", str: 'message.networkError' });
                    });
                break
            case 'deleteSelected':
                historyApi.
                    batchDeleteHistory(selectedTags.value)
                    .then((res) => {
                        fetchHistory()
                        message({ type: "success", str: 'message.deleteSuccess' });
                    })
                    .catch((err) => {
                        message({ type: "warn", str: 'message.networkError' });
                    });
                break
            case 'deleteSelectedFavorite':
                historyApi
                    .batchDeleteFavorite(itemToDelete.value)
                    .then((res) => {
                        fetchFavorites()
                        window.postMessage({
                            type: 'weilin_prompt_ui_refresh_all_data',
                        }, '*')
                        message({ type: "success", str: 'message.deleteSuccess' });
                    })
                    .catch((err) => {
                        message({ type: "warn", str: 'message.networkError' });
                    });
                break
        }

        closeDeleteDialog()
    } catch (error) {
        message({ type: "warn", str: 'message.networkError' });
    }
}

const selectAllTagsChange = (event) => {
    if (event.target.checked) {
        if (currentTab.value === 'history') {
            selectedTags.value = history.value.map(item => item.id_index)
        } else {
            selectedTags.value = favorites.value.map(item => item.id_index)
        }
    } else {
        selectedTags.value = []
    }
}

// 改进的 RGBA 转换函数
const hexToRgba = (hex, alpha) => {
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${alpha / 100})`
}

// 关闭删除对话框
const closeDeleteDialog = () => {
    showDeleteDialog.value = false
    deleteType.value = ''
    itemToDelete.value = null
}

// 保存标签
const saveTag = () => {
    if (!currentTag.value.tag) {
        message({ type: "warn", str: 'history.dialog.tag_placeholder' });
        return
    }

    if (isEditingTag.value) {
        historyApi
            .editFavorite({
                id_index: currentTag.value.id_index,
                name: currentTag.value.name,
                tag: currentTag.value.tag,
                color: currentTag.value.color,
            })
            .then((res) => {
                fetchFavorites()
                window.postMessage({
                    type: 'weilin_prompt_ui_refresh_all_data',
                }, '*')
                message({ type: "success", str: 'message.editSuccess' });
            })
            .catch((err) => {
                message({ type: "warn", str: 'message.networkError' });
            });
    } else {
        historyApi
            .addFavorite({
                name: currentTag.value.name,
                tag: currentTag.value.tag,
                color: currentTag.value.color,
            })
            .then((res) => {
                fetchFavorites()
                window.postMessage({
                    type: 'weilin_prompt_ui_refresh_all_data',
                }, '*')
                message({ type: "success", str: 'message.addSuccess' });
            })
            .catch((err) => {
                message({ type: "warn", str: 'message.networkError' });
            });
    }

    closeTagDialog()
}


const fetchHistory = () => {
    historyApi
        .getHistory({})
        .then((res) => {
            history.value = res.data;
            filteredHistory.value = history.value; // 初始化过滤后的历史记录
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
        });
};

const fetchFavorites = () => {
    historyApi
        .getFavorite()
        .then((res) => {
            favorites.value = res.data;
            filteredFavorites.value = favorites.value;
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
        });
};

const filterHistory = () => {
    // 根据搜索查询过滤历史记录
    filteredHistory.value = history.value.filter(item =>
        item.tag.includes(searchQuery.value)
    );
};

const filterFavorites = () => {
    // 根据搜索查询过滤收藏夹记录
    filteredFavorites.value = favorites.value.filter(item =>
        item.tag.includes(searchQuery.value)
    );
};

const refreshHistory = () => {
    // 刷新历史记录
    fetchHistory();
};

const refreshFavorites = () => {
    // 刷新收藏夹记录
    fetchFavorites();
};

const addToFavorites = (item) => {
    // 添加到收藏夹的逻辑
    historyApi
        .addFavorite({ tag: item.tag })
        .then((res) => {
            if (res.code === 200) {
                window.postMessage({
                    type: 'weilin_prompt_ui_refresh_all_data',
                }, '*')
                fetchFavorites()
                message({ type: "success", str: 'message.addFavoriteSuccess' });
            } else {
                message({ type: "success", str: 'message.addFavoriteIsExist' });
            }
        })
        .catch((err) => {
            message({ type: "warn", str: 'message.networkError' });
        });
};

const useItem = (item) => {
    // 发送消息通知
    window.postMessage({
        type: 'weilin_prompt_ui_user_history_tag',
        tagText: item.tag
    }, '*')
};


const bulkDelete = () => {
    selectedTags.value = []
    isDeleteBatch.value = true
};

const cancelDelete = () => {
    selectedTags.value = []
    isDeleteBatch.value = false
    selectAllTags.value = 0
}

onMounted(() => {
    fetchHistory();
    fetchFavorites();
});
</script>

<style scoped>
/* 添加样式 */
.container {
    margin: 0 auto;
    padding: 20px;
}

h1 {
    font-size: 28px;
    text-align: center;
    color: var(--weilin-prompt-ui-primary-text);
}

.tab-container {
    display: flex;
    justify-content: center;
    margin-bottom: 20px;
}

.tab-button {
    padding: 10px 20px;
    border: none;
    border-radius: 4px;
    background-color: var(--weilin-prompt-ui-secondary-bg);
    color: var(--weilin-prompt-ui-primary-text);
    cursor: pointer;
    transition: background-color 0.3s;
    margin: 0 5px;
}

.tab-button.active {
    background-color: var(--weilin-prompt-ui-primary-color);
    color: white;
}

.tab-button:hover {
    background-color: var(--weilin-prompt-ui-primary-color);
}

.search-container {
    display: flex;
    justify-content: space-between;
    margin-bottom: 20px;
}

.search-input {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-primary-text);
    font-size: 14px;
}

.search-input:focus {
    outline: none;
    border-color: var(--weilin-prompt-ui-primary-color);
    box-shadow: 0 0 0 2px var(--weilin-prompt-ui-primary-color-fade);
}

.history-list {
    list-style-type: none;
    padding: 0;
}

.history-item {
    padding: 10px;
    margin: 5px 0;
    background-color: var(--weilin-prompt-ui-token-bg);
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    transition: box-shadow 0.3s;
}

.history-item:hover {
    box-shadow: 0 2px 5px var(--weilin-prompt-ui-hover-bg-color);
}

.refresh-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-secondary-bg);
    cursor: pointer;
    transition: all 0.2s ease;
    margin-right: 10px;
}

.refresh-btn:hover {
    background: var(--weilin-prompt-ui-hover-bg);
    border-color: var(--weilin-prompt-ui-primary-color);
}

.refresh-icon {
    fill: var(--weilin-prompt-ui-primary-text);
}

.action-buttons {
    padding-top: 10px;
    display: flex;
    gap: 8px;
    /* 按钮之间的间距 */
}

.favorite-btn,
.delete-favorite-btn,
.use-btn {
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-secondary-bg);
    cursor: pointer;
    transition: transform .2s;
    width: 25px;
    height: 25px;
    font-size: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
}

.favorite-btn:hover,
.delete-favorite-btn:hover,
.use-btn:hover {
    transform: scale(1.1);
    /* 悬停时放大效果 */
}

.favorite-icon,
.delete-favorite-icon,
.use-icon {
    fill: var(--weilin-prompt-ui-primary-text);
}

.tag-checkbox {
    margin-left: 3px;
    /* 复选框与标签文本之间的间距 */
}

.add-his-btn,
.bulk-delete-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 32px;
    height: 32px;
    padding: 0;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-secondary-bg);
    cursor: pointer;
    transition: all 0.2s ease;
    margin-left: 10px;
}

.add-his-btn:hover,
.bulk-delete-btn:hover {
    background: var(--weilin-prompt-ui-hover-bg);
    border-color: var(--weilin-prompt-ui-primary-color);
}

.add-icon,
.bulk-delete-icon {
    fill: var(--weilin-prompt-ui-primary-text);
}



/* 对话框样式 */
.dialog-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 9999;
}

.dialog-content {
    background: var(--weilin-prompt-ui-primary-bg);
    border-radius: 8px;
    min-width: 400px;
    max-width: 90%;
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
    box-sizing: border-box;
}

.dialog-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid var(--weilin-prompt-ui-border-color);
}

.dialog-header h2 {
    margin: 0;
    font-size: 18px;
    color: var(--primary-text);
}

.dialog-body {
    padding: 20px;
    box-sizing: border-box;
}

.dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 20px;
    border-top: 1px solid var(--border-color);
}

.form-group {
    margin-bottom: 16px;
    box-sizing: border-box;
    width: 100%;
}

.form-group:last-child {
    margin-bottom: 0;
}

.form-group label {
    display: block;
    margin-bottom: 8px;
    color: var(--primary-text);
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: 8px 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-input-bg);
    color: var(--weilin-prompt-ui-primary-text);
    font-size: 14px;
    transition: all 0.3s ease;
    box-sizing: border-box;
}

.form-group textarea {
    resize: vertical;
    min-height: 100px;
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--weilin-prompt-ui-primary-color);
    box-shadow: 0 0 0 2px rgba(var(--weilin-prompt-ui-primary-color-rgb), 0.1);
}

.cancel-btn,
.confirm-btn {
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.cancel-btn {
    background: none;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    color: var(--weilin-prompt-ui-secondary-text);
}

.confirm-btn {
    background: var(--weilin-prompt-ui-primary-color);
    border: none;
    color: white;
}

.cancel-btn:hover {
    background: var(--weilin-prompt-ui-hover-bg-color);
}

.confirm-btn:hover {
    opacity: 0.9;
}

.close-btn {
    border: none;
    background: none;
    font-size: 20px;
    color: var(--weilin-prompt-ui-secondary-text);
    cursor: pointer;
    padding: 4px;
    line-height: 1;
}

.close-btn:hover {
    color: var(--weilin-prompt-ui-primary-text);
}

/* 确认对话框特定样式 */
.confirm-dialog {
    min-width: 300px !important;
    max-width: 400px !important;
    width: 90%;
    box-sizing: border-box;
}

.confirm-message {
    margin: 0;
    color: var(--weilin-prompt-ui-primary-text);
    text-align: center;
}

.delete-btn {
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    background: var(--weilin-prompt-ui-danger-color, #ff4d4f);
    border: none;
    color: white;
    transition: all 0.3s ease;
}

.delete-btn:hover {
    opacity: 0.9;
}

.has-delete-action-btn {
    background: var(--weilin-prompt-ui-primary-color);
    border: none;
    color: white;
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.has-delete-action-btn:hover {
    opacity: 0.9;
}

.cancel-delete-btn {
    background: none;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    color: var(--weilin-prompt-ui-secondary-text);
    padding: 8px 16px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.cancel-delete-btn:hover {
    background: var(--weilin-prompt-ui-hover-bg-color);
}

/* 对话框动画 */
.dialog-overlay {
    animation: fadeIn 0.2s ease;
}

.dialog-content {
    animation: slideIn 0.2s ease;
}

@keyframes fadeIn {
    from {
        opacity: 0;
    }

    to {
        opacity: 1;
    }
}

@keyframes slideIn {
    from {
        transform: translateY(-20px);
        opacity: 0;
    }

    to {
        transform: translateY(0);
        opacity: 1;
    }
}

.color-picker {
    display: flex;
    gap: 12px;
    padding: 12px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    background: var(--weilin-prompt-ui-secondary-bg);
}

.color-preview {
    width: 48px;
    height: 48px;
    border-radius: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    background-image: linear-gradient(45deg, #ccc 25%, transparent 25%),
        linear-gradient(-45deg, #ccc 25%, transparent 25%),
        linear-gradient(45deg, transparent 75%, #ccc 75%),
        linear-gradient(-45deg, transparent 75%, #ccc 75%);
    background-size: 10px 10px;
    background-position: 0 0, 0 5px, 5px -5px, -5px 0px;
}

.color-controls {
    flex: 1;
    display: flex;
    flex-direction: column;
    gap: 8px;
}

.color-input {
    width: 100%;
    height: 32px;
    padding: 0;
    border: 1px solid var(--weilin-prompt-ui-border-color);
    border-radius: 4px;
    cursor: pointer;
}

.alpha-control {
    display: flex;
    align-items: center;
    gap: 8px;
}

.alpha-slider {
    flex: 1;
    height: 8px;
    -webkit-appearance: none;
    background: linear-gradient(to right, transparent, currentColor);
    border-radius: 4px;
    border: 1px solid var(--weilin-prompt-ui-border-color);
}

.alpha-slider::-webkit-slider-thumb {
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border-radius: 50%;
    background: var(--weilin-prompt-ui-primary-color);
    cursor: pointer;
    border: 2px solid white;
    box-shadow: 0 0 2px rgba(0, 0, 0, 0.3);
}

.alpha-value {
    min-width: 48px;
    text-align: right;
    color: var(--weilin-prompt-ui-secondary-text);
}

.favor-name-box {
    padding: 4px 8px;
    border-radius: 4px;
    margin-right: 8px;
    display: inline-flex;
    align-items: center;
    min-width: 40px;
    height: 24px;
    box-shadow: 0 1px 2px rgba(0, 0, 0, 0.1);
    width: 100%;
    margin-bottom: 10px;
}

.favor-name {
    font-size: 12px;
    font-weight: 500;
    color: #fff;
    text-shadow: 0 1px 1px rgba(0, 0, 0, 0.2);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    max-width: 200px;
}
</style>