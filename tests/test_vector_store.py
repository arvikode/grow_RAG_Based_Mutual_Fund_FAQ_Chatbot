"""
Unit tests for vector_store.py module.
Tests FAISS vector store operations.
"""
import os
import sys
import pytest
import shutil
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.vector_store import VectorStore
from langchain_core.documents import Document


class TestVectorStore:
    """Test suite for VectorStore class."""
    
    @pytest.fixture
    def vector_store(self, tmp_path):
        """Create a VectorStore instance with temporary path."""
        # Use a temporary directory for testing
        test_path = str(tmp_path / "test_faiss")
        
        with patch('src.vector_store.FAISS_PATH', test_path):
            vs = VectorStore()
            vs.faiss_path = test_path
            yield vs
            
            # Cleanup
            if os.path.exists(test_path):
                shutil.rmtree(test_path)
    
    @pytest.fixture
    def sample_documents(self):
        """Create sample documents for testing."""
        return [
            Document(
                page_content="HDFC Flexi Cap Fund has expense ratio of 1.05%",
                metadata={"source": "https://example.com/1", "scheme": "HDFC Flexi Cap"}
            ),
            Document(
                page_content="Exit load is 1% if redeemed within 1 year",
                metadata={"source": "https://example.com/2", "scheme": "HDFC Flexi Cap"}
            ),
            Document(
                page_content="Minimum SIP amount is Rs. 100",
                metadata={"source": "https://example.com/3", "scheme": "HDFC Flexi Cap"}
            )
        ]
    
    def test_init(self, vector_store):
        """Test VectorStore initialization."""
        assert vector_store.faiss_path is not None
        assert vector_store.embedding_function is not None
        assert vector_store._db is None
    
    def test_add_documents_creates_new_db(self, vector_store, sample_documents):
        """Test adding documents creates a new database."""
        count = vector_store.add_documents(sample_documents)
        
        assert count == 3
        assert os.path.exists(vector_store.faiss_path)
        assert vector_store._db is not None
    
    def test_add_documents_empty_list(self, vector_store):
        """Test adding empty document list."""
        count = vector_store.add_documents([])
        
        assert count == 0
    
    def test_add_documents_persists(self, vector_store, sample_documents):
        """Test that added documents are persisted to disk."""
        vector_store.add_documents(sample_documents)
        
        # Check that index files are created
        assert os.path.exists(vector_store.faiss_path)
        
        # Create new instance and verify it can load
        vs2 = VectorStore()
        vs2.faiss_path = vector_store.faiss_path
        db = vs2.get_db()
        
        assert db is not None
    
    def test_get_db_loads_existing(self, vector_store, sample_documents):
        """Test get_db loads existing database."""
        # Create database
        vector_store.add_documents(sample_documents)
        vector_store._db = None  # Reset internal reference
        
        # Load database
        db = vector_store.get_db()
        
        assert db is not None
    
    def test_get_db_returns_none_when_no_db(self, vector_store):
        """Test get_db returns None when no database exists."""
        db = vector_store.get_db()
        
        assert db is None
    
    def test_clear_removes_database(self, vector_store, sample_documents):
        """Test clear removes the database."""
        # Create database
        vector_store.add_documents(sample_documents)
        assert os.path.exists(vector_store.faiss_path)
        
        # Clear database
        vector_store.clear()
        
        assert not os.path.exists(vector_store.faiss_path)
        assert vector_store._db is None
    
    def test_clear_when_no_database(self, vector_store):
        """Test clear doesn't error when no database exists."""
        # Should not raise an error
        vector_store.clear()
        
        assert vector_store._db is None
    
    def test_query_returns_relevant_documents(self, vector_store, sample_documents):
        """Test querying returns relevant documents."""
        vector_store.add_documents(sample_documents)
        
        results = vector_store.query("What is the expense ratio?", k=2)
        
        assert len(results) <= 2
        assert all(isinstance(r, tuple) for r in results)
        assert all(len(r) == 2 for r in results)  # (doc, score) tuples
    
    def test_query_empty_database(self, vector_store):
        """Test querying empty database returns empty list."""
        results = vector_store.query("test query")
        
        assert results == []
    
    def test_query_k_parameter(self, vector_store, sample_documents):
        """Test query respects k parameter."""
        vector_store.add_documents(sample_documents)
        
        results_k1 = vector_store.query("expense ratio", k=1)
        results_k2 = vector_store.query("expense ratio", k=2)
        
        assert len(results_k1) == 1
        assert len(results_k2) == 2
    
    def test_query_relevance_scores(self, vector_store, sample_documents):
        """Test query returns relevance scores."""
        vector_store.add_documents(sample_documents)
        
        results = vector_store.query("expense ratio", k=3)
        
        # Check that scores are present
        # Note: FAISS similarity scores can be outside 0-1 range (cosine similarity)
        import numpy as np
        for doc, score in results:
            assert isinstance(score, (int, float, np.number))
            assert score is not None
    
    def test_query_returns_documents_with_metadata(self, vector_store, sample_documents):
        """Test query returns documents with metadata."""
        vector_store.add_documents(sample_documents)
        
        results = vector_store.query("expense ratio", k=1)
        
        doc, score = results[0]
        assert hasattr(doc, 'metadata')
        assert 'source' in doc.metadata
        assert 'scheme' in doc.metadata
    
    def test_add_documents_to_existing_db(self, vector_store, sample_documents):
        """Test adding documents to existing database."""
        # Add initial documents
        vector_store.add_documents(sample_documents[:2])
        
        # Add more documents
        new_docs = [sample_documents[2]]
        count = vector_store.add_documents(new_docs)
        
        assert count == 1
        
        # Verify all documents are searchable
        results = vector_store.query("SIP", k=5)
        assert len(results) > 0
    
    def test_multiple_queries_same_db(self, vector_store, sample_documents):
        """Test multiple queries on the same database."""
        vector_store.add_documents(sample_documents)
        
        results1 = vector_store.query("expense ratio", k=1)
        results2 = vector_store.query("exit load", k=1)
        results3 = vector_store.query("SIP amount", k=1)
        
        assert len(results1) > 0
        assert len(results2) > 0
        assert len(results3) > 0
        
        # Different queries should return different top results
        assert results1[0][0].page_content != results2[0][0].page_content


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
