"""
Simple report generation - JSON, HTML, and Markdown
"""
import json
from datetime import datetime
from simple_spec import REQUIREMENTS


def generate_reports(coverage_data, feature_coverage_data=None):
    """Generate all report formats"""
    if feature_coverage_data is None:
        feature_coverage_data = {}
    generate_json(coverage_data, feature_coverage_data)
    generate_html(coverage_data, feature_coverage_data)
    generate_markdown(coverage_data, feature_coverage_data)
    generate_table(coverage_data, feature_coverage_data)


def generate_json(coverage_data, feature_coverage_data=None):
    """JSON report for CI/CD"""
    if feature_coverage_data is None:
        feature_coverage_data = {}

    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values()
                   if tests and all(t['outcome'] == 'PASS' for t in tests))

    # Calculate total examples tested
    total_examples = 0
    total_tests = 0
    for tests in coverage_data.values():
        for test in tests:
            total_tests += 1
            total_examples += test.get('hypothesis_examples', 1)

    # Calculate feature coverage
    from simple_spec import get_all_features
    all_features = get_all_features()
    total_features = len(all_features)
    covered_features = len(feature_coverage_data)
    verified_features = sum(1 for tests in feature_coverage_data.values()
                           if tests and all(t['outcome'] == 'PASS' for t in tests))

    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total,
            "covered": covered,
            "verified": verified,
            "coverage_percent": round(covered / total * 100, 1),
            "verification_percent": round(verified / total * 100, 1),
            "total_test_scenarios": total_examples,
            "total_tests": total_tests,
            "total_features": total_features,
            "features_covered": covered_features,
            "features_verified": verified_features,
            "feature_coverage_percent": round(covered_features / total_features * 100, 1) if total_features > 0 else 0,
            "feature_verification_percent": round(verified_features / total_features * 100, 1) if total_features > 0 else 0
        },
        "requirements": {},
        "feature_coverage": feature_coverage_data
    }
    
    for req_id, req_spec in REQUIREMENTS.items():
        tests = coverage_data.get(req_id, [])
        all_pass = all(t['outcome'] == 'PASS' for t in tests) if tests else False

        req_report = {
            "description": req_spec["description"],
            "priority": req_spec["priority"],
            "covered": len(tests) > 0,
            "verified": len(tests) > 0 and all_pass,
            "tests": tests
        }

        # Add feature coverage for this requirement
        if 'features' in req_spec:
            req_features = req_spec['features']
            feature_details = {}

            for feat_id, feat_desc in req_features.items():
                if feat_id in feature_coverage_data:
                    feat_tests = feature_coverage_data[feat_id]
                    all_pass_feat = all(t['outcome'] == 'PASS' for t in feat_tests)
                    total_examples = sum(t.get('examples', 1) for t in feat_tests)
                    feature_details[feat_id] = {
                        "description": feat_desc,
                        "covered": True,
                        "verified": all_pass_feat,
                        "examples": total_examples
                    }
                else:
                    feature_details[feat_id] = {
                        "description": feat_desc,
                        "covered": False,
                        "verified": False,
                        "examples": 0
                    }

            req_report["features"] = feature_details

        report["requirements"][req_id] = req_report
    
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✓ report.json created")


