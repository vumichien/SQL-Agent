import { test, expect } from './fixtures/auth.fixture'

/**
 * E2E Tests: Query Workflow
 * Tests the complete query flow: question → SQL → results → visualization
 */

test.describe('Query Workflow', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    // Navigate to chat page
    await authenticatedPage.goto('/chat')
    await authenticatedPage.waitForSelector(
      '[data-testid="chat-input"], .chat-input, textarea',
      { timeout: 10000 }
    )
  })

  test('should display empty state on initial load', async ({ authenticatedPage }) => {
    // Check for empty state
    await expect(
      authenticatedPage.locator('.empty-state, [data-testid="empty-state"]')
    ).toBeVisible()

    // Check for suggested questions
    await expect(
      authenticatedPage.locator('.suggested-questions, [data-testid="suggested-questions"]')
    ).toBeVisible()
  })

  test('should send a question and receive response', async ({ authenticatedPage }) => {
    // Find chat input
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )

    // Type a question
    await chatInput.fill('How many customers are there?')

    // Submit the question (press Enter or click send button)
    await chatInput.press('Enter')

    // Wait for loading indicator
    await expect(
      authenticatedPage.locator('.loading-indicator, [data-testid="loading-indicator"]')
    ).toBeVisible({ timeout: 5000 })

    // Wait for response (SQL display or results)
    await expect(
      authenticatedPage.locator('.sql-display, .results-table, [data-testid="sql-display"]')
    ).toBeVisible({ timeout: 30000 })

    // Verify user message is displayed
    await expect(
      authenticatedPage.locator('.user-message:has-text("How many customers")')
    ).toBeVisible()

    // Verify assistant response is displayed
    await expect(
      authenticatedPage.locator('.assistant-message, [data-testid="assistant-message"]')
    ).toBeVisible()
  })

  test('should display SQL syntax highlighting', async ({ authenticatedPage }) => {
    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Show me the first 5 customers')
    await chatInput.press('Enter')

    // Wait for SQL display
    await authenticatedPage.waitForSelector('.sql-display, [data-testid="sql-display"]', {
      timeout: 30000,
    })

    // Verify SQL is displayed with syntax highlighting
    const sqlDisplay = authenticatedPage.locator('.sql-display, [data-testid="sql-display"]')
    await expect(sqlDisplay).toBeVisible()

    // Verify code element exists (Shiki generates code elements)
    await expect(sqlDisplay.locator('code, pre')).toBeVisible()
  })

  test('should display results table with data', async ({ authenticatedPage }) => {
    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('List all genres')
    await chatInput.press('Enter')

    // Wait for results table
    await authenticatedPage.waitForSelector('.results-table, .el-table, [role="table"]', {
      timeout: 30000,
    })

    // Verify table is displayed
    const resultsTable = authenticatedPage.locator('.results-table, .el-table')
    await expect(resultsTable).toBeVisible()

    // Verify table has headers and rows
    await expect(resultsTable.locator('thead, [role="rowgroup"]')).toBeVisible()
    await expect(resultsTable.locator('tbody tr, [role="row"]')).toHaveCount(1, {
      timeout: 5000,
    })
  })

  test('should copy SQL to clipboard', async ({ authenticatedPage, context }) => {
    // Grant clipboard permissions
    await context.grantPermissions(['clipboard-read', 'clipboard-write'])

    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Show albums')
    await chatInput.press('Enter')

    // Wait for SQL display
    await authenticatedPage.waitForSelector('.sql-display, [data-testid="sql-display"]', {
      timeout: 30000,
    })

    // Find and click copy button
    const copyButton = authenticatedPage.locator(
      'button:has-text("Copy"), button[title="Copy"], .copy-button'
    )
    await copyButton.first().click()

    // Wait for success notification
    await expect(
      authenticatedPage.locator('.el-message--success, [role="alert"]')
    ).toBeVisible({ timeout: 3000 })
  })

  test('should display Plotly chart when available', async ({ authenticatedPage }) => {
    // Send a question that typically generates a chart
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Show sales by country')
    await chatInput.press('Enter')

    // Wait for chart container
    await authenticatedPage.waitForSelector('.plotly-chart, [data-testid="plotly-chart"]', {
      timeout: 40000,
    })

    // Verify chart is displayed
    const chart = authenticatedPage.locator('.plotly-chart, [data-testid="plotly-chart"]')
    await expect(chart).toBeVisible()

    // Verify Plotly div exists
    await expect(chart.locator('.plotly, [data-plotly]')).toBeVisible({ timeout: 10000 })
  })

  test('should show loading indicator while processing', async ({ authenticatedPage }) => {
    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Complex query test')
    await chatInput.press('Enter')

    // Verify loading indicator appears immediately
    await expect(
      authenticatedPage.locator('.loading-indicator, [data-testid="loading-indicator"]')
    ).toBeVisible({ timeout: 2000 })

    // Verify typing animation or loading dots
    const loadingIndicator = authenticatedPage.locator(
      '.loading-indicator, [data-testid="loading-indicator"]'
    )
    await expect(loadingIndicator.locator('.dot, .typing-dot, span')).toHaveCount(3, {
      timeout: 2000,
    })
  })

  test('should auto-scroll to latest message', async ({ authenticatedPage }) => {
    // Send multiple questions
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )

    for (let i = 1; i <= 3; i++) {
      await chatInput.fill(`Question ${i}`)
      await chatInput.press('Enter')

      // Wait for response
      await authenticatedPage.waitForTimeout(2000)
    }

    // Verify the latest message is visible (auto-scrolled)
    const lastMessage = authenticatedPage.locator('.user-message:has-text("Question 3")')
    await expect(lastMessage).toBeVisible()
  })

  test('should disable input while processing', async ({ authenticatedPage }) => {
    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Test question')
    await chatInput.press('Enter')

    // Verify input is disabled during processing
    await expect(chatInput).toBeDisabled({ timeout: 2000 })

    // Wait for response
    await authenticatedPage.waitForSelector('.assistant-message, [data-testid="assistant-message"]', {
      timeout: 30000,
    })

    // Verify input is enabled after response
    await expect(chatInput).toBeEnabled({ timeout: 5000 })
  })

  test('should display error message on API failure', async ({ authenticatedPage }) => {
    // Mock API to return error
    await authenticatedPage.route('**/api/v0/query', (route) => {
      route.fulfill({
        status: 500,
        contentType: 'application/json',
        body: JSON.stringify({ error: 'Internal server error' }),
      })
    })

    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('This will fail')
    await chatInput.press('Enter')

    // Wait for error message
    await expect(
      authenticatedPage.locator('.el-message--error, [role="alert"]')
    ).toBeVisible({ timeout: 10000 })
  })

  test('should support multiline input with Shift+Enter', async ({ authenticatedPage }) => {
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )

    // Type first line
    await chatInput.fill('Line 1')

    // Press Shift+Enter for new line
    await chatInput.press('Shift+Enter')

    // Type second line
    await chatInput.type('Line 2')

    // Verify content has multiple lines
    const content = await chatInput.inputValue()
    expect(content).toContain('\n')
  })

  test('should click suggested question', async ({ authenticatedPage }) => {
    // Find first suggested question
    const suggestedQuestion = authenticatedPage
      .locator('.suggested-question, [data-testid="suggested-question"]')
      .first()

    // Click it
    await suggestedQuestion.click()

    // Verify question is added to input or submitted
    await expect(
      authenticatedPage.locator('.user-message, .loading-indicator')
    ).toBeVisible({ timeout: 5000 })
  })

  test('should download CSV from results table', async ({ authenticatedPage }) => {
    // Send a question
    const chatInput = authenticatedPage.locator(
      '[data-testid="chat-input"], .chat-input textarea, textarea'
    )
    await chatInput.fill('Show customers')
    await chatInput.press('Enter')

    // Wait for results table
    await authenticatedPage.waitForSelector('.results-table, .el-table', {
      timeout: 30000,
    })

    // Setup download handler
    const downloadPromise = authenticatedPage.waitForEvent('download')

    // Click download button
    const downloadButton = authenticatedPage.locator(
      'button:has-text("CSV"), button:has-text("Download"), .download-button'
    )
    await downloadButton.first().click()

    // Wait for download
    const download = await downloadPromise
    expect(download.suggestedFilename()).toContain('.csv')
  })
})
