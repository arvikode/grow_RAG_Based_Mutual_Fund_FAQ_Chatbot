"""
Unit tests for retrieval.py module.
Tests document retrieval and context formatting.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.retrieval import Retriever
from langchain_core.documents import Document


class TestRetriever:
    """Test suite for Retriever class."""
    
    @pytest.fixture
    def retriever(self):
        """Create a Retriever instance for testing."""
        return Retriever(k=3)
    
    @pytest.fixture
    def sample_results(self):
        """Create sample retrieval results."""
        return [
            (
                Document(
                    page_content="HDFC Flexi Cap Fund has expense ratio of 1.05%",
                    metadata={
                        "source": "https://example.com/flexi-cap",
                        "scheme": "HDFC Flexi Cap Fund",
                        "description": "Scheme details page"
                    }
                ),
                0.85
            ),
            (
                Document(
                    page_content="The fund charges an annual expense ratio",
                    metadata={
                        "source": "https://example.com/kim.pdf",
                        "scheme": "HDFC Flexi Cap Fund",
                        "description": "KIM PDF"
                    }
                ),
                0.72
            ),
            (
                Document(
                    page_content="Management fees are included in expense ratio",
                    metadata={
                        "source": "https://example.com/general",
                        "scheme": "General Resources",
                        "description": "SEBI FAQs"
                    }
                ),
                0.65
            )
        ]
    
    def test_init_default_k(self):
        """Test Retriever initialization with default k."""
        retriever = Retriever()
        
        assert retriever.k == 3
        assert retriever.vector_store is not None
    
    def test_init_custom_k(self):
        """Test Retriever initialization with custom k."""
        retriever = Retriever(k=5)
        
        assert retriever.k == 5
    
    @patch('src.retrieval.VectorStore')
    def test_retrieve_calls_vector_store(self, mock_vs_class, retriever):
        """Test retrieve method calls vector store query."""
        mock_vs_instance = Mock()
        mock_vs_instance.query.return_value = []
        retriever.vector_store = mock_vs_instance
        
        retriever.retrieve("test query", k=2)
        
        mock_vs_instance.query.assert_called_once_with("test query", k=2)
    
    @patch('src.retrieval.VectorStore')
    def test_retrieve_uses_default_k(self, mock_vs_class, retriever):
        """Test retrieve uses default k when not specified."""
        mock_vs_instance = Mock()
        mock_vs_instance.query.return_value = []
        retriever.vector_store = mock_vs_instance
        
        retriever.retrieve("test query")
        
        mock_vs_instance.query.assert_called_once_with("test query", k=3)
    
    def test_format_context_empty_results(self, retriever):
        """Test format_context with empty results."""
        context, sources = retriever.format_context([])
        
        assert context == "No relevant information found."
        assert sources == []
    
    def test_format_context_single_result(self, retriever, sample_results):
        """Test format_context with single result."""
        context, sources = retriever.format_context([sample_results[0]])
        
        assert "[Source 1]" in context
        assert "expense ratio of 1.05%" in context
        assert len(sources) == 1
        assert sources[0]['url'] == "https://example.com/flexi-cap"
        assert sources[0]['scheme'] == "HDFC Flexi Cap Fund"
        assert sources[0]['relevance_score'] == 0.85
    
    def test_format_context_multiple_results(self, retriever, sample_results):
        """Test format_context with multiple results."""
        context, sources = retriever.format_context(sample_results)
        
        assert "[Source 1]" in context
        assert "[Source 2]" in context
        assert "[Source 3]" in context
        assert "---" in context  # Separator between sources
        assert len(sources) == 3
    
    def test_format_context_preserves_metadata(self, retriever, sample_results):
        """Test format_context preserves all metadata."""
        context, sources = retriever.format_context(sample_results)
        
        for i, source in enumerate(sources):
            assert 'url' in source
            assert 'scheme' in source
            assert 'description' in source
            assert 'relevance_score' in source
            assert source['relevance_score'] == sample_results[i][1]
    
    def test_format_context_handles_missing_metadata(self, retriever):
        """Test format_context handles missing metadata gracefully."""
        results = [
            (
                Document(
                    page_content="Test content",
                    metadata={}  # Empty metadata
                ),
                0.5
            )
        ]
        
        context, sources = retriever.format_context(results)
        
        assert len(sources) == 1
        assert sources[0]['url'] == 'Unknown'
        assert sources[0]['scheme'] == 'General'
        assert sources[0]['description'] == ''
    
    @patch.object(Retriever, 'retrieve')
    @patch.object(Retriever, 'format_context')
    def test_retrieve_and_format(self, mock_format, mock_retrieve, retriever):
        """Test retrieve_and_format combines both operations."""
        mock_results = [Mock(), Mock()]
        mock_retrieve.return_value = mock_results
        mock_format.return_value = ("formatted context", [{"url": "test"}])
        
        context, sources = retriever.retrieve_and_format("test query", k=2)
        
        mock_retrieve.assert_called_once_with("test query", 2)
        mock_format.assert_called_once_with(mock_results)
        assert context == "formatted context"
        assert sources == [{"url": "test"}]
    
    @patch.object(Retriever, 'retrieve')
    def test_retrieve_and_format_uses_default_k(self, mock_retrieve, retriever):
        """Test retrieve_and_format uses default k."""
        mock_retrieve.return_value = []
        
        retriever.retrieve_and_format("test query")
        
        mock_retrieve.assert_called_once_with("test query", None)
    
    def test_format_context_content_structure(self, retriever, sample_results):
        """Test format_context creates proper structure."""
        context, sources = retriever.format_context(sample_results)
        
        # Check structure
        lines = context.split('\n')
        source_markers = [line for line in lines if line.startswith('[Source')]
        
        assert len(source_markers) == 3
        assert all(f"[Source {i+1}]" in context for i in range(3))
    
    def test_format_context_separator(self, retriever, sample_results):
        """Test format_context uses separator between sources."""
        context, sources = retriever.format_context(sample_results)
        
        # Should have 2 separators for 3 sources
        separator_count = context.count('\n---\n')
        assert separator_count == 2
    
    def test_sources_ordered_by_relevance(self, retriever, sample_results):
        """Test sources maintain order from retrieval."""
        context, sources = retriever.format_context(sample_results)
        
        # Sources should be in same order as input
        assert sources[0]['relevance_score'] == 0.85
        assert sources[1]['relevance_score'] == 0.72
        assert sources[2]['relevance_score'] == 0.65
    
    def test_format_context_includes_full_content(self, retriever, sample_results):
        """Test format_context includes full document content."""
        context, sources = retriever.format_context(sample_results)
        
        # All content should be present
        assert "expense ratio of 1.05%" in context
        assert "annual expense ratio" in context
        assert "Management fees" in context


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
