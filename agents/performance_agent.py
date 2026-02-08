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



PERFORMANCE_AGENT_SYSTEM_PROMPT = """
You are a senior performance engineer reviewing code for efficiency and scalability.

Your task:
- Identify ONLY performance or scalability issues.
- Focus on algorithmic complexity, inefficient loops, blocking calls,
  repeated expensive operations, memory usage, and database access patterns.
- Do NOT report logical bugs, security issues, or code style concerns.
- Do NOT speculate beyond the provided code.
- If no performance issues are found, return an empty list.

For each performance issue, provide:
- A short description
- Severity: LOW, MEDIUM, or HIGH
- Line number if applicable, otherwise null
- A concrete optimization recommendation

Return the response STRICTLY in the following JSON format:

{
  "issues": [
    {
      "description": "string",
      "severity": "LOW | MEDIUM | HIGH",
      "line": number | null,
      "recommendation": "string"
    }
  ]
}
"""


class PerformanceAgent:
    def __init__(self):
        self.llm = get_llm()

    def review_code(self, code: str) -> dict:
        messages = [
            SystemMessage(content=PERFORMANCE_AGENT_SYSTEM_PROMPT),
            HumanMessage(content=f"Review the following code for performance issues:\n\n{code}")
        ]

        response = self.llm.invoke(messages)

        try:
            clean_json = extract_json(response.content)
            return json.loads(clean_json)
        except json.JSONDecodeError:
            return {
                "issues": [],
                "error": "Invalid JSON returned by LLM",
                "raw_response": response.content
            }
