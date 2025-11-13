# Test Fixing Roadmap - Achieve 95% Coverage
**Target**: 88/125 → 120/125 passing tests (96% pass rate)
**Coverage**: 67% → 95%+

## Current Status
- **Total Tests**: 125
- **Passing**: 88 (70%)
- **Failing**: 37 (30%)
- **Coverage**: 67%

## Priority Analysis

### 🔴 Critical Issues (Block v1.0.0)

#### 1. Database Type Binding Error (14 failures)
**Root Cause**: Pydantic `HttpUrl` type not compatible with SQLite
**Files Affected**:
- `tests/test_articles.py` (7 failures)
- `tests/test_news_service.py` (7 failures)

**Error**:
```
sqlite3.ProgrammingError: Error binding parameter 12: type 'HttpUrl' is not supported
```

**Fix Strategy**:
```python
# In conftest.py - Add custom type handler
@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_conn, connection_record):
    cursor = dbapi_conn.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# In models - Convert HttpUrl to string
from pydantic import HttpUrl

@validates('url')
def validate_url(self, key, value):
    if isinstance(value, HttpUrl):
        return str(value)
    return value
```

**Time Estimate**: 2 hours

---

#### 2. Response Structure Mismatch (12 failures)
**Root Cause**: Tests expect old response format
**Files Affected**:
- `tests/test_analysis.py` (8 failures)
- `tests/test_health.py` (4 failures)

**Error**:
```python
KeyError: 'success'  # Tests expect {"success": True, "data": {...}}
# But API returns direct response: {"sentiment": "positive", ...}
```

**Fix Strategy**:
```python
# OLD (tests expect):
assert response.json()["success"] is True
assert response.json()["data"]["sentiment"] == "positive"

# NEW (fix tests):
assert response.status_code == 200
assert response.json()["sentiment"] == "positive"
```

**Time Estimate**: 1.5 hours

---

#### 3. PostgreSQL Full-Text Search on SQLite (4 failures)
**Root Cause**: SQLite doesn't support `@@` operator
**Files Affected**:
- `tests/test_search.py` (4 failures)

**Error**:
```
sqlalchemy.exc.OperationalError: unrecognized token: "@"
```

**Fix Strategy**:
```python
# Option 1: Mock full-text search in tests
@pytest.fixture
def mock_search(monkeypatch):
    async def mock_search_fn(*args, **kwargs):
        return []
    monkeypatch.setattr("app.services.news_service.NewsService.search_articles", mock_search_fn)

# Option 2: Use SQLite FTS
CREATE VIRTUAL TABLE articles_fts USING fts5(title, content);

# Option 3: Simple LIKE fallback for tests
if dialect.name == 'sqlite':
    query = query.filter(Article.title.like(f"%{search_term}%"))
else:
    query = query.filter(Article.search_vector.op('@@')(func.plainto_tsquery(search_term)))
```

**Time Estimate**: 2 hours

---

### 🟡 Medium Priority (Improve Coverage)

#### 4. Entity/Trend Tests (2 failures)
**Root Cause**: 422 validation errors
**Fix**: Update request payloads to match schemas
**Time Estimate**: 1 hour

#### 5. Rate Limiting Tests (2 failures)
**Root Cause**: Endpoint verification issues
**Fix**: Update endpoint paths and assertions
**Time Estimate**: 0.5 hours

---

### 🟢 Low Priority (Coverage Boost)

#### 6. Missing Test Coverage Areas
**Current Coverage**: 67%
**Target**: 95%
**Gap**: 28%

