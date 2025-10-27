import { test as base, Page } from '@playwright/test'

/**
 * Authentication Fixture
 * Provides helpers for user authentication in E2E tests
 */

export interface AuthFixture {
  authenticatedPage: Page
}

/**
 * Generate random test user credentials
 */
export function generateTestUser() {
  const timestamp = Date.now()
  return {
    username: `testuser_${timestamp}`,
    email: `testuser_${timestamp}@example.com`,
    password: 'TestPassword123!',
  }
}

/**
 * Extended test with authentication helpers
 */
export const test = base.extend<AuthFixture>({
  authenticatedPage: async ({ page }, use) => {
    // Register and login with a fresh user
    const testUser = generateTestUser()

    // Go to register page
    await page.goto('/register')

    // Fill registration form
    await page.fill('input[type="text"]', testUser.username)
    await page.fill('input[type="email"]', testUser.email)
    await page.locator('input[type="password"]').first().fill(testUser.password)
    await page.locator('input[type="password"]').last().fill(testUser.password)

    // Submit registration
    await page.click('button[type="submit"]')

    // Wait for redirect to login or chat
    await page.waitForURL(/\/(login|chat)/, { timeout: 10000 })

    // If redirected to login, login
    if (page.url().includes('/login')) {
      await page.fill('input[type="text"]', testUser.username)
      await page.fill('input[type="password"]', testUser.password)
      await page.click('button[type="submit"]')
      await page.waitForURL('/chat', { timeout: 10000 })
    }

    // Verify we're authenticated
    await page.waitForSelector('[data-testid="chat-input"], .chat-input', { timeout: 10000 })

    // Use the authenticated page
    await use(page)

    // Cleanup: logout after test
    try {
      await page.goto('/settings')
      await page.click('button:has-text("Logout"), button:has-text("ログアウト")')
    } catch (error) {
      // Ignore logout errors
      console.log('Logout cleanup failed:', error)
    }
  },
})

export { expect } from '@playwright/test'
