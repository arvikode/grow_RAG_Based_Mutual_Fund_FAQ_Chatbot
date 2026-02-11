# How to Start the Mutual Fund Chatbot

## Quick Start (Windows)

### Option 1: Double-click the batch file
Simply double-click `start_server.bat` in the project folder.

### Option 2: Command Line
Open PowerShell or Command Prompt in the project directory and run:

```bash
python -m streamlit run src/app.py
```

## What Happens Next

1. The server will start and show:
   ```
   You can now view your Streamlit app in your browser.
   
   Local URL: http://localhost:8501
   Network URL: http://10.x.x.x:8501
   ```

2. Your browser should automatically open to the chatbot

3. If it doesn't open automatically, manually navigate to: **http://localhost:8501**

## Stopping the Server

Press `Ctrl+C` in the terminal/command prompt window

## Troubleshooting

### Port Already in Use
If you see an error about port 8501 being in use:
- The server is already running! Just open http://localhost:8501
- OR close the existing server and start again

### Module Not Found Errors
Make sure dependencies are installed:
```bash
python -m pip install -r requirements.txt
```

### API Key Errors
Make sure your `.env` file has a valid `GEMINI_API_KEY`:
```
GEMINI_API_KEY=your_actual_api_key_here
LLM_PROVIDER=gemini
GEMINI_MODEL=gemini-flash-latest
```

## Testing the Chatbot

Try these example questions:
- "What is the expense ratio of HDFC Flexi Cap Fund?"
- "What is the exit load for HDFC Large Cap Fund?"
- "What is the minimum SIP amount for HDFC ELSS Tax Saver?"

The chatbot will:
✅ Retrieve relevant documents from the vector database
✅ Generate answers using Gemini AI
✅ Provide source citations
✅ Refuse advice-seeking questions
