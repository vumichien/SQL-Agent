/**
 * Unit tests for Query API
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { queryAPI } from '@/api/query'
import apiClient from '@/api/client'

// Mock apiClient
vi.mock('@/api/client', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

describe('Query API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('sendQuery', () => {
    it('should send query and return response', async () => {
      const mockResponse = {
        id: 'query-123',
        sql: 'SELECT * FROM users',
        df: { columns: ['id', 'name'], data: [[1, 'Alice']] },
        fig: null
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await queryAPI.sendQuery('Show all users')

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/query', {
        question: 'Show all users'
      })
      expect(result).toEqual(mockResponse)
    })

    it('should handle empty question', async () => {
      const mockResponse = { id: 'query-456', sql: null, df: null, fig: null }
      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await queryAPI.sendQuery('')

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/query', { question: '' })
      expect(result).toEqual(mockResponse)
    })
  })

  describe('generateQuestions', () => {
    it('should generate suggested questions', async () => {
      const mockQuestions = ['How many users?', 'Show all orders', 'Total revenue?']
      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockQuestions })

      const result = await queryAPI.generateQuestions()

      expect(apiClient.get).toHaveBeenCalledWith('/api/v0/generate_questions')
      expect(result).toEqual(mockQuestions)
    })

    it('should handle empty questions list', async () => {
      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: [] })

      const result = await queryAPI.generateQuestions()

      expect(result).toEqual([])
    })
  })

  describe('getHistory', () => {
    it('should fetch query history', async () => {
      const mockHistory = [
        { id: 'q1', question: 'Test 1', sql: 'SELECT 1', timestamp: 1000 },
        { id: 'q2', question: 'Test 2', sql: 'SELECT 2', timestamp: 2000 }
      ]
      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockHistory })

      const result = await queryAPI.getHistory()

      expect(apiClient.get).toHaveBeenCalledWith('/api/v0/get_question_history')
      expect(result).toEqual(mockHistory)
    })

    it('should handle empty history', async () => {
      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: [] })

      const result = await queryAPI.getHistory()

      expect(result).toEqual([])
    })
  })

  describe('generateFollowup', () => {
    it('should generate followup questions', async () => {
      const mockFollowups = ['What about last month?', 'Show by category']
      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockFollowups })

      const result = await queryAPI.generateFollowup('Show sales', 'SELECT * FROM sales')

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/generate_followup_questions', {
        question: 'Show sales',
        sql: 'SELECT * FROM sales'
      })
      expect(result).toEqual(mockFollowups)
    })

    it('should handle empty followup list', async () => {
      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: [] })

      const result = await queryAPI.generateFollowup('Test', 'SELECT 1')

      expect(result).toEqual([])
    })
  })
})
