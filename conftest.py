"""
Simple pytest plugin to track requirement coverage
"""
import pytest
from simple_spec import REQUIREMENTS


def requirement(*req_ids):
    """Decorator to link tests to requirements"""
    def decorator(func):
        func._requirements = req_ids
        return func
    return decorator


def pytest_configure(config):
    """Initialize tracking"""
    config._coverage = {req_id: [] for req_id in REQUIREMENTS}


def pytest_runtest_makereport(item, call):
    """Track which tests cover which requirements"""
    if call.when == "call" and hasattr(item.function, '_requirements'):
        outcome = "PASS" if call.excinfo is None else "FAIL"
        
        test_info = {
            'test': item.nodeid,
            'outcome': outcome
        }
        
        # Capture failure details
        if call.excinfo is not None:
            excinfo = call.excinfo
            
            # Parse the error message to extract stimuli, response, and error
            error_msg = str(excinfo.value)
            
            # Try to extract test arguments (stimuli) from pytest parametrize
            stimuli = {}
            if hasattr(item, 'callspec'):
                stimuli = {k: repr(v) for k, v in item.callspec.params.items()}
            
            # If no parametrize, try to read the test source code
            if not stimuli:
                try:
                    import inspect
                    import re
                    # Get the test source code
                    source = inspect.getsource(item.function)
                    # Look for assertions with function calls
                    # Pattern: assert function_name(args) == ...
                    assert_pattern = r'assert\s+(\w+)\((.*?)\)\s*=='
                    match = re.search(assert_pattern, source)
                    if match:
                        func_name = match.group(1)
                        args = match.group(2)
                        stimuli = {'input': args, 'function': func_name}
                except:
                    pass
            
            # Try to parse assertion to get actual value (response) and expected
            response = None
            expected = None
            
            # Look for assert patterns like "assert X == Y"
            if 'assert' in error_msg:
                lines = error_msg.split('\n')
                for i, line in enumerate(lines):
                    if ' == ' in line and 'assert' in line.lower():
                        # Try to extract actual and expected
                        parts = line.split(' == ')
                        if len(parts) == 2:
                            response = parts[0].replace('assert', '').strip()
                            expected = parts[1].strip()
                    # Look for pytest's detailed comparison
                    elif line.strip().startswith('+'):
                        if not response:  # Only set if not already found
                            response = line.strip()[1:].strip()
                    elif line.strip().startswith('-'):
                        if not expected:  # Only set if not already found
                            expected = line.strip()[1:].strip()
            
            test_info['failure'] = {
                'stimuli': stimuli if stimuli else 'Not captured',
                'response': response if response else 'Not captured',
                'expected': expected if expected else 'Not captured',
                'error_message': error_msg,
                'error_type': excinfo.typename
            }
        
        for req_id in item.function._requirements:
            if req_id in item.config._coverage:
                item.config._coverage[req_id].append(test_info)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print coverage report"""
    coverage = config._coverage
    
    # Calculate stats
    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage.values() if tests)
    verified = sum(1 for tests in coverage.values() 
                   if tests and all(t['outcome'] == 'PASS' for t in tests))
    
    terminalreporter.write_sep("=", "Coverage Report")
    terminalreporter.write_line(f"\nTotal Requirements: {total}")
    terminalreporter.write_line(f"Covered: {covered}")
    terminalreporter.write_line(f"Verified (passing): {verified}")
    
    # Show details
    terminalreporter.write_line("\n✅ Verified:")
    for req_id, tests in coverage.items():
        if tests and all(t['outcome'] == 'PASS' for t in tests):
            terminalreporter.write_line(f"  {req_id}: {REQUIREMENTS[req_id]['description']}")
    
    # Show failures
    failing = {req_id: tests for req_id, tests in coverage.items() 
               if tests and not all(t['outcome'] == 'PASS' for t in tests)}
    if failing:
        terminalreporter.write_line("\n⚠️  Failing:")
        for req_id, tests in failing.items():
            terminalreporter.write_line(f"  {req_id}: {REQUIREMENTS[req_id]['description']}")
            for test in tests:
                symbol = "✓" if test['outcome'] == 'PASS' else "✗"
                terminalreporter.write_line(f"    {symbol} {test['test']}")
                
                # Show failure details in clear format
                if test['outcome'] == 'FAIL' and 'failure' in test:
                    failure = test['failure']
                    terminalreporter.write_line(f"       Stimuli (Input): {failure['stimuli']}")
                    terminalreporter.write_line(f"       Response (Actual output): {failure['response']}")
                    terminalreporter.write_line(f"       Expected (Test expects): {failure['expected']}")
                    terminalreporter.write_line(f"       Error: {failure['error_type']}")
    
    # Show uncovered
    uncovered = [req_id for req_id, tests in coverage.items() if not tests]
    if uncovered:
        terminalreporter.write_line("\n❌ Uncovered:")
        for req_id in uncovered:
            terminalreporter.write_line(f"  {req_id}: {REQUIREMENTS[req_id]['description']}")
    
    # Generate reports
    terminalreporter.write_line("")
    terminalreporter.write_sep("-", "Generating Reports")
    try:
        from simple_reports import generate_reports
        generate_reports(coverage)
    except ImportError:
        terminalreporter.write_line("⚠️  simple_reports.py not found - skipping report generation")
        terminalreporter.write_line("   (To generate JSON/HTML/MD reports, ensure simple_reports.py is present)")
