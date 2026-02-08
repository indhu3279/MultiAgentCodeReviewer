# 🤖 Multi-Agent Code Reviewer - Streamlit UI

A comprehensive web-based UI for the Multi-Agent Code Reviewer, built with Streamlit.

## Features

### 📝 Direct Code Review
- Paste code directly into the web interface
- Quick code templates for Python and Java examples
- Real-time review processing with progress indicators

### 🔗 GitHub PR Review
- Review pull requests directly from GitHub
- Automatic code extraction from PR diffs
- Token-based authentication for secure access

### 📊 Comprehensive Analysis
- **🐛 Bug Detection**: Identifies logic errors and potential bugs
- **🔒 Security Analysis**: Detects security vulnerabilities
- **⚡ Performance Review**: Finds optimization opportunities
- **📋 Aggregated Report**: Combined findings with prioritization

### 🎨 User-Friendly Interface
- Color-coded severity indicators (🔴 High, 🟠 Medium, 🟡 Low)
- Categorized issue display with expandable details
- Issue statistics and summaries
- Multiple view options (Code, Reports, Raw JSON)

### ⬇️ Export Capabilities
- Download review reports as JSON
- Easy sharing and integration with other tools

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`:
```
GITHUB_TOKEN=your_github_token_here
GROQ_API_KEY=your_groq_api_key_here
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your default browser at `http://localhost:8501`

## Usage

### Direct Code Review
1. Select "📝 Direct Code" mode from the sidebar
2. Paste your code in the text area
3. (Optional) Use template buttons for quick examples
4. Click "🚀 Start Review"
5. View results and download the report

### GitHub PR Review
1. Select "🔗 GitHub PR" mode from the sidebar
2. Enter repository owner, name, and PR number
3. Provide your GitHub personal access token
4. Click "📥 Fetch & Review PR"
5. View results and download the report

## Review Results

### Summary
- Brief overall assessment of the code

### Issues
Organized by category:
- **🔒 Security Issues**: SQL Injection, XSS, auth vulnerabilities, etc.
- **🐛 Bug Issues**: Logic errors, null pointer exceptions, etc.
- **⚡ Performance Issues**: Algorithm complexity, memory leaks, etc.

Each issue includes:
- Severity level (HIGH/MEDIUM/LOW)
- Detailed description
- Actionable recommendations

### Statistics
- High severity count
- Medium severity count
- Low severity count
- Total issues found

### Detailed Reports
- View full code being reviewed
- Access complete final report
- Inspect individual agent reports
- Export results as JSON

## Creating a GitHub Personal Access Token

1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token"
3. Select scopes: `repo` (full control of private repositories)
4. Copy the token and use it in the app

## Project Structure

```
MultiAgentCodeReviewer/
├── app.py                 # Streamlit UI (NEW)
├── main.py               # Main entry point with example
├── review_pr.py          # GitHub PR review logic
├── requirements.txt      # Dependencies
├── agents/
│   ├── bug_agent.py
│   ├── security_agent.py
│   ├── performance_agent.py
│   └── aggregator_agent.py
├── graph/
│   ├── workflow.py       # LangGraph workflow
│   ├── state.py          # State definitions
│   └── nodes.py          # Graph nodes
├── github_int/
│   ├── client.py         # GitHub API client
│   └── utils.py          # Utility functions
└── config/
    └── llm.py            # LLM configuration
```

## Tips

- Use the sidebar templates for quick testing
- GitHub review works with both public and private repos (with token)
- Review results are cached in session state
- Download reports for documentation and tracking

## Troubleshooting

### "GITHUB_TOKEN not set in environment"
- Ensure your `.env` file is in the project root
- Set the `GITHUB_TOKEN` variable in your `.env` file

### "No code diff found in PR"
- Verify the PR number is correct
- Check that the PR has actual code changes
- Ensure your token has repository access

### "LLM response error"
- Verify your LLM API key (e.g., GROQ_API_KEY) is set
- Check API rate limits and quota
- Ensure you have internet connectivity
