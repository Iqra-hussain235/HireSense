"""
Test script to check Gemini API key validity with new SDK
"""
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')
model_name = os.getenv('GEMINI_MODEL', 'gemini-2.0-flash')

print("=" * 60)
print("GEMINI API KEY TEST (NEW SDK)")
print("=" * 60)
print(f"Using model: {model_name}")

# Check if API key exists
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print("\nPlease add your API key to the .env file:")
    print("GEMINI_API_KEY=your_actual_api_key_here")
    exit(1)

print("✓ API Key found in environment")

# Configure Gemini with new SDK
try:
    client = genai.Client(api_key=api_key)
    print("✓ Gemini client initialized successfully")
except Exception as e:
    print(f"❌ ERROR initializing Gemini client: {e}")
    exit(1)

# Test API connection
print("\nTesting API connection...")
try:
    # List available models
    models = client.models.list()
    model_list = list(models)
    print(f"✓ Found {len(model_list)} available models")
    
    for model in model_list[:10]:  # Show first 10 models
        print(f"  - {model.name}")
except Exception as e:
    print(f"❌ ERROR listing models: {e}")
    print(f"\nError details: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    exit(1)

# Test content generation
print("\nTesting content generation...")
try:
    response = client.models.generate_content(
        model=model_name,
        contents="Hello, please respond with 'API is working'"
    )
    print(f"✓ Content generation successful")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"❌ ERROR generating content: {e}")
    print(f"\nError details: {type(e).__name__}")
    print(f"Error message: {str(e)}")
    
    # Check if it's an API key error
    if "API key" in str(e).lower() or "invalid" in str(e).lower():
        print("\n" + "=" * 60)
        print("API KEY ISSUE DETECTED")
        print("=" * 60)
        print("Your API key appears to be invalid or expired.")
        print("\nPossible reasons:")
        print("1. The API key is incorrect")
        print("2. The API key has been revoked")
        print("3. The API key has expired")
        print("4. The API key doesn't have the required permissions")
        print("\nSolution:")
        print("1. Go to https://makersuite.google.com/app/apikey")
        print("2. Create a new API key")
        print("3. Update your .env file with the new key")
        print("4. Restart the application")
    
    exit(1)

print("\n" + "=" * 60)
print("✓ ALL TESTS PASSED - API IS WORKING")
print("=" * 60)
