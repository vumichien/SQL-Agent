/**
 * Query API - Backend communication for SQL queries
 */

import apiClient from './client'
import type { QueryResponse, QueryHistoryItem } from '@/types/api'

export const queryAPI = {
  /**
   * Send a natural language question to generate SQL and results
   */
  async sendQuery(question: string): Promise<QueryResponse> {
    const { data } = await apiClient.post<any>('/api/v0/query', {
      question,
    })
    
    // Transform backend response to frontend format
    const response: QueryResponse = {
      id: data.id || `query-${Date.now()}`,
      question: data.question,
      sql: data.sql,
      results: null,
      visualization: data.visualization || null,
      error: null
    }
    
    // Convert results from array of objects to QueryResults format
    if (data.results && Array.isArray(data.results)) {
      // Handle both empty and non-empty results
      const columns = data.columns || (data.results.length > 0 ? Object.keys(data.results[0]) : [])
      const dataRows = data.results.map((row: any) => 
        columns.map(col => row[col] ?? null)
      )
      
      response.results = {
        columns,
        data: dataRows,
        rowCount: data.results.length
      }
    }
    
    return response
  },

  /**
   * Generate suggested questions
   */
  async generateQuestions(): Promise<string[]> {
    const { data } = await apiClient.get<string[]>('/api/v0/generate_questions')
    return data
  },

  /**
   * Get query history
   */
  async getHistory(): Promise<QueryHistoryItem[]> {
    const { data } = await apiClient.get<QueryHistoryItem[]>(
      '/api/v0/get_question_history'
    )
    return data
  },

  /**
   * Generate followup questions based on current query
   */
  async generateFollowup(question: string, sql: string): Promise<string[]> {
    const { data } = await apiClient.post<string[]>(
      '/api/v0/generate_followup_questions',
      {
        question,
        sql,
      }
    )
    return data
  },
}

export default queryAPI
