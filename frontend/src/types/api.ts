/**
 * API Types - Type definitions for API requests and responses
 */

export interface QueryRequest {
  question: string
}

export interface QueryResponse {
  id: string
  question: string
  sql: string
  results: QueryResults | null
  visualization: any | null
  error: string | null
}

export interface QueryResults {
  columns: string[]
  data: any[][]
  rowCount: number
}

export interface QueryHistoryItem {
  id: string
  question: string
  sql: string
  timestamp: number
}

export interface TrainingDataItem {
  id: string
  training_data_type: 'ddl' | 'documentation' | 'sql'
  question?: string
  content: string
  sql?: string
  ddl?: string
  documentation?: string
}

export interface TrainRequest {
  ddl?: string
  documentation?: string
  question?: string
  sql?: string
}

export interface TrainResponse {
  status: string
  message: string
}

export interface GetTrainingDataResponse {
  training_data: TrainingDataItem[]
  count: number
}

export interface RemoveTrainingDataResponse {
  status: string
  message: string
}

export interface HealthResponse {
  status: string
  vanna_status: string
  training_data_count: number
  version: string
}
