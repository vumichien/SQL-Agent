/**
 * Unit tests for Auth Store
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { setActivePinia, createPinia } from 'pinia'
import { useAuthStore } from '@/stores/auth'

describe('Auth Store', () => {
  beforeEach(() => {
    setActivePinia(createPinia())
    // Clear localStorage
    localStorage.clear()
    // Reset fetch mock
    global.fetch = vi.fn()
  })

  describe('Initial State', () => {
    it('should initialize with null user and token', () => {
      const store = useAuthStore()
      expect(store.user).toBe(null)
      expect(store.token).toBe(null)
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('Getters', () => {
    it('should return false for isAuthenticated when token is null', () => {
      const store = useAuthStore()
      expect(store.isAuthenticated).toBe(false)
    })

    it('should return true for isAuthenticated when token and user exist', () => {
      const store = useAuthStore()
      store.setToken('test-token')
      store.setUser({ id: '1', email: 'test@example.com', username: 'testuser' })
      expect(store.isAuthenticated).toBe(true)
    })

    it('should return false when only token exists', () => {
      const store = useAuthStore()
      store.setToken('test-token')
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('Actions - Basic Setters', () => {
    it('should set user', () => {
      const store = useAuthStore()
      const user = { id: '1', email: 'test@example.com', username: 'testuser' }
      store.setUser(user)
      expect(store.user).toEqual(user)
    })

    it('should set token', () => {
      const store = useAuthStore()
      const token = 'test-token-123'
      store.setToken(token)
      expect(store.token).toBe(token)
    })

    it('should clear user', () => {
      const store = useAuthStore()
      store.setUser({ id: '1', email: 'test@example.com', username: 'testuser' })
      store.setUser(null)
      expect(store.user).toBe(null)
    })

    it('should clear token', () => {
      const store = useAuthStore()
      store.setToken('test-token')
      store.setToken(null)
      expect(store.token).toBe(null)
    })
  })

  describe('Actions - Login', () => {
    it('should login successfully', async () => {
      const store = useAuthStore()
      const mockToken = 'mock-jwt-token'
      const mockUser = { id: '1', email: 'test@example.com', username: 'testuser' }

      global.fetch = vi.fn()
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ access_token: mockToken })
        } as Response)
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockUser
        } as Response)

      await store.login('test@example.com', 'password123')

      expect(store.token).toBe(mockToken)
      expect(store.user).toEqual(mockUser)
      expect(global.fetch).toHaveBeenCalledTimes(2)
    })

    it('should throw error on login failure', async () => {
      const store = useAuthStore()

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Invalid credentials' })
      } as Response)

      await expect(store.login('test@example.com', 'wrongpassword')).rejects.toThrow(
        'Invalid credentials'
      )
      expect(store.token).toBe(null)
      expect(store.user).toBe(null)
    })

    it('should throw generic error when detail is missing', async () => {
      const store = useAuthStore()

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({})
      } as Response)

      await expect(store.login('test@example.com', 'wrongpassword')).rejects.toThrow(
        'Login failed'
      )
    })
  })

  describe('Actions - Register', () => {
    it('should register and auto-login successfully', async () => {
      const store = useAuthStore()
      const mockUser = { id: '1', email: 'new@example.com', username: 'newuser' }
      const mockToken = 'mock-jwt-token'

      global.fetch = vi.fn()
        // Register call
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ user: mockUser })
        } as Response)
        // Auto-login call
        .mockResolvedValueOnce({
          ok: true,
          json: async () => ({ access_token: mockToken })
        } as Response)
        // Fetch profile call
        .mockResolvedValueOnce({
          ok: true,
          json: async () => mockUser
        } as Response)

      await store.register('new@example.com', 'newuser', 'password123')

      expect(store.user).toEqual(mockUser)
      expect(store.token).toBe(mockToken)
      expect(global.fetch).toHaveBeenCalledTimes(3)
    })

    it('should throw error on registration failure', async () => {
      const store = useAuthStore()

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Email already exists' })
      } as Response)

      await expect(
        store.register('existing@example.com', 'user', 'password123')
      ).rejects.toThrow('Email already exists')
    })
  })

  describe('Actions - Logout', () => {
    it('should logout and clear state', () => {
      const store = useAuthStore()
      store.setToken('test-token')
      store.setUser({ id: '1', email: 'test@example.com', username: 'testuser' })

      store.logout()

      expect(store.token).toBe(null)
      expect(store.user).toBe(null)
      expect(store.isAuthenticated).toBe(false)
    })
  })

  describe('Actions - Fetch User Profile', () => {
    it('should fetch user profile successfully', async () => {
      const store = useAuthStore()
      const mockUser = { id: '1', email: 'test@example.com', username: 'testuser' }
      store.setToken('test-token')

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockUser
      } as Response)

      await store.fetchUserProfile()

      expect(store.user).toEqual(mockUser)
      expect(global.fetch).toHaveBeenCalledWith('/api/v0/auth/me', {
        method: 'GET',
        headers: {
          Authorization: 'Bearer test-token'
        }
      })
    })

    it('should logout on fetch profile failure', async () => {
      const store = useAuthStore()
      store.setToken('invalid-token')
      store.setUser({ id: '1', email: 'test@example.com', username: 'testuser' })

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Unauthorized' })
      } as Response)

      await store.fetchUserProfile()

      expect(store.user).toBe(null)
      expect(store.token).toBe(null)
    })

    it('should do nothing if token is not set', async () => {
      const store = useAuthStore()

      await store.fetchUserProfile()

      expect(global.fetch).not.toHaveBeenCalled()
    })
  })

  describe('Actions - Refresh Token', () => {
    it('should refresh token successfully', async () => {
      const store = useAuthStore()
      const oldToken = 'old-token'
      const newToken = 'new-token'
      store.setToken(oldToken)

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => ({ access_token: newToken })
      } as Response)

      await store.refreshToken()

      expect(store.token).toBe(newToken)
      expect(global.fetch).toHaveBeenCalledWith('/api/v0/auth/refresh', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${oldToken}`
        }
      })
    })

    it('should logout on refresh token failure', async () => {
      const store = useAuthStore()
      store.setToken('expired-token')
      store.setUser({ id: '1', email: 'test@example.com', username: 'testuser' })

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: false,
        json: async () => ({ detail: 'Token expired' })
      } as Response)

      await store.refreshToken()

      expect(store.token).toBe(null)
      expect(store.user).toBe(null)
    })

    it('should do nothing if token is not set', async () => {
      const store = useAuthStore()

      await store.refreshToken()

      expect(global.fetch).not.toHaveBeenCalled()
    })
  })

  describe('Actions - Initialize', () => {
    it('should fetch profile if token exists but user is null', async () => {
      const store = useAuthStore()
      const mockUser = { id: '1', email: 'test@example.com', username: 'testuser' }
      store.setToken('existing-token')

      global.fetch = vi.fn().mockResolvedValueOnce({
        ok: true,
        json: async () => mockUser
      } as Response)

      await store.initialize()

      expect(store.user).toEqual(mockUser)
    })

    it('should not fetch profile if token is null', async () => {
      const store = useAuthStore()

      await store.initialize()

      expect(global.fetch).not.toHaveBeenCalled()
    })

    it('should not fetch profile if user already exists', async () => {
      const store = useAuthStore()
      store.setToken('existing-token')
      store.setUser({ id: '1', email: 'test@example.com', username: 'testuser' })

      await store.initialize()

      expect(global.fetch).not.toHaveBeenCalled()
    })
  })
})
