/**
 * API Fixture
 * Provides mock API responses for E2E tests
 */

export const mockQueryResponse = {
  id: 'test-query-123',
  type: 'sql',
  text: 'SELECT * FROM Customer LIMIT 5',
  df: {
    columns: ['CustomerId', 'FirstName', 'LastName', 'Email'],
    data: [
      [1, 'John', 'Doe', 'john@example.com'],
      [2, 'Jane', 'Smith', 'jane@example.com'],
      [3, 'Bob', 'Johnson', 'bob@example.com'],
      [4, 'Alice', 'Williams', 'alice@example.com'],
      [5, 'Charlie', 'Brown', 'charlie@example.com'],
    ],
  },
  fig: null,
  error: null,
  success: true,
}

export const mockPlotlyResponse = {
  data: [
    {
      x: ['John', 'Jane', 'Bob', 'Alice', 'Charlie'],
      y: [5, 8, 3, 10, 7],
      type: 'bar',
    },
  ],
  layout: {
    title: 'Sample Chart',
    xaxis: { title: 'Names' },
    yaxis: { title: 'Values' },
  },
}

export const mockHistoryResponse = [
  {
    id: 'hist-1',
    question: 'How many customers are there?',
    sql: 'SELECT COUNT(*) FROM Customer',
    timestamp: new Date().toISOString(),
  },
  {
    id: 'hist-2',
    question: 'Show top 5 albums',
    sql: 'SELECT * FROM Album LIMIT 5',
    timestamp: new Date(Date.now() - 3600000).toISOString(),
  },
]

export const mockTrainingData = [
  {
    id: 'train-1',
    training_data_type: 'sql',
    question: 'How many customers?',
    content: 'SELECT COUNT(*) FROM Customer',
  },
  {
    id: 'train-2',
    training_data_type: 'ddl',
    question: null,
    content: 'CREATE TABLE Customer (CustomerId INT, FirstName TEXT, ...)',
  },
  {
    id: 'train-3',
    training_data_type: 'documentation',
    question: null,
    content: 'Customer table stores customer information...',
  },
]

/**
 * Setup mock API routes
 */
export async function setupMockAPI(page: any) {
  // Mock health endpoint
  await page.route('**/api/v0/health', (route: any) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify({ status: 'healthy', database: 'connected' }),
    })
  })

  // Mock query endpoint
  await page.route('**/api/v0/query', (route: any) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockQueryResponse),
    })
  })

  // Mock history endpoint
  await page.route('**/api/v0/get_question_history', (route: any) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockHistoryResponse),
    })
  })

  // Mock training data endpoint
  await page.route('**/api/v0/get_training_data', (route: any) => {
    route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(mockTrainingData),
    })
  })
}
