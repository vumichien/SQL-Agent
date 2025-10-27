/**
 * Auth API - Authentication endpoints
 */

import apiClient from './client'

export interface LoginRequest {
  username: string // Email used as username
  password: string
}

export interface RegisterRequest {
  email: string
  username: string
  password: string
}

export interface AuthResponse {
  access_token: string
  token_type: string
}

export interface UserResponse {
  id: number
  email: string
  username: string
  created_at: string
}

export const authAPI = {
  /**
   * Login with email and password
   */
  async login(email: string, password: string): Promise<AuthResponse> {
    // OAuth2 password flow expects form data
    const formData = new URLSearchParams()
    formData.append('username', email)
    formData.append('password', password)

    const { data } = await apiClient.post<AuthResponse>('/api/v0/auth/login', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    return data
  },

  /**
   * Register a new user
   */
  async register(email: string, username: string, password: string): Promise<UserResponse> {
    const { data } = await apiClient.post<UserResponse>('/api/v0/auth/register', {
      email,
      username,
      password,
    })
    return data
  },

  /**
   * Get current user profile
   */
  async getProfile(): Promise<UserResponse> {
    const { data } = await apiClient.get<UserResponse>('/api/v0/auth/me')
    return data
  },

  /**
   * Refresh access token
   */
  async refreshToken(): Promise<AuthResponse> {
    const { data } = await apiClient.post<AuthResponse>('/api/v0/auth/refresh')
    return data
  },
}
