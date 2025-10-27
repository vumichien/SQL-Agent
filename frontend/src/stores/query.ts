/**
 * Query Store - Manages SQL queries, results, and history
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Query } from '@/types/store'
import { useAuthStore } from './auth'

export const useQueryStore = defineStore(
  'query',
  () => {
    // State
    const currentQuery = ref<Query | null>(null)
    const history = ref<Query[]>([])
    const isLoading = ref(false)
    const error = ref<string | null>(null)

    // Actions
    const sendQuery = async (question: string): Promise<void> => {
      isLoading.value = true
      error.value = null

      try {
        const authStore = useAuthStore()
        const headers: HeadersInit = {
          'Content-Type': 'application/json',
        }

        // Add auth token if available
        if (authStore.token) {
          headers['Authorization'] = `Bearer ${authStore.token}`
        }

        const response = await fetch('/api/v0/query', {
          method: 'POST',
          headers,
          body: JSON.stringify({ question }),
        })

        if (!response.ok) {
          const errorData = await response.json()
          throw new Error(errorData.detail || 'Query failed')
        }

        const data = await response.json()

        // Create query object
        const query: Query = {
          id: data.id || generateQueryId(),
          question: question,
          sql: data.sql || null,
          results: data.df
            ? {
                columns: data.df.columns || [],
                data: data.df.data || [],
                rowCount: data.df.data?.length || 0,
              }
            : null,
          chart: data.fig || null,
          timestamp: Date.now(),
        }

        // Update current query
        currentQuery.value = query

        // Add to history (prepend to show newest first)
        history.value.unshift(query)

        // Limit history to 50 items
        if (history.value.length > 50) {
          history.value = history.value.slice(0, 50)
        }
      } catch (err) {
        const errorMessage = err instanceof Error ? err.message : 'Unknown error'
        error.value = errorMessage
        console.error('Query error:', err)
        throw err
      } finally {
        isLoading.value = false
      }
    }

    const loadHistory = async (): Promise<void> => {
      try {
        const authStore = useAuthStore()
        const headers: HeadersInit = {}

        if (authStore.token) {
          headers['Authorization'] = `Bearer ${authStore.token}`
        }

        const response = await fetch('/api/v0/get_question_history', {
          method: 'GET',
          headers,
        })

        if (!response.ok) {
          throw new Error('Failed to load history')
        }

        const data = await response.json()

        // Transform API response to Query objects
        if (data.questions && Array.isArray(data.questions)) {
          history.value = data.questions.map((item: any, index: number) => ({
            id: item.id || `history-${index}`,
            question: item.question || '',
            sql: item.sql || null,
            results: item.df || null,
            chart: item.fig || null,
            timestamp: item.timestamp || Date.now(),
          }))
        }
      } catch (err) {
        console.error('Load history error:', err)
      }
    }

    const loadQueryById = async (id: string): Promise<void> => {
      try {
        const authStore = useAuthStore()
        const headers: HeadersInit = {
          'Content-Type': 'application/json',
        }

        if (authStore.token) {
          headers['Authorization'] = `Bearer ${authStore.token}`
        }

        const response = await fetch('/api/v0/load_question', {
          method: 'POST',
          headers,
          body: JSON.stringify({ id }),
        })

        if (!response.ok) {
          throw new Error('Failed to load query')
        }

        const data = await response.json()

        // Find in history or create new query object
        const historyQuery = history.value.find((q) => q.id === id)

        currentQuery.value = historyQuery || {
          id: id,
          question: data.question || '',
          sql: data.sql || null,
          results: data.df || null,
          chart: data.fig || null,
          timestamp: Date.now(),
        }
      } catch (err) {
        console.error('Load query error:', err)
        throw err
      }
    }

    const clearHistory = () => {
      history.value = []
    }

    const clearError = () => {
      error.value = null
    }

    const clearCurrentQuery = () => {
      currentQuery.value = null
    }

    const deleteQueryFromHistory = (id: string) => {
      history.value = history.value.filter((q) => q.id !== id)
    }

    const addQuery = (query: Query) => {
      // Add to history (prepend to show newest first)
      history.value.unshift(query)

      // Limit history to 50 items
      if (history.value.length > 50) {
        history.value = history.value.slice(0, 50)
      }

      // Update current query
      currentQuery.value = query
    }

    // Helper function to generate unique query ID
    const generateQueryId = (): string => {
      return `query-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`
    }

    return {
      // State
      currentQuery,
      history,
      isLoading,
      error,

      // Actions
      sendQuery,
      loadHistory,
      loadQueryById,
      clearHistory,
      clearError,
      clearCurrentQuery,
      deleteQueryFromHistory,
      addQuery,
    }
  },
  {
    persist: true,
  }
)
