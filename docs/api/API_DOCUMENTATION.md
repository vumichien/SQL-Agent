# API Documentation - Detomo SQL AI

## Base URL
```
http://localhost:5000
```

## Authentication
Currently no authentication required (add in production).

---

## Endpoints

### 1. Health Check

**GET** `/api/v0/health`

Check API health and backend status.

**Response**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "backend": "claude_agent_sdk",
  "database": "connected"
}
```

**Example**
```bash
curl http://localhost:5000/api/v0/health
```

---

### 2. Generate SQL

**POST** `/api/v0/generate_sql`

Generate SQL from natural language question.

**Request Body**
```json
{
  "question": "How many customers are there?"
}
```

**Response**
```json
{
  "question": "How many customers are there?",
  "sql": "SELECT COUNT(*) FROM customers",
  "status": "success"
}
```

**Example**
```bash
curl -X POST http://localhost:5000/api/v0/generate_sql \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers are there?"}'
```

**Errors**
- `400`: Missing or empty question
- `500`: SQL generation failed

---

### 3. Run SQL

**POST** `/api/v0/run_sql`

Execute SQL query and return results.

**Request Body**
```json
{
  "sql": "SELECT COUNT(*) as count FROM customers"
}
```

**Response**
```json
{
  "data": [{"count": 59}],
  "columns": ["count"],
  "row_count": 1,
  "status": "success"
}
```

**Example**
```bash
curl -X POST http://localhost:5000/api/v0/run_sql \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT COUNT(*) as count FROM customers"}'
```

**Errors**
- `400`: Missing or empty SQL
- `500`: SQL execution failed

---

### 4. Ask (Question → SQL → Results)

**POST** `/api/v0/ask`

Complete workflow: question → SQL generation → execution → results.

**Request Body**
```json
{
  "question": "What are the top 5 customers by total purchases?"
}
```

**Response**
```json
{
  "question": "What are the top 5 customers by total purchases?",
  "sql": "SELECT c.FirstName, c.LastName, SUM(i.Total) as total_purchases FROM customers c JOIN invoices i ON c.CustomerId = i.CustomerId GROUP BY c.CustomerId ORDER BY total_purchases DESC LIMIT 5",
  "data": [
    {"FirstName": "Helena", "LastName": "Holý", "total_purchases": 49.62},
    ...
  ],
  "columns": ["FirstName", "LastName", "total_purchases"],
  "row_count": 5,
  "status": "success"
}
```

**Example**
```bash
curl -X POST http://localhost:5000/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What are the top 5 customers by total purchases?"}'
```

**Errors**
- `400`: Missing or empty question
- `500`: Processing failed

---

### 5. Generate Plotly Figure

**POST** `/api/v0/generate_plotly_figure`

Generate Plotly visualization from SQL results.

**Request Body**
```json
{
  "sql": "SELECT Name, COUNT(*) as count FROM tracks GROUP BY GenreId LIMIT 10",
  "chart_type": "bar"
}
```

**Parameters**
- `sql` (required): SQL query to visualize
- `chart_type` (optional): Chart type (`bar`, `line`, `pie`)

**Response**
```json
{
  "figure": "{...plotly JSON...}",
  "chart_type": "bar",
  "status": "success"
}
```

**Example**
```bash
curl -X POST http://localhost:5000/api/v0/generate_plotly_figure \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT Name, COUNT(*) as count FROM genres", "chart_type": "bar"}'
```

**Errors**
- `400`: Missing SQL or no data to visualize
- `500`: Visualization generation failed

---

### 6. Get Training Data

**GET** `/api/v0/get_training_data`

Get training data statistics.

**Response**
```json
{
  "ddl_count": 12,
  "documentation_count": 11,
  "sql_count": 70,
  "total": 93,
  "items": [...],
  "status": "success"
}
```

**Example**
```bash
curl http://localhost:5000/api/v0/get_training_data
```

---

### 7. Add Training Data

**POST** `/api/v0/train`

Add new training data.

**Request Body - SQL Training**
```json
{
  "type": "sql",
  "question": "How many albums?",
  "sql": "SELECT COUNT(*) FROM albums"
}
```

**Request Body - DDL Training**
```json
{
  "type": "ddl",
  "ddl": "CREATE TABLE customers (CustomerId INTEGER PRIMARY KEY, ...)"
}
```

**Request Body - Documentation Training**
```json
{
  "type": "documentation",
  "documentation": "The customers table stores all customer information..."
}
```

**Response**
```json
{
  "message": "Training data added successfully",
  "type": "sql",
  "id": "12345",
  "status": "success"
}
```

**Example**
```bash
curl -X POST http://localhost:5000/api/v0/train \
  -H "Content-Type: application/json" \
  -d '{"type": "sql", "question": "How many albums?", "sql": "SELECT COUNT(*) FROM albums"}'
