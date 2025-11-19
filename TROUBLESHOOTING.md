# Troubleshooting Guide

## "Reports not being generated?"

### Problem
You run `pytest simple_test.py -v` but don't see:
```
✓ report.json created
✓ report.html created
✓ report.md created
```

### Solution
Make sure `simple_reports.py` is in the same directory as your test files.

**File structure should be:**
```
your_directory/
  ├── simple_spec.py
  ├── simple_code.py
  ├── simple_test.py
  ├── conftest.py
  └── simple_reports.py  ← This file is needed!
```

### What happens without simple_reports.py?
Tests still run fine, but you'll see:
```
⚠️  simple_reports.py not found - skipping report generation
```

The console report still works - you just won't get JSON/HTML/MD files.

### To get reports:
1. Make sure `simple_reports.py` is present
2. Run tests again: `python -m pytest simple_test.py -v`
3. You'll see: `✓ report.json created` etc.
4. Check: `ls report.*` to verify files exist

## "ImportError: No module named 'simple_conftest'"

### Problem
```
ImportError: No module named 'simple_conftest'
```

### Solution
The file should be named `conftest.py` (not `simple_conftest.py`) in your working directory.

**Correct:**
```
your_directory/
  ├── conftest.py  ← Named exactly this
  ├── simple_test.py
  └── ...
```

**The import in simple_test.py should be:**
```python
from conftest import requirement  # ✓ Correct
```

**Not:**
```python
from simple_conftest import requirement  # ✗ Wrong
```

## "Hypothesis not found"

### Problem
```
ModuleNotFoundError: No module named 'hypothesis'
```

### Solution
Install it:
```bash
pip install hypothesis
```

## "Pytest not found"

### Problem
```
pytest: command not found
```

### Solution
Install it:
```bash
pip install pytest
```

## Minimal Test - Does it work?

Run this in an empty directory to test:

```bash
# 1. Create directory
mkdir test_hypothesis
cd test_hypothesis

# 2. Copy these 4 essential files:
#    - simple_spec.py
#    - simple_code.py
#    - simple_test.py
#    - conftest.py

# 3. Run without reports (works!)
python -m pytest simple_test.py -v
# Should see: 3 passed

# 4. Add simple_reports.py

# 5. Run with reports (now generates files!)
python -m pytest simple_test.py -v
# Should see: ✓ report.json created, etc.

# 6. Verify
ls report.*
# Should show: report.html report.json report.md
```

## Quick Checklist

✅ Python 3.7+ installed?
✅ pytest installed? (`pip install pytest`)
✅ hypothesis installed? (`pip install hypothesis`)
✅ Files in same directory?
✅ conftest.py named correctly (not simple_conftest.py)?
✅ simple_reports.py present (for reports)?

## Still Having Issues?

### Test with minimal setup:
```bash
# Just 4 files needed to run tests:
simple_spec.py
simple_code.py
simple_test.py
conftest.py

# Optional for reports:
simple_reports.py
```

### Verify imports:
```python
# In simple_test.py, should have:
from conftest import requirement

# NOT:
from simple_conftest import requirement
```

## Success Looks Like This

```bash
$ python -m pytest simple_test.py -v

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

That's it! If you see this, everything is working perfectly. 🎉
