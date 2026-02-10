"""
Unit tests for data_loader.py module.
Tests document loading, chunking, and metadata handling.
"""
import os
import sys
import pytest
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.data_loader import DataLoader


class TestDataLoader:
    """Test suite for DataLoader class."""
    
    @pytest.fixture
    def data_loader(self):
        """Create a DataLoader instance for testing."""
        return DataLoader(urls_csv_path="test_urls.csv")
    
    @pytest.fixture
    def sample_csv_data(self, tmp_path):
        """Create a temporary CSV file for testing."""
        csv_file = tmp_path / "test_urls.csv"
        csv_content = """scheme,url,description,date_accessed
Test Scheme,https://example.com/test.pdf,Test PDF,2026-02-10
Test Scheme,https://example.com/page,Test Page,2026-02-10"""
        csv_file.write_text(csv_content)
        return str(csv_file)
    
    def test_init(self, data_loader):
        """Test DataLoader initialization."""
        assert data_loader.urls_csv_path == "test_urls.csv"
        assert data_loader.chunk_size == 1000
        assert data_loader.chunk_overlap == 200
    
    def test_load_urls_file_not_found(self, data_loader):
        """Test load_urls raises error when file doesn't exist."""
        with pytest.raises(FileNotFoundError):
            data_loader.load_urls()
    
    def test_load_urls_success(self, tmp_path):
        """Test successful URL loading from CSV."""
        csv_file = tmp_path / "test_urls.csv"
        csv_content = """scheme,url,description,date_accessed
Scheme1,https://example.com,Test,2026-02-10"""
        csv_file.write_text(csv_content)
        
        loader = DataLoader(urls_csv_path=str(csv_file))
        df = loader.load_urls()
        
        assert len(df) == 1
        assert df.iloc[0]['scheme'] == 'Scheme1'
        assert df.iloc[0]['url'] == 'https://example.com'
    
    @patch('src.data_loader.requests.get')
    @patch('src.data_loader.pypdf.PdfReader')
    def test_fetch_pdf_content_success(self, mock_pdf_reader, mock_get, data_loader):
        """Test successful PDF content extraction."""
        # Mock HTTP response
        mock_response = Mock()
        mock_response.content = b"fake pdf content"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        # Mock PDF reader
        mock_page = Mock()
        mock_page.extract_text.return_value = "Test PDF content"
        mock_reader_instance = Mock()
        mock_reader_instance.pages = [mock_page]
        mock_pdf_reader.return_value = mock_reader_instance
        
        content = data_loader.fetch_pdf_content("https://example.com/test.pdf")
        
        assert "Test PDF content" in content
        mock_get.assert_called_once()
    
    @patch('src.data_loader.requests.get')
    def test_fetch_pdf_content_error(self, mock_get, data_loader):
        """Test PDF fetch handles errors gracefully."""
        mock_get.side_effect = Exception("Network error")
        
        content = data_loader.fetch_pdf_content("https://example.com/test.pdf")
        
        assert content == ""
    
    @patch('src.data_loader.requests.get')
    def test_fetch_html_content_success(self, mock_get, data_loader):
        """Test successful HTML content extraction."""
        mock_response = Mock()
        mock_response.content = b"<html><body><p>Test content</p></body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        content = data_loader.fetch_html_content("https://example.com")
        
        assert "Test content" in content
        mock_get.assert_called_once()
    
    @patch('src.data_loader.requests.get')
    def test_fetch_html_content_removes_scripts(self, mock_get, data_loader):
        """Test that scripts and styles are removed from HTML."""
        mock_response = Mock()
        mock_response.content = b"""
        <html>
            <head><script>alert('test')</script></head>
            <body>
                <p>Keep this</p>
                <script>remove this</script>
                <style>remove this too</style>
            </body>
        </html>
        """
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response
        
        content = data_loader.fetch_html_content("https://example.com")
        
        assert "Keep this" in content
        assert "alert" not in content
        assert "remove this" not in content
    
    @patch('src.data_loader.requests.get')
    def test_fetch_html_content_error(self, mock_get, data_loader):
        """Test HTML fetch handles errors gracefully."""
        mock_get.side_effect = Exception("Network error")
        
        content = data_loader.fetch_html_content("https://example.com")
        
        assert content == ""
    
    def test_split_text(self, data_loader):
        """Test text splitting into chunks."""
        text = "A" * 2500  # Create text longer than chunk_size
        metadata = {"source": "test", "scheme": "Test"}
        
        docs = data_loader.split_text(text, metadata)
        
        assert len(docs) > 1  # Should be split into multiple chunks
        assert all(len(doc.page_content) <= 1000 for doc in docs)
        assert all(doc.metadata == metadata for doc in docs)
    
    def test_split_text_short_content(self, data_loader):
        """Test splitting short text (single chunk)."""
        text = "Short text"
        metadata = {"source": "test"}
        
        docs = data_loader.split_text(text, metadata)
        
        assert len(docs) == 1
        assert docs[0].page_content == text
        assert docs[0].metadata == metadata
    
    @patch.object(DataLoader, 'fetch_pdf_content')
    def test_process_url_pdf(self, mock_fetch_pdf, data_loader):
        """Test processing a PDF URL."""
        mock_fetch_pdf.return_value = "PDF content here"
        
        row = {
            'url': 'https://example.com/test.pdf',
            'scheme': 'Test Scheme',
            'description': 'Test PDF'
        }
        
        docs = data_loader.process_url(row)
        
        assert len(docs) > 0
        assert docs[0].metadata['source'] == 'https://example.com/test.pdf'
        assert docs[0].metadata['scheme'] == 'Test Scheme'
        mock_fetch_pdf.assert_called_once()
    
    @patch.object(DataLoader, 'fetch_html_content')
    def test_process_url_html(self, mock_fetch_html, data_loader):
        """Test processing an HTML URL."""
        mock_fetch_html.return_value = "HTML content here"
        
        row = {
            'url': 'https://example.com/page',
            'scheme': 'Test Scheme',
            'description': 'Test Page'
        }
        
        docs = data_loader.process_url(row)
        
        assert len(docs) > 0
        assert docs[0].metadata['source'] == 'https://example.com/page'
        mock_fetch_html.assert_called_once()
    
    @patch.object(DataLoader, 'fetch_html_content')
    def test_process_url_empty_content(self, mock_fetch_html, data_loader):
        """Test processing URL with empty content."""
        mock_fetch_html.return_value = ""
        
        row = {
            'url': 'https://example.com/empty',
            'scheme': 'Test',
            'description': 'Empty'
        }
        
        docs = data_loader.process_url(row)
        
        assert docs == []
    
    @patch.object(DataLoader, 'load_urls')
    @patch.object(DataLoader, 'process_url')
    def test_load_and_process_all(self, mock_process_url, mock_load_urls, data_loader):
        """Test loading and processing all URLs."""
        # Mock CSV data
        import pandas as pd
        mock_df = pd.DataFrame([
            {'url': 'https://example.com/1', 'scheme': 'S1', 'description': 'D1'},
            {'url': 'https://example.com/2', 'scheme': 'S2', 'description': 'D2'}
        ])
        mock_load_urls.return_value = mock_df
        
        # Mock document processing
        from langchain_core.documents import Document
        mock_process_url.return_value = [
            Document(page_content="test", metadata={"source": "test"})
        ]
        
        docs = data_loader.load_and_process_all()
        
        assert len(docs) == 2  # 2 URLs, each returning 1 doc
        assert mock_process_url.call_count == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
