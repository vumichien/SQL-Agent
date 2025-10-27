/**
 * Unit tests for Auth API
 */

import { describe, it, expect, beforeEach, vi } from 'vitest'
import { authAPI } from '@/api/auth'
import apiClient from '@/api/client'

// Mock apiClient
vi.mock('@/api/client', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn()
  }
}))

describe('Auth API', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('login', () => {
    it('should login and return auth response', async () => {
      const mockResponse = {
        access_token: 'mock-token-123',
        token_type: 'bearer'
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await authAPI.login('test@example.com', 'password123')

      expect(apiClient.post).toHaveBeenCalledWith(
        '/api/v0/auth/login',
        expect.any(URLSearchParams),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      )
      expect(result).toEqual(mockResponse)
    })

    it('should format login data as form data', async () => {
      const mockResponse = { access_token: 'token', token_type: 'bearer' }
      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      await authAPI.login('user@test.com', 'pass')

      const callArgs = vi.mocked(apiClient.post).mock.calls[0]
      const formData = callArgs[1] as URLSearchParams
      expect(formData.get('username')).toBe('user@test.com')
      expect(formData.get('password')).toBe('pass')
    })
  })

  describe('register', () => {
    it('should register and return user response', async () => {
      const mockResponse = {
        id: 1,
        email: 'new@example.com',
        username: 'newuser',
        created_at: '2024-01-01T00:00:00Z'
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await authAPI.register('new@example.com', 'newuser', 'password123')

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/auth/register', {
        email: 'new@example.com',
        username: 'newuser',
        password: 'password123'
      })
      expect(result).toEqual(mockResponse)
    })
  })

  describe('getProfile', () => {
    it('should fetch user profile', async () => {
      const mockProfile = {
        id: 1,
        email: 'user@example.com',
        username: 'testuser',
        created_at: '2024-01-01T00:00:00Z'
      }

      vi.mocked(apiClient.get).mockResolvedValueOnce({ data: mockProfile })

      const result = await authAPI.getProfile()

      expect(apiClient.get).toHaveBeenCalledWith('/api/v0/auth/me')
      expect(result).toEqual(mockProfile)
    })
  })

  describe('refreshToken', () => {
    it('should refresh token and return new auth response', async () => {
      const mockResponse = {
        access_token: 'new-token-456',
        token_type: 'bearer'
      }

      vi.mocked(apiClient.post).mockResolvedValueOnce({ data: mockResponse })

      const result = await authAPI.refreshToken()

      expect(apiClient.post).toHaveBeenCalledWith('/api/v0/auth/refresh')
      expect(result).toEqual(mockResponse)
    })
  })
})
