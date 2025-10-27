# E2E Tests - Playwright

This directory contains end-to-end tests for the Detomo SQL AI frontend application.

## Overview

The E2E tests use [Playwright](https://playwright.dev/) to test the complete application flow from the user's perspective, covering:

- **Authentication**: User registration, login, logout
- **Query Workflow**: Asking questions, viewing SQL, results, and visualizations
- **History Management**: Viewing, loading, searching, and deleting query history
- **Training Data**: Managing training data (add, view, search, delete)
- **UI Features**: Theme switching, language switching, responsive design

## Test Structure

```
e2e/
├── fixtures/          # Test fixtures and helpers
│   ├── auth.fixture.ts    # Authentication helpers
│   └── api.fixture.ts     # API mocks
├── auth.spec.ts       # Authentication tests
├── query.spec.ts      # Query workflow tests
├── history.spec.ts    # History management tests
├── training.spec.ts   # Training data tests
└── ui.spec.ts         # UI features tests
```

## Running Tests

### Run All Tests
```bash
npm run test:e2e
```

### Run Tests with UI Mode (Interactive)
```bash
npm run test:e2e:ui
```

### Run Tests in Debug Mode
```bash
npm run test:e2e:debug
```

### Run Tests in Headed Mode (See Browser)
```bash
npm run test:e2e:headed
```

### Run Tests for Specific Browser
```bash
# Chromium only
npm run test:e2e:chromium

# Firefox only
npm run test:e2e:firefox

# Webkit (Safari) only
npm run test:e2e:webkit
```

### View Test Report
```bash
npm run test:e2e:report
```

## Test Configuration

Configuration is in `playwright.config.ts`:

- **Browsers**: Chromium, Firefox, Webkit
- **Base URL**: http://localhost:5174
- **Timeout**: 60s per test
- **Retries**: 2 retries on CI, 0 locally
- **Screenshots**: On failure
- **Video**: On failure
- **Trace**: On first retry

## Writing Tests

### Using Authentication Fixture

For tests that require authentication, use the `authenticatedPage` fixture:

```typescript
import { test, expect } from './fixtures/auth.fixture'

test('should do something authenticated', async ({ authenticatedPage }) => {
  await authenticatedPage.goto('/chat')
  // Test code...
})
```

This automatically:
1. Registers a new test user
2. Logs in
3. Navigates to the page
4. Cleans up (logs out) after the test

### Using API Mocks

For tests that need to mock API responses:

```typescript
import { setupMockAPI } from './fixtures/api.fixture'

test('should work with mocked API', async ({ page }) => {
  await setupMockAPI(page)
  // Test code...
})
```

## Best Practices

1. **Use Data Test IDs**: Prefer `[data-testid]` selectors over CSS classes
2. **Wait for Elements**: Always wait for elements to be visible before interacting
3. **Clean State**: Each test should be independent and not rely on previous test state
4. **Use Fixtures**: Use the authentication fixture for tests requiring login
5. **Mock When Appropriate**: Mock API calls for faster, more reliable tests
6. **Check Visibility**: Always verify elements are visible before assertions
7. **Handle Timeouts**: Use appropriate timeouts for network operations

## Debugging

### Run Specific Test File
```bash
npx playwright test e2e/auth.spec.ts
```

### Run Specific Test
```bash
npx playwright test e2e/auth.spec.ts -g "should login with valid credentials"
```

### Debug Mode with Inspector
```bash
npx playwright test --debug
```

### View Trace
After a test failure, view the trace:
```bash
npx playwright show-trace playwright-report/trace.zip
```

## CI Integration

Tests are configured to run in CI with:
- 2 retries on failure
- Single worker (no parallelization)
- Full traces on failure
- JSON report output

## Prerequisites

Before running E2E tests:

1. **Backend Server**: Ensure backend is running on http://localhost:8000
2. **Frontend Dev Server**: Automatically started by Playwright (or start manually)
3. **Database**: Backend should have access to database

## Common Issues

### Tests Timing Out
- Increase timeout in `playwright.config.ts`
- Check if backend is running
- Check network connectivity

### Authentication Issues
- Clear browser storage between test runs
- Verify backend auth endpoints are working
- Check for unique usernames (tests use timestamps)

### Element Not Found
- Add explicit waits: `await page.waitForSelector()`
- Check if element IDs/classes match
- Use Playwright Inspector to debug: `--debug`

### Flaky Tests
- Add explicit waits instead of timeouts
- Check for race conditions
- Ensure proper cleanup between tests

## Resources

- [Playwright Documentation](https://playwright.dev/docs/intro)
- [Playwright Best Practices](https://playwright.dev/docs/best-practices)
- [Playwright API Reference](https://playwright.dev/docs/api/class-playwright)
- [Test Fixtures](https://playwright.dev/docs/test-fixtures)

## Test Coverage

Current E2E test coverage:

- ✅ User Registration (4 tests)
- ✅ User Login (3 tests)
- ✅ User Logout (1 test)
- ✅ Query Workflow (14 tests)
- ✅ History Management (9 tests)
- ✅ Training Data Management (12 tests)
- ✅ UI Features (15+ tests)

**Total: 58+ E2E tests**
