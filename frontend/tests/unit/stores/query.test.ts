/**
 * Unit tests for Query Store
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useQueryStore } from '@/stores/query'
import { useAuthStore } from '@/stores/auth'

describe('Query Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    localStorage.clear()
    global.fetch = vi.fn()
  })

  describe('Initial State', () => {
    it('should initialize with null currentQuery and empty history', () => {
      const store = useQueryStore()
      expect(store.currentQuery).toBe(null)
      expect(store.history).toEqual([])
      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
    })
  })

  describe('Actions - Send Query', () => {
    it('should send query successfully and update state', async () => {
      const store = useQueryStore()
      const mockResponse = {
        id: 'query-123',
        sql: 'SELECT * FROM users',
        df: {
          columns: ['id', 'name'],
          data: [
            [1, 'Alice'],
            [2, 'Bob']
          ]
        },
        fig: { data: [], layout: {} }
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse
      } as Response)

      await store.sendQuery('Show all users')

      expect(store.isLoading).toBe(false)
      expect(store.error).toBe(null)
      expect(store.currentQuery).toBeDefined()
      expect(store.currentQuery?.question).toBe('Show all users')
      expect(store.currentQuery?.sql).toBe('SELECT * FROM users')
      expect(store.currentQuery?.results?.rowCount).toBe(2)
      expect(store.history).toHaveLength(1)
    })

    it('should include auth token in request when user is authenticated', async () => {
      const authStore = useAuthStore()
      const queryStore = useQueryStore()

      authStore.setToken('test-token')

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ id: 'query-123', sql: 'SELECT 1' })
      } as Response)

      await queryStore.sendQuery('Test query')

      expect(global.fetch).toHaveBeenCalledWith(
        '/api/v0/query',
        expect.objectContaining({
          headers: expect.objectContaining({
            Authorization: 'Bearer test-token'
          })
        })
      )
    })

    it('should handle query without results', async () => {
      const store = useQueryStore()
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({
          id: 'query-123',
          sql: 'SELECT * FROM empty_table'
        })
      } as Response)

      await store.sendQuery('Show empty table')

      expect(store.currentQuery?.results).toBe(null)
    })

    it('should handle query error', async () => {
      const store = useQueryStore()
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Invalid query' })
      } as Response)

      await expect(store.sendQuery('Invalid query')).rejects.toThrow('Invalid query')

      expect(store.error).toBe('Invalid query')
      expect(store.isLoading).toBe(false)
      expect(store.currentQuery).toBe(null)
    })

    it('should limit history to 50 items', async () => {
      const store = useQueryStore()

      // Mock 51 successful queries
      for (let i = 0; i < 51; i++) {
        global.fetch = vi.fn().mockResolvedValueOnce({
          ok: true,
          json: async () => ({
            id: `query-${i}`,
            sql: `SELECT ${i}`
          })
        } as Response)

        await store.sendQuery(`Query ${i}`)
      }

      expect(store.history).toHaveLength(50)
      expect(store.history[0].question).toBe('Query 50') // Newest first
    })

    it('should generate query ID if not provided', async () => {
      const store = useQueryStore()
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ sql: 'SELECT 1' })
      } as Response)

      await store.sendQuery('Test query')

      expect(store.currentQuery?.id).toMatch(/^query-/)
    })
  })

  describe('Actions - Load History', () => {
    it('should load history successfully', async () => {
      const store = useQueryStore()
      const mockHistory = {
        questions: [
          {
            id: 'query-1',
            question: 'Query 1',
            sql: 'SELECT 1',
            timestamp: 1000
          },
          {
            id: 'query-2',
            question: 'Query 2',
            sql: 'SELECT 2',
            timestamp: 2000
          }
        ]
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockHistory
      } as Response)

      await store.loadHistory()

      expect(store.history).toHaveLength(2)
      expect(store.history[0].id).toBe('query-1')
      expect(store.history[1].id).toBe('query-2')
    })

    it('should handle empty history', async () => {
      const store = useQueryStore()
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ questions: [] })
      } as Response)

      await store.loadHistory()

      expect(store.history).toEqual([])
    })

    it('should handle load history error gracefully', async () => {
      const store = useQueryStore()
      const consoleErrorSpy = vi.spyOn(console, 'error').mockImplementation(() => {})

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Failed' })
      } as Response)

      await store.loadHistory()

      expect(consoleErrorSpy).toHaveBeenCalled()
      consoleErrorSpy.mockRestore()
    })
  })

  describe('Actions - Load Query By ID', () => {
    it('should load query from history', async () => {
      const store = useQueryStore()
      const query = {
        id: 'query-123',
        question: 'Test',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      }

      store.addQuery(query)

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => query
      } as Response)

      await store.loadQueryById('query-123')

      expect(store.currentQuery).toEqual(query)
    })

    it('should load query from API if not in history', async () => {
      const store = useQueryStore()
      const mockQuery = {
        question: 'Test query',
        sql: 'SELECT 1',
        df: null,
        fig: null
      }

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockQuery
      } as Response)

      await store.loadQueryById('query-456')

      expect(store.currentQuery?.question).toBe('Test query')
    })

    it('should handle load query error', async () => {
      const store = useQueryStore()
      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Not found' })
      } as Response)

      await expect(store.loadQueryById('invalid-id')).rejects.toThrow()
    })
  })

  describe('Actions - Clear Methods', () => {
    it('should clear history', () => {
      const store = useQueryStore()
      store.addQuery({
        id: 'query-1',
        question: 'Test',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      })

      store.clearHistory()

      expect(store.history).toEqual([])
    })

    it('should clear error', () => {
      const store = useQueryStore()
      store.error = 'Test error'

      store.clearError()

      expect(store.error).toBe(null)
    })

    it('should clear current query', () => {
      const store = useQueryStore()
      store.addQuery({
        id: 'query-1',
        question: 'Test',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      })

      store.clearCurrentQuery()

      expect(store.currentQuery).toBe(null)
      expect(store.history).toHaveLength(1) // History not affected
    })
  })

  describe('Actions - Delete Query From History', () => {
    it('should delete query from history', () => {
      const store = useQueryStore()
      const query1 = {
        id: 'query-1',
        question: 'Test 1',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      }
      const query2 = {
        id: 'query-2',
        question: 'Test 2',
        sql: 'SELECT 2',
        results: null,
        chart: null,
        timestamp: Date.now()
      }

      store.addQuery(query1)
      store.addQuery(query2)

      store.deleteQueryFromHistory('query-1')

      expect(store.history).toHaveLength(1)
      expect(store.history[0].id).toBe('query-2')
    })

    it('should do nothing if query ID not found', () => {
      const store = useQueryStore()
      store.addQuery({
        id: 'query-1',
        question: 'Test',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      })

      store.deleteQueryFromHistory('non-existent-id')

      expect(store.history).toHaveLength(1)
    })
  })

  describe('Actions - Add Query', () => {
    it('should add query to history and set as current', () => {
      const store = useQueryStore()
      const query = {
        id: 'query-1',
        question: 'Test',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      }

      store.addQuery(query)

      expect(store.currentQuery).toEqual(query)
      expect(store.history).toHaveLength(1)
      expect(store.history[0]).toEqual(query)
    })

    it('should prepend new query to history', () => {
      const store = useQueryStore()
      const query1 = {
        id: 'query-1',
        question: 'Test 1',
        sql: 'SELECT 1',
        results: null,
        chart: null,
        timestamp: Date.now()
      }
      const query2 = {
        id: 'query-2',
        question: 'Test 2',
        sql: 'SELECT 2',
        results: null,
        chart: null,
        timestamp: Date.now()
      }

      store.addQuery(query1)
      store.addQuery(query2)

      expect(store.history[0]).toEqual(query2) // Newest first
      expect(store.history[1]).toEqual(query1)
    })

    it('should limit history to 50 items when adding', () => {
      const store = useQueryStore()

      // Add 51 queries
      for (let i = 0; i < 51; i++) {
        store.addQuery({
          id: `query-${i}`,
          question: `Query ${i}`,
          sql: `SELECT ${i}`,
          results: null,
          chart: null,
          timestamp: Date.now()
        })
      }

      expect(store.history).toHaveLength(50)
      expect(store.history[0].id).toBe('query-50') // Newest
      expect(store.history[49].id).toBe('query-1') // Oldest (query-0 removed)
    })
  })
})