def generate_html(coverage_data, feature_coverage_data=None):
    """HTML report for humans"""
    if feature_coverage_data is None:
        feature_coverage_data = {}

    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values()
                   if tests and all(t['outcome'] == 'PASS' for t in tests))

    # Calculate total examples tested
    total_examples = 0
    for tests in coverage_data.values():
        for test in tests:
            total_examples += test.get('hypothesis_examples', 1)

    # Calculate feature coverage
    from simple_spec import get_all_features
    all_features = get_all_features()
    total_features = len(all_features)
    covered_features = len(feature_coverage_data)
    verified_features = sum(1 for tests in feature_coverage_data.values()
                           if tests and all(t['outcome'] == 'PASS' for t in tests))
    feature_pct = round(verified_features / total_features * 100, 1) if total_features > 0 else 0

    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 30px;
                     box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .stat {{ display: inline-block; margin: 10px 20px; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #27ae60; }}
        .coverage-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 14px; }}
        .coverage-table th {{ background: #34495e; color: white; padding: 12px; text-align: left; }}
        .coverage-table td {{ padding: 10px; border-bottom: 1px solid #ddd; }}
        .coverage-table tr:hover {{ background: #f5f5f5; }}
        .coverage-table .req-cell {{ font-weight: bold; color: #2c3e50; }}
        .coverage-table .test-cell {{ font-family: monospace; font-size: 12px; }}
        .req {{ border-left: 4px solid #95a5a6; padding: 15px; margin: 15px 0;
               background: #f8f9fa; border-radius: 4px; }}
        .req.verified {{ border-left-color: #27ae60; background: #d5f4e6; }}
        .req.failing {{ border-left-color: #e74c3c; background: #fadbd8; }}
        .req.uncovered {{ border-left-color: #e67e22; background: #fdebd0; }}
        .test {{ margin: 8px 0 8px 20px; font-family: monospace; font-size: 14px; }}
        .pass {{ color: #27ae60; }}
        .fail {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📊 Test Coverage Report</h1>
        <p style="color: #7f8c8d;">Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>

        <div class="summary">
            <div class="stat">
                <div>Total Requirements</div>
                <div class="stat-value">{total}</div>
            </div>
            <div class="stat">
                <div>Verified</div>
                <div class="stat-value" style="color: #27ae60;">{verified}</div>
            </div>
            <div class="stat">
                <div>Coverage</div>
                <div class="stat-value">{round(covered/total*100)}%</div>
            </div>
            <div class="stat">
                <div>Test Scenarios</div>
                <div class="stat-value" style="color: #3498db;">{total_examples:,}</div>
            </div>
            <div class="stat">
                <div>Feature Coverage</div>
                <div class="stat-value" style="color: #9b59b6;">{feature_pct}%</div>
            </div>
        </div>

        <h2>Coverage Table</h2>
        <table class="coverage-table">
            <thead>
                <tr>
                    <th>Requirement</th>
                    <th>Description</th>
                    <th>Test Case</th>
                    <th>Status</th>
                    <th style="text-align: right;">Examples</th>
                </tr>
            </thead>
            <tbody>
"""

    # Add table rows to HTML
    for req_id in sorted(REQUIREMENTS.keys()):
        tests = coverage_data.get(req_id, [])
        req = REQUIREMENTS[req_id]

        if not tests:
            html += f"""
                <tr>
                    <td class="req-cell">{req_id}</td>
                    <td>{req['description']}</td>
                    <td class="test-cell">No tests</td>
                    <td>❌ UNCOVERED</td>
                    <td style="text-align: right;">0</td>
                </tr>"""
        else:
            for i, test in enumerate(tests):
                examples = test.get('hypothesis_examples', 1)
                status = '✅ PASS' if test['outcome'] == 'PASS' else '❌ FAIL'
                html += f"""
                <tr>
                    <td class="req-cell">{req_id if i == 0 else ''}</td>
                    <td>{req['description'] if i == 0 else ''}</td>
                    <td class="test-cell">{test['test']}</td>
                    <td>{status}</td>
                    <td style="text-align: right;">{examples:,}</td>
                </tr>"""

    html += """
            </tbody>
        </table>

        <h2>Detailed Requirements</h2>
"""
    
    for req_id in sorted(REQUIREMENTS.keys()):
        req = REQUIREMENTS[req_id]
        tests = coverage_data.get(req_id, [])
        
        if not tests:
            status = "uncovered"
            icon = "❌"
        elif all(t['outcome'] == 'PASS' for t in tests):
            status = "verified"
            icon = "✅"
        else:
            status = "failing"
            icon = "⚠️"
        
        html += f"""
        <div class="req {status}">
            <div style="font-weight: bold; margin-bottom: 8px;">
                {icon} {req_id}: {req["description"]}
                <span style="background: #95a5a6; color: white; padding: 2px 8px;
                      border-radius: 3px; font-size: 12px; margin-left: 10px;">
                    {req["priority"]}
                </span>
            </div>
"""

        # Add feature coverage for this requirement
        if 'features' in req:
            req_features = req['features']
            covered_count = sum(1 for feat_id in req_features.keys() if feat_id in feature_coverage_data)
            verified_count = sum(1 for feat_id in req_features.keys()
                                if feat_id in feature_coverage_data
                                and all(t['outcome'] == 'PASS' for t in feature_coverage_data[feat_id]))
            pct = round(verified_count/len(req_features)*100, 1) if req_features else 0

            html += f"<div style='margin: 10px 0; font-size: 14px;'><strong>Features:</strong> {verified_count}/{len(req_features)} verified ({pct}%)</div>"
            html += "<ul style='margin: 5px 0; font-size: 13px;'>"

            for feat_id, feat_desc in sorted(req_features.items()):
                if feat_id in feature_coverage_data:
                    feat_tests = feature_coverage_data[feat_id]
                    all_pass = all(t['outcome'] == 'PASS' for t in feat_tests)
                    total_examples = sum(t.get('examples', 1) for t in feat_tests)
                    symbol = "✓" if all_pass else "✗"
                    color = "#27ae60" if all_pass else "#e74c3c"
                    html += f"<li style='color: {color};'>{symbol} <strong>{feat_id}:</strong> {feat_desc} ({total_examples:,} examples)</li>"
                else:
                    html += f"<li style='color: #e74c3c;'>✗ <strong>{feat_id}:</strong> {feat_desc} (❌ NOT TESTED)</li>"

            html += "</ul>"

        if tests:
            html += "<div style='margin-top: 10px;'><strong>Tests:</strong></div>"
            for test in tests:
                symbol = "✓" if test['outcome'] == 'PASS' else "✗"
                css_class = "pass" if test['outcome'] == 'PASS' else "fail"
                examples = test.get('hypothesis_examples', 1)
                examples_text = f" ({examples:,} scenarios)" if examples > 1 else ""
                html += f"<div class='test {css_class}'>{symbol} {test['test']}{examples_text}</div>"

                # Show failure details in structured format
                if test['outcome'] == 'FAIL' and 'failure' in test:
                    failure = test['failure']
                    html += f"<div style='margin-left: 40px; padding: 15px; background: #fff5f5; "
                    html += f"border-left: 3px solid #e74c3c; margin-top: 5px; font-size: 13px; "
                    html += f"border-radius: 4px;'>"
                    html += f"<div style='margin-bottom: 8px;'><strong style='color: #e74c3c;'>❌ Test Failure</strong></div>"
                    html += f"<div style='margin: 5px 0;'><strong>Stimuli (Input):</strong> <code>{failure['stimuli']}</code></div>"
                    html += f"<div style='margin: 5px 0;'><strong>Response (Actual output):</strong> <code>{failure['response']}</code></div>"
                    html += f"<div style='margin: 5px 0;'><strong>Expected (Test expects):</strong> <code>{failure['expected']}</code></div>"
                    html += f"<div style='margin: 5px 0;'><strong>Error Type:</strong> <code>{failure['error_type']}</code></div>"
                    html += "</div>"
        else:
            html += "<div style='color: #e74c3c; margin-top: 8px;'>No tests</div>"

        html += "</div>"
    
    html += """
    </div>
</body>
</html>
"""
    
    with open("report.html", "w") as f:
        f.write(html)
    
    print("✓ report.html created")


def generate_markdown(coverage_data, feature_coverage_data=None):
    """Markdown report for documentation"""
    if feature_coverage_data is None:
        feature_coverage_data = {}

    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values()
                   if tests and all(t['outcome'] == 'PASS' for t in tests))

    # Calculate total examples tested
    total_examples = 0
    for tests in coverage_data.values():
        for test in tests:
            total_examples += test.get('hypothesis_examples', 1)

    # Calculate feature coverage
    from simple_spec import get_all_features
    all_features = get_all_features()
    total_features = len(all_features)
    covered_features = len(feature_coverage_data)
    verified_features = sum(1 for tests in feature_coverage_data.values()
                           if tests and all(t['outcome'] == 'PASS' for t in tests))
    feature_pct = round(verified_features / total_features * 100, 1) if total_features > 0 else 0

    md = f"""# Test Coverage Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Total Requirements:** {total}
- **Covered:** {covered} ({round(covered/total*100, 1)}%)
- **Verified:** {verified} ({round(verified/total*100, 1)}%)
- **Test Scenarios:** {total_examples:,} examples tested
- **Feature Coverage:** {verified_features}/{total_features} features verified ({feature_pct}%)

## Coverage Table

| Requirement | Description | Test Case | Status | Examples |
|-------------|-------------|-----------|--------|----------|
"""

    # Add table rows to markdown
    for req_id in sorted(REQUIREMENTS.keys()):
        tests = coverage_data.get(req_id, [])
        req = REQUIREMENTS[req_id]

        if not tests:
            md += f"| {req_id} | {req['description']} | No tests | ❌ UNCOVERED | 0 |\n"
        else:
            for i, test in enumerate(tests):
                examples = test.get('hypothesis_examples', 1)
                status = '✅ PASS' if test['outcome'] == 'PASS' else '❌ FAIL'
                req_cell = req_id if i == 0 else ''
                desc_cell = req['description'] if i == 0 else ''
                md += f"| {req_cell} | {desc_cell} | `{test['test']}` | {status} | {examples:,} |\n"

    md += """
## Detailed Requirements

"""

    for req_id in sorted(REQUIREMENTS.keys()):
        req = REQUIREMENTS[req_id]
        tests = coverage_data.get(req_id, [])

        if not tests:
            icon = "❌"
        elif all(t['outcome'] == 'PASS' for t in tests):
            icon = "✅"
        else:
            icon = "⚠️"

        md += f"\n### {icon} {req_id}: {req['description']}\n\n"
        md += f"**Priority:** {req['priority']}\n\n"

        # Add feature coverage for this requirement
        if 'features' in req:
            req_features = req['features']
            covered_count = sum(1 for feat_id in req_features.keys() if feat_id in feature_coverage_data)
            verified_count = sum(1 for feat_id in req_features.keys()
                                if feat_id in feature_coverage_data
                                and all(t['outcome'] == 'PASS' for t in feature_coverage_data[feat_id]))
            pct = round(verified_count/len(req_features)*100, 1) if req_features else 0

            md += f"**Features:** {verified_count}/{len(req_features)} verified ({pct}%)\n\n"

            for feat_id, feat_desc in sorted(req_features.items()):
                if feat_id in feature_coverage_data:
                    feat_tests = feature_coverage_data[feat_id]
                    all_pass = all(t['outcome'] == 'PASS' for t in feat_tests)
                    total_examples = sum(t.get('examples', 1) for t in feat_tests)
                    symbol = "✓" if all_pass else "✗"
                    md += f"- {symbol} **{feat_id}:** {feat_desc} ({total_examples:,} examples)\n"
                else:
                    md += f"- ✗ **{feat_id}:** {feat_desc} (❌ NOT TESTED)\n"

            md += "\n"

        if tests:
            md += "**Tests:**\n"
            for test in tests:
                symbol = "✓" if test['outcome'] == 'PASS' else "✗"
                examples = test.get('hypothesis_examples', 1)
                examples_text = f" ({examples:,} scenarios)" if examples > 1 else ""
                md += f"- {symbol} `{test['test']}`{examples_text}\n"

                # Show failure details
                if test['outcome'] == 'FAIL' and 'failure' in test:
                    failure = test['failure']
                    md += f"  - **Stimuli (Input):** `{failure['stimuli']}`\n"
                    md += f"  - **Response (Actual output):** `{failure['response']}`\n"
                    md += f"  - **Expected (Test expects):** `{failure['expected']}`\n"
                    md += f"  - **Error Type:** `{failure['error_type']}`\n"
        else:
            md += "*No tests*\n"

        md += "\n"
    
    with open("report.md", "w") as f:
        f.write(md)

    print("✓ report.md created")


def generate_table(coverage_data, feature_coverage_data=None):
    """Table report for terminal viewing"""
    if feature_coverage_data is None:
        feature_coverage_data = {}

    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values()
                   if tests and all(t['outcome'] == 'PASS' for t in tests))

    # Calculate total examples tested
    total_examples = 0
    total_tests = 0
    for tests in coverage_data.values():
        for test in tests:
            total_tests += 1
            total_examples += test.get('hypothesis_examples', 1)

    # Calculate feature coverage
    from simple_spec import get_all_features
    all_features = get_all_features()
    total_features = len(all_features)
    verified_features = sum(1 for tests in feature_coverage_data.values()
                           if tests and all(t['outcome'] == 'PASS' for t in tests))
    feature_pct = round(verified_features / total_features * 100, 1) if total_features > 0 else 0

    # Prepare table data
    rows = []
    for req_id in sorted(REQUIREMENTS.keys()):
        tests = coverage_data.get(req_id, [])
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

    # Build table as string
    output = []
    output.append("")
    output.append("="*120)
    output.append("TEST COVERAGE TABLE")
    output.append("="*120)
    output.append("")
    output.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    output.append(f"Summary: {verified}/{total} requirements verified ({round(verified/total*100, 1)}%)")
    output.append(f"Total Test Scenarios: {total_examples:,} examples across {total_tests} tests")
    output.append(f"Feature Coverage: {verified_features}/{total_features} features verified ({feature_pct}%)")
    output.append("")

    # Table header
    separator = f"+{'-'*(col1_width+2)}+{'-'*(col2_width+2)}+{'-'*(col3_width+2)}+{'-'*(col4_width+2)}+{'-'*(col5_width+2)}+"
    output.append(separator)
    output.append(f"| {'Requirement':<{col1_width}} | {'Description':<{col2_width}} | {'Test Case':<{col3_width}} | {'Status':<{col4_width}} | {'Examples':<{col5_width}} |")
    output.append(separator)

    # Table rows
    for row in rows:
        req_id, desc, test, status, examples = row
        output.append(f"| {req_id:<{col1_width}} | {desc:<{col2_width}} | {test:<{col3_width}} | {status:<{col4_width}} | {examples:<{col5_width}} |")

    output.append(separator)
    output.append("")

    # Add feature coverage details
    output.append("="*120)
    output.append("FEATURE COVERAGE DETAILS")
    output.append("="*120)
    output.append("")

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
        output.append(f"{req_id}: {req['description']}")
        output.append(f"  Features: {verified_count}/{len(req_features)} verified ({pct}%)")
        output.append("")

        for feat_id, feat_desc in sorted(req_features.items()):
            if feat_id in feature_coverage_data:
                tests = feature_coverage_data[feat_id]
                all_pass = all(t['outcome'] == 'PASS' for t in tests)
                total_examples = sum(t.get('examples', 1) for t in tests)
                symbol = "✓" if all_pass else "✗"
                output.append(f"    {symbol} {feat_id}: {feat_desc} ({total_examples:,} examples)")
            else:
                output.append(f"    ✗ {feat_id}: {feat_desc} (❌ NOT TESTED)")

        output.append("")

    # Write to file
    with open("report_table.txt", "w") as f:
        f.write("\n".join(output))

    print("✓ report_table.txt created")
