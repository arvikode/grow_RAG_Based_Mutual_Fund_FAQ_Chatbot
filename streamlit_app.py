"""
Streamlit app entry point for deployment.
This file is required by Streamlit Cloud in the root directory.
"""
import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import and run the main app
from app import main

if __name__ == "__main__":
    main()
