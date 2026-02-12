# Mutual Fund RAG Chatbot - Milestone 1 Submission

## 1. Working Prototype
**Link**: [Insert Streamlit Cloud Link Here]
*(If hosting is not possible, please include a link to a ≤3-min demo video here)*

---

## 2. Disclaimer Snippet
> **⚠️ Important Disclaimer:**
> This chatbot provides factual information only. It does NOT provide investment advice or recommendations.
> For personalized investment advice, please consult a SEBI-registered investment advisor.

---

## 3. README & Setup

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

## ⚠️ Known Limitations
- **Limited Scope**: Covers only 5 HDFC Mutual Fund schemes.
- **Static Data**: Information is based on documents collected in Feb 2026; real-time NAV/performance is not available.
- **Official Sources Only**: Does not use third-party analysis or news.
- **No Advice**: strictly prohibits investment advice, portfolio reviews, or forward-looking statements.
- **Context Window**: Long answers may be truncated; designed for short, factual responses.

---

## 4. Source List (Official URLs)

| Scheme | URL | Description | Date Accessed |
|---|---|---|---|
| HDFC Flexi Cap Fund | https://www.hdfcfund.com/explore/mutual-funds/hdfc-flexi-cap-fund/direct | Official scheme details page with NAV, portfolio, riskometer, benchmark info | 2026-02-10 |
| HDFC Flexi Cap Fund | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021,%202025_1.pdf | KIM PDF with expense ratio, exit load, min SIP details | 2026-02-10 |
| HDFC Flexi Cap Fund | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021,%202025.pdf | SID PDF with full scheme facts, riskometer, benchmark | 2026-02-10 |
| HDFC Large Cap Fund | https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct | Official scheme details page with NAV, portfolio, riskometer, benchmark info (formerly HDFC Top 100 Fund) | 2026-02-10 |
| HDFC Large Cap Fund | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Large%20Cap%20Fund%20dated%20November%2021,%202025.pdf | KIM PDF with expense ratio, exit load, min SIP details | 2026-02-10 |
| HDFC Large Cap Fund | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20Large%20Cap%20Fund%20dated%20November%2021,%202025.pdf | SID PDF with full scheme facts, riskometer, benchmark | 2026-02-10 |
| HDFC ELSS Tax Saver Fund | https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver/direct | Official scheme details page with NAV, portfolio, riskometer, benchmark, lock-in info | 2026-02-10 |
| HDFC ELSS Tax Saver Fund | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021,%202025.pdf | KIM PDF with expense ratio, exit load, min SIP, ELSS lock-in details | 2026-02-10 |
| HDFC ELSS Tax Saver Fund | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021,%202025.pdf | SID PDF with full scheme facts, riskometer, benchmark, lock-in | 2026-02-10 |
| HDFC Small Cap Fund | https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/direct | Official scheme details page with NAV, portfolio, riskometer, benchmark info | 2026-02-10 |
| HDFC Small Cap Fund | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Small%20Cap%20Fund%20dated%20November%2021,%202025.pdf | KIM PDF with expense ratio, exit load, min SIP details | 2026-02-10 |
| HDFC Small Cap Fund | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20Small%20Cap%20Fund%20dated%20November%2021,%202025.pdf | SID PDF with full scheme facts, riskometer, benchmark | 2026-02-10 |
| HDFC Balanced Advantage Fund | https://www.hdfcfund.com/explore/mutual-funds/hdfc-balanced-advantage-fund/direct | Official scheme details page with NAV, portfolio, riskometer, benchmark info | 2026-02-10 |
| HDFC Balanced Advantage Fund | https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Balanced%20Advantage%20Fund%20dated%20November%2021,%202025.pdf | KIM PDF with expense ratio, exit load, min SIP details | 2026-02-10 |
| HDFC Balanced Advantage Fund | https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20Balanced%20Advantage%20Fund%20dated%20November%2021,%202025.pdf | SID PDF with full scheme facts, riskometer, benchmark | 2026-02-10 |
| General Resources | https://www.hdfcfund.com/statutory-disclosure/total-expense-ratio-of-mutual-fund-schemes/reports | HDFC TER reports page for expense ratios across schemes | 2026-02-10 |
| General Resources | https://www.hdfcfund.com/statutory-disclosure/portfolio/monthly-portfolio | Monthly portfolio disclosures with benchmark comparisons | 2026-02-10 |
| General Resources | https://www.sebi.gov.in/sebi_data/faqfiles/sep-2024/1727242783639.pdf | SEBI Investor FAQs PDF: Covers expense ratio, exit load, min SIP, statements | 2026-02-10 |
| General Resources | https://investor.sebi.gov.in/exit_load.html | SEBI guide on exit load and mutual fund basics | 2026-02-10 |
| General Resources | https://www.amfiindia.com/ | AMFI Official Website - Investor Corner & Knowledge Center accessible from home page | 2026-02-10 |
| General Resources | https://www.nism.ac.in/wp-content/uploads/2021/02/FAQsOnMfs-3-1.pdf | NISM Mutual Fund FAQs: Min SIP, ELSS lock-in, basics | 2026-02-10 |

---

## 5. Sample Q&A

### Factual Questions

**1. Expense Ratio**
- **Q**: What is the expense ratio of HDFC Flexi Cap Fund?
- **A**: The expense ratio of HDFC Flexi Cap Fund (Direct Plan) is 1.05% per annum as of November 2025.
- **Source**: [HDFC Flexi Cap KIM](https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021,%202025_1.pdf)
- **Last updated from sources**: February 2026

