#!/usr/bin/env python
"""
Display test coverage as a table
"""
import json
import sys


def print_table():
    """Print test coverage in table format"""

    # Read the JSON report
    try:
        with open("report.json") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("❌ Error: report.json not found. Run tests first!")
        print("   python -m pytest simple_test.py -v")
        return False

    # Prepare table data
    rows = []
    for req_id in sorted(report["requirements"].keys()):
        req_data = report["requirements"][req_id]
        description = req_data["description"]
        tests = req_data["tests"]

        if not tests:
            # No tests for this requirement
            rows.append([req_id, description, "No tests", "❌ UNCOVERED", "0"])
        else:
            # Add a row for each test
            for i, test in enumerate(tests):
                test_name = test["test"]
                outcome = test["outcome"]
                status = "✅ PASS" if outcome == "PASS" else "❌ FAIL"
                examples = test.get("hypothesis_examples", 1)
                examples_str = f"{examples:,}"

                # For first test of a requirement, show full req info
                if i == 0:
                    rows.append([req_id, description, test_name, status, examples_str])
                else:
                    # For subsequent tests, leave req columns empty for cleaner look
                    rows.append(["", "", test_name, status, examples_str])

    # Calculate column widths
    col1_width = max(len(row[0]) for row in rows) if rows else 10
    col2_width = max(len(row[1]) for row in rows) if rows else 40
    col3_width = max(len(row[2]) for row in rows) if rows else 50
    col4_width = 12
    col5_width = 10

    # Ensure minimum widths
    col1_width = max(col1_width, 10)
    col2_width = max(col2_width, 40)
    col3_width = max(col3_width, 50)

    # Print header
    print("\n" + "="*120)
    print("TEST COVERAGE TABLE")
    print("="*120)
    print(f"\nGenerated: {report['timestamp']}")
    summary = report['summary']
    print(f"Summary: {summary['verified']}/{summary['total']} requirements verified ({summary['verification_percent']}%)")
    total_scenarios = summary.get('total_test_scenarios', 0)
    if total_scenarios > 0:
        print(f"Total Test Scenarios: {total_scenarios:,} examples tested\n")
    else:
        print()

    # Print table header
    separator = f"+{'-'*(col1_width+2)}+{'-'*(col2_width+2)}+{'-'*(col3_width+2)}+{'-'*(col4_width+2)}+{'-'*(col5_width+2)}+"
    print(separator)
    print(f"| {'Requirement':<{col1_width}} | {'Description':<{col2_width}} | {'Test Case':<{col3_width}} | {'Status':<{col4_width}} | {'Examples':<{col5_width}} |")
    print(separator)

    # Print rows
    for row in rows:
        req_id, desc, test, status, examples = row
        print(f"| {req_id:<{col1_width}} | {desc:<{col2_width}} | {test:<{col3_width}} | {status:<{col4_width}} | {examples:<{col5_width}} |")

    print(separator)
    print()

    return True


if __name__ == "__main__":
    success = print_table()
    sys.exit(0 if success else 1)
