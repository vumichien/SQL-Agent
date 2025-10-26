# TASK 10: Integration Testing

**Status**: ⬜ Not Started
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 01-08 (All components + Frontend)
**Phase**: 5 - Testing & QA

---

## OVERVIEW

Test complete system integration - end-to-end flows.

---

## OBJECTIVES

1. Test full query flow: NL → SQL → Execute → Visualize
2. Test API endpoint integration
3. Test training pipeline
4. Test cache-based workflow

---

## TEST FILES

Create `tests/integration/test_full_flow.py`:

```python
import pytest
from src.detomo_vanna import DetomoVanna


def test_full_query_flow():
    """Test complete NL to SQL to results flow"""
    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "agent_endpoint": "http://localhost:8000/generate"
    })
    vn.connect_to_sqlite("data/chinook.db")

    # Generate SQL
    sql = vn.generate_sql("How many customers?")
    assert "SELECT" in sql.upper()
    assert "Customer" in sql

    # Execute SQL
    df = vn.run_sql(sql)
    assert len(df) > 0

    # Generate visualization (may be None for simple count)
    fig = vn.get_plotly_figure(sql=sql, df=df)
    # Assert based on result
```

---

## SUCCESS CRITERIA

- [ ] End-to-end tests passing
- [ ] All API integration tests passing
- [ ] Training pipeline working
- [ ] No blocking issues

---

**Last Updated**: 2025-10-26
