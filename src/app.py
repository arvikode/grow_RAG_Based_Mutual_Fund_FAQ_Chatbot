"""
Streamlit chatbot interface for Mutual Fund RAG FAQ.
Provides a user-friendly chat interface with guardrails and source citations.
"""
import streamlit as st
import sys
import os
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from guardrails import get_guardrails
from answer_generator import get_answer_generator


# Page configuration
st.set_page_config(
    page_title="Mutual Fund FAQ Chatbot",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        text-align: center;
        margin-bottom: 2rem;
    }
    .disclaimer {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        padding: 1rem;
        margin: 1rem 0;
        border-radius: 4px;
    }
    .example-question {
        background-color: #e7f3ff;
        padding: 0.5rem 1rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        cursor: pointer;
        border: 1px solid #b3d9ff;
    }
    .example-question:hover {
        background-color: #cce5ff;
    }
    .source-citation {
        background-color: #f8f9fa;
        padding: 0.5rem;
        margin: 0.5rem 0;
        border-radius: 4px;
        border-left: 3px solid #28a745;
        font-size: 0.9rem;
    }
    .refusal-message {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 4px;
        border-left: 4px solid #ffc107;
    }
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 2rem;
    }
    .bot-message {
        background-color: #f5f5f5;
        margin-right: 2rem;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'guardrails' not in st.session_state:
        st.session_state.guardrails = get_guardrails()
    if 'answer_generator' not in st.session_state:
        try:
            st.session_state.answer_generator = get_answer_generator(k=5)
        except Exception as e:
            st.error(f"Error initializing answer generator: {e}")
            st.session_state.answer_generator = None


def display_welcome():
    """Display welcome message and instructions."""
    st.markdown('<div class="main-header">💰 Mutual Fund FAQ Chatbot</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Get factual information about HDFC mutual fund schemes</div>', unsafe_allow_html=True)
    
    # Disclaimer
    st.markdown("""
    <div class="disclaimer">
        <strong>⚠️ Important Disclaimer:</strong><br>
        This chatbot provides <strong>factual information only</strong>. It does NOT provide investment advice or recommendations.
        For personalized investment advice, please consult a SEBI-registered investment advisor.
    </div>
    """, unsafe_allow_html=True)


def display_sidebar():
    """Display sidebar with information and examples."""
    with st.sidebar:
        st.header("📚 About")
        st.write("""
        This chatbot answers factual questions about 5 HDFC mutual fund schemes:
        - HDFC Flexi Cap Fund
        - HDFC Large Cap Fund
        - HDFC ELSS Tax Saver
        - HDFC Small Cap Fund
        - HDFC Balanced Advantage Fund
        """)
        
        st.header("✅ Example Questions")
        st.write("Click on any question to ask:")
        
        example_questions = st.session_state.guardrails.get_example_factual_questions()
        
        for i, question in enumerate(example_questions[:5]):
            if st.button(f"💬 {question}", key=f"example_{i}", use_container_width=True):
                st.session_state.current_question = question
        
        st.header("🚫 What I Cannot Do")
        st.write("""
        I cannot provide:
        - Investment recommendations
        - Advice on which fund to choose
        - Portfolio allocation suggestions
        - Predictions about returns
        - Timing advice for investments
        """)
        
        st.header("📖 Resources")
        st.markdown("""
        - [SEBI Investor Education](https://investor.sebi.gov.in/)
        - [AMFI Investor Corner](https://www.amfiindia.com/investor-corner)
        - [NISM FAQs](https://www.nism.ac.in/wp-content/uploads/2021/02/FAQsOnMfs-3-1.pdf)
        - [HDFC Total Expense Ratio](https://www.hdfcfund.com/statutory-disclosure/total-expense-ratio-of-mutual-fund-schemes/reports)
        - [HDFC Monthly Portfolios](https://www.hdfcfund.com/statutory-disclosure/portfolio/monthly-portfolio)
        - [SEBI Exit Load Guide](https://investor.sebi.gov.in/exit_load.html)
        """)


def display_chat_message(role, content, sources=None, is_refusal=False):
    """Display a chat message."""
    if role == "user":
        st.markdown(f'<div class="chat-message user-message"><strong>You:</strong><br>{content}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-message bot-message"><strong>Bot:</strong><br>{content}</div>', unsafe_allow_html=True)
        
        # Display sources if available
        if sources and len(sources) > 0:
            st.markdown("**📚 Sources:**")
            for i, source in enumerate(sources, 1):
                scheme = source.get('scheme', 'Unknown')
                url = source.get('url', '#')
                score = source.get('relevance_score', 0)
                st.markdown(f"""
                <div class="source-citation">
                    <strong>[{i}]</strong> {scheme}<br>
                    <a href="{url}" target="_blank">🔗 View Source</a> | Relevance: {score:.2f}
                </div>
                """, unsafe_allow_html=True)


def process_question(question):
    """Process a user question through guardrails and RAG pipeline."""
    # Check guardrails first
    is_advice, refusal_response = st.session_state.guardrails.check_and_respond(question)
    
    if is_advice:
        return refusal_response
    
    # Process through RAG pipeline
    if st.session_state.answer_generator is None:
        return {
            "question": question,
            "answer": "Error: Answer generator not initialized. Please check your configuration.",
            "sources": [],
            "timestamp": datetime.now().isoformat()
        }
    
    try:
        response = st.session_state.answer_generator.generate_answer(question)
        return response
    except Exception as e:
        return {
            "question": question,
            "answer": f"Error generating answer: {str(e)}",
            "sources": [],
            "timestamp": datetime.now().isoformat(),
            "error": str(e)
        }


def main():
    """Main application function."""
    initialize_session_state()
    display_welcome()
    display_sidebar()
    
    # Chat interface
    st.header("💬 Ask a Question")
    
    # Display chat history
    for message in st.session_state.messages:
        display_chat_message(
            message['role'],
            message['content'],
            message.get('sources'),
            message.get('is_refusal', False)
        )
    
    # Handle example question click
    if 'current_question' in st.session_state:
        question = st.session_state.current_question
        del st.session_state.current_question
        
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': question
        })
        
        # Process question
        with st.spinner('Thinking...'):
            response = process_question(question)
        
        # Add bot response
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response['answer'],
            'sources': response.get('sources', []),
            'is_refusal': response.get('is_advice_refusal', False)
        })
        
        st.rerun()
    
    # Chat input
    question = st.chat_input("Type your question here...")
    
    if question:
        # Add user message
        st.session_state.messages.append({
            'role': 'user',
            'content': question
        })
        
        # Process question
        with st.spinner('Thinking...'):
            response = process_question(question)
        
        # Add bot response
        st.session_state.messages.append({
            'role': 'assistant',
            'content': response['answer'],
            'sources': response.get('sources', []),
            'is_refusal': response.get('is_advice_refusal', False)
        })
        
        st.rerun()
    
    # Clear chat button
    if len(st.session_state.messages) > 0:
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.rerun()


if __name__ == "__main__":
    main()
