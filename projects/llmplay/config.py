"""
Loads API keys from a local .env file (never committed — see .env.example for the template).
"""

import os

from dotenv import load_dotenv

load_dotenv()

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

_missing = [name for name, value in [
    ("MISTRAL_API_KEY", MISTRAL_API_KEY),
    ("GROQ_API_KEY", GROQ_API_KEY),
    ("GEMINI_API_KEY", GEMINI_API_KEY),
] if not value]

if _missing:
    raise RuntimeError(
        f"Missing API key(s) in .env: {', '.join(_missing)}. "
        f"Copy .env.example to .env and fill in your keys."
    )
