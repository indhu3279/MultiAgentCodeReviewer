from typing import TypedDict, Optional, Dict, Any

class ReviewState(TypedDict):
    code: str
    bug_report: Optional[Dict[str, Any]]
    security_report: Optional[Dict[str, Any]]
    performance_report: Optional[Dict[str, Any]]
    final_review: Optional[Dict[str, Any]]
