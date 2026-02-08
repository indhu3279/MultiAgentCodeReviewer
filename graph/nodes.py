from agents.bug_agent import BugDetectionAgent
from agents.security_agent import SecurityAgent
from agents.performance_agent import PerformanceAgent
from agents.aggregator_agent import AggregatorAgent
from graph.state import ReviewState


bug_agent = BugDetectionAgent()
security_agent = SecurityAgent()
performance_agent = PerformanceAgent()
aggregator_agent = AggregatorAgent()


def bug_node(state: ReviewState) -> ReviewState:
    return {"bug_report": bug_agent.review_code(state["code"])}


def security_node(state: ReviewState) -> ReviewState:
    return {"security_report": security_agent.review_code(state["code"])}


def performance_node(state: ReviewState) -> ReviewState:
    return {"performance_report": performance_agent.review_code(state["code"])}


def aggregator_node(state: ReviewState) -> ReviewState:
    return {
        "final_review": aggregator_agent.aggregate(
            bug_report=state.get("bug_report"),
            security_report=state.get("security_report"),
            performance_report=state.get("performance_report"),
        )
    }
