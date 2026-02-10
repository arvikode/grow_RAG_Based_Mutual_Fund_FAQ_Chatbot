"""
Unit tests for embeddings.py module.
Tests embedding function initialization and generation.
"""
import os
import sys
import pytest
import numpy as np

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.embeddings import get_embedding_function


class TestEmbeddings:
    """Test suite for embeddings module."""
    
    def test_get_embedding_function_returns_instance(self):
        """Test that get_embedding_function returns an embeddings instance."""
        embeddings = get_embedding_function()
        
        assert embeddings is not None
        assert hasattr(embeddings, 'embed_documents')
        assert hasattr(embeddings, 'embed_query')
    
    def test_embedding_function_is_singleton(self):
        """Test that multiple calls return the same type of instance."""
        embeddings1 = get_embedding_function()
        embeddings2 = get_embedding_function()
        
        # Both should be the same class type
        assert type(embeddings1) == type(embeddings2)
    
    def test_embed_query(self):
        """Test embedding a single query string."""
        embeddings = get_embedding_function()
        
        query = "What is the expense ratio?"
        embedding = embeddings.embed_query(query)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
        assert all(isinstance(x, float) for x in embedding)
    
    def test_embed_documents(self):
        """Test embedding multiple documents."""
        embeddings = get_embedding_function()
        
        documents = [
            "HDFC Flexi Cap Fund",
            "Expense ratio is 1.05%",
            "Exit load is 1%"
        ]
        
        doc_embeddings = embeddings.embed_documents(documents)
        
        assert isinstance(doc_embeddings, list)
        assert len(doc_embeddings) == 3
        assert all(isinstance(emb, list) for emb in doc_embeddings)
        assert all(len(emb) > 0 for emb in doc_embeddings)
    
    def test_embedding_dimensions_consistent(self):
        """Test that embeddings have consistent dimensions."""
        embeddings = get_embedding_function()
        
        query1 = "Short query"
        query2 = "This is a much longer query with more words"
        
        emb1 = embeddings.embed_query(query1)
        emb2 = embeddings.embed_query(query2)
        
        # Embeddings should have same dimension regardless of input length
        assert len(emb1) == len(emb2)
    
    def test_embedding_similarity(self):
        """Test that similar texts have similar embeddings."""
        embeddings = get_embedding_function()
        
        text1 = "HDFC mutual fund expense ratio"
        text2 = "HDFC fund expense ratio"
        text3 = "Weather forecast for tomorrow"
        
        emb1 = embeddings.embed_query(text1)
        emb2 = embeddings.embed_query(text2)
        emb3 = embeddings.embed_query(text3)
        
        # Calculate cosine similarity
        def cosine_similarity(a, b):
            a = np.array(a)
            b = np.array(b)
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        sim_1_2 = cosine_similarity(emb1, emb2)
        sim_1_3 = cosine_similarity(emb1, emb3)
        
        # Similar texts should have higher similarity
        assert sim_1_2 > sim_1_3
        assert sim_1_2 > 0.7  # Should be quite similar
    
    def test_empty_string_handling(self):
        """Test handling of empty strings."""
        embeddings = get_embedding_function()
        
        # Should not crash on empty string
        embedding = embeddings.embed_query("")
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
    
    def test_special_characters_handling(self):
        """Test handling of special characters."""
        embeddings = get_embedding_function()
        
        text_with_special = "Expense ratio: 1.05% (₹100 minimum)"
        embedding = embeddings.embed_query(text_with_special)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0
    
    def test_long_text_handling(self):
        """Test handling of very long text."""
        embeddings = get_embedding_function()
        
        # Create a long text (but within model limits)
        long_text = " ".join(["word"] * 500)
        embedding = embeddings.embed_query(long_text)
        
        assert isinstance(embedding, list)
        assert len(embedding) > 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
