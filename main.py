import json
from graph.workflow import build_review_graph

if __name__ == "__main__":
    code_sample = """
    @GetMapping("/user")
    public User getUser(@RequestParam String id) {
        return jdbcTemplate.queryForObject(
            "SELECT * FROM users WHERE id = '" + id + "'",
            User.class
        );
    }
    """

    graph = build_review_graph()

    initial_state = {
        "code": code_sample,
        "bug_report": None,
        "security_report": None,
        "performance_report": None,
        "final_review": None,
    }

    result = graph.invoke(initial_state)

    print("Final Review (LangGraph):")
    print(json.dumps(result["final_review"], indent=2))