```

**Errors**
- `400`: Invalid type or missing required fields
- `500`: Training failed

---

### 8. Remove Training Data

**DELETE** `/api/v0/remove_training_data`

Remove training data by ID.

**Request Body**
```json
{
  "id": "training_data_id"
}
```

**Response**
```json
{
  "message": "Training data removed successfully",
  "id": "training_data_id",
  "status": "success"
}
```

**Example**
```bash
curl -X DELETE http://localhost:5000/api/v0/remove_training_data \
  -H "Content-Type: application/json" \
  -d '{"id": "12345"}'
```

**Errors**
- `400`: Missing ID
- `500`: Removal failed

---

## Error Responses

All errors follow this format:

```json
{
  "error": "Error message",
  "status": "error"
}
```

### Error Codes

- `400 Bad Request`: Invalid request parameters
- `404 Not Found`: Endpoint not found
- `500 Internal Server Error`: Server-side error

---

## CORS

CORS is enabled for all `/api/*` endpoints with origin `*` (configure for production).

---

## Rate Limiting

Currently no rate limiting (add in production).

---

## Backend Information

Check which LLM backend is active:

```bash
curl http://localhost:5000/api/v0/health | jq .backend
```

Returns: `"claude_agent_sdk"` or `"anthropic_api"`

---

## Complete Example Workflow

### 1. Ask a question in natural language
```bash
curl -X POST http://localhost:5000/api/v0/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "顧客は何人いますか？"}' | jq
```

### 2. Response includes SQL and results
```json
{
  "question": "顧客は何人いますか？",
  "sql": "SELECT COUNT(*) FROM customers",
  "data": [{"COUNT(*)": 59}],
  "columns": ["COUNT(*)"],
  "row_count": 1,
  "status": "success"
}
```

### 3. Generate visualization
```bash
curl -X POST http://localhost:5000/api/v0/generate_plotly_figure \
  -H "Content-Type: application/json" \
  -d '{"sql": "SELECT Country, COUNT(*) as count FROM customers GROUP BY Country ORDER BY count DESC LIMIT 10", "chart_type": "bar"}' | jq .figure
```

---

## Testing

### Run All Tests
```bash
pytest tests/api/ -v
```

### Test Specific Endpoint
```bash
pytest tests/api/test_api_endpoints.py::test_generate_sql -v
```

### Test Backend Switching
```bash
pytest tests/api/test_backend_switching.py -v
```

---

## Development

### Start Server
```bash
python app.py
```

Server runs on `http://localhost:5000`

### Debug Mode
Set in `.env`:
```
FLASK_DEBUG=True
LOG_LEVEL=DEBUG
```

---

## Production Considerations

1. **Authentication**: Add API key authentication
2. **Rate Limiting**: Implement rate limiting
3. **CORS**: Configure specific origins
4. **Logging**: Enhanced logging and monitoring
5. **Error Handling**: More detailed error messages
6. **Validation**: Stricter input validation
7. **Caching**: Cache frequent queries

---

**Last Updated**: 2025-10-26
**Version**: 1.0.0
