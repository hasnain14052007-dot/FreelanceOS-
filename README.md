# 🚀 FreelanceOS: The Agentic Copilot

FreelanceOS uses a multi-agent AI crew to analyze freelance job postings, spot red flags, generate tailored proposals, and draft project plans. Upgraded for production with strict security and a modern UI.

## Features
- **4-Agent Crew:** Lead Scout, Proposal Architect, Project Manager, Finance Officer.
- **Secure by Design:** API keys are processed server-side. Errors are sanitized.
- **Rate Limiting:** Prevents API abuse on free tiers.
- **Export:** Download comprehensive reports as PDF.
- **Modern UI:** Built on Streamlit with a custom theme and wide layout.

## Local Setup
1. Clone the repo and navigate to the directory.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and add your Gemini API Key.
4. Run: `streamlit run app.py`

## Deployment on Streamlit Community Cloud
1. `git add .` -> `git commit -m "Production release"` -> `git push origin main`
2. Go to [share.streamlit.io](https://share.streamlit.io), click "New app".
3. Select your repository, branch, and set the main file path to `app.py`.
4. Click **Advanced settings** before deploying and add your key in the **Secrets** field:
   ```toml
   GEMINI_API_KEY = "your-actual-api-key"