# Mutual Fund RAG Chatbot

A facts-only FAQ chatbot for mutual fund schemes using Retrieval-Augmented Generation (RAG). Built as a learning project for understanding fintech applications and RAG architecture.

## 📋 Project Overview

**Assignment**: RAG-based Mutual Fund FAQ Chatbot (Milestone 1)  
**Deadline**: February 12, 2026  
**Scope**: Answer factual questions about mutual fund schemes using official sources only

### Key Features
- ✅ Facts-only responses (no investment advice)
- ✅ Source citations for every answer
- ✅ Covers 5 HDFC mutual fund schemes
- ✅ Uses 27 official sources (AMC, SEBI, AMFI, NISM)
- ✅ Polite refusal of advice-seeking questions

---

## 🎯 Scope

### AMC Selected
**HDFC Mutual Fund**

### Schemes Covered (5)
1. **HDFC Flexi Cap Fund** - Flexi-cap equity
2. **HDFC Large Cap Fund** - Large-cap equity (formerly HDFC Top 100 Fund)
3. **HDFC ELSS Tax Saver** - Tax-saving equity with 3-year lock-in
4. **HDFC Small Cap Fund** - Small-cap equity
5. **HDFC Balanced Advantage Fund** - Hybrid fund

### Questions Answered
- Expense ratio
- Exit load
- Minimum SIP amount
- Lock-in period (ELSS)
- Riskometer level
- Benchmark index
- How to download statements

### Questions Refused (Advice)
- "Should I invest in this fund?"
- "Which fund is better?"
- "How much should I invest?"

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         User Interface                       │
│                    (Streamlit/Gradio/Notebook)              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Question Processing                       │
│              (Intent Detection + Guardrails)                │
└────────────────────────┬────────────────────────────────────┘
                         │
                ┌────────┴────────┐
                │                 │
                ▼                 ▼
         [Factual Q]        [Advice Q]
                │                 │
                │                 └──► Polite Refusal
                │                      + Educational Link
                ▼
┌─────────────────────────────────────────────────────────────┐
│                    RAG Pipeline                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Embedding  │→ │   Vector DB  │→ │  Retrieval   │      │
│  │   (Query)    │  │  (ChromaDB)  │  │  (Top 3)     │      │
│  └──────────────┘  └──────────────┘  └──────┬───────┘      │
└────────────────────────────────────────────┬────────────────┘
                                             │
                                             ▼
┌─────────────────────────────────────────────────────────────┐
│                    LLM Generation                            │
│         (OpenAI/Gemini/Groq + Prompt Template)              │
│                                                              │
│  Instructions:                                               │
│  - Answer only from provided context                        │
│  - Keep answer ≤3 sentences                                 │
│  - Include source URL                                       │
│  - Add "Last updated: [date]"                               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Response Display                          │
│              (Answer + Citation + Timestamp)                │
└─────────────────────────────────────────────────────────────┘
```

---

## 📂 Project Structure

```
mutual-fund-rag-chatbot/
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
├── official-urls.csv                   # Original source URLs
├── official-urls-corrected.csv         # Validated & corrected URLs
├── phase1-url-validation-report.md     # URL validation findings
│
├── src/                                # Source code (Phase 2+)
│   ├── data_loader.py                  # Load documents from URLs
│   ├── embeddings.py                   # Create embeddings
│   ├── vector_store.py                 # ChromaDB operations
│   ├── retrieval.py                    # Retrieve relevant chunks
│   ├── llm.py                          # LLM integration
│   ├── guardrails.py                   # Advice detection & refusal
│   └── app.py                          # Streamlit UI
│
├── data/                               # Downloaded documents
│   ├── pdfs/                           # KIM, SID PDFs
│   └── html/                           # Scraped web pages
│
├── chroma_db/                          # Vector database (gitignored)
│
├── tests/                              # Test cases
│   └── sample_qa.md                    # Sample Q&A for validation
│
├── docs/                               # Documentation
│   ├── setup.md                        # Setup instructions
│   ├── architecture.md                 # Detailed architecture
│   └── known_limitations.md            # Known issues
│
└── requirements.txt                    # Python dependencies
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Language** | Python 3.9+ | Core development |
| **RAG Framework** | LangChain | Document processing & RAG pipeline |
| **Vector DB** | ChromaDB | Store document embeddings |
| **Embeddings** | sentence-transformers | Convert text to vectors (free) |
| **LLM** | OpenAI GPT-3.5-turbo | Generate answers |
| **UI** | Streamlit | Web interface |
| **Web Scraping** | BeautifulSoup4 | Extract content from URLs |
| **PDF Processing** | PyPDF2 | Parse PDF documents |

---

## 📊 Data Sources (27 URLs)

### HDFC AMC Sources (20)
- 5 scheme pages (NAV, riskometer, benchmark)
- 5 KIM PDFs (expense ratio, exit load, min SIP)
- 5 SID PDFs (comprehensive scheme facts)
- 5 factsheet references

### Regulatory Sources (7)
- **SEBI**: Investor FAQs, exit load guide
- **AMFI**: Knowledge center, investor education, CAS guide
- **NISM**: Mutual fund FAQs PDF

All sources are official and publicly accessible.

---

## 🚀 Development Phases