**Untested Areas**:
1. **Error Handlers** (app/core/*)
   - Exception handlers
   - Custom exception classes
   - Error response formatting

2. **Middleware** (app/core/audit_logger.py, security_headers.py)
   - Request/response logging
   - Security headers injection
   - Error handling in middleware

3. **Edge Cases**:
   - Empty inputs
   - Invalid data types
   - Boundary conditions
   - Concurrent operations

4. **Database Operations**:
   - Migration scripts
   - Connection pooling
   - Transaction rollback
   - Constraint violations

5. **NLP Service Edge Cases**:
   - Very long texts (>10,000 chars)
   - Special characters
   - Multiple languages (error handling)
   - Empty entity extraction

6. **Scraper Service**:
   - RSS parsing errors
   - Network timeouts
   - Invalid HTML
   - Duplicate detection

**Time Estimate**: 6 hours

---

## Implementation Plan

### Phase 1: Critical Fixes (Day 1 - 5.5 hours)
```bash
# 1. Fix HttpUrl binding (2h)
- Update conftest.py with type handlers
- Modify NewsArticle model to convert HttpUrl
- Test with sample data

# 2. Fix response assertions (1.5h)
- Update test_analysis.py assertions
- Update test_health.py assertions
- Verify all response structures

# 3. Fix full-text search (2h)
- Implement SQLite FTS fallback
- Update search service with dialect detection
- Test search functionality
```

**Expected Result**: 88/125 → 108/125 passing (86%)

---

### Phase 2: Medium Priority Fixes (Day 2 - 1.5 hours)
```bash
# 4. Fix entity/trend tests (1h)
- Update request payloads
- Verify schema requirements
- Test validation logic

# 5. Fix rate limiting tests (0.5h)
- Update endpoint paths
- Verify rate limit logic
```

**Expected Result**: 108/125 → 112/125 passing (90%)

---

### Phase 3: Coverage Boost (Day 2-3 - 6 hours)
```bash
# 6. Add missing tests
- Error handler tests (1.5h)
- Middleware tests (1.5h)
- Edge case tests (1.5h)
- Database operation tests (1h)
- NLP edge cases (0.5h)

# 7. Integration tests
- End-to-end workflows (1h)
```

**Expected Result**: Coverage 67% → 95%+

---

## Test Categories Breakdown

### Unit Tests (50 tests)
- ✅ NLP Service: 27/27 (100%)
- ✅ Security Headers: 9/9 (100%)
- ⚠️ News Service: 2/9 (22%)
- ⚠️ Analysis Service: 0/5 (0%)

### API Tests (60 tests)
- ⚠️ Articles: 7/14 (50%)
- ⚠️ Analysis: 3/11 (27%)
- ✅ Health: 9/12 (75%)
- ⚠️ Search: 2/6 (33%)
- ✅ Entities/Trends: 10/12 (83%)
- ✅ Rate Limiting: 3/5 (60%)

### Integration Tests (15 tests)
- ✅ Article Comprehensive: 12/14 (86%)
- ⚠️ Analysis Comprehensive: 9/12 (75%)
- ✅ Health Comprehensive: 8/9 (89%)

---

## Success Criteria

### Minimum Requirements (v1.0.0)
- [ ] Test Pass Rate: 95%+ (120/125 tests)
- [ ] Code Coverage: 95%+
- [ ] All Critical Issues Fixed
- [ ] No SQL injection vulnerabilities
- [ ] No hardcoded secrets
- [ ] All error handlers tested

### Stretch Goals
- [ ] Test Pass Rate: 98%+ (123/125 tests)
- [ ] Code Coverage: 97%+
- [ ] Performance tests added
- [ ] Load tests passing
- [ ] Security scan 100% clean

---

## Execution Checklist

### Pre-Work
- [x] Analyze current test failures
- [x] Categorize by root cause
- [x] Estimate time requirements
- [x] Create todo list

### Phase 1 Execution
- [ ] Fix HttpUrl type binding
- [ ] Run tests: `pytest tests/test_articles.py tests/test_news_service.py -v`
- [ ] Fix response structure assertions
- [ ] Run tests: `pytest tests/test_analysis.py tests/test_health.py -v`
- [ ] Fix full-text search
- [ ] Run tests: `pytest tests/test_search.py -v`
- [ ] Commit: "fix: resolve critical test failures (HttpUrl, response structure, FTS)"

### Phase 2 Execution
- [ ] Fix entity/trend tests
- [ ] Fix rate limiting tests
- [ ] Run full suite: `pytest tests/ -v`
- [ ] Commit: "fix: resolve medium priority test failures"

### Phase 3 Execution
- [ ] Add error handler tests
- [ ] Add middleware tests
- [ ] Add edge case tests
- [ ] Run with coverage: `pytest tests/ --cov=app --cov-report=html`
- [ ] Verify 95%+ coverage
- [ ] Commit: "test: add comprehensive test coverage to 95%+"

### Final Validation
- [ ] Run full suite: `pytest tests/ -v --cov=app --cov-report=term`
- [ ] Verify coverage: ≥95%
- [ ] Run security scan: `bandit -r app/`
- [ ] Run linters: `black app/ tests/ && flake8 app/`
- [ ] Update CHANGELOG.md
- [ ] Create git tag: `git tag -a v1.0.0 -m "Release v1.0.0"`
- [ ] Push: `git push origin main --tags`

---

## Risk Assessment

### High Risk
- **HttpUrl conversion**: May break existing functionality
  - Mitigation: Test thoroughly with real data
  
### Medium Risk
- **Full-text search fallback**: Performance degradation on SQLite
  - Mitigation: Document that PostgreSQL required for production

### Low Risk
- **Response structure changes**: Only affects tests
  - Mitigation: Update tests, not production code

---

## Time Estimate Summary

| Phase | Tasks | Time |
|-------|-------|------|
| Phase 1 | Critical fixes | 5.5h |
| Phase 2 | Medium priority | 1.5h |
| Phase 3 | Coverage boost | 6h |
| **Total** | **All phases** | **13h** |

**Team Capacity**: Elite team (9 members)
**Parallel Execution**: ~3 hours (with 3 parallel tracks)

---

## Success Metrics

**Before**:
- Pass Rate: 70% (88/125)
- Coverage: 67%
- Failing Tests: 37

**After (Target)**:
- Pass Rate: 96%+ (120/125)
- Coverage: 95%+
- Failing Tests: ≤5

**Delta**:
- +32 tests fixed
- +28% coverage increase
- -32 failures

---

## Next Steps

1. **NOW**: Start Phase 1 - Fix HttpUrl binding
2. **Hour 2**: Fix response structure assertions
3. **Hour 4**: Fix full-text search
4. **Hour 5.5**: Start Phase 2
5. **Hour 7**: Start Phase 3
6. **Hour 13**: Final validation and release

**Team Assignment**:
- **Track 1** (Dr. Aisha Patel): HttpUrl binding + News Service tests
- **Track 2** (Elena Volkov): Response structure + Analysis/Health tests
- **Track 3** (João Silva): Full-text search + Search tests
- **Track 4** (All): Coverage boost (parallel on different modules)

**Ready to execute!** 🚀
