#!/usr/bin/env python
"""
CI/CD Integration - Check verification percentage

Use this in your CI/CD pipeline to enforce quality gates.

Example usage:
    python check_coverage.py --min-verification 95
"""
import json
import sys
import argparse


def check_coverage(min_verification=95.0):
    """Check if verification meets minimum threshold"""
    
    # Read the JSON report
    try:
        with open("report.json") as f:
            report = json.load(f)
    except FileNotFoundError:
        print("❌ Error: report.json not found. Run tests first!")
        return False
    
    # Get metrics
    summary = report["summary"]
    total = summary["total"]
    verified = summary["verified"]
    verification_pct = summary["verification_percent"]
    
    print("\n" + "="*60)
    print("CI/CD QUALITY GATE CHECK")
    print("="*60)
    print(f"\nTotal Requirements: {total}")
    print(f"Verified: {verified}")
    print(f"Verification: {verification_pct}%")
    print(f"Minimum Required: {min_verification}%")
    
    # Check if we meet the threshold
    if verification_pct >= min_verification:
        print(f"\n✅ PASS - Verification {verification_pct}% >= {min_verification}%")
        print("Build can proceed!")
        return True
    else:
        print(f"\n❌ FAIL - Verification {verification_pct}% < {min_verification}%")
        
        # Show what's failing
        failing = []
        uncovered = []
        
        for req_id, req_data in report["requirements"].items():
            if not req_data["covered"]:
                uncovered.append(req_id)
            elif not req_data["verified"]:
                failing.append(req_id)
        
        if uncovered:
            print(f"\n❌ Uncovered requirements ({len(uncovered)}):")
            for req_id in uncovered:
                print(f"   {req_id}: {report['requirements'][req_id]['description']}")
        
        if failing:
            print(f"\n⚠️  Failing requirements ({len(failing)}):")
            for req_id in failing:
                print(f"   {req_id}: {report['requirements'][req_id]['description']}")
        
        print("\nBuild blocked! Fix tests before merging.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check test verification for CI/CD")
    parser.add_argument(
        "--min-verification",
        type=float,
        default=95.0,
        help="Minimum verification percentage required (default: 95.0)"
    )
    
    args = parser.parse_args()
    
    passed = check_coverage(args.min_verification)
    sys.exit(0 if passed else 1)
