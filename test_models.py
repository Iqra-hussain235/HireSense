"""
Test script to find which Gemini model has available quota
"""
import os
from dotenv import load_dotenv
from google import genai

# Load environment variables
load_dotenv()

# Get API key
api_key = os.getenv('GEMINI_API_KEY')

print("=" * 60)
print("TESTING AVAILABLE GEMINI MODELS")
print("=" * 60)

# Initialize client
client = genai.Client(api_key=api_key)

# List of models to test
models_to_test = [
    "gemini-2.5-flash",
    "gemini-2.5-pro", 
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite-001",
]

working_models = []

for model_name in models_to_test:
    print(f"\nTesting {model_name}...")
    try:
        response = client.models.generate_content(
            model=model_name,
            contents="Hello, please respond with 'working'"
        )
        print(f"✅ {model_name} - WORKING")
        print(f"   Response: {response.text[:50]}...")
        working_models.append(model_name)
    except Exception as e:
        error_msg = str(e)
        if "quota" in error_msg.lower() or "exceeded" in error_msg.lower():
            print(f"❌ {model_name} - QUOTA EXCEEDED")
        elif "not found" in error_msg.lower() or "404" in error_msg:
            print(f"❌ {model_name} - NOT FOUND")
        else:
            print(f"❌ {model_name} - ERROR: {error_msg[:50]}...")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"Working models: {len(working_models)}")
if working_models:
    print("Available models:")
    for model in working_models:
        print(f"  - {model}")
else:
    print("No models with available quota found.")
    print("Please wait for quota reset or upgrade your plan.")

# Update .env with working model if found
if working_models:
    best_model = working_models[0]
    print(f"\n✅ Recommended model: {best_model}")
    print(f"Add this to your .env file:")
    print(f"GEMINI_MODEL={best_model}")
