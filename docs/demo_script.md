# Demo Script

3-minute demonstration script for the Mutual Fund RAG Chatbot. Use this as a guide for recording a demo video or giving a live presentation.

---

## Introduction (30 seconds)

**[Screen: Welcome page of the chatbot]**

"Hello! This is the Mutual Fund RAG Chatbot - a facts-only FAQ assistant for HDFC mutual fund schemes.

This chatbot uses Retrieval-Augmented Generation to answer questions using only official sources from HDFC, SEBI, AMFI, and NISM.

It covers 5 HDFC schemes and provides factual information with source citations. Importantly, it does NOT provide investment advice."

---

## Demo 1: Factual Question with Citation (45 seconds)

**[Screen: Chat interface]**

"Let's start with a factual question. I'll ask about the expense ratio of HDFC Flexi Cap Fund."

**Type**: "What is the expense ratio of HDFC Flexi Cap Fund?"

**[Wait for response]**

"As you can see, the chatbot:
1. Provides a specific answer with the exact percentage
2. Includes source citations with clickable links
3. Shows the relevance score for transparency

Let me click on this source link to verify..."

**[Click on source URL]**

"And here's the official HDFC document confirming the information. This ensures users can always verify the facts."

---

## Demo 2: Advice Refusal (30 seconds)

**[Screen: Back to chat interface]**

"Now let's see what happens when someone asks for investment advice."

**Type**: "Should I invest in HDFC ELSS Tax Saver?"

**[Wait for response]**

"The chatbot politely refuses to provide advice and instead:
1. Explains it can only provide facts
2. Recommends consulting a SEBI-registered advisor
3. Provides educational resources

This guardrail ensures the chatbot stays within safe, factual boundaries."

---

## Demo 3: Multiple Questions (45 seconds)

**[Screen: Chat interface]**

"Let's ask a few more questions to show the breadth of knowledge."

**Type**: "What is the exit load for HDFC Large Cap Fund?"

**[Wait for response]**

"Great! It provides the specific exit load structure with citations."

**Type**: "What is the minimum SIP amount for HDFC Small Cap Fund?"

**[Wait for response]**

"And here's the minimum SIP amount. Notice how each answer is concise - typically 2-3 sentences - making it easy to quickly get the information you need."

---

## Demo 4: Edge Case (30 seconds)

**[Screen: Chat interface]**

"Let's try an edge case - a comparison question."

**Type**: "Which is better: HDFC Flexi Cap or HDFC Large Cap?"

**[Wait for response]**

"The chatbot recognizes this as advice-seeking and refuses to compare funds. However, if you ask for factual details about each fund individually, it will happily provide that information."

---

## Closing & Key Features (30 seconds)

**[Screen: Sidebar showing example questions and resources]**

"To summarize, this chatbot:
- ✅ Answers factual questions about 5 HDFC schemes
- ✅ Provides source citations for every answer
- ✅ Refuses investment advice politely
- ✅ Uses only official, verified sources
- ✅ Keeps answers concise and clear

The sidebar shows example questions and helpful resources.

This is a learning project demonstrating RAG architecture for fintech applications. Thank you for watching!"

---

## Technical Notes for Recording

### Preparation
1. Clear chat history before starting
2. Have example questions ready to copy-paste
3. Test all source links beforehand
4. Ensure good internet connection for API calls

### Recording Tips
- **Screen Resolution**: 1920x1080 recommended
- **Recording Software**: OBS Studio, Loom, or Streamlit's built-in recording
- **Audio**: Use a good microphone, speak clearly
- **Pacing**: Pause briefly after each response to let viewers read
- **Cursor**: Highlight important parts (answer, sources, refusal messages)

### Questions to Demonstrate

**Factual (choose 2-3)**:
- "What is the expense ratio of HDFC Flexi Cap Fund?"
- "What is the exit load for HDFC Large Cap Fund?"
- "What is the minimum SIP amount for HDFC Small Cap Fund?"
- "What is the lock-in period for HDFC ELSS?"
- "What is the benchmark index for HDFC Balanced Advantage Fund?"

**Advice (choose 1-2)**:
- "Should I invest in HDFC ELSS Tax Saver?"
- "Which fund is better: HDFC Flexi Cap or Large Cap?"
- "Can you recommend a fund for me?"

**Edge Cases (choose 1)**:
- "Compare HDFC Flexi Cap and HDFC Large Cap"
- "What is the NAV?" (missing fund name)
- "Hello" (greeting)

### Post-Production
- Add title slide at the beginning
- Include disclaimer: "Educational project - not for investment advice"
- Add captions/subtitles if possible
- Export as MP4, max 3 minutes

---

## Alternative: Live Demo Checklist

If presenting live instead of recording:

- [ ] Open chatbot in browser beforehand
- [ ] Clear chat history
- [ ] Have questions ready in a text file to copy-paste
- [ ] Test internet connection
- [ ] Have backup screenshots in case of API issues
- [ ] Prepare to explain RAG architecture if asked
- [ ] Be ready to show the code structure (optional)

---

**Last Updated**: February 11, 2026  
**Demo Duration**: ~3 minutes  
**Difficulty**: Easy
