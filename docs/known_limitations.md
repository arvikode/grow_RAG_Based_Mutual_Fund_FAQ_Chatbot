# Known Limitations

This document outlines the known limitations, constraints, and edge cases of the Mutual Fund RAG Chatbot.

## Data Coverage Limitations

### 1. Limited Scheme Coverage
- **Limitation**: Only covers 5 HDFC mutual fund schemes
- **Impact**: Cannot answer questions about other HDFC schemes or other AMCs
- **Schemes Covered**:
  - HDFC Flexi Cap Fund
  - HDFC Large Cap Fund
  - HDFC ELSS Tax Saver
  - HDFC Small Cap Fund
  - HDFC Balanced Advantage Fund

### 2. SID PDF Access Issues
- **Limitation**: 5 Scheme Information Documents (SIDs) returned 403 errors during data collection
- **Impact**: Some detailed scheme information may be missing
- **Mitigation**: Key Information Memorandums (KIMs) and scheme pages provide sufficient data for most queries

### 3. Data Freshness
- **Limitation**: Data is static, collected in February 2026
- **Impact**: 
  - NAV values are not real-time
  - Expense ratios may change quarterly
  - Fund manager changes won't be reflected
- **Recommendation**: Always verify critical information on official HDFC website

## Functional Limitations

### 4. No Real-Time Data
- **Limitation**: Cannot fetch current NAV, AUM, or performance data
- **Impact**: Historical data only; users need to check official sources for latest values
- **Workaround**: Chatbot provides source URLs for users to verify current data

### 5. No Investment Advice
- **Limitation**: Designed to refuse all advice-seeking questions
- **Impact**: Cannot help with:
  - Fund selection
  - Portfolio allocation
  - Investment timing
  - Return predictions
  - Risk assessment for individuals
- **By Design**: This is a safety feature, not a bug

### 6. Limited to Official Sources
- **Limitation**: Only uses official AMC, SEBI, AMFI, and NISM sources
- **Impact**: Cannot answer questions about:
  - Third-party fund ratings
  - Comparison with competitors
  - Market news or trends
  - Expert opinions

## Technical Limitations

### 7. LLM API Rate Limits
- **Limitation**: Gemini free tier has rate limits (60 requests/minute)
- **Impact**: Users may see "Rate Limit Exceeded" errors during heavy usage
- **Solution**: Wait 30-60 seconds and retry, or upgrade API plan

### 8. LLM API Quota Limits
- **Limitation**: Free tier has daily quota limits
- **Impact**: Chatbot may stop working after extensive use
- **Solution**: Wait until next day, or upgrade to paid tier

### 9. Context Window Limitations
- **Limitation**: LLM has limited context window (max 1000 tokens output)
- **Impact**: Very long answers may be truncated
- **Mitigation**: Answers are designed to be ≤3 sentences

### 10. Vector Search Accuracy
- **Limitation**: Retrieval may not always find the most relevant documents
- **Impact**: Occasionally may say "I don't have information" when data exists
- **Mitigation**: Retrieves top 5 documents to improve coverage

## Edge Cases & Known Issues

### 11. Incomplete Data in PDFs
- **Limitation**: Some PDFs contain links/tables instead of actual values
- **Example**: TER might show "Click here" instead of the percentage
- **Impact**: Chatbot will indicate data is unavailable and provide source URL
- **Status**: Working as designed (provides transparency)

### 12. Ambiguous Questions
- **Limitation**: Struggles with vague or incomplete questions
- **Examples**:
  - "What is the NAV?" (which fund?)
  - "expense ratio" (incomplete sentence)
  - "Tell me everything" (too broad)
- **Impact**: May return generic or no answer
- **Recommendation**: Users should ask specific questions

### 13. Comparison Questions
- **Limitation**: Treats comparisons as advice-seeking
- **Examples**:
  - "HDFC Flexi Cap vs Large Cap"
  - "Which has lower expense ratio?"
- **Impact**: These are blocked even if factual
- **Rationale**: Comparisons can imply recommendations

### 14. Greeting Detection Edge Cases
- **Limitation**: May misclassify some casual questions
- **Examples**:
  - "What can you do?" → Treated as greeting
  - "Who are you?" → Treated as greeting
- **Impact**: Minor; doesn't affect core functionality

## Performance Limitations

### 15. Response Time
- **Limitation**: Responses take 2-5 seconds
- **Factors**:
  - Vector search: ~0.5s
  - LLM generation: 1-4s
  - Network latency: variable
- **Impact**: Not suitable for real-time chat applications

### 16. Concurrent Users (Streamlit Cloud)
- **Limitation**: Free Streamlit Cloud tier has resource limits
- **Impact**: May slow down with 10+ concurrent users
- **Solution**: Upgrade to Streamlit Cloud paid tier for production use

## Deployment Limitations

### 17. FAISS Index Size
- **Limitation**: Vector database must be committed to git
- **Impact**: Increases repository size (~50MB)
- **Alternative**: Could use cloud-hosted vector DB (ChromaDB, Pinecone)

### 18. Cold Start Time
- **Limitation**: First request after inactivity takes longer
- **Impact**: 10-15 second delay on Streamlit Cloud after idle period
- **Mitigation**: Keep-alive pings (not implemented)

## Compliance & Legal Limitations

### 19. No Personalization
- **Limitation**: Cannot store user data or preferences
- **Impact**: Every session is independent
- **By Design**: Privacy and compliance requirement

### 20. No PII Collection
- **Limitation**: Cannot accept PAN, Aadhaar, phone, email
- **Impact**: Cannot provide account-specific information
- **By Design**: Security and privacy requirement

## Future Improvements

These limitations could be addressed in future versions:
- [ ] Expand to more schemes and AMCs
- [ ] Integrate real-time NAV API
- [ ] Implement caching for faster responses
- [ ] Add support for more document types
- [ ] Improve comparison handling (factual only)
- [ ] Better handling of incomplete data in PDFs

---

## Reporting Issues

If you encounter a limitation not listed here, please:
1. Check if it's a known edge case above
2. Verify your API key and configuration
3. Review error messages (they often include solutions)
4. Document the issue with example question and expected behavior

---

**Last Updated**: February 11, 2026  
**Version**: 1.0 (Phase 6)
