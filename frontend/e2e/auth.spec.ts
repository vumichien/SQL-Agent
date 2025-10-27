import { test, expect } from '@playwright/test'
import { generateTestUser } from './fixtures/auth.fixture'

/**
 * E2E Tests: Authentication Flow
 * Tests user registration, login, and logout functionality
 */

test.describe('Authentication Flow', () => {
  test.describe('User Registration', () => {
    test('should register a new user successfully', async ({ page }) => {
      const testUser = generateTestUser()

      // Navigate to register page
      await page.goto('/register')

      // Verify we're on the register page
      await expect(page).toHaveURL(/\/register/)
      await expect(
        page.locator('h2:has-text("Register"), h2:has-text("登録")')
      ).toBeVisible()

      // Fill registration form
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', testUser.email)
      await page.locator('input[type="password"]').first().fill(testUser.password)
      await page.locator('input[type="password"]').last().fill(testUser.password)

      // Submit registration
      await page.click('button[type="submit"]')

      // Should redirect to login or chat page
      await page.waitForURL(/\/(login|chat)/, { timeout: 10000 })
    })

    test('should show error for duplicate username', async ({ page }) => {
      const testUser = generateTestUser()

      // Register first time
      await page.goto('/register')
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', testUser.email)
      await page.locator('input[type="password"]').first().fill(testUser.password)
      await page.locator('input[type="password"]').last().fill(testUser.password)
      await page.click('button[type="submit"]')
      await page.waitForURL(/\/(login|chat)/, { timeout: 10000 })

      // Try to register again with same username
      await page.goto('/register')
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', `different_${testUser.email}`)
      await page.locator('input[type="password"]').first().fill(testUser.password)
      await page.locator('input[type="password"]').last().fill(testUser.password)
      await page.click('button[type="submit"]')

      // Should show error message
      await expect(
        page.locator('.el-message--error, .el-notification--error, [role="alert"]')
      ).toBeVisible({ timeout: 5000 })
    })

    test('should validate password requirements', async ({ page }) => {
      await page.goto('/register')

      const testUser = generateTestUser()
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', testUser.email)

      // Try weak password
      await page.locator('input[type="password"]').first().fill('weak')
      await page.locator('input[type="password"]').first().blur()

      // Should show validation error or disable submit
      const submitButton = page.locator('button[type="submit"]')
      const isDisabled = await submitButton.isDisabled()

      expect(isDisabled).toBe(true)
    })

    test('should validate password confirmation match', async ({ page }) => {
      await page.goto('/register')

      const testUser = generateTestUser()
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', testUser.email)
      await page.locator('input[type="password"]').first().fill(testUser.password)
      await page.locator('input[type="password"]').last().fill('DifferentPassword123!')
      await page.locator('input[type="password"]').last().blur()

      // Should show validation error
      await expect(
        page.locator('.el-form-item__error, .error-message')
      ).toBeVisible({ timeout: 2000 })
    })
  })

  test.describe('User Login', () => {
    test('should login with valid credentials', async ({ page }) => {
      // First register a user
      const testUser = generateTestUser()
      await page.goto('/register')
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', testUser.email)
      await page.locator('input[type="password"]').first().fill(testUser.password)
      await page.locator('input[type="password"]').last().fill(testUser.password)
      await page.click('button[type="submit"]')
      await page.waitForURL(/\/(login|chat)/, { timeout: 10000 })

      // If not on chat page, navigate to login
      if (!page.url().includes('/chat')) {
        await page.goto('/login')

        // Login
        await page.fill('input[type="text"]', testUser.username)
        await page.fill('input[type="password"]', testUser.password)
        await page.click('button[type="submit"]')

        // Should redirect to chat
        await page.waitForURL('/chat', { timeout: 10000 })
      }

      // Verify we're on chat page and authenticated
      await expect(page).toHaveURL('/chat')
      await expect(
        page.locator('[data-testid="chat-input"], .chat-input, textarea')
      ).toBeVisible()
    })

    test('should show error for invalid credentials', async ({ page }) => {
      await page.goto('/login')

      // Try to login with invalid credentials
      await page.fill('input[type="text"]', 'nonexistentuser')
      await page.fill('input[type="password"]', 'wrongpassword')
      await page.click('button[type="submit"]')

      // Should show error message
      await expect(
        page.locator('.el-message--error, .el-notification--error, [role="alert"]')
      ).toBeVisible({ timeout: 5000 })

      // Should stay on login page
      await expect(page).toHaveURL(/\/login/)
    })

    test('should redirect to login when accessing protected route unauthenticated', async ({
      page,
    }) => {
      // Try to access chat page without authentication
      await page.goto('/chat')

      // Should redirect to login
      await page.waitForURL('/login', { timeout: 10000 })
      await expect(page).toHaveURL('/login')
    })
  })

  test.describe('User Logout', () => {
    test('should logout successfully', async ({ page }) => {
      // First login
      const testUser = generateTestUser()
      await page.goto('/register')
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="email"]', testUser.email)
      await page.locator('input[type="password"]').first().fill(testUser.password)
      await page.locator('input[type="password"]').last().fill(testUser.password)
      await page.click('button[type="submit"]')
      await page.waitForURL(/\/(login|chat)/, { timeout: 10000 })

      if (!page.url().includes('/chat')) {
        await page.goto('/login')
        await page.fill('input[type="text"]', testUser.username)
        await page.fill('input[type="password"]', testUser.password)
        await page.click('button[type="submit"]')
        await page.waitForURL('/chat', { timeout: 10000 })
      }

      // Navigate to settings and logout
      await page.goto('/settings')
      await page.click('button:has-text("Logout"), button:has-text("ログアウト")')

      // Should redirect to login
      await page.waitForURL('/login', { timeout: 10000 })
      await expect(page).toHaveURL('/login')

      // Verify cannot access protected routes
      await page.goto('/chat')
      await page.waitForURL('/login', { timeout: 10000 })
      await expect(page).toHaveURL('/login')
    })
  })

  test.describe('Navigation Links', () => {
    test('should navigate between login and register pages', async ({ page }) => {
      await page.goto('/login')

      // Click link to register
      await page.click('a:has-text("Register"), a:has-text("登録")')
      await expect(page).toHaveURL(/\/register/)

      // Click link back to login
      await page.click('a:has-text("Login"), a:has-text("ログイン")')
      await expect(page).toHaveURL(/\/login/)
    })
  })
})
