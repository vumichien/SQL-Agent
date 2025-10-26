# TASK MASTER - Detomo SQL AI

**Project**: Detomo SQL AI v2.0 (Vanna + Claude Agent SDK)
**PRD Version**: 2.0
**Last Updated**: 2025-10-26

---

## OVERVIEW

This task master tracks the complete implementation of Detomo SQL AI, a Text-to-SQL application using Vanna AI framework with Claude Agent SDK as the LLM endpoint.

**Technology Stack**:
- RAG Framework: Vanna AI
- LLM Backend: Claude Agent SDK (HTTP endpoint)
- LLM Model: Claude Sonnet 4.5
- Vector DB: ChromaDB
- Target DB: SQLite (Chinook)
- API: Flask
- Frontend: React/Vue (Vanna-Flask pattern)

---

## TASK CHECKLIST

### Phase 1: Core Backend Setup

#### ⬜ TASK 01: Claude Agent Endpoint Server
**Status**: Not Started
**File**: [tasks/TASK_01_claude_agent_endpoint.md](tasks/TASK_01_claude_agent_endpoint.md)
**Estimated Time**: 4-6 hours
**Dependencies**: None

**Deliverables**:
- [ ] `claude_agent_server.py` implemented
- [ ] `/generate` endpoint working
- [ ] `/health` endpoint working
- [ ] Error handling implemented
- [ ] Tested with curl/Postman
- [ ] Unit tests: `tests/unit/test_agent_endpoint.py`

**Success Criteria**:
- Server runs on http://localhost:8000
- Can receive prompt and return SQL text
- Response time < 3s

---

#### ⬜ TASK 02: Vanna Custom Class Implementation
**Status**: Not Started
**File**: [tasks/TASK_02_vanna_custom_class.md](tasks/TASK_02_vanna_custom_class.md)
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 01 (Claude Agent endpoint must be running)

**Deliverables**:
- [ ] `src/detomo_vanna.py` created
- [ ] `ClaudeAgentChat` class implemented
- [ ] `DetomoVanna` class implemented
- [ ] Integration with Claude Agent SDK tested
- [ ] Unit tests: `tests/unit/test_detomo_vanna.py`

**Success Criteria**:
- Vanna can call Claude Agent SDK successfully
- `submit_prompt()` works correctly
- RAG retrieval integrated with LLM calls

---

### Phase 2: Training Data & Knowledge Base

#### ⬜ TASK 03: Training Data Preparation
**Status**: Not Started
**File**: [tasks/TASK_03_training_data_preparation.md](tasks/TASK_03_training_data_preparation.md)
**Estimated Time**: 8-10 hours
**Dependencies**: None (can be done in parallel with TASK 01-02)

**Deliverables**:
- [ ] Folder structure created: `training_data/chinook/{ddl,documentation,questions}/`
- [ ] DDL files for all Chinook tables (11 tables)
- [ ] Documentation files for tables (EN/JP)
- [ ] Q&A JSON files with 50+ examples (EN/JP)
- [ ] README.md in training_data folder

**Success Criteria**:
- At least 50 Q&A pairs covering various query types
- Bilingual support (English + Japanese)
- Well-documented schemas

---

#### ⬜ TASK 04: Training Script
**Status**: Not Started
**File**: [tasks/TASK_04_training_script.md](tasks/TASK_04_training_script.md)
**Estimated Time**: 4-6 hours
**Dependencies**: TASK 02 (DetomoVanna class), TASK 03 (Training data)

**Deliverables**:
- [ ] `scripts/train_chinook.py` created
- [ ] Script loads DDL files
- [ ] Script loads documentation
- [ ] Script loads Q&A pairs
- [ ] Verification function implemented
- [ ] Integration tests: `tests/integration/test_training.py`

**Success Criteria**:
- All training data loaded successfully to ChromaDB
- Can verify training data count
- Script is idempotent (can re-run safely)

---

### Phase 3: API Layer (Core)

#### ⬜ TASK 05: Flask API Core Endpoints
**Status**: Not Started
**File**: [tasks/TASK_05_flask_api_core.md](tasks/TASK_05_flask_api_core.md)
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 02 (DetomoVanna), TASK 04 (Training data loaded)

**Deliverables**:
- [ ] `app.py` created with Flask setup
- [ ] `/api/v0/query` endpoint implemented
- [ ] `/api/v0/train` endpoint implemented
- [ ] `/api/v0/health` endpoint implemented
- [ ] CORS configured
- [ ] Integration tests: `tests/integration/test_api_core.py`

**Success Criteria**:
- API runs on http://localhost:5000
- Can query natural language → get SQL results
- Can add training data via API

---

#### ⬜ TASK 06: Cache Implementation
**Status**: Not Started
**File**: [tasks/TASK_06_cache_implementation.md](tasks/TASK_06_cache_implementation.md)
**Estimated Time**: 3-4 hours
**Dependencies**: None (can be done in parallel)

