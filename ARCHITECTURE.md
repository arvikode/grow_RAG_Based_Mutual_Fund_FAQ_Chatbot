# Architecture Documentation

## System Overview

The Mutual Fund RAG Chatbot is built using a Retrieval-Augmented Generation (RAG) architecture to ensure factual accuracy and source transparency.

---

## High-Level Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                         USER LAYER                                │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Streamlit Web Interface                                   │  │
│  │  - Welcome message + disclaimer                            │  │
│  │  - Example questions                                       │  │
│  │  - Text input for queries                                  │  │
│  │  - Answer display with citations                           │  │
│  └────────────────────────────────────────────────────────────┘  │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                              │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Guardrails Module (guardrails.py)                         │  │
│  │  - Intent classification (factual vs. advice)              │  │
│  │  - Advice question detection                               │  │
│  │  - Refusal message generation                              │  │
│  └──────────────┬─────────────────────────┬───────────────────┘  │
│                 │                         │                       │
│          [Factual Q]                [Advice Q]                    │
│                 │                         │                       │
│                 │                         └──► Polite Refusal     │
│                 ▼                              + Educational Link │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  RAG Orchestrator (app.py)                                 │  │
│  │  - Coordinate retrieval + generation                       │  │
│  │  - Format final response                                   │  │
│  └──────────────┬─────────────────────────────────────────────┘  │
└─────────────────┼────────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                    RETRIEVAL LAYER                                │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Retrieval Module (retrieval.py)                           │  │
│  │  1. Convert query to embedding                             │  │
│  │  2. Similarity search in vector DB                         │  │
│  │  3. Return top-k relevant chunks (k=3)                     │  │
│  └──────────────┬─────────────────────────────────────────────┘  │
│                 │                                                 │
│                 ▼                                                 │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Vector Store (vector_store.py)                            │  │
│  │  - ChromaDB instance                                       │  │
│  │  - Stores document chunks + embeddings                     │  │
│  │  - Metadata: source URL, scheme name, doc type             │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                    GENERATION LAYER                               │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  LLM Module (llm.py)                                       │  │
│  │  - Takes: query + retrieved chunks                         │  │
│  │  - Prompt template with instructions                       │  │
│  │  - Generates: concise answer + citation                    │  │
│  │  - Adds: "Last updated: [date]"                            │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
                  │
                  ▼
┌──────────────────────────────────────────────────────────────────┐
│                    DATA LAYER                                     │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Data Loader (data_loader.py)                              │  │
│  │  - Load documents from URLs (PDFs + web pages)             │  │
│  │  - Text extraction (PyPDF2, BeautifulSoup)                 │  │
│  │  - Chunking strategy (500-word chunks, 50-word overlap)    │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Embeddings Module (embeddings.py)                         │  │
│  │  - Model: sentence-transformers/all-MiniLM-L6-v2           │  │
│  │  - Convert text chunks to 384-dim vectors                  │  │
│  └────────────────────────────────────────────────────────────┘  │
│                                                                   │
│  ┌────────────────────────────────────────────────────────────┐  │
│  │  Source Documents (data/)                                  │  │
│  │  - 27 official URLs (HDFC, SEBI, AMFI, NISM)              │  │
│  │  - Cached PDFs and HTML files                              │  │
│  └────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Data Loader (`data_loader.py`)

**Purpose**: Load and preprocess documents from official sources

**Key Functions**:
- `load_urls_from_csv()` - Read source URLs from CSV
- `download_pdf(url)` - Download PDF documents
- `scrape_webpage(url)` - Extract text from HTML pages
- `chunk_text(text, chunk_size=500, overlap=50)` - Split into chunks

**Chunking Strategy**:
- **Chunk size**: 500 words (balance between context and precision)
- **Overlap**: 50 words (preserve context across chunks)
- **Metadata**: Store source URL, scheme name, document type

---

### 2. Embeddings Module (`embeddings.py`)

**Purpose**: Convert text to vector representations

**Model**: `sentence-transformers/all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Speed**: Fast (good for prototyping)
- **Quality**: Good for semantic search
- **Cost**: Free (runs locally)

**Key Functions**:
- `create_embeddings(texts)` - Batch embed text chunks
- `embed_query(query)` - Embed user question

---

### 3. Vector Store (`vector_store.py`)

**Purpose**: Store and retrieve document embeddings

**Database**: FAISS (Facebook AI Similarity Search)
- **Type**: In-memory vector database
- **Persistence**: Local disk storage (`faiss_index` directory)
- **Similarity**: Cosine similarity
- **Path Handling**: Absolute path resolution to ensure access from any working directory

**Schema**:
```python
{
    "id": "chunk_001",
    "embedding": [0.123, 0.456, ...],  # 384-dim vector
    "text": "The expense ratio of HDFC Flexi Cap...",
    "metadata": {
        "source_url": "https://...",
        "scheme_name": "HDFC Flexi Cap Fund",
        "doc_type": "KIM",
        "date_accessed": "2026-02-09"
    }
}
```

**Key Functions**:
- `create_collection()` - Initialize ChromaDB collection
- `add_documents(chunks, embeddings, metadata)` - Store chunks
- `similarity_search(query_embedding, k=3)` - Find top-k matches

---

### 4. Retrieval Module (`retrieval.py`)

**Purpose**: Find relevant document chunks for a query

**Process**:
1. Embed user query using same model
2. Perform cosine similarity search in vector DB
3. Return top-3 most relevant chunks with metadata

**Key Functions**:
- `retrieve(query, k=3)` - Main retrieval function
- `format_context(chunks)` - Format chunks for LLM

**Retrieval Parameters**:
- **k**: 3 (balance between context and noise)
- **Similarity threshold**: 0.5 (filter irrelevant results)

---

### 5. LLM Module (`llm.py`)

**Purpose**: Generate natural language answers from retrieved context

**LLM**: OpenAI GPT-3.5-turbo (or alternatives: Gemini, Groq)

**Prompt Template**:
```
You are a helpful assistant that answers questions about mutual fund schemes.

