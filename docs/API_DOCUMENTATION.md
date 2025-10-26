# API Documentation - Detomo SQL AI

**Project**: Detomo SQL AI v2.0
**API Version**: 2.0.0
**Base URL**: `http://localhost:8000`
**Last Updated**: 2025-10-26

---

## Table of Contents

1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Core Endpoints](#core-endpoints)
4. [Multi-Step Workflow Endpoints](#multi-step-workflow-endpoints)
5. [Training Data Endpoints](#training-data-endpoints)
6. [Utility Endpoints](#utility-endpoints)
7. [Error Handling](#error-handling)
8. [Rate Limiting](#rate-limiting)
9. [Examples](#examples)

---

## Overview

The Detomo SQL AI API provides two approaches for converting natural language to SQL:

### **Approach 1: All-in-One** (Simple)
Single endpoint that does everything: NL → SQL → Execute → Visualize

**Use when**: You want a simple, one-call solution

**Endpoint**: `POST /api/v0/query`

### **Approach 2: Multi-Step** (Advanced)
Separate endpoints for each step, with caching between steps

**Use when**: You need fine-grained control or want to cache intermediate results

**Endpoints**: `generate_sql` → `run_sql` → `generate_plotly_figure`

---

## Authentication

**Current Version**: No authentication required (MVP)

**Production**: Will require API key in header:
```
Authorization: Bearer YOUR_API_KEY
```

---

## Core Endpoints

### 1. Query (All-in-One)

Convert natural language to SQL, execute it, and generate visualization in a single call.

**Endpoint**: `POST /api/v0/query`

**Request Body**:
```json
{
  "question": "How many customers are there?",
  "language": "en"
}
```

**Parameters**:
- `question` (string, required): Natural language question in English or Japanese
- `language` (string, optional): Language code (`"en"` or `"jp"`), default: `"en"`

**Response** (200 OK):
```json
{
  "question": "How many customers are there?",
  "sql": "SELECT COUNT(*) FROM Customer",
  "results": [
    {
      "COUNT(*)": 59
    }
  ],
  "columns": ["COUNT(*)"],
  "visualization": {
    "data": [...],
    "layout": {...}
  },
  "row_count": 1
}
```

**Response Fields**:
- `question`: Original question
- `sql`: Generated SQL query
- `results`: Query results as array of objects
- `columns`: Column names in results
- `visualization`: Plotly figure JSON (null if no visualization)
- `row_count`: Number of rows returned

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "List the top 5 customers by total spending",
    "language": "en"
  }'
```

**Example Response**:
```json
{
  "question": "List the top 5 customers by total spending",
  "sql": "SELECT c.CustomerId, c.FirstName, c.LastName, SUM(i.Total) as TotalSpending FROM Customer c JOIN Invoice i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId ORDER BY TotalSpending DESC LIMIT 5",
  "results": [
    {"CustomerId": 6, "FirstName": "Helena", "LastName": "Holý", "TotalSpending": 49.62},
    {"CustomerId": 26, "FirstName": "Richard", "LastName": "Cunningham", "TotalSpending": 47.62},
    {"CustomerId": 57, "FirstName": "Luis", "LastName": "Rojas", "TotalSpending": 46.62},
    {"CustomerId": 45, "FirstName": "Ladislav", "LastName": "Kovács", "TotalSpending": 45.62},
    {"CustomerId": 46, "FirstName": "Hugh", "LastName": "O'Reilly", "TotalSpending": 45.62}
  ],
  "columns": ["CustomerId", "FirstName", "LastName", "TotalSpending"],
  "visualization": {
    "data": [
      {
        "x": ["Helena Holý", "Richard Cunningham", "Luis Rojas", "Ladislav Kovács", "Hugh O'Reilly"],
        "y": [49.62, 47.62, 46.62, 45.62, 45.62],
        "type": "bar"
      }
    ],
    "layout": {
      "title": "Top 5 Customers by Total Spending"
    }
  },
  "row_count": 5
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Missing or empty 'question' field"
}
```

**Error Response** (500 Internal Server Error):
```json
{
  "detail": "Query failed: table 'Customers' does not exist"
}
```

---

### 2. Add Training Data

Add training data to improve SQL generation accuracy.

**Endpoint**: `POST /api/v0/train`

**Request Body** (Option 1: DDL):
```json
{
  "ddl": "CREATE TABLE Product (ProductId INTEGER PRIMARY KEY, Name TEXT, Price REAL)"
}
```

**Request Body** (Option 2: Documentation):
```json
{
  "documentation": "The Product table stores information about products. The Price column is in USD."
}
```

**Request Body** (Option 3: Q&A Pair):
```json
{
  "question": "How many products are there?",
  "sql": "SELECT COUNT(*) FROM Product"
}
```

**Parameters**:
- `ddl` (string, optional): CREATE TABLE statement
- `documentation` (string, optional): Table/column description
- `question` (string, optional): Example question
- `sql` (string, optional): Corresponding SQL (required if `question` provided)

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Q&A pair added to training data"
}
```

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the most expensive products?",
    "sql": "SELECT Name, Price FROM Product ORDER BY Price DESC LIMIT 10"
  }'
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Invalid training data format. Provide 'ddl', 'documentation', or ('question' + 'sql')"
}
```

---

### 3. API Health Check

Check the health of the entire system.

**Endpoint**: `GET /api/v0/health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "Detomo SQL AI API",
  "version": "2.0.0",
  "llm_endpoint": "http://localhost:8000/generate",
  "database": "data/chinook.db - Connected",
  "training_data_count": 93
}
```

**Response Fields**:
- `status`: Health status (`"healthy"` or `"unhealthy"`)
- `service`: Service name
- `version`: API version
- `llm_endpoint`: LLM endpoint URL
- `database`: Database connection status
- `training_data_count`: Number of training items in ChromaDB

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/v0/health
```

**Error Response** (503 Service Unavailable):
```json
{
  "detail": "Database not connected"
}
```

---

## Multi-Step Workflow Endpoints

These endpoints follow the Vanna-Flask pattern, allowing fine-grained control over the query process with caching.

### 4. Generate Questions

Generate suggested questions based on training data.

**Endpoint**: `GET /api/v0/generate_questions`

**Response** (200 OK):
```json
{
  "questions": [
    "How many customers are there?",
    "List the top 10 customers by spending",
    "What are the most popular genres?",
    "Show me the total sales by country",
    "Which artists have the most albums?"
  ]
}
```

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/v0/generate_questions
```

---

### 5. Generate SQL

Generate SQL from natural language question and cache the result.

**Endpoint**: `POST /api/v0/generate_sql`

**Request Body**:
```json
{
  "question": "How many customers are from Brazil?"
}
```

**Parameters**:
- `question` (string, required): Natural language question

**Response** (200 OK):
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "question": "How many customers are from Brazil?",
  "sql": "SELECT COUNT(*) FROM Customer WHERE Country = 'Brazil'"
}
```

**Response Fields**:
- `id`: Cache ID (use this for subsequent steps)
- `question`: Original question
- `sql`: Generated SQL query

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are from Brazil?"}'
```

**Important**: Save the `id` field for use in subsequent steps (`run_sql`, `generate_plotly_figure`, `load_question`).

---

### 6. Run SQL

Execute SQL from a cached query.

**Endpoint**: `POST /api/v0/run_sql`

**Request Body**:
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**Parameters**:
- `id` (string, required): Cache ID from `generate_sql`

**Response** (200 OK):
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "results": [
    {
      "COUNT(*)": 5
    }
  ],
  "columns": ["COUNT(*)"],
  "row_count": 1
}
```

**Response Fields**:
- `id`: Cache ID
- `results`: Query results as array of objects
- `columns`: Column names
- `row_count`: Number of rows

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/run_sql \
  -H "Content-Type: application/json" \
  -d '{"id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"}'
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Cache ID not found: f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "No SQL found in cache for this ID"
}
```

---

### 7. Generate Plotly Figure

Generate a Plotly visualization from cached query results.

**Endpoint**: `POST /api/v0/generate_plotly_figure`

**Request Body**:
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**Parameters**:
- `id` (string, required): Cache ID from `run_sql`

**Response** (200 OK):
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "figure": {
    "data": [
      {
        "x": ["Brazil"],
        "y": [5],
        "type": "bar"
      }
    ],
    "layout": {
      "title": "Customers from Brazil",
      "xaxis": {"title": "Country"},
      "yaxis": {"title": "Count"}
    }
  }
}
```

**Response Fields**:
- `id`: Cache ID
- `figure`: Plotly figure JSON (null if visualization not possible)

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/generate_plotly_figure \
  -H "Content-Type: application/json" \
  -d '{"id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"}'
```

**Note**: Visualization generation is optional. If it fails, the endpoint returns `figure: null` instead of an error.

---

### 8. Generate Followup Questions

Generate related follow-up questions based on the current query.

**Endpoint**: `POST /api/v0/generate_followup_questions`

**Request Body**:
```json
{
  "question": "How many customers are from Brazil?",
  "sql": "SELECT COUNT(*) FROM Customer WHERE Country = 'Brazil'",
  "df": [{"COUNT(*)": 5}]
}
```

**Parameters**:
- `question` (string, required): Original question
- `sql` (string, optional): Generated SQL
- `df` (array, optional): Query results

**Response** (200 OK):
```json
{
  "questions": [
    "How many customers are from each country?",
    "Which country has the most customers?",
    "List all customers from Brazil",
    "What is the total spending by customers from Brazil?",
    "How many customers are from South America?"
  ]
}
```

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/generate_followup_questions \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How many customers are from Brazil?",
    "sql": "SELECT COUNT(*) FROM Customer WHERE Country = '\''Brazil'\''",
    "df": [{"COUNT(*)": 5}]
  }'
```

---

### 9. Load Question

Load complete cached query state by ID.

**Endpoint**: `POST /api/v0/load_question`

**Request Body**:
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**Parameters**:
- `id` (string, required): Cache ID

**Response** (200 OK):
```json
{
  "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "question": "How many customers are from Brazil?",
  "sql": "SELECT COUNT(*) FROM Customer WHERE Country = 'Brazil'",
  "results": [{"COUNT(*)": 5}],
  "columns": ["COUNT(*)"],
  "figure": {
    "data": [...],
    "layout": {...}
  },
  "row_count": 1
}
```

**Response Fields**:
- `id`: Cache ID
- `question`: Original question (null if not cached)
- `sql`: Generated SQL (null if not cached)
- `results`: Query results (null if not executed)
- `columns`: Column names (null if not executed)
- `figure`: Plotly figure (null if not generated)
- `row_count`: Number of rows (null if not executed)

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/load_question \
  -H "Content-Type: application/json" \
  -d '{"id": "f47ac10b-58cc-4372-a567-0e02b2c3d479"}'
```

**Use Case**: Restore a previous query from history

---

### 10. Get Question History

Get history of all cached questions.

**Endpoint**: `GET /api/v0/get_question_history`

**Response** (200 OK):
```json
{
  "history": [
    {
      "id": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
      "question": "How many customers are from Brazil?"
    },
    {
      "id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
      "question": "List the top 10 albums by sales"
    },
    {
      "id": "12345678-1234-1234-1234-123456789012",
      "question": "What are the most popular genres?"
    }
  ]
}
```

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/v0/get_question_history
```

**Use Case**: Display query history in UI sidebar

---

## Training Data Endpoints

### 11. Get Training Data

Get all training data from ChromaDB.

**Endpoint**: `GET /api/v0/get_training_data`

**Response** (200 OK):
```json
{
  "training_data": [
    {
      "id": "1a2b3c4d",
      "training_data_type": "sql",
      "question": "How many customers?",
      "content": "SELECT COUNT(*) FROM Customer"
    },
    {
      "id": "5e6f7g8h",
      "training_data_type": "ddl",
      "content": "CREATE TABLE Customer (CustomerId INTEGER PRIMARY KEY, ...)"
    },
    {
      "id": "9i0j1k2l",
      "training_data_type": "documentation",
      "content": "The Customer table stores customer information..."
    }
  ],
  "count": 93
}
```

**Response Fields**:
- `training_data`: Array of training items with metadata
- `count`: Total number of training items

**Example Request**:
```bash
curl -X GET http://localhost:8000/api/v0/get_training_data
```

---

### 12. Remove Training Data

Remove a specific training data item by ID.

**Endpoint**: `POST /api/v0/remove_training_data`

**Request Body**:
```json
{
  "id": "1a2b3c4d"
}
```

**Parameters**:
- `id` (string, required): Training data ID from `get_training_data`

**Response** (200 OK):
```json
{
  "status": "success",
  "message": "Training data removed: 1a2b3c4d"
}
```

**Example Request**:
```bash
curl -X POST http://localhost:8000/api/v0/remove_training_data \
  -H "Content-Type: application/json" \
  -d '{"id": "1a2b3c4d"}'
```

**Use Case**: Remove incorrect or outdated training examples

---

## Utility Endpoints

### 13. Download CSV

Download query results as a CSV file.

**Endpoint**: `GET /api/v0/download_csv?id={cache_id}`

**Parameters**:
- `id` (string, required): Cache ID from query execution

**Response** (200 OK):
```
Content-Type: text/csv
Content-Disposition: attachment; filename="How many customers are from Brazil.csv"

COUNT(*)
5
```

**Example Request**:
```bash
curl -X GET "http://localhost:8000/api/v0/download_csv?id=f47ac10b-58cc-4372-a567-0e02b2c3d479" \
  -o results.csv
```

**Browser Usage**:
```
http://localhost:8000/api/v0/download_csv?id=f47ac10b-58cc-4372-a567-0e02b2c3d479
```

**Error Response** (404 Not Found):
```json
{
  "detail": "Cache ID not found: f47ac10b-58cc-4372-a567-0e02b2c3d479"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "No results found in cache for this ID"
}
```

---

### 14. LLM Endpoint Health

Check health of the LLM endpoint (internal use).

**Endpoint**: `GET /health`

**Response** (200 OK):
```json
{
  "status": "healthy",
  "service": "Claude Agent SDK LLM Endpoint",
  "version": "1.0.0"
}
```

**Example Request**:
```bash
curl -X GET http://localhost:8000/health
```

---

### 15. Serve UI

Serve the main web UI.

**Endpoint**: `GET /`

**Response**: HTML page (static/index.html)

**Example**:
Open browser to `http://localhost:8000`

---

## Error Handling

### Standard Error Response Format

```json
{
  "detail": "Error message explaining what went wrong"
}
```

### HTTP Status Codes

| Code | Meaning | When |
|------|---------|------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid input (missing field, wrong format) |
| 404 | Not Found | Resource not found (cache ID, training data ID) |
| 500 | Internal Server Error | Server error (LLM failure, database error, code exception) |
| 503 | Service Unavailable | Service not ready (DetomoVanna not initialized, database disconnected) |

### Common Errors

**1. Missing Question**
```json
{
  "detail": "Missing or empty 'question' field"
}
```

**2. Cache ID Not Found**
```json
{
  "detail": "Cache ID not found: abc-123-def"
}
```

**3. SQL Execution Error**
```json
{
  "detail": "Query failed: no such table: Customers"
}
```

**4. Service Not Ready**
```json
{
  "detail": "DetomoVanna not initialized"
}
```

**5. Invalid Training Data**
```json
{
  "detail": "Invalid training data format. Provide 'ddl', 'documentation', or ('question' + 'sql')"
}
```

---

## Rate Limiting

**Current Version**: No rate limiting (MVP)

**Production**: Rate limits will be applied:
- **Free Tier**: 100 requests/hour
- **Pro Tier**: 1000 requests/hour
- **Enterprise**: Custom limits

**Rate Limit Headers** (future):
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640995200
```

---

## Examples

### Example 1: Simple Query (All-in-One)

```bash
# Ask a question, get SQL + results + chart
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the top 5 selling albums?"
  }'
```

**Response**:
```json
{
  "question": "What are the top 5 selling albums?",
  "sql": "SELECT a.Title, COUNT(il.InvoiceLineId) as Sales FROM Album a JOIN Track t ON a.AlbumId = t.AlbumId JOIN InvoiceLine il ON t.TrackId = il.TrackId GROUP BY a.AlbumId ORDER BY Sales DESC LIMIT 5",
  "results": [
    {"Title": "Minha Historia", "Sales": 27},
    {"Title": "Greatest Hits", "Sales": 26},
    {"Title": "Prenda Minha", "Sales": 25},
    {"Title": "The Office: Season 3", "Sales": 24},
    {"Title": "Unplugged", "Sales": 24}
  ],
  "columns": ["Title", "Sales"],
  "visualization": {...},
  "row_count": 5
}
```

---

### Example 2: Multi-Step Workflow

```bash
# Step 1: Generate SQL
response=$(curl -X POST http://localhost:8000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many tracks are in each genre?"}')

# Extract cache ID
id=$(echo $response | jq -r '.id')

# Step 2: Execute SQL
curl -X POST http://localhost:8000/api/v0/run_sql \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$id\"}"

# Step 3: Generate visualization
curl -X POST http://localhost:8000/api/v0/generate_plotly_figure \
  -H "Content-Type: application/json" \
  -d "{\"id\": \"$id\"}"

# Step 4: Download results as CSV
curl -X GET "http://localhost:8000/api/v0/download_csv?id=$id" \
  -o results.csv
```

---

### Example 3: Add Training Data

```bash
# Add DDL
curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{
    "ddl": "CREATE TABLE Product (ProductId INTEGER PRIMARY KEY, Name TEXT, Price REAL)"
  }'

# Add documentation
curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{
    "documentation": "Product table contains all products sold in the store. Prices are in USD."
  }'

# Add Q&A pair
curl -X POST http://localhost:8000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What are the most expensive products?",
    "sql": "SELECT Name, Price FROM Product ORDER BY Price DESC LIMIT 10"
  }'
```

---

### Example 4: Japanese Language Query

```bash
# Ask question in Japanese
curl -X POST http://localhost:8000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{
    "question": "顧客数は何人ですか？",
    "language": "jp"
  }'
