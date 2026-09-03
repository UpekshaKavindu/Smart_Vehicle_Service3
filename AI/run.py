"""Run the Customer AI Service."""

import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY", "")
    if not api_key or "XXXX" in api_key:
        print("⚠️  WARNING: GOOGLE_API_KEY is not set in .env file!")
        print("   Get your API key from: https://aistudio.google.com/apikey")
        print("   Then add it to the .env file")
        print()

    print("🚀 Starting Customer AI Service...")
    print(f"   📍 API Docs: http://localhost:8000/docs")
    print(f"   📍 Health: http://localhost:8000/health")
    print()

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )