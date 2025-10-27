/**
 * Unit tests for Training Store
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useTrainingStore } from '@/stores/training'

// Mock trainingAPI
vi.mock('@/api/training', () => ({
  trainingAPI: {
    getTrainingData: vi.fn(),
    addTraining: vi.fn(),
    removeTraining: vi.fn()
  }
}))

// Mock ElMessage
vi.mock('element-plus', () => ({
  ElMessage: {
    success: vi.fn(),
    error: vi.fn()
  }
}))

import { trainingAPI } from '@/api/training'
import { ElMessage } from 'element-plus'

describe('Training Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    vi.clearAllMocks()
  })

  describe('Initial State', () => {
    it('should initialize with empty training data', () => {
      const store = useTrainingStore()
      expect(store.trainingData).toEqual([])
      expect(store.count).toBe(0)
      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
    })
  })

  describe('Actions - Fetch Training Data', () => {
    it('should fetch training data successfully', async () => {
      const store = useTrainingStore()
      const mockData = {
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

      vi.mocked(trainingAPI.getTrainingData).mockResolvedValueOnce(mockData)

      await store.fetchTrainingData()

      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
      expect(store.trainingData).toHaveLength(2)
      expect(store.count).toBe(2)
      expect(store.trainingData[0].id).toBe('training-1')
      expect(store.trainingData[0].question).toBe('How many users?')
    })

    it('should handle empty training data', async () => {
      const store = useTrainingStore()
      vi.mocked(trainingAPI.getTrainingData).mockResolvedValueOnce({
        training_data: [],
        count: 0
      })

      await store.fetchTrainingData()

      expect(store.trainingData).toEqual([])
      expect(store.count).toBe(0)
    })

    it('should handle fetch error', async () => {
      const store = useTrainingStore()
      const error = new Error('Network error')
      vi.mocked(trainingAPI.getTrainingData).mockRejectedValueOnce(error)

      await store.fetchTrainingData()

      expect(store.error).toBe('Network error')
      expect(store.isLoading).toBe(false)
      expect(ElMessage.error).toHaveBeenCalledWith(
        'Failed to fetch training data: Network error'
      )
    })

    it('should generate IDs for items without IDs', async () => {
      const store = useTrainingStore()
      const mockData = {
        training_data: [
          { question: 'Test?', sql: 'SELECT 1' },
          { question: 'Test2?', sql: 'SELECT 2' }
        ],
        count: 2
      }

      vi.mocked(trainingAPI.getTrainingData).mockResolvedValueOnce(mockData)

      await store.fetchTrainingData()

      expect(store.trainingData[0].id).toMatch(/^training-/)
      expect(store.trainingData[1].id).toMatch(/^training-/)
    })

    it('should use default training_data_type if not provided', async () => {
      const store = useTrainingStore()
      const mockData = {
        training_data: [{ question: 'Test?', sql: 'SELECT 1' }],
        count: 1
      }

      vi.mocked(trainingAPI.getTrainingData).mockResolvedValueOnce(mockData)

      await store.fetchTrainingData()

      expect(store.trainingData[0].training_data_type).toBe('sql')
    })
  })

  describe('Actions - Add Training Data', () => {
    it('should add training data successfully', async () => {
      const store = useTrainingStore()
      const request = {
        question: 'New question?',
        sql: 'SELECT * FROM new_table',
        training_data_type: 'sql'
      }

      vi.mocked(trainingAPI.addTraining).mockResolvedValueOnce({
        message: 'Training data added'
      })
      vi.mocked(trainingAPI.getTrainingData).mockResolvedValueOnce({
        training_data: [
          {
            id: 'training-1',
            question: 'New question?',
            sql: 'SELECT * FROM new_table',
            training_data_type: 'sql'
          }
        ],
        count: 1
      })

      await store.addTrainingData(request)

      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
      expect(ElMessage.success).toHaveBeenCalledWith('Training data added')
      expect(store.trainingData).toHaveLength(1)
    })

    it('should handle add training data error', async () => {
      const store = useTrainingStore()
      const request = {
        question: 'Test?',
        sql: 'SELECT 1',
        training_data_type: 'sql'
      }
      const error = new Error('Failed to add')

      vi.mocked(trainingAPI.addTraining).mockRejectedValueOnce(error)

      await expect(store.addTrainingData(request)).rejects.toThrow('Failed to add')

      expect(store.error).toBe('Failed to add')
      expect(store.isLoading).toBe(false)
    })

    it('should use default message if not provided', async () => {
      const store = useTrainingStore()
      const request = {
        ddl: 'CREATE TABLE test (id INT)',
        training_data_type: 'ddl'
      }

      vi.mocked(trainingAPI.addTraining).mockResolvedValueOnce({})
      vi.mocked(trainingAPI.getTrainingData).mockResolvedValueOnce({
        training_data: [],
        count: 0
      })

      await store.addTrainingData(request)

      expect(ElMessage.success).toHaveBeenCalledWith('Training data added successfully')
    })
  })

  describe('Actions - Remove Training Data', () => {
    it('should remove training data successfully', async () => {
      const store = useTrainingStore()

      // Set up initial state
      store.trainingData = [
        {
          id: 'training-1',
          question: 'Test 1?',
          sql: 'SELECT 1',
          training_data_type: 'sql'
        },
        {
          id: 'training-2',
          question: 'Test 2?',
          sql: 'SELECT 2',
          training_data_type: 'sql'
        }
      ]
      store.count = 2

      vi.mocked(trainingAPI.removeTraining).mockResolvedValueOnce({
        message: 'Training data removed'
      })

      await store.removeTrainingData('training-1')

      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
      expect(ElMessage.success).toHaveBeenCalledWith('Training data removed')
      expect(store.trainingData).toHaveLength(1)
      expect(store.trainingData[0].id).toBe('training-2')
      expect(store.count).toBe(1)
    })

    it('should handle remove training data error', async () => {
      const store = useTrainingStore()
      const error = new Error('Failed to remove')

      vi.mocked(trainingAPI.removeTraining).mockRejectedValueOnce(error)

      await expect(store.removeTrainingData('training-1')).rejects.toThrow('Failed to remove')

      expect(store.error).toBe('Failed to remove')
      expect(store.isLoading).toBe(false)
    })

    it('should use default message if not provided', async () => {
      const store = useTrainingStore()
      store.trainingData = [
        {
          id: 'training-1',
          question: 'Test?',
          sql: 'SELECT 1',
          training_data_type: 'sql'
        }
      ]
      store.count = 1

      vi.mocked(trainingAPI.removeTraining).mockResolvedValueOnce({})

      await store.removeTrainingData('training-1')

      expect(ElMessage.success).toHaveBeenCalledWith('Training data removed successfully')
    })

    it('should do nothing if ID not found in local state', async () => {
      const store = useTrainingStore()
      store.trainingData = [
        {
          id: 'training-1',
          question: 'Test?',
          sql: 'SELECT 1',
          training_data_type: 'sql'
        }
      ]
      store.count = 1

      vi.mocked(trainingAPI.removeTraining).mockResolvedValueOnce({
        message: 'Removed'
      })

      await store.removeTrainingData('non-existent-id')

      expect(store.trainingData).toHaveLength(1) // Still has the original item
      expect(store.count).toBe(1)
    })
  })

  describe('Actions - Clear Error', () => {
    it('should clear error', () => {
      const store = useTrainingStore()
      store.error = 'Test error'

      store.clearError()

      expect(store.error).toBe(null)
    })
  })
})
