/**
 * Training Store - Manages training data
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { TrainingItem } from '@/types/store'
import type { TrainRequest } from '@/types/api'
import { trainingAPI } from '@/api/training'
import { ElMessage } from 'element-plus'

export const useTrainingStore = defineStore('training', () => {
  // State
  const trainingData = ref<TrainingItem[]>([])
  const count = ref(0)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  const fetchTrainingData = async (): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const data = await trainingAPI.getTrainingData()

      if (data.training_data && Array.isArray(data.training_data)) {
        trainingData.value = data.training_data.map(
          (item: any, index: number) => ({
            id: item.id || `training-${index}`,
            question: item.question || null,
            content: item.content || item.sql || item.ddl || item.documentation || '',
            training_data_type: item.training_data_type || 'sql',
            // Keep legacy fields for backward compatibility
            sql: item.sql || undefined,
            ddl: item.ddl || undefined,
            documentation: item.documentation || undefined,
          })
        )
        count.value = data.count || trainingData.value.length
      }
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error'
      error.value = errorMessage
      console.error('Fetch training data error:', err)
      ElMessage.error(`Failed to fetch training data: ${errorMessage}`)
    } finally {
      isLoading.value = false
    }
  }

  const addTrainingData = async (request: TrainRequest): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await trainingAPI.addTraining(request)
      ElMessage.success(response.message || 'Training data added successfully')

      // Refresh training data after adding
      await fetchTrainingData()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error'
      error.value = errorMessage
      console.error('Add training data error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const removeTrainingData = async (id: string): Promise<void> => {
    isLoading.value = true
    error.value = null

    try {
      const response = await trainingAPI.removeTraining(id)
      ElMessage.success(response.message || 'Training data removed successfully')

      // Remove from local state
      trainingData.value = trainingData.value.filter((item) => item.id !== id)
      count.value = trainingData.value.length
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Unknown error'
      error.value = errorMessage
      console.error('Remove training data error:', err)
      throw err
    } finally {
      isLoading.value = false
    }
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    trainingData,
    count,
    isLoading,
    error,

    // Actions
    fetchTrainingData,
    addTrainingData,
    removeTrainingData,
    clearError,
  }
})