```

**Response**:
```json
{
  "question": "顧客数は何人ですか？",
  "sql": "SELECT COUNT(*) FROM Customer",
  "results": [{"COUNT(*)": 59}],
  "columns": ["COUNT(*)"],
  "visualization": null,
  "row_count": 1
}
```

---

### Example 5: Python Client

```python
import requests
import json

# Base URL
BASE_URL = "http://localhost:8000"

# Ask a question
def query(question: str):
    response = requests.post(
        f"{BASE_URL}/api/v0/query",
        json={"question": question}
    )
    return response.json()

# Multi-step workflow
def multi_step_query(question: str):
    # Step 1: Generate SQL
    resp1 = requests.post(
        f"{BASE_URL}/api/v0/generate_sql",
        json={"question": question}
    )
    data = resp1.json()
    cache_id = data["id"]
    print(f"SQL: {data['sql']}")

    # Step 2: Execute SQL
    resp2 = requests.post(
        f"{BASE_URL}/api/v0/run_sql",
        json={"id": cache_id}
    )
    print(f"Results: {resp2.json()['results']}")

    # Step 3: Generate chart
    resp3 = requests.post(
        f"{BASE_URL}/api/v0/generate_plotly_figure",
        json={"id": cache_id}
    )
    return resp3.json()

