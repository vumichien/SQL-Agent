# TASK 07: Flask API Extended (Vanna-Flask Pattern)

**Status**: ⬜ Not Started
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 05 (Core API), TASK 06 (Cache)
**Phase**: 3 - API Layer

---

## OVERVIEW

Extend Flask API with 11 vanna-flask endpoints for complete UI integration.

**Reference**: PRD Section 5.3, 5.4

---

## OBJECTIVES

Implement all 11 endpoints from vanna-flask pattern:
1. `/api/v0/generate_questions` - Get suggested questions
2. `/api/v0/generate_sql` - Convert NL to SQL (cache result)
3. `/api/v0/run_sql` - Execute SQL from cached query
4. `/api/v0/generate_plotly_figure` - Generate chart
5. `/api/v0/generate_followup_questions` - Suggest related questions
6. `/api/v0/load_question` - Load complete cached state
7. `/api/v0/get_question_history` - Load all previous queries
8. `/api/v0/get_training_data` - View training examples
9. `/api/v0/train` - Add new training data (already in TASK 05)
10. `/api/v0/remove_training_data` - Delete training example
11. `/api/v0/download_csv` - Export results as CSV

---

## IMPLEMENTATION

Update `app.py` - add at top:

```python
from cache import MemoryCache

cache = MemoryCache()

def requires_cache(fields):
    def decorator(f):
        def wrapper(*args, **kwargs):
            query_id = request.args.get('id')
            if not query_id:
                return jsonify({"error": "Missing 'id' parameter"}), 400
            if not cache.get(id=query_id, field=fields[0]):
                return jsonify({"error": "Query ID not found in cache"}), 404
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator
```

Add endpoints (see PRD Section 5.4 for complete code).

---

## SUCCESS CRITERIA

- [ ] All 11 endpoints implemented
- [ ] Cache integration working
- [ ] CSV download functional
- [ ] Integration tests passing

---

**Last Updated**: 2025-10-26
