import { test, expect } from './fixtures/auth.fixture'

/**
 * E2E Tests: UI Features
 * Tests theme switching, language switching, and responsive design
 */

test.describe('UI Features', () => {
  test.beforeEach(async ({ authenticatedPage }) => {
    // Navigate to chat page
    await authenticatedPage.goto('/chat')
    await authenticatedPage.waitForLoadState('networkidle')
  })

  test.describe('Theme Switching', () => {
    test('should toggle between light and dark mode', async ({ authenticatedPage }) => {
      // Find theme toggle button (usually in header)
      const themeToggle = authenticatedPage.locator(
        'button[title*="theme"], button:has([class*="moon"]), button:has([class*="sun"]), .theme-toggle'
      )

      // Get initial theme
      const htmlElement = authenticatedPage.locator('html')
      const initialTheme = await htmlElement.getAttribute('class')
      const isDarkInitially = initialTheme?.includes('dark')

      // Click theme toggle
      await themeToggle.first().click()

      // Wait for theme change
      await authenticatedPage.waitForTimeout(500)

      // Verify theme changed
      const newTheme = await htmlElement.getAttribute('class')
      const isDarkNow = newTheme?.includes('dark')

      expect(isDarkNow).not.toBe(isDarkInitially)

      // Toggle back
      await themeToggle.first().click()
      await authenticatedPage.waitForTimeout(500)

      // Verify theme reverted
      const finalTheme = await htmlElement.getAttribute('class')
      const isDarkFinal = finalTheme?.includes('dark')
      expect(isDarkFinal).toBe(isDarkInitially)
    })

    test('should persist theme preference across page reloads', async ({ authenticatedPage }) => {
      // Find theme toggle
      const themeToggle = authenticatedPage.locator(
        'button[title*="theme"], button:has([class*="moon"]), button:has([class*="sun"]), .theme-toggle'
      )

      // Set to dark mode
      const htmlElement = authenticatedPage.locator('html')
      let currentTheme = await htmlElement.getAttribute('class')

      if (!currentTheme?.includes('dark')) {
        await themeToggle.first().click()
        await authenticatedPage.waitForTimeout(500)
      }

      // Reload page
      await authenticatedPage.reload()
      await authenticatedPage.waitForLoadState('networkidle')

      // Verify dark mode persisted
      currentTheme = await htmlElement.getAttribute('class')
      expect(currentTheme).toContain('dark')
    })

    test('should update all components with theme change', async ({ authenticatedPage }) => {
      // Get initial background color of a component
      const chatContainer = authenticatedPage.locator(
        '.chat-container, .message-list, main, [data-testid="chat-container"]'
      )
      const initialBg = await chatContainer.first().evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor
      })

      // Toggle theme
      const themeToggle = authenticatedPage.locator(
        'button[title*="theme"], button:has([class*="moon"]), button:has([class*="sun"])'
      )
      await themeToggle.first().click()
      await authenticatedPage.waitForTimeout(500)

      // Get new background color
      const newBg = await chatContainer.first().evaluate((el) => {
        return window.getComputedStyle(el).backgroundColor
      })

      // Colors should be different
      expect(newBg).not.toBe(initialBg)
    })
  })

  test.describe('Language Switching', () => {
    test('should switch between English and Japanese', async ({ authenticatedPage }) => {
      // Find language toggle button
      const langToggle = authenticatedPage.locator(
        'button:has-text("EN"), button:has-text("JA"), button:has-text("日本語"), .language-toggle'
      )

      // Get initial button text
      const initialText = await langToggle.first().textContent()

      // Click to switch language
      await langToggle.first().click()
      await authenticatedPage.waitForTimeout(500)

      // Verify button text changed
      const newText = await langToggle.first().textContent()
      expect(newText).not.toBe(initialText)

      // Verify page content changed language
      const pageContent = await authenticatedPage.locator('body').textContent()

      if (newText?.includes('EN')) {
        // Now in Japanese, should see Japanese text
        expect(pageContent).toMatch(/チャット|メッセージ|送信/)
      } else {
        // Now in English, should see English text
        expect(pageContent).toMatch(/Chat|Message|Send/)
      }
    })

    test('should persist language preference across page reloads', async ({ authenticatedPage }) => {
      // Find language toggle
      const langToggle = authenticatedPage.locator(
        'button:has-text("EN"), button:has-text("JA"), button:has-text("日本語")'
      )

      // Switch to Japanese if not already
      const initialText = await langToggle.first().textContent()
      if (!initialText?.includes('EN')) {
        await langToggle.first().click()
        await authenticatedPage.waitForTimeout(500)
      }

      // Verify we're in Japanese
      let currentText = await langToggle.first().textContent()
      const isJapanese = currentText?.includes('EN') // Button shows EN when in JP mode

      // Reload page
      await authenticatedPage.reload()
      await authenticatedPage.waitForLoadState('networkidle')

      // Verify language persisted
      currentText = await langToggle.first().textContent()
      expect(currentText?.includes('EN')).toBe(isJapanese)
    })

    test('should translate all UI text when switching language', async ({ authenticatedPage }) => {
      // Switch to English first
      const langToggle = authenticatedPage.locator(
        'button:has-text("EN"), button:has-text("JA")'
      )

      let buttonText = await langToggle.first().textContent()
      if (buttonText?.includes('EN')) {
        // Already in Japanese, switch to English
        await langToggle.first().click()
        await authenticatedPage.waitForTimeout(500)
      }

      // Verify English text in common elements
      const pageContent = await authenticatedPage.locator('body').textContent()
      expect(pageContent).toMatch(/Chat|History|Training|Settings/)

      // Switch to Japanese
      await langToggle.first().click()
      await authenticatedPage.waitForTimeout(500)

      // Verify Japanese text
      const japaneseContent = await authenticatedPage.locator('body').textContent()
      expect(japaneseContent).toMatch(/チャット|履歴|トレーニング|設定/)
    })
  })

  test.describe('Responsive Design', () => {
    test('should adapt layout for mobile viewport', async ({ authenticatedPage, context }) => {
      // Set mobile viewport
      await authenticatedPage.setViewportSize({ width: 375, height: 667 })

      // Verify mobile layout (sidebar might be hidden)
      const sidebar = authenticatedPage.locator('.sidebar, .el-aside, aside')

      if (await sidebar.count() > 0) {
        const sidebarWidth = await sidebar.first().evaluate((el) => {
          return window.getComputedStyle(el).width
        })

        // On mobile, sidebar might be hidden or collapsed
        expect(sidebarWidth).toMatch(/0px|auto/)
      }
    })

    test('should show mobile menu button on small screens', async ({ authenticatedPage }) => {
      // Set mobile viewport
      await authenticatedPage.setViewportSize({ width: 375, height: 667 })

      // Find mobile menu button (hamburger)
      const menuButton = authenticatedPage.locator(
        'button[aria-label*="menu"], button:has([class*="menu"]), .mobile-menu-button'
      )

      if (await menuButton.count() > 0) {
        await expect(menuButton.first()).toBeVisible()
      }
    })

    test('should display properly on tablet viewport', async ({ authenticatedPage }) => {
      // Set tablet viewport
      await authenticatedPage.setViewportSize({ width: 768, height: 1024 })

      // Verify layout adapts
      const mainContent = authenticatedPage.locator('main, .main-content, .app-main')
      await expect(mainContent.first()).toBeVisible()

      // Verify no horizontal scroll
      const hasHorizontalScroll = await authenticatedPage.evaluate(() => {
        return document.documentElement.scrollWidth > document.documentElement.clientWidth
      })

      expect(hasHorizontalScroll).toBe(false)
    })
  })

  test.describe('Navigation', () => {
    test('should navigate between pages using sidebar', async ({ authenticatedPage }) => {
      // Click History link in sidebar
      const historyLink = authenticatedPage.locator(
        'a[href="/history"], a:has-text("History"), a:has-text("履歴")'
      )

      if (await historyLink.count() > 0) {
        await historyLink.first().click()
        await expect(authenticatedPage).toHaveURL('/history')
      }

      // Click Training link
      const trainingLink = authenticatedPage.locator(
        'a[href="/training"], a:has-text("Training"), a:has-text("トレーニング")'
      )

      if (await trainingLink.count() > 0) {
        await trainingLink.first().click()
        await expect(authenticatedPage).toHaveURL('/training')
      }

      // Click Settings link
      const settingsLink = authenticatedPage.locator(
        'a[href="/settings"], a:has-text("Settings"), a:has-text("設定")'
      )

      if (await settingsLink.count() > 0) {
        await settingsLink.first().click()
        await expect(authenticatedPage).toHaveURL('/settings')
      }

      // Navigate back to chat
      const chatLink = authenticatedPage.locator(
        'a[href="/chat"], a:has-text("Chat"), a:has-text("チャット")'
      )

      if (await chatLink.count() > 0) {
        await chatLink.first().click()
        await expect(authenticatedPage).toHaveURL('/chat')
      }
    })

    test('should highlight active navigation item', async ({ authenticatedPage }) => {
      // Navigate to different pages and verify active state
      await authenticatedPage.goto('/chat')

      const chatLink = authenticatedPage.locator(
        'a[href="/chat"], nav a:has-text("Chat"), nav a:has-text("チャット")'
      )

      if (await chatLink.count() > 0) {
        // Check if active class is applied
        const classes = await chatLink.first().getAttribute('class')
        expect(classes).toMatch(/active|is-active|router-link-active/)
      }
    })

    test('should display breadcrumbs', async ({ authenticatedPage }) => {
      // Navigate to a page
      await authenticatedPage.goto('/training')

      // Find breadcrumb
      const breadcrumb = authenticatedPage.locator('.el-breadcrumb, .breadcrumb, nav[aria-label="Breadcrumb"]')

      if (await breadcrumb.count() > 0) {
        await expect(breadcrumb.first()).toBeVisible()

        // Verify breadcrumb shows current page
        const breadcrumbText = await breadcrumb.textContent()
        expect(breadcrumbText).toMatch(/Training|トレーニング/)
      }
    })
  })

  test.describe('User Profile', () => {
    test('should display user profile in header', async ({ authenticatedPage }) => {
      // Find user profile button/dropdown
      const userProfile = authenticatedPage.locator(
        '.user-profile, .el-dropdown, [data-testid="user-profile"]'
      )

      if (await userProfile.count() > 0) {
        await expect(userProfile.first()).toBeVisible()
      }
    })

    test('should open user dropdown menu', async ({ authenticatedPage }) => {
      // Find user profile dropdown
      const userDropdown = authenticatedPage.locator(
        '.user-profile, .el-dropdown, button:has([class*="user"])'
      )

      if (await userDropdown.count() > 0) {
        await userDropdown.first().click()

        // Verify dropdown menu is visible
        await expect(
          authenticatedPage.locator('.el-dropdown-menu, [role="menu"]')
        ).toBeVisible({ timeout: 3000 })

        // Verify menu items
        await expect(
          authenticatedPage.locator('.el-dropdown-menu__item, [role="menuitem"]')
        ).toHaveCount(1, { timeout: 2000 })
      }
    })
  })

  test.describe('Accessibility', () => {
    test('should be keyboard navigable', async ({ authenticatedPage }) => {
      // Tab through interactive elements
      await authenticatedPage.keyboard.press('Tab')
      await authenticatedPage.keyboard.press('Tab')
      await authenticatedPage.keyboard.press('Tab')

      // Verify focus is visible
      const focusedElement = await authenticatedPage.evaluate(() => {
        return document.activeElement?.tagName
      })

      expect(focusedElement).toMatch(/BUTTON|INPUT|A|TEXTAREA/)
    })

    test('should have proper ARIA labels', async ({ authenticatedPage }) => {
      // Check for ARIA labels on key elements
      const buttons = authenticatedPage.locator('button[aria-label], button[title]')
      const inputs = authenticatedPage.locator('input[aria-label], input[placeholder]')

      const buttonCount = await buttons.count()
      const inputCount = await inputs.count()

      expect(buttonCount + inputCount).toBeGreaterThan(0)
    })
  })

  test.describe('Performance', () => {
    test('should load page within reasonable time', async ({ authenticatedPage }) => {
      const startTime = Date.now()

      await authenticatedPage.goto('/chat')
      await authenticatedPage.waitForLoadState('networkidle')

      const loadTime = Date.now() - startTime

      // Page should load within 5 seconds
      expect(loadTime).toBeLessThan(5000)
    })

    test('should have no console errors', async ({ authenticatedPage }) => {
      const consoleErrors: string[] = []

      authenticatedPage.on('console', (message) => {
        if (message.type() === 'error') {
          consoleErrors.push(message.text())
        }
      })

      await authenticatedPage.goto('/chat')
      await authenticatedPage.waitForLoadState('networkidle')
      await authenticatedPage.waitForTimeout(2000)

      // Filter out known acceptable errors (like network errors in test environment)
      const criticalErrors = consoleErrors.filter(
        (error) =>
          !error.includes('Failed to load resource') &&
          !error.includes('net::ERR_') &&
          !error.includes('404')
      )

      expect(criticalErrors.length).toBe(0)
    })
  })
})