# Add training data
def add_training(question: str, sql: str):
    response = requests.post(
        f"{BASE_URL}/api/v0/train",
        json={"question": question, "sql": sql}
    )
    return response.json()

# Example usage
if __name__ == "__main__":
    result = query("How many customers are there?")
    print(json.dumps(result, indent=2))
```

---

### Example 6: JavaScript/TypeScript Client

```javascript
const BASE_URL = 'http://localhost:8000';

// Simple query
async function query(question) {
  const response = await fetch(`${BASE_URL}/api/v0/query`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ question }),
  });
  return await response.json();
}

// Multi-step workflow
async function multiStepQuery(question) {
  // Step 1: Generate SQL
  const resp1 = await fetch(`${BASE_URL}/api/v0/generate_sql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question }),
  });
  const data1 = await resp1.json();
  console.log('SQL:', data1.sql);

  // Step 2: Execute SQL
  const resp2 = await fetch(`${BASE_URL}/api/v0/run_sql`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: data1.id }),
  });
  const data2 = await resp2.json();
  console.log('Results:', data2.results);

  // Step 3: Generate chart
  const resp3 = await fetch(`${BASE_URL}/api/v0/generate_plotly_figure`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ id: data1.id }),
  });
  return await resp3.json();
}

// Example usage
(async () => {
  const result = await query('How many customers are there?');
  console.log(result);
})();
```

---

## OpenAPI/Swagger Documentation

Interactive API documentation is available at:

**Swagger UI**: `http://localhost:8000/docs`

**ReDoc**: `http://localhost:8000/redoc`

These provide:
- Interactive API explorer
- Request/response schemas
- Try-it-out functionality
- Automatic validation

---

## Versioning

The API uses semantic versioning: `MAJOR.MINOR.PATCH`

**Current Version**: `2.0.0`

**Version History**:
- `2.0.0` (2025-10-26): Initial release with unified FastAPI architecture
- `1.0.0` (2025-10-25): Development version (Flask architecture)

**Breaking Changes**:
- Version changes in URL path (e.g., `/api/v1/...`, `/api/v2/...`)
- Major version changes announced 30 days in advance
- Deprecated endpoints supported for at least 90 days

---

## Support

For issues or questions:
- **GitHub Issues**: [github.com/detomo/sql-ai/issues](https://github.com/detomo/sql-ai/issues)
- **Email**: support@detomo.com
- **Documentation**: [docs.detomo.com](https://docs.detomo.com)

---

**Document Version**: 1.0
**Last Updated**: 2025-10-26
**API Version**: 2.0.0
