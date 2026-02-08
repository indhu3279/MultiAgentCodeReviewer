import json
from langchain_core.messages import SystemMessage, HumanMessage
from config.llm import get_llm

BUG_AGENT_SYSTEM_PROMPT = """
You are a senior software engineer performing a strict bug review.

Your task:
- Identify ONLY logical, runtime, or edge-case bugs.
- Do NOT comment on code style, performance, or security.
- Do NOT make assumptions beyond the given code.
- If no bugs are found, return an empty list.

For each bug, provide:
- A short description
- Severity: LOW, MEDIUM, or HIGH
- Line number if applicable, otherwise null
- A concrete fix suggestion

Return the response STRICTLY in the following JSON format:

{
  "bugs": [
    {
      "description": "string",
      "severity": "LOW | MEDIUM | HIGH",
      "line": number | null,
      "suggestion": "string"
    }
  ]
}
"""

class BugDetectionAgent:
    def __init__(self):
        self.llm = get_llm()

    def review_code(self, code: str) -> dict:
        messages = [
            SystemMessage(content=BUG_AGENT_SYSTEM_PROMPT),
            HumanMessage(content=f"Review the following code for bugs:\n\n{code}")
        ]

        response = self.llm.invoke(messages)

        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return {
                "bugs": [],
                "error": "Invalid JSON returned by LLM",
                "raw_response": response.content
            }
