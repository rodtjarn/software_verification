# Quick Reference Cheat Sheet

## Installation
```bash
pip install pytest hypothesis
```

## Run Tests
```bash
# Run tests and generate all reports
python -m pytest simple_test.py -v

# Check quality gate
python check_coverage.py --min-verification 95
```

## View Reports
```bash
# Easy way - use the viewer (recommended)
python view_reports.py              # List all available reports
python view_reports.py table        # View table (syntax highlighted with bat)
python view_reports.py json         # View JSON summary
python view_reports.py html         # Open HTML in browser
python view_reports.py md           # View markdown report

# View documentation
python view_reports.py readme       # README.md
python view_reports.py quick        # This file
python view_reports.py start        # START_HERE.txt

# Manual way
cat report_table.txt                # Plain table
cat report.json                     # Raw JSON
bat report.md                       # Markdown (if bat installed)
```

## Current Stats
- **Requirements**: 4/4 verified (100%)
- **Features**: 10/11 verified (90.9%)
- **Test Scenarios**: 2,002 examples
- **Reports**: JSON, HTML, MD, Table

## File Structure
```
simple_spec.py          ← Define requirements and features
simple_code.py          ← Code to test
simple_test.py          ← Tests with decorators
conftest.py             ← Tracking plugin (don't modify)
simple_reports.py       ← Report generators
check_coverage.py       ← CI/CD quality gates
show_table.py           ← View table anytime
```

## How to Add a New Test

### Step 1: Add requirement with features
```python
# In simple_spec.py
"REQ-5": {
    "description": "Your requirement description",
    "priority": "high",
    "features": {
        "F5.1": "First feature description",
        "F5.2": "Second feature description"
    }
}
```

### Step 2: Write test with decorators
```python
# In simple_test.py
from conftest import requirement, feature

@requirement("REQ-5")           # Link to requirement
@feature("F5.1", "F5.2")        # Link to features
@given(st.text())               # Hypothesis strategy
@settings(max_examples=100)     # Number of test cases
def test_your_property(s):
    assert your_function(s) == expected_result
```

### Step 3: Run
```bash
python -m pytest simple_test.py -v
```

All reports update automatically!

## Decorators

### @requirement()
Links test to one or more requirements:
```python
@requirement("REQ-1")              # Single requirement
@requirement("REQ-1", "REQ-2")     # Multiple requirements
```

### @feature()
Links test to one or more features:
```python
@feature("F1.1")                   # Single feature
@feature("F1.1", "F1.2", "F1.3")  # Multiple features
```

### @given() - Hypothesis
Provides random test inputs:
```python
@given(st.text())                  # Random strings
@given(st.integers())              # Random integers
@given(st.lists(st.text()))        # Random lists of strings
```

### @settings()
Controls Hypothesis behavior:
```python
@settings(max_examples=100)        # Test 100 examples
@settings(max_examples=1000)       # Test 1000 examples
```

## Common Hypothesis Strategies

```python
from hypothesis import strategies as st

# Strings
st.text()                          # Any string (including empty)
st.text(min_size=1)                # Non-empty string
st.text(min_size=5, max_size=10)   # 5-10 characters

# Numbers
st.integers()                      # Any integer
st.integers(min_value=0)           # Non-negative
st.integers(min_value=1, max_value=100)  # 1-100
st.floats()                        # Any float

# Collections
st.lists(st.text())                # List of strings
st.lists(st.integers(), min_size=1)  # Non-empty list of ints
st.tuples(st.text(), st.integers())  # Tuple of (string, int)
st.dictionaries(st.text(), st.integers())  # Dict mapping strings to ints

# Booleans and choices
st.booleans()                      # True or False
st.sampled_from(['a', 'b', 'c'])   # One of the values
```

## Example Output

### Console Report
```
Total Requirements: 4
Covered: 4
Verified (passing): 4
Total Test Scenarios: 2,002 examples

Total Features: 11
Covered: 10 (90.9%)
Verified: 10 (90.9%)

✅ Verified:
  REQ-1: reverse_string returns the reversed string
  REQ-2: reversing twice returns the original string
  REQ-3: reverse_string handles empty strings
  REQ-4: reverse_string preserves string length
```

