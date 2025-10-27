import { test, expect } from './fixtures/auth.fixture'

/**
 * E2E Tests: Query History
 * Tests history sidebar, loading history items, and deleting history
 */

test.describe('Query History', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    // Navigate to chat page
    await authenticatedPage.goto('/chat')
    await authenticatedPage.waitForSelector(
      '[data-testid="chat-input"], .chat-input, textarea',
      { timeout: 10000 }
    )
  })

  test('should open and close history sidebar', async ({ authenticatedPage }) => {
    // Find and click history button
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button, [data-testid="history-button"]'
    )
    await historyButton.click()

    // Verify sidebar is visible
    await expect(
      authenticatedPage.locator('.history-sidebar, .el-drawer, [role="dialog"]')
    ).toBeVisible({ timeout: 5000 })

    // Close sidebar by clicking close button or backdrop
    const closeButton = authenticatedPage.locator(
      '.el-drawer__close, button[aria-label="Close"], .close-button'
    )
    await closeButton.first().click()

    // Verify sidebar is hidden
    await expect(
      authenticatedPage.locator('.history-sidebar, .el-drawer')
    ).not.toBeVisible({ timeout: 5000 })
  })

  test('should display history items after queries', async ({ authenticatedPage }) => {
    // Send a few questions first
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )

    // Send first question
    await chatInput.fill('How many customers?')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(3000)

    // Send second question
    await chatInput.fill('Show all albums')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(3000)

    // Open history sidebar
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button, [data-testid="history-button"]'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Verify history items are displayed
    const historyItems = authenticatedPage.locator('.history-item, [data-testid="history-item"]')
    await expect(historyItems.first()).toBeVisible({ timeout: 5000 })

    // Verify at least 2 items (our queries)
    const count = await historyItems.count()
    expect(count).toBeGreaterThanOrEqual(2)
  })

  test('should load history item when clicked', async ({ authenticatedPage }) => {
    // Send a unique question
    const uniqueQuestion = `Test query at ${Date.now()}`
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill(uniqueQuestion)
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(3000)

    // Clear chat by refreshing
    await authenticatedPage.reload()
    await authenticatedPage.waitForSelector(
      '[data-testid="chat-input"], .chat-input, textarea',
      { timeout: 10000 }
    )

    // Open history sidebar
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Find and click the history item with our unique question
    const historyItem = authenticatedPage.locator(
      `.history-item:has-text("${uniqueQuestion}"), [data-testid="history-item"]:has-text("${uniqueQuestion}")`
    )
    await historyItem.first().click()

    // Wait for messages to load
    await authenticatedPage.waitForTimeout(2000)

    // Verify the question is loaded in the chat
    await expect(
      authenticatedPage.locator(`.user-message:has-text("${uniqueQuestion}")`)
    ).toBeVisible({ timeout: 5000 })
  })

  test('should search/filter history items', async ({ authenticatedPage }) => {
    // Send a few different questions
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )

    await chatInput.fill('Show customers')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(2000)

    await chatInput.fill('Show albums')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(2000)

    // Open history sidebar
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Find search input
    const searchInput = authenticatedPage.locator(
      '.history-sidebar input[type="text"], .el-drawer input[placeholder*="Search"], [data-testid="history-search"]'
    )

    if (await searchInput.count() > 0) {
      // Type search query
      await searchInput.fill('customers')

      // Wait for filtering
      await authenticatedPage.waitForTimeout(1000)

      // Verify filtered results
      const historyItems = authenticatedPage.locator('.history-item, [data-testid="history-item"]')
      const visibleItems = await historyItems.filter({ hasText: 'customers' }).count()
      expect(visibleItems).toBeGreaterThan(0)
    }
  })

  test('should delete history item', async ({ authenticatedPage }) => {
    // Send a unique question
    const uniqueQuestion = `Delete test at ${Date.now()}`
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill(uniqueQuestion)
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(3000)

    // Open history sidebar
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Find the history item
    const historyItem = authenticatedPage.locator(
      `.history-item:has-text("${uniqueQuestion}"), [data-testid="history-item"]:has-text("${uniqueQuestion}")`
    )

    // Find and click delete button within the item
    const deleteButton = historyItem.locator(
      'button[title*="Delete"], button:has([class*="delete"]), .delete-button'
    )
    await deleteButton.first().click()

    // Confirm deletion in dialog if present
    const confirmButton = authenticatedPage.locator(
      'button:has-text("Confirm"), button:has-text("Yes"), button:has-text("確認"), .el-message-box__btns button'
    )
    if (await confirmButton.count() > 0) {
      await confirmButton.first().click()
    }

    // Wait for deletion
    await authenticatedPage.waitForTimeout(2000)

    // Verify item is removed
    await expect(historyItem).not.toBeVisible({ timeout: 5000 })
  })

  test('should show empty state when no history', async ({ authenticatedPage }) => {
    // Open history sidebar on fresh account
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Check for empty state (might have items if previous tests ran)
    const emptyState = authenticatedPage.locator(
      '.empty-state, [data-testid="empty-state"], .el-empty'
    )
    const historyItems = authenticatedPage.locator('.history-item, [data-testid="history-item"]')

    const itemCount = await historyItems.count()
    if (itemCount === 0) {
      await expect(emptyState).toBeVisible()
    }
  })

  test('should refresh history', async ({ authenticatedPage }) => {
    // Open history sidebar
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Find refresh button
    const refreshButton = authenticatedPage.locator(
      'button[title*="Refresh"], button:has([class*="refresh"]), .refresh-button'
    )

    if (await refreshButton.count() > 0) {
      await refreshButton.first().click()

      // Wait for refresh to complete
      await authenticatedPage.waitForTimeout(1000)

      // Verify history items are still visible
      const historyItems = authenticatedPage.locator('.history-item, [data-testid="history-item"]')
      if (await historyItems.count() > 0) {
        await expect(historyItems.first()).toBeVisible()
      }
    }
  })

  test('should display history item timestamp', async ({ authenticatedPage }) => {
    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Show tracks')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(3000)

    // Open history sidebar
    const historyButton = authenticatedPage.locator(
      'button[title*="History"], button:has-text("History"), .history-button'
    )
    await historyButton.click()

    // Wait for history sidebar
    await authenticatedPage.waitForSelector('.history-sidebar, .el-drawer', { timeout: 5000 })

    // Verify timestamp is displayed (relative time like "just now", "1 min ago")
    const historyItem = authenticatedPage.locator('.history-item, [data-testid="history-item"]')
    const timestamp = historyItem.first().locator(
      '.timestamp, [data-testid="timestamp"], .time, small'
    )
    await expect(timestamp).toBeVisible()
  })

  test('should show badge with history count', async ({ authenticatedPage }) => {
    // Send a few questions to create history
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )

    await chatInput.fill('Query 1')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(2000)

    await chatInput.fill('Query 2')
    await chatInput.press('Enter')
    await authenticatedPage.waitForTimeout(2000)

    // Check for badge on history button
    const badge = authenticatedPage.locator(
      '.el-badge__content, .badge, [data-testid="history-badge"]'
    )

    if (await badge.count() > 0) {
      await expect(badge).toBeVisible()
      const badgeText = await badge.textContent()
      expect(parseInt(badgeText || '0')).toBeGreaterThan(0)
    }
  })
})
