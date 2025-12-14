#!/usr/bin/env python3
"""
Quick script to show uncovered features
"""
import json

def show_uncovered_features():
    with open("report.json", "r") as f:
        report = json.load(f)

    print("=" * 80)
    print("UNCOVERED FEATURES")
    print("=" * 80)
    print()

    uncovered_found = False

    for req_id, req_data in report["requirements"].items():
        if "features" not in req_data:
            continue

        uncovered_in_req = []
        for feat_id, feat_data in req_data["features"].items():
            if not feat_data["covered"]:
                uncovered_in_req.append((feat_id, feat_data["description"]))

        if uncovered_in_req:
            uncovered_found = True
            print(f"📋 {req_id}: {req_data['description']}")
            for feat_id, feat_desc in uncovered_in_req:
                print(f"   ❌ {feat_id}: {feat_desc}")
            print()

    if not uncovered_found:
        print("✅ All features are covered!")
        print()

    # Summary
    summary = report["summary"]
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Feature Coverage: {summary['features_verified']}/{summary['total_features']} verified ({summary['feature_coverage_percent']}%)")
    print(f"Missing: {summary['total_features'] - summary['features_verified']} features")
    print()

if __name__ == "__main__":
    show_uncovered_features()
