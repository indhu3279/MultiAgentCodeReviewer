from langgraph.graph import StateGraph, END
from graph.state import ReviewState
from graph.nodes import (
    bug_node,
    security_node,
    performance_node,
    aggregator_node,
)

def build_review_graph():
    graph = StateGraph(ReviewState)

    # A simple start node to seed the graph and branch to parallel reviewers.
    def start_node(state: ReviewState) -> ReviewState:
        return state


    # Nodes
    graph.add_node("start", start_node)
    graph.add_node("bug", bug_node)
    graph.add_node("security", security_node)
    graph.add_node("performance", performance_node)
    graph.add_node("aggregate", aggregator_node)

    # Parallel execution: start branches into reviewers
    graph.set_entry_point("start")
    graph.add_edge("start", "bug")
    graph.add_edge("start", "security")
    graph.add_edge("start", "performance")

    # Collect results into aggregator
    graph.add_edge("bug", "aggregate")
    graph.add_edge("security", "aggregate")
    graph.add_edge("performance", "aggregate")

    graph.add_edge("aggregate", END)

    return graph.compile()
