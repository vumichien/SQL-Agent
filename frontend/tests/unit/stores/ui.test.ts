/**
 * Unit tests for UI Store
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useUIStore } from '@/stores/ui'

describe('UI Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    document.documentElement.classList.remove('dark')
  })

  describe('Initial State', () => {
    it('should initialize with default values', () => {
      const store = useUIStore()
      expect(store.theme).toBe('light')
      expect(store.language).toBe('en')
      expect(store.sidebarCollapsed).toBe(false)
    })
  })

  describe('Getters', () => {
    it('should return false for isDark when theme is light', () => {
      const store = useUIStore()
      expect(store.isDark).toBe(false)
    })

    it('should return true for isDark when theme is dark', () => {
      const store = useUIStore()
      store.setTheme('dark')
      expect(store.isDark).toBe(true)
    })

    it('should return false for isSidebarCollapsed initially', () => {
      const store = useUIStore()
      expect(store.isSidebarCollapsed).toBe(false)
    })

    it('should return true for isSidebarCollapsed when collapsed', () => {
      const store = useUIStore()
      store.setSidebarCollapsed(true)
      expect(store.isSidebarCollapsed).toBe(true)
    })
  })

  describe('Actions - Theme', () => {
    it('should set theme to dark', () => {
      const store = useUIStore()
      store.setTheme('dark')
      expect(store.theme).toBe('dark')
      expect(document.documentElement.classList.contains('dark')).toBe(true)
    })

    it('should set theme to light', () => {
      const store = useUIStore()
      store.setTheme('dark')
      store.setTheme('light')
      expect(store.theme).toBe('light')
      expect(document.documentElement.classList.contains('dark')).toBe(false)
    })

    it('should toggle theme from light to dark', () => {
      const store = useUIStore()
      store.toggleTheme()
      expect(store.theme).toBe('dark')
      expect(document.documentElement.classList.contains('dark')).toBe(true)
    })

    it('should toggle theme from dark to light', () => {
      const store = useUIStore()
      store.setTheme('dark')
      store.toggleTheme()
      expect(store.theme).toBe('light')
      expect(document.documentElement.classList.contains('dark')).toBe(false)
    })

    it('should set isDark computed property', () => {
      const store = useUIStore()
      store.isDark = true
      expect(store.theme).toBe('dark')
      expect(store.isDark).toBe(true)

      store.isDark = false
      expect(store.theme).toBe('light')
      expect(store.isDark).toBe(false)
    })
  })

  describe('Actions - Language', () => {
    it('should set language to Japanese', () => {
      const store = useUIStore()
      store.setLanguage('ja')
      expect(store.language).toBe('ja')
      expect(localStorage.getItem('ui-locale')).toBe('ja')
    })

    it('should set language to English', () => {
      const store = useUIStore()
      store.setLanguage('en')
      expect(store.language).toBe('en')
      expect(localStorage.getItem('ui-locale')).toBe('en')
    })

    it('should toggle language from English to Japanese', () => {
      const store = useUIStore()
      store.toggleLanguage()
      expect(store.language).toBe('ja')
    })

    it('should toggle language from Japanese to English', () => {
      const store = useUIStore()
      store.setLanguage('ja')
      store.toggleLanguage()
      expect(store.language).toBe('en')
    })
  })

  describe('Actions - Sidebar', () => {
    it('should collapse sidebar', () => {
      const store = useUIStore()
      store.setSidebarCollapsed(true)
      expect(store.sidebarCollapsed).toBe(true)
      expect(store.isSidebarCollapsed).toBe(true)
    })

    it('should expand sidebar', () => {
      const store = useUIStore()
      store.setSidebarCollapsed(true)
      store.setSidebarCollapsed(false)
      expect(store.sidebarCollapsed).toBe(false)
      expect(store.isSidebarCollapsed).toBe(false)
    })

    it('should toggle sidebar from expanded to collapsed', () => {
      const store = useUIStore()
      store.toggleSidebar()
      expect(store.sidebarCollapsed).toBe(true)
    })

    it('should toggle sidebar from collapsed to expanded', () => {
      const store = useUIStore()
      store.setSidebarCollapsed(true)
      store.toggleSidebar()
      expect(store.sidebarCollapsed).toBe(false)
    })
  })

  describe('Actions - Initialize', () => {
    it('should apply current theme on initialization', () => {
      const store = useUIStore()
      store.setTheme('dark')

      // Manually call initialize (simulating store creation)
      store.initialize()

      expect(document.documentElement.classList.contains('dark')).toBe(true)
    })

    it('should load language from localStorage on initialization', () => {
      localStorage.setItem('ui-locale', 'ja')

      const store = useUIStore()
      store.initialize()

      expect(store.language).toBe('ja')
    })

    it('should keep default language if localStorage is empty', () => {
      const store = useUIStore()
      store.initialize()

      expect(store.language).toBe('en')
    })

    it('should ignore invalid language from localStorage', () => {
      localStorage.setItem('ui-locale', 'invalid')

      const store = useUIStore()
      store.initialize()

      expect(store.language).toBe('en')
    })
  })

  describe('Theme Application', () => {
    it('should add dark class to documentElement when theme is dark', () => {
      const store = useUIStore()
      store.setTheme('dark')
      expect(document.documentElement.classList.contains('dark')).toBe(true)
    })

    it('should remove dark class from documentElement when theme is light', () => {
      const store = useUIStore()
      document.documentElement.classList.add('dark')
      store.setTheme('light')
      expect(document.documentElement.classList.contains('dark')).toBe(false)
    })
  })
})
