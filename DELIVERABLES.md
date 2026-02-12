# Deliverables for Milestone 1 Submission

## 1. Working Prototype Link
- **Streamlit App**: [Your App Link Here] (Deploy via Streamlit Cloud)
- **Alt**: Local video demo (≤3 min) if hosting is not possible.

## 2. Source List
- **File**: `official-urls.csv`
- **Location**: Root directory
- **Description**: Contains 27 validated official URLs from HDFC, SEBI, AMFI, and NISM.

## 3. README
- **File**: `README.md`
- **Location**: Root directory
- **Content**: Setup steps, Scope (5 HDFC schemes), and Known Limitations.

## 4. Sample Q&A File
- **File**: `sample_qa.md`
- **Location**: `tests/sample_qa.md`
- **Content**: 15 sample questions and answers (10 factual, 5 refusals) with citations.

## 5. Disclaimer Snippet
- **File**: `disclaimer.txt`
- **Location**: Root directory
- **Content**: Exact text used in the chatbot UI for the disclaimer.

## Submission Checklist
- [ ] Deploy app to Streamlit Cloud and get the link.
- [ ] Verify `official-urls.csv` is up to date (run `python src/url_validator.py` if unsure).
- [ ] Verify `tests/sample_qa.md` matches `src/app.py` logic.
- [ ] Zip the following files if direct file upload is required:
    - `official-urls.csv`
    - `README.md`
    - `tests/sample_qa.md`
    - `disclaimer.txt`
