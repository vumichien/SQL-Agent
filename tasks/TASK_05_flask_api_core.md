# TASK 05: Flask API Core Endpoints

**Status**: ⬜ Not Started
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 02 (DetomoVanna), TASK 04 (Training data loaded)
**Phase**: 3 - API Layer (Core)

---

## OVERVIEW

Build Flask API with core endpoints for querying and training.

**Reference**: PRD Section 4.5

---

## OBJECTIVES

1. Create `app.py` with Flask setup
2. Implement `/api/v0/query` endpoint
3. Implement `/api/v0/train` endpoint
4. Implement `/api/v0/health` endpoint
5. Add CORS support
6. Write integration tests

---

## IMPLEMENTATION

Create `app.py`:

```python
from flask import Flask, request, jsonify
from flask_cors import CORS
from src.detomo_vanna import DetomoVanna
import os
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Initialize Vanna once
vn = DetomoVanna(config={
    "path": "./detomo_vectordb",
    "client": "persistent",
    "agent_endpoint": os.getenv("CLAUDE_AGENT_ENDPOINT", "http://localhost:8000/generate"),
    "model": "claude-sonnet-4-5"
})

# Connect to database
vn.connect_to_sqlite("data/chinook.db")


@app.route("/api/v0/query", methods=["POST"])
def query():
    """Main endpoint for natural language SQL queries."""
    data = request.json
    question = data.get("question")

    if not question:
        return jsonify({"error": "Missing 'question' field"}), 400

    try:
        # Generate SQL
        sql = vn.generate_sql(question)

        # Execute SQL
        df = vn.run_sql(sql)

        # Generate visualization if applicable
        fig = None
        try:
            fig = vn.get_plotly_figure(sql=sql, df=df, question=question)
            fig_json = fig.to_json() if fig else None
        except:
            fig_json = None

        return jsonify({
            "sql": sql,
            "results": df.to_dict(orient='records'),
            "columns": df.columns.tolist(),
            "visualization": fig_json
        })

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/v0/train", methods=["POST"])
def train():
    """Add training data to Vanna"""
    data = request.json

    try:
        if data.get("ddl"):
            vn.train(ddl=data["ddl"])
            return jsonify({"status": "success", "message": "DDL added"})

        elif data.get("documentation"):
            vn.train(documentation=data["documentation"])
            return jsonify({"status": "success", "message": "Documentation added"})

        elif data.get("question") and data.get("sql"):
            vn.train(question=data["question"], sql=data["sql"])
            return jsonify({"status": "success", "message": "Q&A pair added"})

        else:
            return jsonify({"error": "Invalid training data format"}), 400

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/v0/health", methods=["GET"])
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "framework": "Vanna AI",
        "llm": "Claude Agent SDK"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
```

---

## SUCCESS CRITERIA

- [ ] `app.py` created
- [ ] API runs on http://localhost:5000
- [ ] `/api/v0/query` endpoint works
- [ ] `/api/v0/train` endpoint works
- [ ] `/api/v0/health` endpoint works
- [ ] CORS enabled
- [ ] Error handling implemented
- [ ] Integration tests passing

---

## TESTING

```bash
# Terminal 1: Start Claude Agent
python claude_agent_server.py

# Terminal 2: Start Flask API
python app.py

# Terminal 3: Test endpoints
curl http://localhost:5000/api/v0/health

curl -X POST http://localhost:5000/api/v0/query \
  -H "Content-Type: application/json" \
  -d '{"question": "How many customers?"}'
```

---

## REFERENCES

- **PRD Section 4.5**: Flask API

---

**Last Updated**: 2025-10-26
