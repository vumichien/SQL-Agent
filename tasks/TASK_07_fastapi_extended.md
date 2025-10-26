# TASK 07: FastAPI Extended Endpoints (Vanna-Flask Pattern)

**Status**: ⬜ Not Started
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 05 (Core API), TASK 06 (Cache)
**Phase**: 3 - API Layer

---

## OVERVIEW

Extend the unified FastAPI server with 10 additional vanna-flask pattern endpoints for advanced UI workflows with caching.

**Reference**: PRD Section 5.3, 5.4

---

## OBJECTIVES

Implement 10 additional endpoints from vanna-flask pattern (note: `/api/v0/train` already implemented in TASK_05):

1. `/api/v0/generate_questions` - Get suggested questions
2. `/api/v0/generate_sql` - Convert NL to SQL (cache result)
3. `/api/v0/run_sql` - Execute SQL from cached query
4. `/api/v0/generate_plotly_figure` - Generate chart
5. `/api/v0/generate_followup_questions` - Suggest related questions
6. `/api/v0/load_question` - Load complete cached state
7. `/api/v0/get_question_history` - Load all previous queries
8. `/api/v0/get_training_data` - View training examples
9. `/api/v0/remove_training_data` - Delete training example
10. `/api/v0/download_csv` - Export results as CSV

**Architecture Note**: These endpoints will be added to `claude_agent_server.py` (the unified FastAPI server), not a separate Flask server.

---

## IMPLEMENTATION

Update `claude_agent_server.py` - add at top:

```python
from cache import MemoryCache
from fastapi import Query, Response
from fastapi.responses import StreamingResponse
import io

# Initialize cache
cache = MemoryCache()
```

**Note on Workflow**:
- **Simple workflow** (TASK_05): `/api/v0/query` - one request, get everything
- **Advanced workflow** (TASK_07): Multi-step with caching
  1. `generate_sql` → get SQL, review it, cache it with ID
  2. `run_sql` → execute SQL from cache
  3. `generate_plotly_figure` → create visualization
  4. `load_question` → retrieve full cached state

Add 10 advanced endpoints to the unified FastAPI server (see implementation details below).

---

## SUCCESS CRITERIA

- [ ] All 10 additional endpoints implemented in `claude_agent_server.py`
- [ ] Cache integration working with MemoryCache
- [ ] CSV download functional
- [ ] Multi-step workflow (generate_sql → run_sql → generate_figure) working
- [ ] Question history tracking functional
- [ ] Training data management (get/remove) working
- [ ] Integration tests passing
- [ ] Existing TASK_05 endpoints still working

---

**Last Updated**: 2025-10-26