INSTRUCTIONS:
1. Answer ONLY based on the provided context below
2. Keep your answer to 3 sentences maximum
3. Include the source URL at the end
4. Add "Last updated from sources: [date]"
5. If the context doesn't contain the answer, say "I don't have that information"

CONTEXT:
{retrieved_chunks}

QUESTION:
{user_question}

ANSWER:
```

**Key Functions**:
- `generate_answer(query, context)` - Generate answer
- `extract_citation(chunks)` - Get source URL
- `format_response(answer, citation, date)` - Final formatting

---

### 6. Guardrails Module (`guardrails.py`)

**Purpose**: Detect and refuse advice-seeking questions

**Detection Strategy**:
- **Keyword matching**: "should I", "which is better", "recommend"
- **LLM-based classification**: Use LLM to classify intent
- **Hybrid approach**: Combine both for accuracy

**Refusal Template**:
```
I can only provide facts about mutual fund schemes, not investment advice.

For personalized recommendations, please consult a SEBI-registered 
financial advisor.

Learn more: [SEBI Investor Education](https://investor.sebi.gov.in/)
```

**Key Functions**:
- `is_advice_question(query)` - Detect advice intent
- `generate_refusal(query)` - Create polite refusal
- `get_educational_link(topic)` - Suggest relevant resources

---

### 7. Streamlit UI (`app.py`)

**Purpose**: User-facing web interface

**Components**:
1. **Header**: Welcome message + disclaimer
2. **Example Questions**: 3 clickable sample questions
3. **Input**: Text box for custom questions
4. **Output**: Answer + citation + timestamp
5. **Footer**: Disclaimer ("Facts-only, no advice")

**UI Flow**:
```
User enters question
    ↓
Guardrails check
    ↓
If advice → Show refusal
If factual → RAG pipeline → Show answer + citation
```

---

## Data Flow

### Indexing Phase (One-time)

```
1. Load URLs from CSV
   ↓
2. Download/scrape documents
   ↓
3. Extract text content
   ↓
4. Split into 500-word chunks
   ↓
5. Create embeddings for each chunk
   ↓
6. Store in ChromaDB with metadata
```

### Query Phase (Runtime)

```
1. User asks question
   ↓
2. Guardrails: Is it advice?
   ├─ Yes → Return refusal message
   └─ No → Continue
       ↓
3. Embed query
   ↓
4. Similarity search (top-3 chunks)
   ↓
5. Format context from chunks
   ↓
6. LLM generates answer
   ↓
7. Extract citation from metadata
   ↓
8. Format response with timestamp
   ↓
9. Display to user
```

---

## Design Decisions

### Why RAG over Fine-tuning?
- ✅ **Transparency**: Can cite exact sources
- ✅ **Freshness**: Easy to update documents
- ✅ **Cost**: No expensive fine-tuning needed
- ✅ **Accuracy**: Grounded in official sources

### Why ChromaDB?
- ✅ **Simplicity**: Easy to set up locally
- ✅ **Speed**: Fast for small-medium datasets
- ✅ **Free**: No cloud costs
- ✅ **Persistence**: Saves to disk

### Why 500-word Chunks?
- ✅ **Context**: Large enough for complete facts
- ✅ **Precision**: Small enough to avoid noise
- ✅ **LLM limits**: Fits within context window

### Why Top-3 Retrieval?
- ✅ **Coverage**: Enough context for most questions
- ✅ **Noise**: Not too much irrelevant info
- ✅ **Cost**: Fewer tokens to LLM

---

## Performance Considerations

### Latency Breakdown (Estimated)

| Component | Time | Optimization |
|-----------|------|--------------|
| Embedding query | ~50ms | Use local model |
| Vector search | ~100ms | ChromaDB is fast |
| LLM generation | ~2-3s | Use streaming |
| **Total** | **~3s** | Acceptable for prototype |

### Scalability

**Current**: 27 URLs, ~500 chunks
- ✅ ChromaDB handles this easily

**Future**: 100+ URLs, ~2000 chunks
- Consider: Pinecone, Weaviate, or FAISS

---

## Security & Privacy

### Data Protection
- ✅ No PII collected from users
- ✅ No storage of user queries
- ✅ API keys in `.env` (gitignored)

### Source Validation
- ✅ All sources are official public URLs
- ✅ No third-party blogs or screenshots
- ✅ URLs validated for freshness

---

## Error Handling

### Common Errors

| Error | Cause | Mitigation |
|-------|-------|------------|
| No relevant chunks | Query too specific | Expand search, suggest rephrase |
| LLM timeout | API issues | Retry with exponential backoff |
| PDF download fails | Stale URL | Fallback to cached version |
| Empty answer | Context insufficient | Return "I don't have that info" |

---

## Testing Strategy

### Unit Tests
- Test each module independently
- Mock external dependencies (LLM, URLs)

### Integration Tests
- Test full RAG pipeline end-to-end
- Verify citations are correct

### Manual Testing
- 10-15 diverse questions
- Check answer quality and citations
- Test refusal for advice questions

---

## Future Enhancements

### Phase 2+ (Post-Submission)
- [ ] Multi-AMC support (ICICI, SBI, etc.)
- [ ] Conversational memory (follow-up questions)
- [ ] Advanced filters (scheme type, risk level)
- [ ] Performance comparison (with disclaimers)
- [ ] Multi-language support (Hindi, regional)

---

**Last Updated**: February 9, 2026  
**Version**: 1.0 (Phase 1 Complete)
