# 🤖 Multi-Agent Code Reviewer

**An intelligent, automated code review system powered by multi-agent AI architecture.** This project uses specialized LLM-based agents to review code for bugs, security vulnerabilities, and performance issues, providing comprehensive feedback in a single unified report.

---

## 🎯 Overview

The Multi-Agent Code Reviewer is a distributed code analysis system that orchestrates multiple specialized agents to perform thorough code reviews:

- **🐛 Bug Agent**: Identifies logical errors, runtime issues, and edge-case bugs
- **🔒 Security Agent**: Detects security vulnerabilities (SQL injection, XSS, auth issues, etc.)
- **⚡ Performance Agent**: Finds optimization opportunities and performance bottlenecks
- **📊 Aggregator Agent**: Synthesizes all reports into a prioritized, actionable final review

The system supports both **direct code submissions** and **GitHub Pull Request reviews**, with an intuitive **Streamlit web UI** and a **CLI interface**.

---

## 🏗️ Core Technologies

### **LangChain / LangChain-Core**
- Framework for building LLM-powered applications
- Handles message formatting, prompt chaining, and response parsing
- Abstracts LLM provider details for seamless integration

### **LangGraph**
- **State orchestration engine** for multi-step workflows
- Defines nodes (agents) and edges (state transitions)
- Enables parallel and sequential execution of review agents
- Fault-tolerant graph execution with retry logic

### **Groq LLM API (langchain-groq)**
- High-speed LLM provider with competitive pricing
- Used for all agent reasoning and code analysis
- Supports complex prompt engineering for specialized reviews

### **Streamlit**
- React-like web framework for Python
- Provides interactive UI for both direct code and GitHub PR reviews
- Manages session state and real-time feedback

### **GitHub API**
- Fetches PR metadata and diffs
- Enables automated review comments on pull requests
- Secure token-based authentication

---

## 🔄 Workflow Architecture

### **Phase 1: Code Extraction**
```
User Input (Direct Code / GitHub PR)
         ↓
   Extract Code
         ↓
   State Initialization
```

### **Phase 2: Multi-Agent Review (LangGraph Workflow)**
```
Initial State
     ↓
 ┌──────────────────────────────────────────┐
 │  Parallel Agent Execution                │
 ├──────────────────────────────────────────┤
 │  Bug Agent ────→ Bug Report              │
 │  Security Agent → Security Report        │
 │  Performance Agent → Performance Report  │
 └──────────────────────────────────────────┘
     ↓
 State Aggregation
     ↓
 Aggregator Agent
     ↓
 Final Review Report
```

### **Phase 3: Output & Action**
```
Final Report
     ↓
┌─────────────────────────────────────────┐
│ Option A: Display in Web UI             │
│ Option B: Post as GitHub PR Comment     │
│ Option C: Export as JSON                │
└─────────────────────────────────────────┘
```

### **Agent Responsibilities**

| Agent | Input | Output | Focus |
|-------|-------|--------|-------|
| **Bug Agent** | Raw code | Bug list (desc, severity, line, fix) | Logic errors, runtime issues |
| **Security Agent** | Raw code | Vulnerability list with remediation | Auth, injection, XSS, encryption |
| **Performance Agent** | Raw code | Bottleneck list with optimization tips | Complexity, memory, concurrency |
| **Aggregator Agent** | All reports | Unified JSON with summary & severity sort | Prioritization, deduplication |

-

## 🚀 Installation & Setup

### **1. Clone & Install Dependencies**

```bash
cd c:\Users\indhu\projects\MultiAgentCodeReviewer
pip install -r requirements.txt
```

### **2. Get API Keys**

#### **Groq API Key**
1. Go to https://console.groq.com
2. Sign up / login
3. Create API key in Developer section
4. Copy key (starts with `sk-`)

#### **GitHub Personal Access Token** (optional, for PR reviews)
1. Go to https://github.com/settings/tokens
2. Click "Generate new token (classic)"
3. Select scopes: `repo` (full control of repositories)
4. Copy token (starts with `ghp_`)

### **3. Configure Environment**

Create `.env` in project root:

```env
GROQ_API_KEY=sk-...your-groq-key...
GITHUB_TOKEN=ghp_...your-github-token...
```

**Important:** Add `.env` to `.gitignore` to never commit secrets.

### **4. Verify Setup**

```bash
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('GROQ', os.getenv('GROQ_API_KEY') is not None); print('GITHUB', os.getenv('GITHUB_TOKEN') is not None)"
```

---

## 🔗 How It Works: Deep Dive

### **1. State Management (LangGraph)**
The workflow maintains a **shared state** across all agents:

```python
{
    "code": "function code being reviewed",
    "bug_report": {...},
    "security_report": {...},
    "performance_report": {...},
    "final_review": {...}
}
```

Each agent reads the initial state, adds its findings, and passes the updated state forward.

### **2. Parallel Execution**
Bug, Security, and Performance agents run in **parallel** for speed:
- No dependencies between them
- Results merged in aggregator stage
- Typical runtime: 5-15 seconds for 50-200 lines of code

### **3. Agent Prompting**
Each agent uses a **specialized system prompt**:
- Bug Agent: "Identify ONLY logical and runtime bugs..."
- Security Agent: "Find authentication, injection, XSS vulnerabilities..."
- Performance Agent: "Analyze complexity, memory usage, concurrency..."

This specialization prevents hallucination and keeps reviews focused.

### **4. JSON Parsing**
Agents return **strict JSON format** to ensure structured output:
```python
response = json.loads(llm_response.content)
# Always has predictable structure for downstream processing
```

## 📊 Performance Metrics

| Metric | Typical Value |
|--------|---------------|
| **Single Agent Review** | 2-4 seconds |
| **All 3 Agents (Parallel)** | 4-6 seconds |
| **Aggregation** | 1-2 seconds |
| **Total E2E** | ~10 seconds |
| **Max Code Size** | 10,000 lines (per agent) |

---


**Happy Code Reviewing! 🚀**
