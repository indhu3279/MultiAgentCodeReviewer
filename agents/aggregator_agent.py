import json
import re
from langchain_core.messages import SystemMessage, HumanMessage
from config.llm import get_llm


def extract_json(text: str) -> str:
    """
    Robustly extract the first JSON object from an LLM response.
    """
    # Remove markdown fences
    text = re.sub(r"```(?:json)?", "", text)
    text = text.replace("```", "").strip()

    # Find first '{' and last '}'
    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1:
        raise ValueError("No JSON object found in response")

    return text[start:end + 1]



AGGREGATOR_SYSTEM_PROMPT = """
You are a senior technical lead aggregating code review feedback.

Your task:
- Combine findings from bug, security, and performance reviews.
- Do NOT introduce new issues.
- Deduplicate overlapping findings.
- Prioritize issues using the following order:
  1. Security
  2. Bugs
  3. Performance
- Within each category, order by severity: HIGH, MEDIUM, LOW.
- Be concise, clear, and actionable.

Return the final review STRICTLY in the following JSON format:

{
  "summary": "Brief overall assessment",
  "issues": [
    {
      "category": "SECURITY | BUG | PERFORMANCE",
      "severity": "HIGH | MEDIUM | LOW",
      "description": "string",
      "recommendation": "string"
    }
  ]
}
"""


class AggregatorAgent:
    def __init__(self):
        self.llm = get_llm()

    def aggregate(
        self,
        bug_report: dict,
        security_report: dict,
        performance_report: dict
    ) -> dict:
        messages = [
            SystemMessage(content=AGGREGATOR_SYSTEM_PROMPT),
            HumanMessage(
                content=f"""
Bug Review:
{json.dumps(bug_report, indent=2)}

Security Review:
{json.dumps(security_report, indent=2)}

Performance Review:
{json.dumps(performance_report, indent=2)}
"""
            )
        ]

        response = self.llm.invoke(messages)

        try:
            clean_json = extract_json(response.content)
            return json.loads(clean_json)
        except json.JSONDecodeError:
            return {
                "summary": "Aggregation failed due to invalid LLM response",
                "issues": [],
                "raw_response": response.content
            }
