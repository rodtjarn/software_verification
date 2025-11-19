# Quick Reference Cheat Sheet

## Installation
```bash
pip install pytest hypothesis
```

## Run Tests
```bash
python -m pytest simple_test.py -v
```

## File Structure
```
simple_spec.py          ← Define requirements (3 requirements)
simple_code.py          ← Code to test (1 function)
simple_test.py          ← Tests (3 tests)
conftest.py             ← Magic tracking (don't modify)
```

## How to Add a New Test

### Step 1: Add requirement
```python
# In simple_spec.py
"REQ-4": {
    "description": "Your requirement here",
    "priority": "high"
}
```

### Step 2: Write test
```python
# In simple_test.py
@requirement("REQ-4")
@given(st.text())  # Use Hypothesis for random inputs
def test_your_property(s):
    assert some_property(s) == expected
```

### Step 3: Run
```bash
python -m pytest simple_test.py -v
```

## Hypothesis Strategies

Common input types:
```python
@given(st.text())              # Any string
@given(st.text(min_size=1))    # Non-empty string  
@given(st.integers())          # Any integer
@given(st.floats())            # Any float
@given(st.lists(st.text()))    # List of strings
```

## Example Output

### All Tests Passing
```
Total Requirements: 3
Covered: 3
Verified (passing): 3

✅ Verified:
  REQ-1: reverse_string returns the reversed string
  REQ-2: reversing twice returns the original string
  REQ-3: reverse_string handles empty strings
```

### One Test Failing
```
Total Requirements: 3
Covered: 3
Verified (passing): 2

✅ Verified:
  REQ-2: reversing twice returns the original string
  REQ-3: reverse_string handles empty strings

⚠️  Failing:
  REQ-1: reverse_string returns the reversed string
    ✓ simple_test.py::test_basic_reversal
    ✗ simple_test.py::test_intentional_failure
```

## Key Differences

**Covered** = Has tests (might be failing)
**Verified** = Has tests AND all pass

## That's It!

This is the simplest possible setup:
- 3 requirements
- 1 function
- 3 tests
- Automatic tracking

Add more requirements and tests as needed!
