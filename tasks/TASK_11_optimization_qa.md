# TASK 11: Optimization & QA

**Status**: ⬜ Not Started
**Estimated Time**: 10-12 hours
**Dependencies**: TASK 10 (All tests passing)
**Phase**: 5 - Testing & QA

---

## OVERVIEW

SQL accuracy testing, performance benchmarking, and optimization.

---

## OBJECTIVES

1. SQL accuracy testing with around 20 queries
2. Performance benchmarking
3. Accuracy report (target ≥85%)
4. Performance report (target <5s p95)
5. Bug fixes
6. Prompt optimization

---

## TEST QUERIES

Create `tests/accuracy/test_queries.json`:

```json
[
  {
    "id": 1,
    "question": "How many customers?",
    "expected_sql": "SELECT COUNT(*) FROM Customer",
    "category": "simple_count"
  },
  {
    "id": 2,
    "question": "Show all albums by AC/DC",
    "expected_pattern": "Artist.*AC/DC",
    "category": "filter"
  }
]
```

Create `tests/accuracy/test_sql_accuracy.py`:

```python
import pytest
import json
from src.detomo_vanna import DetomoVanna


def load_test_queries():
    with open('tests/accuracy/test_queries.json') as f:
        return json.load(f)


@pytest.mark.parametrize("test_case", load_test_queries())
def test_sql_accuracy(test_case):
    """Test SQL generation accuracy"""
    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "agent_endpoint": "http://localhost:8000/generate"
    })

    generated_sql = vn.generate_sql(test_case['question'])

    # Check if expected pattern is in generated SQL
    if 'expected_sql' in test_case:
        assert test_case['expected_sql'].lower() in generated_sql.lower()
```

---

## PERFORMANCE BENCHMARKING

Create `tests/performance/benchmark.py`:

```python
import time
from src.detomo_vanna import DetomoVanna


def benchmark_query_time():
    vn = DetomoVanna(config={
        "path": "./detomo_vectordb",
        "agent_endpoint": "http://localhost:8000/generate"
    })

    questions = [
        "How many customers?",
        "Show top 10 albums",
        "Revenue by genre"
    ]

    times = []
    for q in questions:
        start = time.time()
        vn.generate_sql(q)
        elapsed = time.time() - start
        times.append(elapsed)
        print(f"{q}: {elapsed:.2f}s")

    avg = sum(times) / len(times)
    p95 = sorted(times)[int(len(times) * 0.95)]

    print(f"\nAverage: {avg:.2f}s")
    print(f"P95: {p95:.2f}s")

    assert p95 < 5.0, f"P95 response time {p95:.2f}s exceeds 5s target"


if __name__ == "__main__":
    benchmark_query_time()
```

---

## DELIVERABLES

1. Accuracy test results (≥85% target)
2. Performance benchmark results (<5s p95)
3. Bug fix list and resolutions
4. Optimization recommendations

---

## SUCCESS CRITERIA

- [ ] SQL accuracy ≥85%
- [ ] Response time <5s (p95)
- [ ] No critical bugs
- [ ] Performance report generated
- [ ] Accuracy report generated

---

**Last Updated**: 2025-10-26
