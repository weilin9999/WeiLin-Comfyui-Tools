// src/stores/tagStore.js
import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useTagStore = defineStore('tag', () => {
  // 定义 categories 变量
  const categories = ref([]);
  const userSetting = ref({user_lang: 'zh_CN'})

  // 更新 categories 的方法
  const setCategories = (newCategories) => {
    categories.value = newCategories;
  };

  const setUserSetting = (newUserSetting) => {
    userSetting.value = newUserSetting;
  };

  return {
    categories,
    setCategories,
    userSetting,
    setUserSetting,
  };
});