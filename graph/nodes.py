from agents.bug_agent import BugDetectionAgent
from agents.security_agent import SecurityAgent
from agents.performance_agent import PerformanceAgent
from agents.aggregator_agent import AggregatorAgent
from graph.state import ReviewState

# Lazy-load agents to allow Streamlit to read secrets first
_agents = {}

def _get_agents():
    """Lazy-load agents on first use"""
    global _agents
    if not _agents:
        _agents = {
            "bug": BugDetectionAgent(),
            "security": SecurityAgent(),
            "performance": PerformanceAgent(),
            "aggregator": AggregatorAgent(),
        }
    return _agents


def bug_node(state: ReviewState) -> ReviewState:
    agents = _get_agents()
    return {"bug_report": agents["bug"].review_code(state["code"])}


def security_node(state: ReviewState) -> ReviewState:
    agents = _get_agents()
    return {"security_report": agents["security"].review_code(state["code"])}


def performance_node(state: ReviewState) -> ReviewState:
    agents = _get_agents()
    return {"performance_report": agents["performance"].review_code(state["code"])}


def aggregator_node(state: ReviewState) -> ReviewState:
    agents = _get_agents()
    return {
        "final_review": agents["aggregator"].aggregate(
            bug_report=state.get("bug_report"),
            security_report=state.get("security_report"),
            performance_report=state.get("performance_report"),
        )
    }
