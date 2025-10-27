/**
 * Vue I18n Configuration
 * Sets up internationalization for the application
 */

import { createI18n } from 'vue-i18n'
import en from './locales/en.json'
import ja from './locales/ja.json'

// Type for available locales
export type Locale = 'en' | 'ja'

// Get default locale from localStorage or browser settings
const getDefaultLocale = (): Locale => {
  const stored = localStorage.getItem('ui-locale')
  if (stored === 'en' || stored === 'ja') {
    return stored
  }

  // Try to get from browser language
  const browserLang = navigator.language.toLowerCase()
  if (browserLang.startsWith('ja')) {
    return 'ja'
  }

  return 'en' // Default to English
}

// Create i18n instance
const i18n = createI18n({
  legacy: false, // Use Composition API mode
  locale: getDefaultLocale(),
  fallbackLocale: 'en',
  messages: {
    en,
    ja,
  },
  globalInjection: true, // Enable global $t
  missingWarn: false, // Disable warnings for missing keys in production
  fallbackWarn: false,
})

export default i18n
