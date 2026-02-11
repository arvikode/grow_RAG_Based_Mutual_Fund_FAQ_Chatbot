# Setup Instructions

Complete guide to setting up and running the Mutual Fund RAG Chatbot locally and deploying to Streamlit Cloud.

## Prerequisites

- **Python**: Version 3.9 or higher
- **Git**: For cloning the repository
- **API Key**: Google Gemini API key (free tier available) or Grok API key

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/grow_RAG_Based_Mutual_Fund_FAQ_Chatbot.git
cd grow_RAG_Based_Mutual_Fund_FAQ_Chatbot
```

### 2. Create Virtual Environment

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy the example environment file:
   ```bash
   copy .env.example .env  # Windows
   cp .env.example .env    # macOS/Linux
   ```

2. Edit `.env` and add your API key:
   ```env
   GEMINI_API_KEY=your_actual_api_key_here
   LLM_PROVIDER=gemini
   GEMINI_MODEL=gemini-pro
   MAX_TOKENS=1000
   TEMPERATURE=0.1
   ```

3. Get a free Gemini API key:
   - Visit: https://makersuite.google.com/app/apikey
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy and paste into `.env`

### 5. Run the Application

```bash
streamlit run src\app.py
```

The app will open in your browser at `http://localhost:8501`

---

## Streamlit Cloud Deployment

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at https://streamlit.io/cloud)
- Google Gemini API key

### Deployment Steps

#### 1. Push Code to GitHub

```bash
git add .
git commit -m "Prepare for Streamlit deployment"
git push origin main
```

#### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Select your repository: `yourusername/grow_RAG_Based_Mutual_Fund_FAQ_Chatbot`
4. Set main file path: `src/app.py`
5. Click "Advanced settings"

#### 3. Configure Secrets

In the "Secrets" section, paste the following (replace with your actual API key):

```toml
GEMINI_API_KEY = "your_actual_gemini_api_key_here"
LLM_PROVIDER = "gemini"
GEMINI_MODEL = "gemini-pro"
MAX_TOKENS = "1000"
TEMPERATURE = "0.1"
```

#### 4. Deploy

Click "Deploy!" and wait for the app to build (2-3 minutes).

### Important Notes for Deployment

- **Secrets**: Never commit API keys to GitHub. Always use Streamlit's secrets management.
- **FAISS Index**: The vector database (`faiss_index/`) must be committed to the repository for deployment to work.
- **Dependencies**: Ensure `requirements.txt` includes all necessary packages.

---

## Troubleshooting

### Issue: "ModuleNotFoundError"

**Solution**: Make sure you've activated the virtual environment and installed all dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "GEMINI_API_KEY not set"

**Solution**: 
1. Check that `.env` file exists in the project root
2. Verify the API key is correctly set (no quotes, no spaces)
3. For Streamlit Cloud, check the Secrets section in app settings

### Issue: "API QUOTA EXCEEDED"

**Solution**: 
- Gemini free tier has rate limits
- Wait a few minutes and try again
- Consider upgrading at https://ai.google.dev/pricing

### Issue: "FAISS index not found"

**Solution**: The vector database needs to be built first. If missing:
```bash
python src/vector_store.py
```

### Issue: Streamlit app won't start

**Solution**:
1. Check Python version: `python --version` (must be 3.9+)
2. Verify Streamlit is installed: `pip show streamlit`
3. Try running with verbose output: `streamlit run src/app.py --logger.level=debug`

---

## Testing the Installation

After setup, test the chatbot with these sample questions:

1. **Factual Question**: "What is the expense ratio of HDFC Flexi Cap Fund?"
   - Should return a specific percentage with source citation

2. **Advice Question**: "Should I invest in HDFC ELSS?"
   - Should politely refuse and suggest consulting a financial advisor

3. **Greeting**: "Hello"
   - Should respond with a friendly greeting

If all three work correctly, your setup is complete! ✅

---

## Next Steps

- Read [known_limitations.md](./known_limitations.md) to understand the chatbot's constraints
- Review [demo_script.md](./demo_script.md) to see example interactions
- Check the main [README.md](../README.md) for project overview

---

## Support

For issues or questions:
- Check the [known_limitations.md](./known_limitations.md) file
- Review error messages carefully (they include helpful suggestions)
- Ensure you're using the latest version from GitHub
