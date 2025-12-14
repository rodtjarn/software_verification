#!/usr/bin/env python3
"""
Simple script to view test coverage reports
"""
import os
import sys
import subprocess
import json
from pathlib import Path

REPORTS = {
    'json': 'report.json',
    'html': 'report.html',
    'md': 'report.md',
    'table': 'report_table.txt',
    'markdown': 'report.md',  # alias
}

DOCS = {
    'readme': 'README.md',
    'start': 'START_HERE.txt',
    'quick': 'QUICK_REFERENCE.md',
    'cheat': 'QUICK_REFERENCE.md',  # alias
    'complete': 'COMPLETE_README.md',
    'troubleshooting': 'TROUBLESHOOTING.md',
    'viewing': 'VIEWING_GUIDE.md',
    'view': 'VIEWING_GUIDE.md',  # alias
}

def has_bat():
    """Check if bat is available"""
    try:
        subprocess.run(['bat', '--version'], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False

def has_browser():
    """Check if xdg-open or open is available"""
    for cmd in ['xdg-open', 'open']:
        try:
            subprocess.run(['which', cmd], capture_output=True, check=True)
            return cmd
        except subprocess.CalledProcessError:
            continue
    return None

def view_with_bat(filepath):
    """View file with bat (syntax highlighting)"""
    subprocess.run(['bat', '--style=grid,numbers', '--paging=always', filepath])

def view_with_cat(filepath):
    """View file with cat"""
    subprocess.run(['cat', filepath])

def view_html(filepath):
    """Open HTML in browser"""
    browser_cmd = has_browser()
    if browser_cmd:
        subprocess.run([browser_cmd, filepath])
        print(f"\n✓ Opened {filepath} in browser")
    else:
        print(f"\n⚠️  No browser command found (xdg-open/open)")
        print(f"   Please open manually: file://{os.path.abspath(filepath)}")

def view_json_summary(filepath):
    """Show JSON summary"""
    with open(filepath) as f:
        data = json.load(f)

    summary = data.get('summary', {})
    print("\n" + "="*60)
    print("COVERAGE SUMMARY (from report.json)")
    print("="*60)
    print(f"\nRequirements:")
    print(f"  Total: {summary.get('total', 'N/A')}")
    print(f"  Covered: {summary.get('covered', 'N/A')}")
    print(f"  Verified: {summary.get('verified', 'N/A')}")
    print(f"  Coverage: {summary.get('coverage_percent', 'N/A')}%")
    print(f"  Verification: {summary.get('verification_percent', 'N/A')}%")

    print(f"\nFeatures:")
    print(f"  Total: {summary.get('total_features', 'N/A')}")
    print(f"  Covered: {summary.get('features_covered', 'N/A')}")
    print(f"  Verified: {summary.get('features_verified', 'N/A')}")
    print(f"  Coverage: {summary.get('feature_coverage_percent', 'N/A')}%")
    print(f"  Verification: {summary.get('feature_verification_percent', 'N/A')}%")

    print(f"\nTest Scenarios:")
    print(f"  Total scenarios tested: {summary.get('total_test_scenarios', 'N/A'):,}")
    print(f"  Total tests: {summary.get('total_tests', 'N/A')}")
    print("="*60)
    print("\nUse 'view_reports.py json --full' to see complete JSON")

def view_file(filepath, format_type=None):
    """View a file with appropriate viewer"""
    if not os.path.exists(filepath):
        print(f"✗ File not found: {filepath}")
        print(f"\n  Run tests first: python -m pytest simple_test.py -v")
        return False

    # Special handling for JSON summary
    if format_type == 'json' and '--full' not in sys.argv:
        view_json_summary(filepath)
        return True

    # Special handling for HTML
    if filepath.endswith('.html'):
        view_html(filepath)
        return True

    # Use bat if available, otherwise cat
    if has_bat():
        view_with_bat(filepath)
    else:
        view_with_cat(filepath)

    return True

def list_reports():
    """List available reports"""
    print("\n" + "="*60)
    print("AVAILABLE REPORTS")
    print("="*60)
    print("\nTest Coverage Reports:")
    for key, filename in REPORTS.items():
        if key in ['markdown']:  # Skip aliases
            continue
        exists = "✓" if os.path.exists(filename) else "✗"
        print(f"  {exists} {key:10} → {filename}")

    print("\nDocumentation:")
    for key, filename in DOCS.items():
        if key in ['cheat', 'view']:  # Skip aliases
            continue
        exists = "✓" if os.path.exists(filename) else "✗"
        print(f"  {exists} {key:15} → {filename}")

    print("\n" + "="*60)
    print("\nUsage:")
    print("  python view_reports.py <report>       # View a report")
    print("  python view_reports.py json           # View JSON summary")
    print("  python view_reports.py json --full    # View full JSON")
    print("  python view_reports.py html           # Open HTML in browser")
    print("  python view_reports.py md             # View markdown report")
    print("  python view_reports.py table          # View table report")
    print("\nDocumentation:")
    print("  python view_reports.py readme         # Complete guide")
    print("  python view_reports.py quick          # Quick reference")
    print("  python view_reports.py start          # 5-minute quick start")
    print("  python view_reports.py viewing        # This viewing guide")
    print("\nExamples:")
    print("  python view_reports.py table          # Quick coverage check")
    print("  python view_reports.py html           # Visual dashboard")
    print("  python view_reports.py json           # Summary stats")
    print("  python view_reports.py quick          # Decorator reference")
    print("="*60 + "\n")

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ['-h', '--help', 'help']:
        list_reports()
        return

    report_key = sys.argv[1].lower()

    # Check if it's a report
    if report_key in REPORTS:
        filepath = REPORTS[report_key]
        view_file(filepath, report_key)
    # Check if it's documentation
    elif report_key in DOCS:
        filepath = DOCS[report_key]
        view_file(filepath)
    # Try as direct filename
    elif os.path.exists(report_key):
        view_file(report_key)
    else:
        print(f"\n✗ Unknown report: {report_key}")
        print(f"\nAvailable reports: {', '.join(set(REPORTS.keys()) | set(DOCS.keys()))}")
        print(f"\nRun 'python view_reports.py' to see all options")

if __name__ == '__main__':
    main()
