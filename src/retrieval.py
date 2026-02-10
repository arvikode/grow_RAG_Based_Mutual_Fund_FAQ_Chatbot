from .vector_store import VectorStore

class Retriever:
    def __init__(self, k=3):
        """
        Initialize the retriever.
        
        Args:
            k: Number of top documents to retrieve
        """
        self.vector_store = VectorStore()
        self.k = k
    
    def retrieve(self, query: str, k: int = None):
        """
        Retrieve relevant documents for a query.
        
        Args:
            query: The user's question
            k: Number of documents to retrieve (overrides default)
            
        Returns:
            List of tuples (document, relevance_score)
        """
        k = k or self.k
        results = self.vector_store.query(query, k=k)
        return results
    
    def format_context(self, results):
        """
        Format retrieved documents into context for LLM.
        
        Args:
            results: List of (document, score) tuples from retrieve()
            
        Returns:
            Formatted string with context and sources
        """
        if not results:
            return "No relevant information found.", []
        
        context_parts = []
        sources = []
        
        for i, (doc, score) in enumerate(results, 1):
            # Extract content and metadata
            content = doc.page_content
            source_url = doc.metadata.get('source', 'Unknown')
            scheme = doc.metadata.get('scheme', 'General')
            description = doc.metadata.get('description', '')
            
            # Format context chunk
            context_parts.append(f"[Source {i}]\n{content}\n")
            
            # Store source info
            sources.append({
                'url': source_url,
                'scheme': scheme,
                'description': description,
                'relevance_score': score
            })
        
        context = "\n---\n".join(context_parts)
        return context, sources
    
    def retrieve_and_format(self, query: str, k: int = None):
        """
        Retrieve documents and format them for LLM consumption.
        
        Args:
            query: The user's question
            k: Number of documents to retrieve
            
        Returns:
            Tuple of (formatted_context, sources_list)
        """
        results = self.retrieve(query, k)
        return self.format_context(results)

if __name__ == "__main__":
    # Test the retriever
    retriever = Retriever(k=3)
    
    test_query = "What is the expense ratio of HDFC Flexi Cap Fund?"
    print(f"Query: {test_query}\n")
    
    context, sources = retriever.retrieve_and_format(test_query)
    
    print("Context for LLM:")
    print(context)
    print("\n" + "="*80 + "\n")
    print("Sources:")
    for i, source in enumerate(sources, 1):
        print(f"{i}. {source['scheme']} - {source['description']}")
        print(f"   URL: {source['url']}")
        print(f"   Relevance: {source['relevance_score']:.4f}\n")
