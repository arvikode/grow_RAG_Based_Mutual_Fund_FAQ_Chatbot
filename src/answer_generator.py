"""
Answer generator module that integrates retrieval and LLM.
Provides end-to-end question answering with source citations.
"""
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from .retrieval import Retriever
from .llm import LLM


class AnswerGenerator:
    """
    Generates answers to questions using RAG (Retrieval-Augmented Generation).
    Combines document retrieval with LLM generation.
    """
    
    def __init__(
        self,
        retriever: Optional[Retriever] = None,
        llm: Optional[LLM] = None,
        k: int = 3
    ):
        """
        Initialize answer generator.
        
        Args:
            retriever: Retriever instance (creates new if None)
            llm: LLM instance (creates new if None)
            k: Number of documents to retrieve
        """
        self.retriever = retriever or Retriever(k=k)
        self.llm = llm or LLM()
        self.k = k
    
    def generate_answer(
        self,
        question: str,
        k: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> Dict:
        """
        Generate an answer to a question using RAG.
        
        Args:
            question: User's question
            k: Number of documents to retrieve (overrides default)
            temperature: LLM temperature (overrides default)
            
        Returns:
            Dictionary containing:
                - question: Original question
                - answer: Generated answer
                - sources: List of source metadata
                - timestamp: When the answer was generated
                - retrieved_docs: Number of documents retrieved
        """
        # Retrieve relevant documents
        num_docs = k if k is not None else self.k
        context, sources = self.retriever.retrieve_and_format(question, k=num_docs)
        
        # Check if we have any relevant information
        if not sources:
            return {
                "question": question,
                "answer": "I don't have enough information to answer this question. Please try rephrasing or ask about a different topic.",
                "sources": [],
                "timestamp": datetime.now().isoformat(),
                "retrieved_docs": 0
            }
        
        # Create prompt and generate answer
        prompt = self.llm.create_prompt(question, context, sources)
        
        try:
            answer = self.llm.generate(prompt, temperature=temperature)
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error generating answer: {str(e)}",
                "sources": sources,
                "timestamp": datetime.now().isoformat(),
                "retrieved_docs": len(sources),
                "error": str(e)
            }
        
        return {
            "question": question,
            "answer": answer,
            "sources": sources,
            "timestamp": datetime.now().isoformat(),
            "retrieved_docs": len(sources)
        }
    
    def format_response(self, result: Dict) -> str:
        """
        Format the answer result as a human-readable string.
        
        Args:
            result: Result dictionary from generate_answer()
            
        Returns:
            Formatted response string
        """
        output = []
        output.append(f"Question: {result['question']}")
        output.append("")
        output.append(result['answer'])
        output.append("")
        
        if result.get('sources'):
            output.append("Sources:")
            for i, source in enumerate(result['sources'], 1):
                output.append(f"  [{i}] {source['scheme']} - {source['url']}")
                if source.get('description'):
                    output.append(f"      {source['description']}")
                output.append(f"      Relevance: {source['relevance_score']:.4f}")
        
        output.append("")
        output.append(f"Retrieved {result['retrieved_docs']} relevant documents")
        output.append(f"Generated at: {result['timestamp']}")
        
        return "\n".join(output)
    
    def answer_questions(self, questions: List[str]) -> List[Dict]:
        """
        Answer multiple questions in batch.
        
        Args:
            questions: List of questions
            
        Returns:
            List of answer result dictionaries
        """
        results = []
        for question in questions:
            result = self.generate_answer(question)
            results.append(result)
        return results


def get_answer_generator(k: int = 3) -> AnswerGenerator:
    """
    Get AnswerGenerator instance with default configuration.
    
    Args:
        k: Number of documents to retrieve
        
    Returns:
        Configured AnswerGenerator instance
    """
    return AnswerGenerator(k=k)


if __name__ == "__main__":
    # Test the answer generator
    import sys
    
    try:
        generator = get_answer_generator()
        
        # Test questions
        test_questions = [
            "What is the expense ratio of HDFC Flexi Cap Fund?",
            "What is the exit load for HDFC Large Cap Fund?",
            "What is the minimum SIP amount for HDFC Small Cap Fund?"
        ]
        
        print("Testing Answer Generator...")
        print("=" * 80)
        
        for question in test_questions:
            print(f"\nQuestion: {question}")
            result = generator.generate_answer(question)
            print(generator.format_response(result))
            print("=" * 80)
            
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
