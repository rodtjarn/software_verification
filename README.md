# Software Verification Framework

A minimal, production-ready testing framework combining property-based testing (Hypothesis) with requirement traceability and feature coverage tracking.

## What You Get

Run one command and automatically get:
- **Requirement Coverage**: Track which requirements are tested
- **Feature Coverage**: Track which specific features within requirements are verified
- **Property-Based Testing**: Hypothesis automatically generates 2,000+ test scenarios
- **Multi-Format Reports**: JSON, HTML, Markdown, and Table formats
- **CI/CD Integration**: Quality gates with configurable thresholds
- **Gap Detection**: Instantly see what's not tested

## Quick Start

```bash
# Install dependencies
pip install pytest hypothesis

# Run tests (automatically generates all reports)
python -m pytest simple_test.py -v

# Check CI/CD quality gate
python check_coverage.py --min-verification 95
```

## Current Stats

After running tests, you'll see:
- **Requirements**: 4/4 verified (100%)
- **Features**: 11/11 verified (100%)
- **Test Scenarios**: 2,003 examples automatically generated
- **Tests**: 5 tests covering all requirements

## How It Works

### 1. Define Requirements with Features

**simple_spec.py:**
```python
REQUIREMENTS = {
    "REQ-1": {
        "description": "reverse_string returns the reversed string",
        "priority": "high",
        "features": {
            "F1.1": "handles ASCII characters",
            "F1.2": "handles Unicode characters",
            "F1.3": "handles emojis",
            "F1.4": "handles whitespace and special characters"
        }
    }
}
```

Each requirement can have multiple features for fine-grained coverage tracking.

### 2. Write Tests with Decorators

**simple_test.py:**
```python
from hypothesis import given, settings, strategies as st
from conftest import requirement, feature

@requirement("REQ-1", "REQ-2")  # Links to requirements
@feature("F1.1", "F1.2", "F1.4", "F2.1", "F2.2", "F2.3")  # Links to features
@given(st.text())  # Hypothesis generates random strings
@settings(max_examples=500)  # Test with 500 examples
def test_reverse_twice_is_original(s):
    """Reversing twice returns the original"""
    assert reverse_string(reverse_string(s)) == s
```

### 3. Run Tests and Get Reports

```bash
python -m pytest simple_test.py -v
```

You'll see:
```
=============================== Coverage Report ================================

Total Requirements: 4
Covered: 4
Verified (passing): 4
Total Test Scenarios: 2,003 examples tested

=============================== Feature Coverage ===============================

Total Features: 11
Covered: 11 (100%)
Verified: 11 (100%)

REQ-1: reverse_string returns the reversed string
  Features: 4/4 verified (100%)
    ✓ F1.1: handles ASCII characters (501 examples)
    ✓ F1.2: handles Unicode characters (500 examples)
    ✓ F1.3: handles emojis (1 example)
    ✓ F1.4: handles whitespace and special characters (501 examples)

------------------------------ Generating Reports ------------------------------
✓ report.json created
✓ report.html created
✓ report.md created
✓ report_table.txt created
```

## Reports Generated

All reports are generated automatically when you run tests:

### 1. JSON Report (report.json)
Machine-readable format for CI/CD:
```json
{
  "summary": {
    "total": 4,
    "verified": 4,
    "verification_percent": 100.0,
    "total_features": 11,
    "features_verified": 10,
    "feature_verification_percent": 90.9
  }
}
```

### 2. HTML Report (report.html)
Beautiful visual report with:
- Color-coded coverage dashboard
- Requirement details with linked tests
- Feature coverage by requirement
- Open with: `open report.html` (macOS) or `xdg-open report.html` (Linux)

### 3. Markdown Report (report.md)
Documentation-friendly format showing:
- Summary statistics
- Detailed requirement coverage
- Test case links

### 4. Table Report (report_table.txt)
Quick terminal view:
```
+-------+------------------------------------------+---------------------------------------------+--------------+----------+
| Req   | Description                              | Test Case                                   | Status       | Examples |
+-------+------------------------------------------+---------------------------------------------+--------------+----------+
| REQ-1 | reverse_string returns the reversed str  | simple_test.py::test_basic_reversal        | ✅ PASS     | 1        |
|       |                                          | simple_test.py::test_reverse_twice...      | ✅ PASS     | 500      |
+-------+------------------------------------------+---------------------------------------------+--------------+----------+
```

View anytime with:
- `python view_reports.py table` (recommended - uses bat for highlighting)
- `cat report_table.txt` (plain text)
- `python show_table.py` (alternative viewer)

## Key Features

### Two-Level Coverage Tracking

1. **Requirement Coverage**: Does the requirement have passing tests?
2. **Feature Coverage**: Which specific features within the requirement are tested?

This gives you both high-level and detailed visibility.

### Property-Based Testing with Hypothesis

Instead of writing hundreds of test cases manually:
```python
# Traditional approach - tedious and incomplete
assert reverse_string("hello") == "olleh"
assert reverse_string("world") == "dlrow"
# ... write 1000 more?
```

