# Failure Details Feature

## Enhanced Failure Reporting

The system captures detailed information about test failures in a **structured format**:

1. ✅ **Stimuli (Input)** - What was passed to the function
2. ✅ **Response (Actual)** - What the function returned
3. ✅ **Expected** - What the function should have returned
4. ✅ **Error Type** - The type of exception

## What You Get

### Console Report
```
⚠️  Failing:
  REQ-1: reverse_string returns the reversed string
    ✗ test_with_parameters[test-wrong]
       Stimuli (Input): {'input_str': 'test', 'expected': 'wrong'}
       Response (Actual): tset
       Expected: wrong
       Error: AssertionError
```

### JSON Report
```json
{
  "test": "test_with_parameters[test-wrong]",
  "outcome": "FAIL",
  "failure": {
    "stimuli": {"input_str": "test", "expected": "wrong"},
    "response": "tset",
    "expected": "wrong",
    "error_type": "AssertionError",
    "error_message": "reverse_string('test') returned 'tset', expected 'wrong'"
  }
}
```

### HTML Report
Visual error box showing:
- **❌ Test Failure** header
- **Stimuli (Input):** Shows the input parameters
- **Response (Actual):** Shows what was returned
- **Expected:** Shows what should have been returned
- **Error Type:** Shows the exception type

### Markdown Report
```markdown
- ✗ `test_with_parameters[test-wrong]`
  - **Stimuli (Input):** `{'input_str': 'test', 'expected': 'wrong'}`
  - **Response (Actual):** `tset`
  - **Expected:** `wrong`
  - **Error Type:** `AssertionError`
```

## Example: Parametrized Test Failure

**Test code:**
```python
@requirement("REQ-1")
@pytest.mark.parametrize("input_str,expected", [
    ("hello", "olleh"),
    ("test", "wrong"),  # Will fail!
])
def test_with_parameters(input_str, expected):
    result = reverse_string(input_str)
    assert result == expected
```

**Console output:**
```
✗ test_with_parameters[test-wrong]
   Stimuli (Input): {'input_str': 'test', 'expected': 'wrong'}
   Response (Actual): tset
   Expected: wrong
   Error: AssertionError
```

**What this tells you:**
- **Input was:** "test"
- **Function returned:** "tset" 
- **Expected:** "wrong"
- You can immediately see the mismatch!

## Example: Hypothesis Test Failure

**Test code:**
```python
@requirement("REQ-1")
@given(st.text())
def test_with_hypothesis(s):
    assert 'x' not in reverse_string(s)  # Will fail for strings with 'x'
```

**Console output:**
```
✗ simple_test_hypothesis_fail.py::test_with_hypothesis
   Error: Found 'x' in reversed string
   Inputs: {'s': "'x'"}  ← Shows the failing input!
```

**What this tells you:**
- The test failed when input was the string 'x'
- Hypothesis found a counterexample
- You can reproduce the failure with that specific input

## Benefits

### 1. Fast Debugging
Instead of:
```
❌ test_something failed
```

You get:
```
❌ test_something failed
   Error: assert 5 == 4
   Inputs: {'x': 3, 'y': 2}
```

Now you know exactly what inputs caused the failure!

### 2. CI/CD Insights
In your CI/CD pipeline, the JSON report contains:
```json
{
  "failure": {
    "type": "AssertionError",
    "message": "Expected 10, got 9",
    "inputs": {"value": 42}
  }
}
```

Parse this to:
- Create detailed bug reports automatically
- Track failure patterns
- Generate test case reproduction steps

### 3. Property-Based Testing
With Hypothesis, when it finds a counterexample:
```python
@given(st.integers())
def test_property(n):
    assert some_function(n) > 0
```

Failure shows:
```
Error: assert -5 > 0
Inputs: {'n': -5}
```

You immediately know which input broke your property!

### 4. Stakeholder Communication
HTML report shows failures in a user-friendly way:
- Red error boxes (can't miss them!)
- Readable error messages
- Context about what was tested

## How It Works

### Automatic Capture
The conftest.py plugin automatically:
1. Detects test failures
2. Extracts error information
3. Captures test parameters (if any)
4. Stores in all report formats

### No Extra Code Needed
Just write your tests normally:
```python
@requirement("REQ-1")
def test_something():
    assert foo() == bar()
```

If it fails, details are captured automatically!

### Works With All Test Types

✅ Regular tests
✅ Parametrized tests (`@pytest.mark.parametrize`)
✅ Hypothesis tests (`@given()`)
✅ Any pytest-compatible test

## Viewing Failure Details

### In Console
Run tests, failures show inline:
```bash
python -m pytest simple_test.py -v
```

### In HTML
Open report.html, failing tests have red error boxes

### In JSON
Parse programmatically:
```python
import json
report = json.load(open('report.json'))
for req_id, req_data in report['requirements'].items():
    for test in req_data['tests']:
        if test['outcome'] == 'FAIL':
            print(f"Failed: {test['test']}")
            print(f"Error: {test['failure']['message']}")
```

### In Markdown
View in any markdown viewer or on GitHub/GitLab

## CI/CD Integration Example

```python
# check_failures.py
import json

report = json.load(open('report.json'))

print("Failed Tests:")
for req_id, req_data in report['requirements'].items():
    for test in req_data['tests']:
        if test['outcome'] == 'FAIL':
            print(f"\n{req_id}: {req_data['description']}")
            print(f"  Test: {test['test']}")
            print(f"  Error: {test['failure']['message']}")
            if 'inputs' in test:
                print(f"  Inputs: {test['inputs']}")
```

Output:
```
Failed Tests:

REQ-1: reverse_string returns the reversed string
  Test: simple_test_failing.py::test_intentional_failure
  Error: assert 'olleh' == 'wrong'
  
  - wrong
  + olleh
```

## Summary

| Format | Shows Error Message | Shows Inputs | Use Case |
|--------|-------------------|--------------|----------|
| Console | ✅ | ✅ | Quick debugging |
| JSON | ✅ | ✅ | CI/CD automation |
| HTML | ✅ | ✅ | Stakeholder reports |
| Markdown | ✅ | ✅ | Documentation |

**All failure details captured automatically - no extra work required!** 🎉
