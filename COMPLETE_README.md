# Simple Hypothesis Testing with Full Automation

A minimal example showing **all 7 key features** in under 300 lines of code.

## ✅ All Features Included

1. ✅ **Machine-readable specifications** - Requirements as structured data
2. ✅ **Test traceability** - `@requirement()` decorator links tests to specs
3. ✅ **Automatic coverage tracking** - Pytest plugin monitors everything
4. ✅ **Gap detection** - Instantly see untested requirements
5. ✅ **Multi-format reporting** - JSON, HTML, and Markdown
6. ✅ **CI/CD integration** - Quality gates with `check_coverage.py`
7. ✅ **Property-based testing** - Hypothesis tests 100+ cases automatically

## Quick Start

```bash
# Install
pip install pytest hypothesis

# Run tests (generates all 3 reports automatically)
python -m pytest simple_test.py -v

# Check CI/CD quality gate
python check_coverage.py --min-verification 95
```

## Files (Only 5!)

```
simple_spec.py          ← 3 requirements (10 lines)
simple_code.py          ← 1 function to test (4 lines)
simple_test.py          ← 3 tests (20 lines)
conftest.py             ← Tracking & reporting (70 lines)
simple_reports.py       ← JSON/HTML/MD generation (150 lines)
check_coverage.py       ← CI/CD integration (60 lines)
```

Total: ~314 lines of code for everything!

## Example Output

```
============================= test session starts ==============================
simple_test.py::test_basic_reversal PASSED                               [ 33%]
simple_test.py::test_reverse_twice_is_original PASSED                    [ 66%]
simple_test.py::test_empty_string PASSED                                 [100%]

=============================== Coverage Report ================================

Total Requirements: 3
Covered: 3
Verified (passing): 3

✅ Verified:
  REQ-1: reverse_string returns the reversed string
  REQ-2: reversing twice returns the original string
  REQ-3: reverse_string handles empty strings

------------------------------ Generating Reports ------------------------------
✓ report.json created
✓ report.html created
✓ report.md created
============================== 3 passed in 0.54s ===============================
```

## Feature Breakdown

### 1. Machine-Readable Specifications

**simple_spec.py:**
```python
REQUIREMENTS = {
    "REQ-1": {
        "description": "reverse_string returns the reversed string",
        "priority": "high"
    },
    "REQ-2": {
        "description": "reversing twice returns the original string",
        "priority": "high"
    },
    "REQ-3": {
        "description": "reverse_string handles empty strings",
        "priority": "medium"
    }
}
```

Structured data means:
- ✅ Easy to parse programmatically
- ✅ Can generate reports automatically
- ✅ Single source of truth

### 2. Test Traceability

**simple_test.py:**
```python
@requirement("REQ-1")          # Links test to requirement
def test_basic_reversal():
    assert reverse_string("hello") == "olleh"

@requirement("REQ-1", "REQ-2")  # One test, multiple requirements
@given(st.text())
def test_reverse_twice_is_original(s):
    assert reverse_string(reverse_string(s)) == s
```

Benefits:
- ✅ Know which tests verify which requirements
- ✅ Know which requirements lack tests
- ✅ Bidirectional traceability

### 3. Automatic Coverage Tracking

**conftest.py** does this automatically:
- Tracks every test run
- Records pass/fail status
- Links to requirements
- No manual work needed!

### 4. Gap Detection

Console shows immediately:
```
❌ Uncovered:
  REQ-4: Some requirement with no tests
```

Also in JSON:
```json
{
  "REQ-4": {
    "covered": false,
    "verified": false,
    "tests": []
  }
}
```

### 5. Multi-Format Reporting

#### JSON (report.json) - For CI/CD
```json
{
  "summary": {
    "total": 3,
    "verified": 3,
    "verification_percent": 100.0
  },
  "requirements": {
    "REQ-1": {
      "covered": true,
      "verified": true,
      "tests": [...]
    }
  }
}
```

#### HTML (report.html) - For Humans
Beautiful visual report with:
- Color-coded requirements (green/yellow/red)
- Summary statistics
- Click to open in browser

#### Markdown (report.md) - For Documentation
```markdown
# Test Coverage Report

## Summary
- Total: 3
- Verified: 3 (100%)

### ✅ REQ-1: reverse_string returns the reversed string
**Tests:**
- ✓ `simple_test.py::test_basic_reversal`
```

### 6. CI/CD Integration

**check_coverage.py:**
```bash
# In your CI/CD pipeline
python -m pytest simple_test.py
python check_coverage.py --min-verification 95

# Exits with code 0 if passing, 1 if failing
```