### ✅ Phase 1: Data Collection & Validation (Complete)
- [x] Select AMC and schemes
- [x] Collect 27 official URLs
- [x] Validate URL accessibility
- [x] Fix stale URLs (HDFC Top 100 → Large Cap)
- [x] Document sources in CSV

**Deliverables**:
- `official-urls-corrected.csv`
- `phase1-url-validation-report.md`

---

### 🔄 Phase 2: RAG Pipeline (In Progress)
- [ ] Load documents from URLs
- [ ] Split into chunks (500 words)
- [ ] Create embeddings
- [ ] Store in ChromaDB
- [ ] Build retrieval function
- [ ] Test with sample questions

**Deliverables**:
- Working retrieval system
- `src/data_loader.py`, `src/embeddings.py`, `src/vector_store.py`

---

### ⏳ Phase 3: LLM Integration (Planned)
- [ ] Connect to LLM API
- [ ] Create prompt template
- [ ] Generate answers with citations
- [ ] Add timestamp ("Last updated: [date]")
- [ ] Test answer quality

**Deliverables**:
- `src/llm.py`
- Sample Q&A file

---

### ⏳ Phase 4: Guardrails (Planned)
- [ ] Detect advice-seeking questions
- [ ] Create polite refusal template
- [ ] Add educational links
- [ ] Test with tricky questions

**Deliverables**:
- `src/guardrails.py`
- Refusal message templates

---

### ⏳ Phase 5: UI Development (Planned)
- [ ] Build Streamlit interface
- [ ] Add welcome message
- [ ] Show 3 example questions
- [ ] Display answer + citation
- [ ] Add disclaimer footer

**Deliverables**:
- `src/app.py`
- Working web interface

---

### ⏳ Phase 6: Testing & Documentation (Planned)
- [ ] Test 10-15 diverse questions
- [ ] Verify all citations work
- [ ] Write setup instructions
- [ ] Document known limitations
- [ ] Record demo video

**Deliverables**:
- `tests/sample_qa.md`
- `docs/setup.md`
- `docs/known_limitations.md`
- Demo video (≤3 minutes)

---

## ⚠️ Constraints & Guardrails

### Must Follow
- ✅ **Public sources only** - No app screenshots or third-party blogs
- ✅ **No PII** - Don't accept PAN, Aadhaar, phone, email
- ✅ **No performance claims** - Don't calculate/compare returns
- ✅ **Facts only** - No investment advice
- ✅ **Transparency** - Always cite sources, keep answers ≤3 sentences

### Refusal Criteria
The chatbot **must refuse** to answer:
- Investment recommendations
- Portfolio allocation advice
- Fund comparisons ("Which is better?")
- Personalized financial planning
- Return predictions

---

## 📝 Sample Interactions

### ✅ Factual Question (Answer)
**User**: "What is the expense ratio of HDFC Flexi Cap Fund?"

**Chatbot**: 
```
The expense ratio of HDFC Flexi Cap Fund (Direct Plan) is 1.05% per annum. 
This fee is charged annually for managing the fund. 
Last updated from sources: February 2026.

Source: [HDFC Flexi Cap KIM](https://files.hdfcfund.com/...)
```

### ❌ Advice Question (Refuse)
**User**: "Should I invest in HDFC ELSS Tax Saver?"

**Chatbot**:
```
I can only provide facts about mutual fund schemes, not investment advice. 
For personalized recommendations, please consult a SEBI-registered financial advisor.

Learn more: [SEBI Investor Education](https://investor.sebi.gov.in/)
```

---

## 🎯 Success Criteria

- ✅ Answers 10+ factual questions accurately
- ✅ Every answer includes a valid source link
- ✅ Refuses advice questions politely
- ✅ Answers are ≤3 sentences
- ✅ All sources are official (HDFC/SEBI/AMFI/NISM)
- ✅ No PII collected
- ✅ Working prototype (hosted or demo video)

---

## 📅 Timeline

| Date | Phase | Status |
|------|-------|--------|
| Feb 9 | Phase 1: Data Collection | ✅ Complete |
| Feb 10 | Phase 2: RAG Pipeline | 🔄 In Progress |
| Feb 11 | Phases 3-5: LLM + UI | ⏳ Planned |
| Feb 12 | Phase 6: Testing & Submission | ⏳ Planned |

**Deadline**: February 12, 2026, 11:59 PM IST

---

## 🔧 Setup Instructions

### Prerequisites
- Python 3.9+
- pip package manager
- OpenAI API key (or alternative LLM)

### Installation
```bash
# Clone repository
git clone <your-repo-url>
cd mutual-fund-rag-chatbot

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys
```

### Run the Chatbot
```bash
streamlit run src/app.py
```

---

## 📚 Learning Resources

- [LangChain Documentation](https://python.langchain.com/)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [SEBI Investor Education](https://investor.sebi.gov.in/)
- [AMFI Knowledge Center](https://www.amfiindia.com/investor-corner/knowledge-center)

---

## 🤝 Contributing

This is a learning project for educational purposes. Not intended for production use.

---

## 📄 License

Educational project - not for commercial use.

---

## 🙏 Acknowledgments

- **HDFC Mutual Fund** - Official scheme documentation
- **SEBI** - Investor education resources
- **AMFI** - Industry knowledge center
- **NISM** - Mutual fund FAQs

---

**Last Updated**: February 9, 2026  
**Status**: Phase 1 Complete, Phase 2 In Progress