**Deliverables**:
- [ ] `cache.py` created
- [ ] `MemoryCache` class implemented
- [ ] All cache methods working (set, get, get_all, delete)
- [ ] Unit tests: `tests/unit/test_cache.py`

**Success Criteria**:
- Cache can store query state (question, sql, df, fig)
- Can generate unique IDs
- All methods have 100% test coverage

---

#### ⬜ TASK 07: Flask API Extended (Vanna-Flask Pattern)
**Status**: Not Started
**File**: [tasks/TASK_07_flask_api_extended.md](tasks/TASK_07_flask_api_extended.md)
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 05 (Core API), TASK 06 (Cache)

**Deliverables**:
- [ ] Update `app.py` with 11 vanna-flask endpoints
- [ ] All endpoints from PRD Section 5.3 implemented
- [ ] Cache integration working
- [ ] CSV download functionality
- [ ] Integration tests: `tests/integration/test_api_extended.py`

**Success Criteria**:
- All 11 endpoints working:
  1. `/api/v0/generate_questions`
  2. `/api/v0/generate_sql`
  3. `/api/v0/run_sql`
  4. `/api/v0/generate_plotly_figure`
  5. `/api/v0/generate_followup_questions`
  6. `/api/v0/load_question`
  7. `/api/v0/get_question_history`
  8. `/api/v0/get_training_data`
  9. `/api/v0/train`
  10. `/api/v0/remove_training_data`
  11. `/api/v0/download_csv`
- Cache-based workflow functional

---

### Phase 4: Frontend UI

#### ⬜ TASK 08: Frontend Setup (Vanna-Flask UI)
**Status**: Not Started
**File**: [tasks/TASK_08_frontend_setup.md](tasks/TASK_08_frontend_setup.md)
**Estimated Time**: 12-16 hours
**Dependencies**: TASK 07 (Extended API endpoints)

**Deliverables**:
- [ ] `static/index.html` created
- [ ] `static/detomo_logo.svg` added
- [ ] Frontend SPA built (React/Vue or fork vanna-flask)
- [ ] Chat interface implemented
- [ ] SQL results display with syntax highlighting
- [ ] Plotly visualization rendering
- [ ] Query history sidebar
- [ ] Training data management UI
- [ ] Dark mode support
- [ ] Bilingual support (EN/JP)
- [ ] Manual testing checklist completed

**Success Criteria**:
- UI accessible at http://localhost:5000
- Can input NL question → see SQL → see results → see chart
- All UI components functional
- Detomo branding applied

---

### Phase 5: Testing & Quality Assurance

#### ⬜ TASK 09: Unit Testing
**Status**: Not Started
**File**: [tasks/TASK_09_testing_unit.md](tasks/TASK_09_testing_unit.md)
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 01-07 (All components implemented)

**Deliverables**:
- [ ] Complete unit tests for all modules
- [ ] Test coverage ≥ 80%
- [ ] All tests passing
- [ ] Coverage report generated

**Test Files**:
- [ ] `tests/unit/test_agent_endpoint.py`
- [ ] `tests/unit/test_detomo_vanna.py`
- [ ] `tests/unit/test_cache.py`

**Success Criteria**:
- pytest runs successfully
- Coverage ≥ 80%
- No critical bugs

---

#### ⬜ TASK 10: Integration Testing
**Status**: Not Started
**File**: [tasks/TASK_10_testing_integration.md](tasks/TASK_10_testing_integration.md)
**Estimated Time**: 8-10 hours
**Dependencies**: TASK 01-08 (All components + Frontend)

**Deliverables**:
- [ ] End-to-end query flow tests
- [ ] API endpoint integration tests
- [ ] Training pipeline tests
- [ ] All tests passing

**Test Files**:
- [ ] `tests/integration/test_training.py`
- [ ] `tests/integration/test_api_core.py`
- [ ] `tests/integration/test_api_extended.py`
- [ ] `tests/integration/test_full_flow.py`

**Success Criteria**:
- Full query flow works end-to-end
- All API endpoints tested
- Training → Query → Visualization works

---

#### ⬜ TASK 11: Optimization & QA
**Status**: Not Started
**File**: [tasks/TASK_11_optimization_qa.md](tasks/TASK_11_optimization_qa.md)
**Estimated Time**: 10-12 hours
**Dependencies**: TASK 10 (All tests passing)

**Deliverables**:
- [ ] SQL accuracy testing with 50+ queries
- [ ] Performance benchmarking
- [ ] Accuracy report (target ≥85%)
- [ ] Performance report (target <5s p95)
- [ ] Bug fixes implemented
- [ ] Prompt optimization done

**Success Criteria**:
- SQL accuracy ≥ 85%
- Response time < 5s (p95)
- No critical bugs
- Performance benchmarks documented

