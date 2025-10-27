/**
 * TypeScript types for Pinia stores
 */

// ============================================
// Auth Store Types
// ============================================

export interface User {
  id: string
  email: string
  username: string
  created_at?: string
}

export interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
}

// ============================================
// Query Store Types
// ============================================

export interface Query {
  id: string
  question: string
  sql: string | null
  results: QueryResults | null
  chart: any | null // Plotly figure
  timestamp: number
  error?: string
}

export interface QueryResults {
  columns: string[]
  data: any[][]
  rowCount: number
}

export interface QueryState {
  currentQuery: Query | null
  history: Query[]
  isLoading: boolean
  error: string | null
}

// ============================================
// Training Store Types
// ============================================

export interface TrainingItem {
  id: string
  question?: string | null
  content: string
  training_data_type: 'sql' | 'ddl' | 'documentation'
  // Legacy fields for backward compatibility
  sql?: string
  ddl?: string
  documentation?: string
}

export interface TrainingState {
  trainingData: TrainingItem[]
  count: number
  isLoading: boolean
  error: string | null
}

// ============================================
// UI Store Types
// ============================================

export type Theme = 'light' | 'dark'
export type Language = 'en' | 'ja'

export interface UIState {
  theme: Theme
  language: Language
  sidebarCollapsed: boolean
}
