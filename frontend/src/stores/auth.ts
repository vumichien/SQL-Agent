/**
 * Auth Store - Manages user authentication state
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User } from '@/types/store'

export const useAuthStore = defineStore(
  'auth',
  () => {
    // State
    const user = ref<User | null>(null)
    const token = ref<string | null>(null)

    // Getters
    const isAuthenticated = computed(() => !!token.value && !!user.value)

    // Actions
    const setUser = (userData: User | null) => {
      user.value = userData
    }

    const setToken = (tokenValue: string | null) => {
      token.value = tokenValue
    }

    const login = async (username: string, password: string): Promise<void> => {
      try {
        const response = await fetch('/api/v0/auth/login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: new URLSearchParams({
            username: username,
            password: password,
          }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Login failed')
        }

        const data = await response.json()
        token.value = data.access_token

        // Fetch user profile after login
        await fetchUserProfile()
      } catch (error) {
        console.error('Login error:', error)
        throw error
      }
    }

    const register = async (
      email: string,
      username: string,
      password: string
    ): Promise<void> => {
      try {
        const response = await fetch('/api/v0/auth/register', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email,
            username,
            password,
          }),
        })

        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Registration failed')
        }

        const data = await response.json()
        user.value = data.user

        // Auto-login after registration
        await login(email, password)
      } catch (error) {
        console.error('Registration error:', error)
        throw error
      }
    }

    const fetchUserProfile = async (): Promise<void> => {
      if (!token.value) return

      try {
        const response = await fetch('/api/v0/auth/me', {
          method: 'GET',
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        })

        if (!response.ok) {
          throw new Error('Failed to fetch user profile')
        }

        const data = await response.json()
        user.value = data
      } catch (error) {
        console.error('Fetch profile error:', error)
        // If token is invalid, logout
        logout()
      }
    }

    const logout = () => {
      user.value = null
      token.value = null
    }

    const refreshToken = async (): Promise<void> => {
      if (!token.value) return

      try {
        const response = await fetch('/api/v0/auth/refresh', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${token.value}`,
          },
        })

        if (!response.ok) {
          throw new Error('Token refresh failed')
        }

        const data = await response.json()
        token.value = data.access_token
      } catch (error) {
        console.error('Refresh token error:', error)
        logout()
      }
    }

    // Initialize: Fetch user profile if token exists
    const initialize = async () => {
      if (token.value && !user.value) {
        await fetchUserProfile()
      }
    }

    return {
      // State
      user,
      token,

      // Getters
      isAuthenticated,

      // Actions
      setUser,
      setToken,
      login,
      register,
      logout,
      refreshToken,
      fetchUserProfile,
      initialize,
    }
  },
  {
    persist: true,
  }
)
