// src/stores/tagStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTagStore = defineStore('tag', () => {
  // 定义 categories 变量
  const categories = ref([]);
  const userSetting = ref({user_lang: 'zh_CN'})
  const isFirstLoading = ref(0)

  // 更新 categories 的方法
  const setCategories = (newCategories) => {
    categories.value = newCategories;
  };

  // 更新 categories 的方法
  const setisFirstLoading = (newData) => {
    isFirstLoading.value = newData;
  };

  const setUserSetting = (newUserSetting) => {
    userSetting.value = newUserSetting;
  };

  return {
    categories,
    setCategories,
    userSetting,
    setUserSetting,
    isFirstLoading,
    setisFirstLoading,
  };
});