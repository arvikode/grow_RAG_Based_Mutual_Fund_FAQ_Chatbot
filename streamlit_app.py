"""
Streamlit app entry point for Streamlit Cloud deployment.
This file must be in the root directory as streamlit_app.py.
"""
import sys
import os

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the main app module
import app

# Streamlit will automatically run the app.py module
# No need to call main() explicitly - Streamlit handles this
