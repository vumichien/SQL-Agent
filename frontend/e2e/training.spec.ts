import { test, expect } from './fixtures/auth.fixture'

/**
 * E2E Tests: Training Data Management
 * Tests adding, viewing, searching, and deleting training data
 */

test.describe('Training Data Management', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    // Navigate to training page
    await authenticatedPage.goto('/training')
    await authenticatedPage.waitForLoadState('networkidle')
  })

  test('should display training data page', async ({ authenticatedPage }) => {
    // Verify page title
    await expect(
      authenticatedPage.locator('h1:has-text("Training"), h1:has-text("トレーニング")')
    ).toBeVisible()

    // Verify training data table or empty state
    const table = authenticatedPage.locator('.el-table, [role="table"]')
    const emptyState = authenticatedPage.locator('.el-empty, .empty-state')

    // Either table or empty state should be visible
    const tableVisible = await table.isVisible().catch(() => false)
    const emptyVisible = await emptyState.isVisible().catch(() => false)

    expect(tableVisible || emptyVisible).toBe(true)
  })

  test('should display statistics cards', async ({ authenticatedPage }) => {
    // Check for statistics cards (SQL, DDL, Documentation counts)
    const statCards = authenticatedPage.locator('.el-card, .stat-card, [data-testid="stat-card"]')

    if (await statCards.count() > 0) {
      await expect(statCards.first()).toBeVisible()
    }
  })

  test('should open add training modal', async ({ authenticatedPage }) => {
    // Find and click add button
    const addButton = authenticatedPage.locator(
      'button:has-text("Add"), button:has-text("追加"), .add-training-button'
    )
    await addButton.first().click()

    // Verify modal is visible
    await expect(
      authenticatedPage.locator('.el-dialog, [role="dialog"]')
    ).toBeVisible({ timeout: 5000 })

    // Verify modal title
    await expect(
      authenticatedPage.locator('.el-dialog__header:has-text("Add"), .el-dialog__header:has-text("追加")')
    ).toBeVisible()
  })

  test('should add SQL training data', async ({ authenticatedPage }) => {
    // Click add button
    const addButton = authenticatedPage.locator(
      'button:has-text("Add"), button:has-text("追加"), .add-training-button'
    )
    await addButton.first().click()

    // Wait for dialog
    await authenticatedPage.waitForSelector('.el-dialog', { timeout: 5000 })

    // Select SQL tab
    const sqlTab = authenticatedPage.locator('.el-tabs__item:has-text("SQL")')
    if (await sqlTab.count() > 0) {
      await sqlTab.click()
    }

    // Fill question field
    const questionInput = authenticatedPage.locator('input[placeholder*="question"], textarea[placeholder*="question"]')
    await questionInput.first().fill(`Test question ${Date.now()}`)

    // Fill SQL field
    const sqlInput = authenticatedPage.locator('textarea[placeholder*="SQL"], input[placeholder*="SQL"]')
    await sqlInput.first().fill('SELECT * FROM Customer LIMIT 10')

    // Submit form
    const submitButton = authenticatedPage.locator(
      '.el-dialog button:has-text("Add"), .el-dialog button:has-text("Submit"), .el-dialog button[type="submit"]'
    )
    await submitButton.click()

    // Wait for success message
    await expect(
      authenticatedPage.locator('.el-message--success, [role="alert"]')
    ).toBeVisible({ timeout: 5000 })
  })

  test('should add DDL training data', async ({ authenticatedPage }) => {
    // Click add button
    const addButton = authenticatedPage.locator(
      'button:has-text("Add"), button:has-text("追加"), .add-training-button'
    )
    await addButton.first().click()

    // Wait for dialog
    await authenticatedPage.waitForSelector('.el-dialog', { timeout: 5000 })

    // Select DDL tab
    const ddlTab = authenticatedPage.locator('.el-tabs__item:has-text("DDL")')
    await ddlTab.click()

    // Fill DDL field
    const ddlInput = authenticatedPage.locator('textarea[placeholder*="DDL"], textarea[placeholder*="CREATE"]')
    await ddlInput.first().fill('CREATE TABLE TestTable (id INT PRIMARY KEY, name TEXT)')

    // Submit form
    const submitButton = authenticatedPage.locator(
      '.el-dialog button:has-text("Add"), .el-dialog button:has-text("Submit")'
    )
    await submitButton.click()

    // Wait for success message
    await expect(
      authenticatedPage.locator('.el-message--success, [role="alert"]')
    ).toBeVisible({ timeout: 5000 })
  })

  test('should add Documentation training data', async ({ authenticatedPage }) => {
    // Click add button
    const addButton = authenticatedPage.locator(
      'button:has-text("Add"), button:has-text("追加"), .add-training-button'
    )
    await addButton.first().click()

    // Wait for dialog
    await authenticatedPage.waitForSelector('.el-dialog', { timeout: 5000 })

    // Select Documentation tab
    const docTab = authenticatedPage.locator('.el-tabs__item:has-text("Documentation"), .el-tabs__item:has-text("ドキュメント")')
    await docTab.click()

    // Fill documentation field
    const docInput = authenticatedPage.locator('textarea[placeholder*="documentation"], textarea[placeholder*="ドキュメント"]')
    await docInput.first().fill(`Test documentation content ${Date.now()}`)

    // Submit form
    const submitButton = authenticatedPage.locator(
      '.el-dialog button:has-text("Add"), .el-dialog button:has-text("Submit")'
    )
    await submitButton.click()

    // Wait for success message
    await expect(
      authenticatedPage.locator('.el-message--success, [role="alert"]')
    ).toBeVisible({ timeout: 5000 })
  })

  test('should validate required fields', async ({ authenticatedPage }) => {
    // Click add button
    const addButton = authenticatedPage.locator(
      'button:has-text("Add"), button:has-text("追加"), .add-training-button'
    )
    await addButton.first().click()

    // Wait for dialog
    await authenticatedPage.waitForSelector('.el-dialog', { timeout: 5000 })

    // Try to submit without filling fields
    const submitButton = authenticatedPage.locator(
      '.el-dialog button:has-text("Add"), .el-dialog button:has-text("Submit")'
    )
    await submitButton.click()

    // Verify validation error or button is disabled
    const errorMessage = authenticatedPage.locator('.el-form-item__error, .error-message')
    const isButtonDisabled = await submitButton.isDisabled()

    const hasError = await errorMessage.count() > 0
    expect(hasError || isButtonDisabled).toBe(true)
  })

  test('should search training data', async ({ authenticatedPage }) => {
    // Find search input
    const searchInput = authenticatedPage.locator(
      'input[placeholder*="Search"], input[placeholder*="検索"]'
    )

    if (await searchInput.count() > 0) {
      // Type search query
      await searchInput.fill('Customer')

      // Wait for filtering
      await authenticatedPage.waitForTimeout(1000)

      // Verify results are filtered
      const rows = authenticatedPage.locator('.el-table tbody tr, [role="row"]')
      if (await rows.count() > 0) {
        const firstRow = rows.first()
        const text = await firstRow.textContent()
        // Results should contain search term (case-insensitive)
        expect(text?.toLowerCase()).toContain('customer')
      }
    }
  })

  test('should view training data details', async ({ authenticatedPage }) => {
    // Find table rows
    const rows = authenticatedPage.locator('.el-table tbody tr, [role="row"]')

    if (await rows.count() > 0) {
      // Find and click view button on first row
      const viewButton = rows.first().locator('button:has-text("View"), button:has-text("表示")')

      if (await viewButton.count() > 0) {
        await viewButton.click()

        // Verify view modal is visible
        await expect(
          authenticatedPage.locator('.el-dialog:has-text("View"), .el-dialog:has-text("詳細")')
        ).toBeVisible({ timeout: 5000 })

        // Close modal
        const closeButton = authenticatedPage.locator('.el-dialog__close, button[aria-label="Close"]')
        await closeButton.first().click()
      }
    }
  })

  test('should delete training data', async ({ authenticatedPage }) => {
    // Find table rows
    const rows = authenticatedPage.locator('.el-table tbody tr, [role="row"]')

    if (await rows.count() > 0) {
      const initialCount = await rows.count()

      // Find and click delete button on first row
      const deleteButton = rows.first().locator('button:has-text("Delete"), button:has-text("削除")')

      if (await deleteButton.count() > 0) {
        await deleteButton.click()

        // Confirm deletion
        const confirmButton = authenticatedPage.locator(
          'button:has-text("Confirm"), button:has-text("Yes"), button:has-text("確認")'
        )
        await confirmButton.first().click()

        // Wait for success message
        await expect(
          authenticatedPage.locator('.el-message--success, [role="alert"]')
        ).toBeVisible({ timeout: 5000 })

        // Wait for table to update
        await authenticatedPage.waitForTimeout(2000)

        // Verify row count decreased
        const newCount = await rows.count()
        expect(newCount).toBeLessThan(initialCount)
      }
    }
  })

  test('should paginate training data', async ({ authenticatedPage }) => {
    // Find pagination controls
    const pagination = authenticatedPage.locator('.el-pagination')

    if (await pagination.isVisible()) {
      // Find next page button
      const nextButton = pagination.locator('button.btn-next, button:has-text("Next")')

      if (await nextButton.isEnabled()) {
        await nextButton.click()

        // Wait for page to load
        await authenticatedPage.waitForTimeout(1000)

        // Verify pagination changed
        const currentPage = pagination.locator('.number.active, .is-active')
        await expect(currentPage).toHaveText('2')
      }
    }
  })

  test('should change page size', async ({ authenticatedPage }) => {
    // Find page size selector
    const pageSizeSelect = authenticatedPage.locator('.el-pagination__sizes .el-select')

    if (await pageSizeSelect.count() > 0) {
      await pageSizeSelect.click()

      // Select different page size (e.g., 50)
      const option = authenticatedPage.locator('.el-select-dropdown__item:has-text("50")')
      if (await option.count() > 0) {
        await option.click()

        // Wait for table to update
        await authenticatedPage.waitForTimeout(1000)

        // Verify more rows are displayed
        const rows = authenticatedPage.locator('.el-table tbody tr')
        const count = await rows.count()
        expect(count).toBeGreaterThan(10)
      }
    }
  })

  test('should filter by training data type', async ({ authenticatedPage }) => {
    // Find filter dropdown or tabs
    const typeFilter = authenticatedPage.locator(
      '.el-select[placeholder*="Type"], .type-filter, .el-tabs'
    )

    if (await typeFilter.count() > 0) {
      // If it's a select dropdown
      if (await typeFilter.locator('.el-select').count() > 0) {
        await typeFilter.click()

        // Select SQL type
        const sqlOption = authenticatedPage.locator('.el-select-dropdown__item:has-text("SQL")')
        await sqlOption.first().click()

        // Wait for filtering
        await authenticatedPage.waitForTimeout(1000)

        // Verify filtered results
        const rows = authenticatedPage.locator('.el-table tbody tr')
        if (await rows.count() > 0) {
          const firstRow = rows.first()
          const text = await firstRow.textContent()
          expect(text).toContain('sql')
        }
      }
    }
  })

  test('should close add modal with cancel button', async ({ authenticatedPage }) => {
    // Click add button
    const addButton = authenticatedPage.locator(
      'button:has-text("Add"), button:has-text("追加"), .add-training-button'
    )
    await addButton.first().click()

    // Wait for dialog
    await authenticatedPage.waitForSelector('.el-dialog', { timeout: 5000 })

    // Click cancel button
    const cancelButton = authenticatedPage.locator(
      '.el-dialog button:has-text("Cancel"), .el-dialog button:has-text("キャンセル")'
    )
    await cancelButton.click()

    // Verify modal is closed
    await expect(authenticatedPage.locator('.el-dialog')).not.toBeVisible({ timeout: 2000 })
  })
})