### With Gap Detection
```
REQ-1: reverse_string returns the reversed string
  Features: 3/4 verified (75.0%)
    ✓ F1.1: handles ASCII characters (501 examples)
    ✓ F1.2: handles Unicode characters (500 examples)
    ✗ F1.3: handles emojis (NOT TESTED)  ← Gap!
    ✓ F1.4: handles whitespace (501 examples)
```

### With Failing Test
```
⚠️  Failing:
  REQ-1: reverse_string returns the reversed string
    ✓ simple_test.py::test_basic_reversal
    ✗ simple_test.py::test_that_fails
       Stimuli (Input): {'input': 'test'}
       Response (Actual): 'tset'
       Expected (Test expects): 'test'
       Error: AssertionError
```

## Reports Generated

All generated automatically after running tests:

| File | Purpose | View With |
|------|---------|-----------|
| report.json | Machine-readable for CI/CD | `cat report.json` |
| report.html | Visual dashboard | `open report.html` |
| report.md | Documentation | `cat report.md` |
| report_table.txt | Quick table view | `cat report_table.txt` |

## CI/CD Integration

```bash
# In your CI/CD pipeline
python -m pytest simple_test.py -v
python check_coverage.py --min-verification 95

# Optional: Check feature coverage too
python check_coverage.py --min-feature-coverage 90
```

**GitHub Actions:**
```yaml
- name: Run tests
  run: python -m pytest simple_test.py -v
- name: Quality gate
  run: python check_coverage.py --min-verification 95
- name: Upload report
  uses: actions/upload-artifact@v2
  with:
    name: coverage-report
    path: report.html
```

## Key Concepts

### Coverage vs Verification
- **Coverage** = Has tests (might be failing)
- **Verification** = Has tests AND all pass

Example:
```
Covered: 4/4 (100%)     ← All have tests
Verified: 3/4 (75%)     ← One is failing
```

### Requirement vs Feature
- **Requirement** = High-level capability (REQ-1, REQ-2, etc.)
- **Feature** = Specific aspect of a requirement (F1.1, F1.2, etc.)

Example:
```
REQ-1: reverse_string returns the reversed string
  ├─ F1.1: handles ASCII characters
  ├─ F1.2: handles Unicode characters
  ├─ F1.3: handles emojis
  └─ F1.4: handles whitespace and special characters
```

### Property-Based vs Example-Based Testing

**Example-Based (traditional):**
```python
def test_reverse():
    assert reverse("abc") == "cba"
    assert reverse("hello") == "olleh"
    # ... write 100 more?
```

**Property-Based (Hypothesis):**
```python
@given(st.text())
def test_reverse_twice(s):
    assert reverse(reverse(s)) == s
    # Tests 100+ cases automatically!
```

## Complete Example

```python
# In simple_spec.py
REQUIREMENTS = {
    "REQ-1": {
        "description": "reverse_string returns the reversed string",
        "priority": "high",
        "features": {
            "F1.1": "handles ASCII characters",
            "F1.2": "handles Unicode characters"
        }
    }
}

# In simple_test.py
from hypothesis import given, settings, strategies as st
from simple_code import reverse_string
from conftest import requirement, feature

@requirement("REQ-1")
@feature("F1.1", "F1.2")
@given(st.text())
@settings(max_examples=500)
def test_reverse_twice(s):
    """Reversing twice returns the original"""
    assert reverse_string(reverse_string(s)) == s
```

## Troubleshooting

**Tests not linking to requirements?**
- Check that you imported `requirement` and `feature` from conftest
- Verify requirement IDs match those in simple_spec.py

**Reports not generated?**
- Ensure simple_reports.py is in the same directory
- Check that conftest.py calls `generate_reports()`

**Feature coverage shows 0%?**
- Make sure you're using the `@feature()` decorator on tests
- Verify feature IDs match those in simple_spec.py

## That's It!

Three simple steps:
1. Define requirements and features in simple_spec.py
2. Write tests with @requirement and @feature decorators
3. Run tests and get automatic reports

Everything else happens automatically!
