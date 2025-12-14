"""
Simple Requirements for String Reversal
"""


def get_all_features():
    """Get flat list of all features across all requirements"""
    all_features = {}
    for req_id, req_data in REQUIREMENTS.items():
        if 'features' in req_data:
            for feat_id, feat_desc in req_data['features'].items():
                all_features[feat_id] = {
                    'description': feat_desc,
                    'requirement': req_id
                }
    return all_features


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
    },
    "REQ-2": {
        "description": "reversing twice returns the original string",
        "priority": "high",
        "features": {
            "F2.1": "idempotency with ASCII strings",
            "F2.2": "idempotency with Unicode strings",
            "F2.3": "idempotency with mixed content"
        }
    },
    "REQ-3": {
        "description": "reverse_string handles empty strings",
        "priority": "medium",
        "features": {
            "F3.1": "empty string returns empty string"
        }
    },
    "REQ-4": {
        "description": "reverse_string preserves string length",
        "priority": "high",
        "features": {
            "F4.1": "length preserved for ASCII",
            "F4.2": "length preserved for Unicode",
            "F4.3": "length preserved for empty strings"
        }
    }
}
