import streamlit as st
import json
import os
from dotenv import load_dotenv
from graph.workflow import build_review_graph
from github_int.client import GitHubClient
from github_int.utils import extract_code_from_pr

# Load environment variables (local development)
load_dotenv()

# Initialize session state for secrets
if "github_token_input" not in st.session_state:
    st.session_state.github_token_input = ""

# Page configuration
st.set_page_config(
    page_title="Multi-Agent Code Reviewer",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
        border-bottom: 2px solid #1f77b4;
        padding-bottom: 0.5rem;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        padding: 1rem;
        border-radius: 0.25rem;
    }
    .error-box {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
        padding: 1rem;
        border-radius: 0.25rem;
    }
    .info-box {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        padding: 1rem;
        border-radius: 0.25rem;
    }
    .issue-card {
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin-bottom: 1rem;
        background-color: #f8f9fa;
        border-radius: 0.25rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">🤖 Multi-Agent Code Reviewer</div>', unsafe_allow_html=True)
st.markdown("Automated code review powered by AI agents for bugs, security, and performance analysis.")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    review_mode = st.radio(
        "Select Review Mode",
        ["📝 Direct Code", "🔗 GitHub PR"],
        help="Choose how you want to submit code for review"
    )
    st.divider()
    
    st.subheader("About")
    st.info(
        """
        This tool uses a multi-agent system to review code:
        - 🐛 **Bug Agent**: Identifies potential bugs and logic errors
        - 🔒 **Security Agent**: Detects security vulnerabilities
        - ⚡ **Performance Agent**: Finds performance bottlenecks
        - 📊 **Aggregator**: Combines all reviews into a final report
        """
    )

# Main content area
if review_mode == "📝 Direct Code":
    st.markdown('<div class="section-header">📝 Submit Code for Review</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        code_input = st.text_area(
            "Paste your code here:",
            height=300,
            placeholder="Paste your code snippet here...",
            key="code_textarea"
        )
    
    with col2:
        st.subheader("Code Templates")
        if st.button("🐍 Python Example"):
            st.session_state.code_textarea = """def process_user_data(user_id, query):
    import os
    connection = os.popen(f"sql -u root -p {query}")
    result = connection.read()
    return result"""
        
        if st.button("☕ Java Example"):
            st.session_state.code_textarea = """@GetMapping("/user")
public User getUser(@RequestParam String id) {
    return jdbcTemplate.queryForObject(
        "SELECT * FROM users WHERE id = '" + id + "'",
        User.class
    );
}"""
    
    if st.button("🚀 Start Review", type="primary", use_container_width=True):
        if not code_input.strip():
            st.error("❌ Please paste some code to review.")
        else:
            with st.spinner("🔍 Running multi-agent review..."):
                try:
                    # Build and run the review graph
                    graph = build_review_graph()
                    
                    initial_state = {
                        "code": code_input,
                        "bug_report": None,
                        "security_report": None,
                        "performance_report": None,
                        "final_review": None,
                    }
                    
                    result = graph.invoke(initial_state)
                    final_review = result["final_review"]
                    
                    # Store results in session state
                    st.session_state.review_results = {
                        "final_review": final_review,
                        "code": code_input,
                        "bug_report": result.get("bug_report"),
                        "security_report": result.get("security_report"),
                        "performance_report": result.get("performance_report"),
                    }
                    
                except Exception as e:
                    st.error(f"❌ Error during review: {str(e)}")

elif review_mode == "🔗 GitHub PR":
    st.markdown('<div class="section-header">🔗 Review GitHub Pull Request</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        repo_owner = st.text_input("Repository Owner", placeholder="e.g., facebook")
    
    with col2:
        repo_name = st.text_input("Repository Name", placeholder="e.g., react")
    
    with col3:
        pr_number = st.number_input("PR Number", min_value=1, value=1)
    
    # Try to get GitHub token from secrets first, then fall back to user input
    default_token = ""
    if "GITHUB_TOKEN" in st.secrets:
        default_token = st.secrets["GITHUB_TOKEN"]
        st.info("✅ Using GitHub token from secrets")
    
    github_token = st.text_input(
        "GitHub Token",
        type="password",
        placeholder="Enter your GitHub token",
        value=default_token,
        help="Your GitHub personal access token (PAT). If using Streamlit Cloud, set in 'Manage app' > 'Secrets'"
    )
    
    if st.button("📥 Fetch & Review PR", type="primary", use_container_width=True):
        if not all([repo_owner, repo_name, github_token]):
            st.error("❌ Please fill in all required fields.")
        else:
            with st.spinner(f"📥 Fetching PR #{pr_number} from {repo_owner}/{repo_name}..."):
                try:
                    # Fetch PR files
                    client = GitHubClient(github_token)
                    files = client.get_pr_files(repo_owner, repo_name, int(pr_number))
                    
                    if not files:
                        st.error("❌ No files found in the PR.")
                    else:
                        st.success(f"✅ Fetched {len(files)} files from PR")
                        
                        # Extract code from PR
                        code = extract_code_from_pr(files)
                        
                        if not code.strip():
                            st.error("❌ No code diff found in PR.")
                        else:
                            st.info(f"📝 Found {len(code)} characters of code to review")
                            
                            # Run review
                            with st.spinner("🔍 Running multi-agent review..."):
                                graph = build_review_graph()
                                
                                initial_state = {
                                    "code": code,
                                    "bug_report": None,
                                    "security_report": None,
                                    "performance_report": None,
                                    "final_review": None,
                                }
                                
                                result = graph.invoke(initial_state)
                                final_review = result["final_review"]
                                
                                st.session_state.review_results = {
                                    "final_review": final_review,
                                    "code": code,
                                    "bug_report": result.get("bug_report"),
                                    "security_report": result.get("security_report"),
                                    "performance_report": result.get("performance_report"),
                                }
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# Display review results
if "review_results" in st.session_state and st.session_state.review_results:
    st.divider()
    st.markdown('<div class="section-header">📊 Review Results</div>', unsafe_allow_html=True)
    
    results = st.session_state.review_results
    final_review = results.get("final_review", {})
    
    # Summary section
    if final_review.get("summary"):
        st.markdown('<div class="info-box">', unsafe_allow_html=True)
        st.markdown(f"**Summary:** {final_review['summary']}")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Issues section
    issues = final_review.get("issues", [])
    
    if issues:
        st.subheader("🔍 Found Issues")
        
        # Categorize issues
        security_issues = [i for i in issues if i.get("category") == "SECURITY"]
        bug_issues = [i for i in issues if i.get("category") == "BUG"]
        perf_issues = [i for i in issues if i.get("category") == "PERFORMANCE"]
        
        # Display security issues
        if security_issues:
            st.subheader("🔒 Security Issues")
            for idx, issue in enumerate(security_issues, 1):
                severity_color = {
                    "HIGH": "🔴",
                    "MEDIUM": "🟠",
                    "LOW": "🟡"
                }.get(issue.get("severity"), "⚪")
                
                with st.expander(f"{severity_color} {issue.get('severity', 'UNKNOWN')} - {issue.get('description', 'No description')}"):
                    st.markdown(f"**Description:** {issue.get('description', 'N/A')}")
                    st.markdown(f"**Recommendation:** {issue.get('recommendation', 'N/A')}")
        
        # Display bug issues
        if bug_issues:
            st.subheader("🐛 Bug Issues")
            for idx, issue in enumerate(bug_issues, 1):
                severity_color = {
                    "HIGH": "🔴",
                    "MEDIUM": "🟠",
                    "LOW": "🟡"
                }.get(issue.get("severity"), "⚪")
                
                with st.expander(f"{severity_color} {issue.get('severity', 'UNKNOWN')} - {issue.get('description', 'No description')}"):
                    st.markdown(f"**Description:** {issue.get('description', 'N/A')}")
                    st.markdown(f"**Recommendation:** {issue.get('recommendation', 'N/A')}")
        
        # Display performance issues
        if perf_issues:
            st.subheader("⚡ Performance Issues")
            for idx, issue in enumerate(perf_issues, 1):
                severity_color = {
                    "HIGH": "🔴",
                    "MEDIUM": "🟠",
                    "LOW": "🟡"
                }.get(issue.get("severity"), "⚪")
                
                with st.expander(f"{severity_color} {issue.get('severity', 'UNKNOWN')} - {issue.get('description', 'No description')}"):
                    st.markdown(f"**Description:** {issue.get('description', 'N/A')}")
                    st.markdown(f"**Recommendation:** {issue.get('recommendation', 'N/A')}")
        
        # Display issue statistics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            total_high = len([i for i in issues if i.get("severity") == "HIGH"])
            st.metric("High Severity", total_high)
        with col2:
            total_medium = len([i for i in issues if i.get("severity") == "MEDIUM"])
            st.metric("Medium Severity", total_medium)
        with col3:
            total_low = len([i for i in issues if i.get("severity") == "LOW"])
            st.metric("Low Severity", total_low)
        with col4:
            st.metric("Total Issues", len(issues))
    else:
        st.success("✅ No issues found! Your code looks great!")
    
    # Code and raw results tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📄 Code", "📋 Final Report", "🐛 Bug Report", "🔒 Security Report"])
    
    with tab1:
        st.code(results.get("code", ""), language="python")
    
    with tab2:
        st.json(final_review)
    
    with tab3:
        if results.get("bug_report"):
            st.json(results["bug_report"])
        else:
            st.info("Bug report not available")
    
    with tab4:
        if results.get("security_report"):
            st.json(results["security_report"])
        else:
            st.info("Security report not available")
    
    # Download results
    col1, col2 = st.columns(2)
    
    with col1:
        json_results = json.dumps(final_review, indent=2)
        st.download_button(
            label="⬇️ Download Review Report",
            data=json_results,
            file_name="code_review_report.json",
            mime="application/json"
        )
    
    with col2:
        if st.button("🔄 New Review"):
            st.session_state.review_results = None
            st.rerun()
