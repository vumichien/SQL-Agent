/**
 * Unit tests for Training API
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { trainingAPI } from '@/api/training'
import apiClient from '@/api/client'

// Mock apiClient
vi.mock('@/api/client', () => ({
  default: {
    get: vi.fn(),
    post: vi.fn(),
    delete: vi.fn()
  }
}))

describe('Training API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('getTrainingData', () => {
    it('should fetch all training data', async () => {
      const mockResponse = {
        training_data: [
          {
            id: 'training-1',
            question: 'How many users?',
            sql: 'SELECT COUNT(*) FROM users',
            training_data_type: 'sql'
          },
          {
            id: 'training-2',
            ddl: 'CREATE TABLE users (id INT)',
            training_data_type: 'ddl'
          }
        ],
        count: 2
      }

      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.getTrainingData()

      expect(apiClient.get).toHaveBeenCalledWith('/api/v0/training')
      expect(result).toEqual(mockResponse)
    })

    it('should handle empty training data', async () => {
      const mockResponse = {
        training_data: [],
        count: 0
      }

      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.getTrainingData()

      expect(result.training_data).toEqual([])
      expect(result.count).toBe(0)
    })
  })

  describe('addTraining', () => {
    it('should add SQL training data', async () => {
      const request = {
        question: 'Show all users',
        sql: 'SELECT * FROM users',
        training_data_type: 'sql'
      }
      const mockResponse = {
        message: 'Training data added successfully'
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.addTraining(request)

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/training', request)
      expect(result).toEqual(mockResponse)
    })

    it('should add DDL training data', async () => {
      const request = {
        ddl: 'CREATE TABLE products (id INT, name VARCHAR(100))',
        training_data_type: 'ddl'
      }
      const mockResponse = {
        message: 'DDL added successfully'
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.addTraining(request)

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/training', request)
      expect(result).toEqual(mockResponse)
    })

    it('should add documentation training data', async () => {
      const request = {
        documentation: 'The users table contains all registered users',
        training_data_type: 'documentation'
      }
      const mockResponse = {
        message: 'Documentation added successfully'
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.addTraining(request)

      expect(result).toEqual(mockResponse)
    })
  })

  describe('removeTraining', () => {
    it('should remove training data by ID', async () => {
      const mockResponse = {
        message: 'Training data removed successfully'
      }

      vi.mocked(apiClient.delete).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.removeTraining('training-123')

      expect(apiClient.delete).toHaveBeenCalledWith('/api/v0/training/training-123')
      expect(result).toEqual(mockResponse)
    })

    it('should handle removing non-existent training data', async () => {
      const mockResponse = {
        message: 'Training data not found'
      }

      vi.mocked(apiClient.delete).mockResolvedValueOnce({ data: mockResponse })

      const result = await trainingAPI.removeTraining('non-existent-id')

      expect(result).toEqual(mockResponse)
    })
  })
})
