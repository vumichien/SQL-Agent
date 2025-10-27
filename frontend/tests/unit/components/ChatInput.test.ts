/**
 * Unit tests for ChatInput component
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { mount, VueWrapper } from '@vue/test-utils'
import ChatInput from '@/components/chat/ChatInput.vue'
import { createI18n } from 'vue-i18n'
import ElementPlus from 'element-plus'

const i18n = createI18n({
  legacy: false,
  locale: 'en',
  messages: {
    en: {
      chat: {
        inputPlaceholder: 'Ask a question...'
      }
    }
  }
})

describe('ChatInput', () => {
  let wrapper: VueWrapper

  beforeEach(() => {
    wrapper = mount(ChatInput, {
      global: {
        plugins: [i18n, ElementPlus],
        stubs: {
          // Un-stub Element Plus components for this test
          ElInput: false,
          ElButton: false,
          ElIcon: false
        }
      }
    })
  })

  describe('Rendering', () => {
    it('should render input field', () => {
      expect(wrapper.find('textarea').exists()).toBe(true)
    })

    it('should render send button', () => {
      expect(wrapper.find('.send-button').exists()).toBe(true)
    })

    it('should have proper placeholder', () => {
      const textarea = wrapper.find('textarea')
      expect(textarea.attributes('placeholder')).toBe('Ask a question...')
    })
  })

  describe('Input Handling', () => {
    it('should update input value when typing', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')

      expect((textarea.element as HTMLTextAreaElement).value).toBe('Test question')
    })

    it('should clear input after sending', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')

      const button = wrapper.find('.send-button')
      await button.trigger('click')

      expect((textarea.element as HTMLTextAreaElement).value).toBe('')
    })
  })

  describe('Send Button', () => {
    it('should be disabled when input is empty', async () => {
      const button = wrapper.find('.send-button')
      expect(button.attributes('disabled')).toBeDefined()
    })

    it('should be enabled when input has value', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')

      const button = wrapper.find('.send-button')
      expect(button.attributes('disabled')).toBeUndefined()
    })

    it('should be disabled when input is only whitespace', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('   ')

      const button = wrapper.find('.send-button')
      expect(button.attributes('disabled')).toBeDefined()
    })

    it('should emit send event when clicked', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')

      const button = wrapper.find('.send-button')
      await button.trigger('click')

      expect(wrapper.emitted('send')).toBeTruthy()
      expect(wrapper.emitted('send')?.[0]).toEqual(['Test question'])
    })

    it('should not emit send event with empty input', async () => {
      const button = wrapper.find('.send-button')
      await button.trigger('click')

      expect(wrapper.emitted('send')).toBeFalsy()
    })

    it('should trim whitespace before sending', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('  Test question  ')

      const button = wrapper.find('.send-button')
      await button.trigger('click')

      expect(wrapper.emitted('send')?.[0]).toEqual(['Test question'])
    })
  })

  describe('Loading State', () => {
    it('should disable input when loading', async () => {
      wrapper = mount(ChatInput, {
        props: { loading: true },
        global: {
          plugins: [i18n, ElementPlus],
          stubs: {
            ElInput: false,
            ElButton: false,
            ElIcon: false
          }
        }
      })

      const textarea = wrapper.find('textarea')
      expect(textarea.attributes('disabled')).toBeDefined()
    })

    it('should disable button when loading', async () => {
      wrapper = mount(ChatInput, {
        props: { loading: true },
        global: {
          plugins: [i18n, ElementPlus],
          stubs: {
            ElInput: false,
            ElButton: false,
            ElIcon: false
          }
        }
      })

      const button = wrapper.find('.send-button')
      expect(button.attributes('disabled')).toBeDefined()
    })

    it('should show loading icon on button when loading', async () => {
      wrapper = mount(ChatInput, {
        props: { loading: true },
        global: {
          plugins: [i18n, ElementPlus],
          stubs: {
            ElInput: false,
            ElButton: false,
            ElIcon: false
          }
        }
      })

      const button = wrapper.find('.send-button')
      // Element Plus adds 'is-loading' class when loading
      expect(button.classes()).toContain('is-loading')
    })

    it('should not emit send event when loading', async () => {
      wrapper = mount(ChatInput, {
        props: { loading: true },
        global: {
          plugins: [i18n, ElementPlus],
          stubs: {
            ElInput: false,
            ElButton: false,
            ElIcon: false
          }
        }
      })

      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')

      const button = wrapper.find('.send-button')
      await button.trigger('click')

      expect(wrapper.emitted('send')).toBeFalsy()
    })
  })

  describe('Keyboard Shortcuts', () => {
    it('should send message on Enter key', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')
      await textarea.trigger('keydown', { key: 'Enter' })

      expect(wrapper.emitted('send')).toBeTruthy()
      expect(wrapper.emitted('send')?.[0]).toEqual(['Test question'])
    })

    it('should not send message on Shift+Enter', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')
      await textarea.trigger('keydown', { key: 'Enter', shiftKey: true })

      expect(wrapper.emitted('send')).toBeFalsy()
    })

    it('should not send message on Enter when input is empty', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.trigger('keydown', { key: 'Enter' })

      expect(wrapper.emitted('send')).toBeFalsy()
    })

    it('should not send message on Enter when loading', async () => {
      wrapper = mount(ChatInput, {
        props: { loading: true },
        global: {
          plugins: [i18n, ElementPlus],
          stubs: {
            ElInput: false,
            ElButton: false,
            ElIcon: false
          }
        }
      })

      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')
      await textarea.trigger('keydown', { key: 'Enter' })

      expect(wrapper.emitted('send')).toBeFalsy()
    })

    it('should clear input after sending with Enter key', async () => {
      const textarea = wrapper.find('textarea')
      await textarea.setValue('Test question')
      await textarea.trigger('keydown', { key: 'Enter' })

      expect((textarea.element as HTMLTextAreaElement).value).toBe('')
    })
  })

  describe('Multiple Sends', () => {
    it('should handle multiple sends correctly', async () => {
      const textarea = wrapper.find('textarea')
      const button = wrapper.find('.send-button')

      await textarea.setValue('First question')
      await button.trigger('click')

      await textarea.setValue('Second question')
      await button.trigger('click')

      expect(wrapper.emitted('send')).toHaveLength(2)
      expect(wrapper.emitted('send')?.[0]).toEqual(['First question'])
      expect(wrapper.emitted('send')?.[1]).toEqual(['Second question'])
    })
  })
})