**2. Exit Load**
- **Q**: What is the exit load for HDFC Large Cap Fund?
- **A**: HDFC Large Cap Fund charges an exit load of 1.00% if units are redeemed within 1 year of allotment. No exit load is charged after 1 year.
- **Source**: [HDFC Large Cap KIM](https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Large%20Cap%20Fund%20dated%20November%2021,%202025.pdf)
- **Last updated from sources**: February 2026

**3. Minimum SIP**
- **Q**: What is the minimum SIP amount for HDFC Small Cap Fund?
- **A**: The minimum SIP amount for HDFC Small Cap Fund is ₹100 per month.
- **Source**: [HDFC Small Cap SID](https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20Small%20Cap%20Fund%20dated%20November%2021,%202025.pdf)
- **Last updated from sources**: February 2026

**4. Lock-in Period**
- **Q**: Does HDFC ELSS Tax Saver have a lock-in period?
- **A**: Yes, HDFC ELSS Tax Saver Fund has a mandatory lock-in period of 3 years from the date of allotment.
- **Source**: [HDFC ELSS SID](https://files.hdfcfund.com/s3fs-public/SID/2025-11/SID-HDFC%20ELSS%20Tax%20Saver%20dated%20November%2021,%202025.pdf)
- **Last updated from sources**: February 2026

**5. Riskometer**
- **Q**: What is the risk level of HDFC Balanced Advantage Fund?
- **A**: The riskometer for HDFC Balanced Advantage Fund indicates "Very High" risk.
- **Source**: [HDFC Balanced Advantage Page](https://www.hdfcfund.com/explore/mutual-funds/hdfc-balanced-advantage-fund/direct)
- **Last updated from sources**: February 2026

**6. Benchmark**
- **Q**: What is the benchmark index for HDFC Large Cap Fund?
- **A**: The benchmark index for HDFC Large Cap Fund is NIFTY 100 TRI.
- **Source**: [HDFC Large Cap Page](https://www.hdfcfund.com/explore/mutual-funds/hdfc-large-cap-fund/direct)
- **Last updated from sources**: February 2026

**7. Statement Download**
- **Q**: How can I download my capital gains statement?
- **A**: You can download capital gains statements (Consolidated Account Statement) from the CAMS or KFintech websites, or via the official AMFI website.
- **Source**: [AMFI Website](https://www.amfiindia.com/)
- **Last updated from sources**: February 2026

**8. Minimum Lump Sum Investment**
- **Q**: What is the minimum lump sum investment for HDFC Flexi Cap Fund?
- **A**: The minimum lump sum investment for HDFC Flexi Cap Fund is ₹5,000.
- **Source**: [HDFC Flexi Cap KIM](https://files.hdfcfund.com/s3fs-public/KIM/2025-11/KIM%20-%20HDFC%20Flexi%20Cap%20Fund%20dated%20November%2021,%202025_1.pdf)
- **Last updated from sources**: February 2026

**9. Fund Category**
- **Q**: What category does HDFC Small Cap Fund belong to?
- **A**: HDFC Small Cap Fund is categorized as an Equity Scheme - Small Cap Fund.
- **Source**: [HDFC Small Cap Page](https://www.hdfcfund.com/explore/mutual-funds/hdfc-small-cap-fund/direct)
- **Last updated from sources**: February 2026

**10. Tax Benefits**
- **Q**: What tax benefits does HDFC ELSS Tax Saver offer?
- **A**: HDFC ELSS Tax Saver offers tax deduction under Section 80C of the Income Tax Act, up to ₹1.5 lakh per financial year.
- **Source**: [HDFC ELSS Page](https://www.hdfcfund.com/explore/mutual-funds/hdfc-elss-tax-saver/direct)
- **Last updated from sources**: February 2026

### Refusal Logic (Advice Questions)

**11. Performance Opinion**
- **Q**: Is HDFC Small Cap Fund a good investment right now?
- **A**: I can only provide facts about mutual fund schemes, not investment advice. For personalized recommendations, please consult a SEBI-registered financial advisor.
- **Refusal Source**: [SEBI Investor Education](https://investor.sebi.gov.in/)

**12. Comparison**
- **Q**: Should I buy HDFC Flexi Cap or HDFC Large Cap?
- **A**: I cannot compare funds or provide investment advice. I can only share factual details like expense ratios or past benchmarks for individual schemes.
- **Refusal Source**: [AMFI Knowledge Center](https://www.amfiindia.com/)

**13. Prediction**
- **Q**: Will HDFC ELSS Tax Saver give 15% returns next year?
- **A**: I cannot predict future returns or provide performance guarantees. Mutual fund investments are subject to market risks.
- **Refusal Source**: [SEBI Risk Factors](https://www.sebi.gov.in/sebi_data/faqfiles/sep-2024/1727242783639.pdf)

**14. Portfolio Allocation**
- **Q**: How much of my portfolio should I allocate to HDFC Balanced Advantage Fund?
- **A**: I cannot provide portfolio allocation advice. Please consult a SEBI-registered investment advisor for personalized portfolio recommendations.
- **Refusal Source**: [SEBI Investor Education](https://investor.sebi.gov.in/)

**15. Investment Timing**
- **Q**: When is the best time to invest in HDFC Small Cap Fund?
- **A**: I cannot provide timing advice or market predictions. For investment strategy guidance, please consult a qualified financial advisor.
- **Refusal Source**: [AMFI Investor Corner](https://www.amfiindia.com/investor-corner)