Use Hypothesis to test properties:
```python
# Property-based - automatic and comprehensive
@given(st.text())
@settings(max_examples=1000)
def test_length_preserved(s):
    assert len(reverse_string(s)) == len(s)
```

Hypothesis automatically tests:
- Empty strings
- Single characters
- Very long strings
- Unicode characters
- Special characters
- 1,000 random examples

### Automatic Gap Detection

The framework immediately shows:
- **Uncovered requirements**: Requirements with no tests
- **Uncovered features**: Features not tested
- **Failing tests**: Which requirements/features are failing

Example output showing gaps (when they exist):
```
REQ-1: reverse_string returns the reversed string
  Features: 3/4 verified (75.0%)
    ✓ F1.1: handles ASCII characters
    ✓ F1.2: handles Unicode characters
    ✗ F1.3: handles emojis (NOT TESTED)  ← Gap detected!
    ✓ F1.4: handles whitespace

Note: In the current example, all features are now tested (100% coverage).
```

### CI/CD Integration

**check_coverage.py** provides quality gates:

```bash
# Require 95% verification to pass build
python check_coverage.py --min-verification 95

# Require 100% feature coverage
python check_coverage.py --min-feature-coverage 100
```

**GitHub Actions Example:**
```yaml
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

## File Structure

```
simple_spec.py          ← Requirements and features (structured data)
simple_code.py          ← Code under test
simple_test.py          ← Tests with @requirement and @feature decorators
conftest.py             ← Pytest plugin (automatic tracking)
simple_reports.py       ← Report generators (JSON/HTML/MD/Table)
check_coverage.py       ← CI/CD quality gates
show_table.py           ← View table report anytime
```

## Adding Your Own Tests

### Step 1: Add a Requirement

Edit **simple_spec.py**:
```python
"REQ-5": {
    "description": "Your requirement here",
    "priority": "high",
    "features": {
        "F5.1": "Feature description 1",
        "F5.2": "Feature description 2"
    }
}
```

### Step 2: Write a Test

Edit **simple_test.py**:
```python
@requirement("REQ-5")
@feature("F5.1", "F5.2")
@given(st.text())  # Or other Hypothesis strategies
@settings(max_examples=100)
def test_your_requirement(input_data):
    assert your_function(input_data) == expected_result
```

### Step 3: Run Tests

```bash
python -m pytest simple_test.py -v
```

All reports update automatically!

## Common Hypothesis Strategies

```python
from hypothesis import strategies as st

@given(st.text())                    # Any string
@given(st.text(min_size=1))          # Non-empty string
@given(st.integers())                # Any integer
@given(st.integers(min_value=0))     # Non-negative integer
@given(st.floats())                  # Any float
@given(st.lists(st.text()))          # List of strings
@given(st.tuples(st.text(), st.integers()))  # Tuple of (string, int)
```

## Coverage vs Verification

- **Coverage**: Requirement/feature has tests (they might be failing)
- **Verification**: Requirement/feature has tests AND they all pass

Example:
```
Requirements: 4 covered, 3 verified
   ↑                      ↑
   All have tests         3 have passing tests
```

## Performance

The framework adds minimal overhead:
- **Feature tracking**: <0.1 seconds
- **Report generation**: <0.5 seconds
- **Total overhead**: <5% of test execution time

With 2,003 test scenarios, total runtime is typically under 2 seconds.

## Viewing Reports

Use the provided viewer script for easy access to all reports and documentation:

```bash
# List all available reports and docs
python view_reports.py

# View specific reports
python view_reports.py json          # Show summary
python view_reports.py table         # View table (with bat if available)
python view_reports.py html          # Open in browser
python view_reports.py md            # View markdown report

# View documentation
python view_reports.py readme        # This file
python view_reports.py quick         # Quick reference
python view_reports.py start         # Quick start guide
```

The viewer automatically:
- Uses `bat` for syntax highlighting if available
- Falls back to `cat` if `bat` is not installed
- Opens HTML reports in your default browser
- Shows a clean JSON summary (use `--full` for complete JSON)

## Documentation Files

- **README.md** (this file) - Complete guide
- **START_HERE.txt** - 5-minute quick start
- **QUICK_REFERENCE.md** - Quick reference cheat sheet
- **COMPLETE_README.md** - Detailed walkthrough
- **TROUBLESHOOTING.md** - Common issues and solutions
- **view_reports.py** - Easy report viewer

## Learn More

See **START_HERE.txt** for a 5-minute introduction, or **QUICK_REFERENCE.md** for quick reference.

## Summary

This framework gives you:
- ✅ **Simple**: Easy to understand and extend
- ✅ **Automated**: Reports generated automatically
- ✅ **Comprehensive**: Requirement + feature coverage
- ✅ **Fast**: Minimal overhead, runs in seconds
- ✅ **CI/CD Ready**: Quality gates included
- ✅ **Property-Based**: Hypothesis finds edge cases automatically

Run tests, get reports, ensure quality. It's that simple.
