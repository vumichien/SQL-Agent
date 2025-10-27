/**
 * Training API - Backend communication for training data management
 */

import apiClient from './client'
import type {
  TrainRequest,
  TrainResponse,
  GetTrainingDataResponse,
  RemoveTrainingDataResponse,
} from '@/types/api'

export const trainingAPI = {
  /**
   * Get all training data
   */
  async getTrainingData(): Promise<GetTrainingDataResponse> {
    const { data } = await apiClient.get<GetTrainingDataResponse>('/api/v0/training')
    return data
  },

  /**
   * Add training data (DDL, documentation, or Q&A pair)
   */
  async addTraining(request: TrainRequest): Promise<TrainResponse> {
    const { data } = await apiClient.post<TrainResponse>('/api/v0/training', request)
    return data
  },

  /**
   * Remove training data by ID
   */
  async removeTraining(id: string): Promise<RemoveTrainingDataResponse> {
    const { data } = await apiClient.delete<RemoveTrainingDataResponse>(
      `/api/v0/training/${id}`
    )
    return data
  },
}

export default trainingAPI
