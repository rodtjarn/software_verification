"""
Simple pytest plugin to track requirement coverage
"""
import pytest
from simple_spec import REQUIREMENTS, get_all_features

# Track Hypothesis statistics
_hypothesis_stats = {}


def requirement(*req_ids):
    """Decorator to link tests to requirements"""
    def decorator(func):
        func._requirements = req_ids
        return func
    return decorator


def feature(*feature_ids):
    """Decorator to mark which features a test covers"""
    def decorator(func):
        if not hasattr(func, '_features'):
            func._features = []
        func._features.extend(feature_ids)
        return func
    return decorator


def pytest_configure(config):
    """Initialize tracking"""
    config._coverage = {req_id: [] for req_id in REQUIREMENTS}
    config._feature_coverage = {}

    # Hook into Hypothesis to track examples
    try:
        from hypothesis.reporting import default, with_reporter

        def hypothesis_reporter(msg):
            # Capture statistics messages
            if "Trying example:" in msg or "examples" in msg.lower():
                # Store for later use
                pass
            default(msg)

        # This will capture Hypothesis output
        # but we'll use a different approach - checking settings
    except ImportError:
        pass


def pytest_runtest_setup(item):
    """Track test setup and check if it's a Hypothesis test"""
    # Check if this test uses Hypothesis
    if hasattr(item, 'function'):
        func = item.function
        # Check for Hypothesis wrapper
        if hasattr(func, 'hypothesis'):
            # This is a Hypothesis test
            test_id = item.nodeid
            _hypothesis_stats[test_id] = {'is_hypothesis': True, 'examples': 0}


