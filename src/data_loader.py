import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
from io import BytesIO
import pypdf
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

class DataLoader:
    def __init__(self, urls_csv_path="official-urls.csv"):
        self.urls_csv_path = urls_csv_path
        self.chunk_size = 1000
        self.chunk_overlap = 200

    def load_urls(self):
        """Read URLs from CSV file."""
        if not os.path.exists(self.urls_csv_path):
            raise FileNotFoundError(f"URL list not found at {self.urls_csv_path}")
        return pd.read_csv(self.urls_csv_path)

    def fetch_pdf_content(self, url):
        """Download and extract text from a PDF URL."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            with BytesIO(response.content) as f:
                reader = pypdf.PdfReader(f)
                text = ""
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            print(f"Error fetching PDF {url}: {e}")
            return ""

    def fetch_html_content(self, url):
        """Fetch and parse text from an HTML URL."""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove scripts and styles
            for script in soup(["script", "style", "nav", "footer"]):
                script.decompose()
                
            text = soup.get_text(separator=' ')
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            return text
        except Exception as e:
            print(f"Error fetching HTML {url}: {e}")
            return ""

    def process_url(self, row):
        """Process a single URL row from the CSV."""
        url = row['url']
        scheme = row['scheme']
        description = row['description']
        
        print(f"Processing: {url}")
        
        content = ""
        if url.lower().endswith('.pdf'):
            content = self.fetch_pdf_content(url)
        else:
            content = self.fetch_html_content(url)
            
        if not content:
            return []
            
        # Create metadata
        metadata = {
            "source": url,
            "scheme": scheme,
            "description": description
        }
        
        return self.split_text(content, metadata)

    def split_text(self, text, metadata):
        """Split text into chunks with metadata."""
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=self.chunk_size,
            chunk_overlap=self.chunk_overlap,
            length_function=len,
        )
        docs = text_splitter.create_documents([text], metadatas=[metadata])
        return docs

    def load_and_process_all(self):
        """Main method to load all data."""
        df = self.load_urls()
        all_docs = []
        
        for _, row in df.iterrows():
            docs = self.process_url(row)
            all_docs.extend(docs)
            
        print(f"Total documents processed: {len(all_docs)}")
        return all_docs

if __name__ == "__main__":
    # Test run
    loader = DataLoader()
    docs = loader.load_and_process_all()
    if docs:
        print(f"Sample chunk: {docs[0].page_content[:200]}")
