"""
Simple report generation - JSON, HTML, and Markdown
"""
import json
from datetime import datetime
from simple_spec import REQUIREMENTS


def generate_reports(coverage_data):
    """Generate all three report formats"""
    generate_json(coverage_data)
    generate_html(coverage_data)
    generate_markdown(coverage_data)


def generate_json(coverage_data):
    """JSON report for CI/CD"""
    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values() 
                   if tests and all(t['outcome'] == 'PASS' for t in tests))
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "summary": {
            "total": total,
            "covered": covered,
            "verified": verified,
            "coverage_percent": round(covered / total * 100, 1),
            "verification_percent": round(verified / total * 100, 1)
        },
        "requirements": {}
    }
    
    for req_id, req_spec in REQUIREMENTS.items():
        tests = coverage_data.get(req_id, [])
        all_pass = all(t['outcome'] == 'PASS' for t in tests) if tests else False
        
        report["requirements"][req_id] = {
            "description": req_spec["description"],
            "priority": req_spec["priority"],
            "covered": len(tests) > 0,
            "verified": len(tests) > 0 and all_pass,
            "tests": tests
        }
    
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✓ report.json created")


def generate_html(coverage_data):
    """HTML report for humans"""
    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values() 
                   if tests and all(t['outcome'] == 'PASS' for t in tests))
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; background: #f5f5f5; }}
        .container {{ max-width: 900px; margin: 0 auto; background: white; padding: 30px; 
                     box-shadow: 0 2px 8px rgba(0,0,0,0.1); border-radius: 8px; }}
        h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; }}
        .summary {{ background: #ecf0f1; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .stat {{ display: inline-block; margin: 10px 20px; }}
        .stat-value {{ font-size: 32px; font-weight: bold; color: #27ae60; }}
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
        </div>
        
        <h2>Requirements</h2>
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
        
        if tests:
            for test in tests:
                symbol = "✓" if test['outcome'] == 'PASS' else "✗"
                css_class = "pass" if test['outcome'] == 'PASS' else "fail"
                html += f"<div class='test {css_class}'>{symbol} {test['test']}</div>"
                
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


def generate_markdown(coverage_data):
    """Markdown report for documentation"""
    total = len(REQUIREMENTS)
    covered = sum(1 for tests in coverage_data.values() if tests)
    verified = sum(1 for tests in coverage_data.values() 
                   if tests and all(t['outcome'] == 'PASS' for t in tests))
    
    md = f"""# Test Coverage Report

Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## Summary

- **Total Requirements:** {total}
- **Covered:** {covered} ({round(covered/total*100, 1)}%)
- **Verified:** {verified} ({round(verified/total*100, 1)}%)

## Requirements

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
        
        if tests:
            md += "**Tests:**\n"
            for test in tests:
                symbol = "✓" if test['outcome'] == 'PASS' else "✗"
                md += f"- {symbol} `{test['test']}`\n"
                
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
