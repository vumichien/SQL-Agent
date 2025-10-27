/**
 * UI Store - Manages UI preferences and state
 */

import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'
import type { Theme, Language } from '@/types/store'

export const useUIStore = defineStore(
  'ui',
  () => {
    // State
    const theme = ref<Theme>('light')
    const language = ref<Language>('en')
    const sidebarCollapsed = ref(false)

    // Computed getters
    const isDark = computed({
      get: () => theme.value === 'dark',
      set: (value: boolean) => {
        setTheme(value ? 'dark' : 'light')
      }
    })

    const isSidebarCollapsed = computed(() => sidebarCollapsed.value)

    // Actions
    const setTheme = (newTheme: Theme) => {
      theme.value = newTheme
      applyTheme(newTheme)
    }

    const toggleTheme = () => {
      const newTheme = theme.value === 'light' ? 'dark' : 'light'
      setTheme(newTheme)
    }

    const setLanguage = (newLanguage: Language) => {
      language.value = newLanguage
      // Sync with i18n (will be done by watcher)
      localStorage.setItem('ui-locale', newLanguage)
    }

    const toggleLanguage = () => {
      const newLanguage = language.value === 'en' ? 'ja' : 'en'
      setLanguage(newLanguage)
    }

    const setSidebarCollapsed = (collapsed: boolean) => {
      sidebarCollapsed.value = collapsed
    }

    const toggleSidebar = () => {
      sidebarCollapsed.value = !sidebarCollapsed.value
    }

    // Helper function to apply theme to DOM
    const applyTheme = (themeName: Theme) => {
      if (themeName === 'dark') {
        document.documentElement.classList.add('dark')
      } else {
        document.documentElement.classList.remove('dark')
      }
    }

    // Initialize theme and language on store creation
    const initialize = () => {
      applyTheme(theme.value)

      // Sync language with localStorage
      const storedLocale = localStorage.getItem('ui-locale')
      if (storedLocale === 'en' || storedLocale === 'ja') {
        language.value = storedLocale
      }
    }

    // Watch theme changes and apply to DOM
    watch(theme, (newTheme) => {
      applyTheme(newTheme)
    })

    return {
      // State
      theme,
      language,
      sidebarCollapsed,

      // Computed
      isDark,
      isSidebarCollapsed,

      // Actions
      setTheme,
      toggleTheme,
      setLanguage,
      toggleLanguage,
      setSidebarCollapsed,
      toggleSidebar,
      initialize,
    }
  },
  {
    persist: true,
  }
)
