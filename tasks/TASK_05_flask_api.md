# Task 05: Flask API Development

**Priority**: HIGH
**Assignee**: Backend Developer
**Estimate**: 16 hours
**Phase**: Phase 2 - API Development

---

## Objective
Implement REST API endpoints for Detomo SQL AI using Flask framework.

---

## Prerequisites
- Task 03 completed (DetomoVanna class working)
- Task 04 completed (Training data loaded)
- Flask understanding

---

## API Endpoints

### Core Endpoints
1. `POST /api/v0/generate_sql` - Generate SQL from natural language
2. `POST /api/v0/run_sql` - Execute SQL query
3. `POST /api/v0/generate_plotly_figure` - Generate visualization
4. `GET /api/v0/get_training_data` - List training data
5. `POST /api/v0/train` - Add training data
6. `DELETE /api/v0/remove_training_data` - Remove training data

---

## Implementation

### File: `app.py`
```python
from flask import Flask, request, jsonify
from flask_cors import CORS
import logging
from src.detomo_vanna_dev import create_vanna_dev
from src.config import config

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Vanna
vn = create_vanna_dev()

@app.route('/api/v0/generate_sql', methods=['POST'])
def generate_sql():
    data = request.json
    question = data.get('question')

    try:
        sql = vn.generate_sql(question)
        return jsonify({'sql': sql, 'status': 'success'})
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

@app.route('/api/v0/run_sql', methods=['POST'])
def run_sql():
    data = request.json
    sql = data.get('sql')

    try:
        df = vn.run_sql(sql)
        return jsonify({
            'df': df.to_dict('records'),
            'columns': df.columns.tolist(),
            'rows': len(df),
            'status': 'success'
        })
    except Exception as e:
        return jsonify({'error': str(e), 'status': 'error'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

[More implementation details...]

---

## Status
- [ ] Not Started
- [ ] In Progress
- [ ] Completed

**Completed Date**: __________