def pytest_runtest_makereport(item, call):
    """Track which tests cover which requirements"""
    if call.when == "call" and hasattr(item.function, '_requirements'):
        outcome = "PASS" if call.excinfo is None else "FAIL"

        test_info = {
            'test': item.nodeid,
            'outcome': outcome
        }

        # Check if this is a Hypothesis test and get example count
        if hasattr(item.function, 'hypothesis'):
            # Try to get the max_examples setting
            try:
                from hypothesis.internal.reflection import get_pretty_function_description
                from hypothesis import settings

                # Try multiple ways to get the settings
                max_examples = 100  # default

                # Method 1: Check if item has hypothesis data stored
                if hasattr(item, 'hypothesis_data'):
                    max_examples = getattr(item.hypothesis_data, 'max_examples', 100)
                # Method 2: Try to get from the function wrapper
                elif hasattr(item.function, '_hypothesis_internal_use_settings'):
                    test_settings = item.function._hypothesis_internal_use_settings
                    max_examples = test_settings.max_examples
                # Method 3: Try to get from hypothesis attribute
                elif hasattr(item.function.hypothesis, '_hypothesis_internal_use_settings'):
                    test_settings = item.function.hypothesis._hypothesis_internal_use_settings
                    max_examples = test_settings.max_examples

                test_info['hypothesis_examples'] = max_examples
            except Exception as e:
                # Fallback: use default
                test_info['hypothesis_examples'] = 100  # default
        else:
            test_info['hypothesis_examples'] = 1  # Regular test = 1 example
        
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

        # Track feature coverage
        if hasattr(item.function, '_features'):
            for feature_id in item.function._features:
                if feature_id not in item.config._feature_coverage:
                    item.config._feature_coverage[feature_id] = []

                feature_test_info = {
                    'test': item.nodeid,
                    'outcome': outcome,
                    'examples': test_info.get('hypothesis_examples', 1)
                }
                item.config._feature_coverage[feature_id].append(feature_test_info)


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """Print coverage report"""
    coverage = config._coverage

    # Calculate stats
    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage.values() if tests)
    verified = sum(1 for tests in coverage.values()
                   if tests and all(t['outcome'] == 'PASS' for t in tests))

    # Calculate total Hypothesis examples tested
    total_examples = 0
    total_tests = 0
    for tests in coverage.values():
        for test in tests:
            total_tests += 1
            total_examples += test.get('hypothesis_examples', 1)

    terminalreporter.write_sep("=", "Coverage Report")
    terminalreporter.write_line(f"\nTotal Requirements: {total}")
    terminalreporter.write_line(f"Covered: {covered}")
    terminalreporter.write_line(f"Verified (passing): {verified}")
    terminalreporter.write_line(f"Total Test Scenarios: {total_examples:,} examples across {total_tests} tests")
    
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

    # Print table view
    terminalreporter.write_line("")
    terminalreporter.write_sep("=", "Coverage Table")

    # Prepare table data
    rows = []
    for req_id in sorted(coverage.keys()):
        tests = coverage[req_id]
        description = REQUIREMENTS[req_id]['description']

        if not tests:
            rows.append([req_id, description, "No tests", "❌ UNCOVERED", "0"])
        else:
            for i, test in enumerate(tests):
                test_name = test['test']
                outcome = test['outcome']
                status = "✅ PASS" if outcome == "PASS" else "❌ FAIL"
                examples = test.get('hypothesis_examples', 1)
                examples_str = f"{examples:,}"

                if i == 0:
                    rows.append([req_id, description, test_name, status, examples_str])
                else:
                    rows.append(["", "", test_name, status, examples_str])

    # Calculate column widths
    col1_width = max((len(row[0]) for row in rows), default=10)
    col2_width = max((len(row[1]) for row in rows), default=40)
    col3_width = max((len(row[2]) for row in rows), default=50)
    col4_width = 12
    col5_width = 10

    # Print table
    separator = f"+{'-'*(col1_width+2)}+{'-'*(col2_width+2)}+{'-'*(col3_width+2)}+{'-'*(col4_width+2)}+{'-'*(col5_width+2)}+"
    terminalreporter.write_line("")
    terminalreporter.write_line(separator)
    terminalreporter.write_line(f"| {'Requirement':<{col1_width}} | {'Description':<{col2_width}} | {'Test Case':<{col3_width}} | {'Status':<{col4_width}} | {'Examples':<{col5_width}} |")
    terminalreporter.write_line(separator)

    for row in rows:
        req_id, desc, test, status, examples = row
        terminalreporter.write_line(f"| {req_id:<{col1_width}} | {desc:<{col2_width}} | {test:<{col3_width}} | {status:<{col4_width}} | {examples:<{col5_width}} |")

    terminalreporter.write_line(separator)

    # Feature Coverage Report
    terminalreporter.write_line("")
    terminalreporter.write_sep("=", "Feature Coverage")

    all_features = get_all_features()
    feature_coverage_data = config._feature_coverage

    total_features = len(all_features)
    covered_features = len(feature_coverage_data)
    verified_features = sum(1 for tests in feature_coverage_data.values()
                           if tests and all(t['outcome'] == 'PASS' for t in tests))

    terminalreporter.write_line(f"\nTotal Features: {total_features}")
    terminalreporter.write_line(f"Covered: {covered_features} ({round(covered_features/total_features*100, 1) if total_features > 0 else 0}%)")
    terminalreporter.write_line(f"Verified: {verified_features} ({round(verified_features/total_features*100, 1) if total_features > 0 else 0}%)")

    # Group features by requirement
    for req_id in sorted(REQUIREMENTS.keys()):
        req = REQUIREMENTS[req_id]
        if 'features' not in req:
            continue

        req_features = req['features']
        covered_count = sum(1 for feat_id in req_features.keys() if feat_id in feature_coverage_data)
        verified_count = sum(1 for feat_id in req_features.keys()
                            if feat_id in feature_coverage_data
                            and all(t['outcome'] == 'PASS' for t in feature_coverage_data[feat_id]))

        pct = round(verified_count/len(req_features)*100, 1) if req_features else 0
        terminalreporter.write_line(f"\n{req_id}: {req['description']}")
        terminalreporter.write_line(f"  Features: {verified_count}/{len(req_features)} verified ({pct}%)")

        for feat_id, feat_desc in sorted(req_features.items()):
            if feat_id in feature_coverage_data:
                tests = feature_coverage_data[feat_id]
                all_pass = all(t['outcome'] == 'PASS' for t in tests)
                total_examples = sum(t.get('examples', 1) for t in tests)
                symbol = "✓" if all_pass else "✗"
                terminalreporter.write_line(f"    {symbol} {feat_id}: {feat_desc} ({total_examples} examples)")
            else:
                terminalreporter.write_line(f"    ✗ {feat_id}: {feat_desc} (NOT TESTED)")

    # Generate reports
    terminalreporter.write_line("")
    terminalreporter.write_sep("-", "Generating Reports")
    try:
        from simple_reports import generate_reports
        generate_reports(coverage, feature_coverage_data)
    except ImportError:
        terminalreporter.write_line("⚠️  simple_reports.py not found - skipping report generation")
        terminalreporter.write_line("   (To generate JSON/HTML/MD reports, ensure simple_reports.py is present)")