---

### Phase 6: Documentation & Deployment

#### ⬜ TASK 12: Documentation
**Status**: Not Started
**File**: [tasks/TASK_12_documentation.md](tasks/TASK_12_documentation.md)
**Estimated Time**: 6-8 hours
**Dependencies**: TASK 11 (All implementation complete)

**Deliverables**:
- [ ] `docs/ARCHITECTURE.md` created
- [ ] `docs/API_DOCUMENTATION.md` created
- [ ] `docs/DEPLOYMENT.md` created
- [ ] `README.md` updated
- [ ] All code comments reviewed

**Success Criteria**:
- Complete architecture documentation
- API docs with examples
- Deployment guide with step-by-step instructions
- README with quick start guide

---

## PROGRESS SUMMARY

### Overall Status
- **Total Tasks**: 12
- **Completed**: 0
- **In Progress**: 0
- **Not Started**: 12
- **Overall Progress**: 0%

### Phase Breakdown
| Phase | Tasks | Status |
|-------|-------|--------|
| Phase 1: Core Backend | TASK 01-02 | ⬜ Not Started |
| Phase 2: Training Data | TASK 03-04 | ⬜ Not Started |
| Phase 3: API Layer | TASK 05-07 | ⬜ Not Started |
| Phase 4: Frontend | TASK 08 | ⬜ Not Started |
| Phase 5: Testing & QA | TASK 09-11 | ⬜ Not Started |
| Phase 6: Documentation | TASK 12 | ⬜ Not Started |

---

## DEPENDENCIES GRAPH

```
TASK 01 (Claude Agent Endpoint)
    ↓
TASK 02 (Vanna Custom Class) ←─────┐
    ↓                               │
TASK 04 (Training Script) ←─ TASK 03 (Training Data)
    ↓
TASK 05 (Flask API Core)
    ↓
TASK 06 (Cache) ──→ TASK 07 (Flask API Extended)
                         ↓
                    TASK 08 (Frontend)
                         ↓
                    TASK 09 (Unit Tests)
                         ↓
                    TASK 10 (Integration Tests)
                         ↓
                    TASK 11 (Optimization & QA)
                         ↓
                    TASK 12 (Documentation)
```

---

## TIMELINE ESTIMATE

| Phase | Duration | Tasks |
|-------|----------|-------|
| Phase 1 | 1-2 days | TASK 01-02 |
| Phase 2 | 2-3 days | TASK 03-04 |
| Phase 3 | 2-3 days | TASK 05-07 |
| Phase 4 | 2-3 days | TASK 08 |
| Phase 5 | 3-4 days | TASK 09-11 |
| Phase 6 | 1 day | TASK 12 |
| **Total** | **11-18 days** | 12 tasks |

---

## SUCCESS CRITERIA (MVP)

From PRD Section 8.1:

### Core Functionality
- [ ] Natural language to SQL works via Vanna + Claude Agent SDK
- [ ] SQL execution returns correct results
- [ ] Basic visualization (Vanna's Plotly)
- [ ] Training data loaded in ChromaDB

### Quality Metrics
- [ ] SQL accuracy ≥ 75% (MVP) / ≥ 85% (V1.0)
- [ ] Response time < 10s (MVP) / < 5s (V1.0)
- [ ] No critical bugs

### API
- [ ] `/api/v0/query` endpoint functional
- [ ] Claude Agent SDK endpoint running
- [ ] Health check endpoints

### Data
- [ ] Chinook database connected via Vanna
- [ ] ≥ 50 Q&A training pairs loaded
- [ ] All DDL and docs loaded

---

## NOTES

### Context Management
- Monitor token usage during implementation
- Create new chat session if context < 20% remaining
- Save progress to files before switching context

### Testing Strategy
- Write tests alongside implementation (TDD approach)
- Run tests after each task completion
- Maintain ≥80% code coverage

### Documentation
- Update this TASK_MASTER.md after each task completion
- Keep detailed notes in individual task files
- Document all issues and solutions

---

## RISK MITIGATION

| Risk | Impact | Mitigation |
|------|--------|------------|
| Claude API costs too high | High | Add caching in agent endpoint, rate limiting |
| Agent SDK endpoint downtime | High | Add health checks, auto-restart, fallback |
| SQL accuracy < 85% | High | More training data, prompt engineering |
| ChromaDB performance issues | Medium | Optimize embedding model, index tuning |
| Frontend complexity | Medium | Use vanna-flask as base, minimal customization |

---

## REFERENCES

- **PRD**: [docs/PRD.md](docs/PRD.md)
- **Claude Setup Guide**: [CLAUDE.md](CLAUDE.md)
- **Task Files**: [tasks/](tasks/)

---

**Last Updated**: 2025-10-26
**Next Review**: After each task completion