Output:
```
============================================================
CI/CD QUALITY GATE CHECK
============================================================

Total Requirements: 3
Verified: 3
Verification: 100.0%
Minimum Required: 95.0%

✅ PASS - Verification 100.0% >= 95.0%
Build can proceed!
```

**GitHub Actions Example:**
```yaml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Install
        run: pip install pytest hypothesis
      - name: Run tests
        run: python -m pytest simple_test.py -v
      - name: Check quality gate
        run: python check_coverage.py --min-verification 95
      - name: Upload HTML report
        uses: actions/upload-artifact@v2
        with:
          name: coverage-report
          path: report.html
```

### 7. Property-Based Testing with Hypothesis

Instead of:
```python
# Manual testing - tedious and incomplete
def test_reverse():
    assert reverse_string("hello") == "olleh"
    assert reverse_string("world") == "dlrow"
    assert reverse_string("") == ""
    assert reverse_string("a") == "a"
    # ... write 100 more?
```

Use Hypothesis:
```python
# Property-based testing - automatic and comprehensive
@given(st.text())
def test_reverse_twice_is_original(s):
    assert reverse_string(reverse_string(s)) == s
```

Hypothesis automatically tests:
- Empty strings
- Single characters
- Very long strings
- Unicode: "Hello 世界"
- Emojis: "🚀🌟"
- Special chars: "\n\t\r"
- 100+ random cases

## Complete Workflow

```
┌─────────────────────────────────────────────────────┐
│ 1. Define Requirements (simple_spec.py)             │
│    REQ-1, REQ-2, REQ-3                              │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 2. Write Code (simple_code.py)                      │
│    def reverse_string(s): return s[::-1]            │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 3. Write Tests (simple_test.py)                     │
│    @requirement("REQ-1")                            │
│    @given(st.text())                                │
│    def test_property(s): ...                        │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 4. Run Tests                                        │
│    pytest simple_test.py -v                         │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 5. Automatic Tracking (conftest.py)                 │
│    - Links tests to requirements                    │
│    - Tracks pass/fail                               │
│    - Detects gaps                                   │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 6. Generate Reports (simple_reports.py)             │
│    - report.json (CI/CD)                            │
│    - report.html (humans)                           │
│    - report.md (docs)                               │
└─────────────────────────────────────────────────────┘
                      ↓
┌─────────────────────────────────────────────────────┐
│ 7. CI/CD Gate (check_coverage.py)                   │
│    ✅ Pass if verification >= 95%                   │
│    ❌ Fail if verification < 95%                    │
└─────────────────────────────────────────────────────┘
```

## Try It Yourself

### See All Features Working

```bash
# 1. Run tests - generates all reports
python -m pytest simple_test.py -v

# 2. Check JSON report
cat report.json

# 3. Open HTML report in browser
open report.html  # macOS
xdg-open report.html  # Linux

# 4. Check markdown report
cat report.md

# 5. Test CI/CD gate (should pass)
python check_coverage.py --min-verification 95
```

### See Gap Detection

```bash
# Run tests with failing test
python -m pytest simple_test_failing.py -v

# See it reported in console, JSON, HTML, and MD
# CI/CD check will fail
python check_coverage.py --min-verification 100
```

## What Makes This Minimal Yet Complete?

**Minimal:**
- Only 5 files (~314 lines total)
- Only 3 requirements
- Only 1 function to test
- Only 3 tests
- Simple, readable code

**Complete:**
- ✅ All 7 features working
- ✅ JSON, HTML, MD reports
- ✅ CI/CD integration
- ✅ Gap detection
- ✅ Hypothesis testing
- ✅ Full traceability

## Key Concepts

### Coverage vs Verification

- **Coverage** = "Has tests" (might be failing)
- **Verification** = "Has tests AND they pass"

Example:
```
Covered: 3/3 (100%)     ← All requirements have tests
Verified: 2/3 (67%)     ← But one test is failing!
```

### Property-Based Testing

Test **properties** not examples:

❌ Bad: `assert reverse("abc") == "cba"`  
✅ Good: `assert reverse(reverse(s)) == s`

The property holds for ALL strings!

## Next Steps

1. ✅ Run the examples
2. ✅ Open report.html in browser
3. ✅ Add a 4th requirement
4. ✅ Write a test for it
5. ✅ See it in all reports automatically

## File Summary

| File | Lines | Purpose |
|------|-------|---------|
| simple_spec.py | 10 | Requirements |
| simple_code.py | 4 | Code to test |
| simple_test.py | 20 | Tests |
| conftest.py | 70 | Tracking |
| simple_reports.py | 150 | Report generation |
| check_coverage.py | 60 | CI/CD integration |

**Total: ~314 lines for everything!**

Simple, sufficient, and complete. 🎉
