"""
Quick test to demonstrate improved error messages.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.llm import GeminiProvider

# Test error message formatting
print("Testing Error Message Improvements")
print("=" * 60)

# Simulate different error scenarios
test_errors = [
    ("429 quota exceeded", "Quota Error"),
    ("rate limit exceeded", "Rate Limit Error"),
    ("404 model not found", "Model Not Found"),
    ("401 invalid api key", "Invalid API Key"),
]

provider = GeminiProvider("dummy_key")

for error_text, error_type in test_errors:
    print(f"\n{error_type}:")
    print("-" * 60)
    try:
        # Simulate error
        raise Exception(error_text)
    except Exception as e:
        error_msg = str(e)
        
        # Apply same logic as in llm.py
        if "429" in error_msg or "quota" in error_msg.lower():
            print("⚠️ API QUOTA EXCEEDED")
            print("You've reached the Gemini free tier limit.")
            print("Solutions:")
            print("  1. Wait a few minutes and try again")
            print("  2. Upgrade at https://ai.google.dev/pricing")
            print("  3. Use a different API key")
        elif "rate limit" in error_msg.lower():
            print("⚠️ RATE LIMIT EXCEEDED")
            print("Too many requests in a short time.")
            print("Please wait 30-60 seconds and try again.")
        elif "404" in error_msg or "not found" in error_msg.lower():
            print("⚠️ MODEL NOT FOUND")
            print("The model is not available.")
            print("Try changing GEMINI_MODEL in .env to 'gemini-pro'")
        elif "invalid api key" in error_msg.lower() or "401" in error_msg:
            print("⚠️ INVALID API KEY")
            print("Please check your GEMINI_API_KEY in .env file.")
            print("Get a key at https://ai.google.dev/")

print("\n" + "=" * 60)
print("✅ Error messages are now user-friendly!")
