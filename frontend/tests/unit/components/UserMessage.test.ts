/**
 * Unit tests for UserMessage component
 */

import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import UserMessage from '@/components/chat/UserMessage.vue'

describe('UserMessage', () => {
  describe('Rendering', () => {
    it('should render user message with question text', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'How many users are there?'
        }
      })

      expect(wrapper.text()).toContain('How many users are there?')
    })

    it('should render avatar', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Test question'
        }
      })

      expect(wrapper.find('.avatar').exists()).toBe(true)
    })

    it('should render message content container', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Test question'
        }
      })

      expect(wrapper.find('.message-content').exists()).toBe(true)
    })

    it('should render message text in paragraph', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Test question'
        }
      })

      const messageText = wrapper.find('.message-text')
      expect(messageText.exists()).toBe(true)
      expect(messageText.text()).toBe('Test question')
    })
  })

  describe('Props', () => {
    it('should accept question prop', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Custom question text'
        }
      })

      expect(wrapper.props('question')).toBe('Custom question text')
    })

    it('should display empty string if question is empty', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: ''
        }
      })

      expect(wrapper.find('.message-text').text()).toBe('')
    })

    it('should handle long question text', () => {
      // Note: trailing space is trimmed when rendering in DOM
      const longQuestion = 'This is a very long question '.repeat(20).trim()
      const wrapper = mount(UserMessage, {
        props: {
          question: longQuestion
        }
      })

      expect(wrapper.find('.message-text').text()).toBe(longQuestion)
    })

    it('should handle special characters in question', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'SELECT * FROM users WHERE name = "John\'s"'
        }
      })

      expect(wrapper.find('.message-text').text()).toContain("John's")
    })

    it('should handle multi-line question', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Line 1\nLine 2\nLine 3'
        }
      })

      expect(wrapper.find('.message-text').text()).toBe('Line 1\nLine 2\nLine 3')
    })
  })

  describe('Styling', () => {
    it('should have user-message class', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Test'
        }
      })

      expect(wrapper.find('.user-message').exists()).toBe(true)
    })

    it('should have avatar with proper class', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Test'
        }
      })

      const avatar = wrapper.find('.avatar')
      expect(avatar.exists()).toBe(true)
      expect(avatar.classes()).toContain('avatar')
    })

    it('should have message-content with proper class', () => {
      const wrapper = mount(UserMessage, {
        props: {
          question: 'Test'
        }
      })

      const messageContent = wrapper.find('.message-content')
      expect(messageContent.exists()).toBe(true)
      expect(messageContent.classes()).toContain('message-content')
    })
  })
})
