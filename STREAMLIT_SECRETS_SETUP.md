# 🔐 Streamlit Cloud Secrets Setup Guide

## Quick Fix for Your Deployment Error

Your app failed because the `GROQ_API_KEY` is not set on Streamlit Cloud. Here's how to fix it:

### Step 1: Go to Your App Settings

1. Visit your deployed app: `https://share.streamlit.io/YOUR_USERNAME/MultiAgentCodeReviewer`
2. Click the **three dots (⋯)** in the top-right corner
3. Select **"Manage app"**

### Step 2: Add Secrets

1. Click on the **"Secrets"** tab
2. Paste the following in the secrets editor:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
GITHUB_TOKEN = "your_actual_github_token_here"
```

**Important:** Replace the placeholder values with your actual keys!

### Step 3: Save and Rerun

1. Click **"Save"**
2. Your app will automatically restart with the new secrets
3. The error should be fixed! ✅

---

## Getting Your API Keys

### 🔑 Groq API Key

1. Go to [console.groq.com](https://console.groq.com)
2. Sign in or create an account
3. Navigate to **API Keys** section
4. Click **"Create New API Key"**
5. Copy the key and paste it in Streamlit Cloud secrets

### 🔑 GitHub Personal Access Token (PAT)

1. Go to [GitHub Settings](https://github.com/settings/tokens)
2. Click **"Generate new token"** → **"Generate new token (classic)"**
3. Give it a name like "Streamlit Code Reviewer"
4. Select scope: `repo` (full control of private repositories)
5. Click **"Generate token"**
6. Copy the token immediately (you won't see it again!)
7. Paste it in Streamlit Cloud secrets

---

## Troubleshooting

### "GROQ_API_KEY is not set"
- ✅ Check that you've added `GROQ_API_KEY` to Streamlit Cloud secrets
- ✅ Make sure the entire app has restarted after adding the secret
- ✅ Refresh the page in your browser

### "Invalid API key"
- ✅ Double-check the key is correct (no extra spaces)
- ✅ Verify the key hasn't expired
- ✅ Make sure you're using the Groq API key, not another service

### "GitHub token not found"
- ✅ The GitHub token is optional - you can enter it manually each time
- ✅ OR add `GITHUB_TOKEN` to Streamlit Cloud secrets for convenience

---

## Testing Locally

Before deploying, test locally with:

```bash
streamlit run app.py
```

Make sure your `.streamlit/secrets.toml` file has:
```toml
GROQ_API_KEY = "your_test_key"
GITHUB_TOKEN = "your_test_token"
```

---

## Security Best Practices

✅ **DO:**
- Use personal access tokens with minimal required scopes
- Rotate keys periodically
- Use Streamlit Cloud secrets instead of hardcoding

❌ **DON'T:**
- Commit secrets to GitHub
- Share your API keys
- Use the same key in multiple environments
- Leave old tokens unused (revoke them)

---

## Next Steps

After fixing the secrets issue:

1. **Verify the app works** - Try both direct code review and GitHub PR review
2. **Test GitHub PR integration** - If using the GitHub feature
3. **Share your app** - The URL is `https://share.streamlit.io/YOUR_USERNAME/MultiAgentCodeReviewer`

Your app should now be fully functional! 🎉
