"""
Async functions to query Mistral, Groq and Gemini with a single prompt.
Each returns a Reply with the response text, latency, token count and exact model used.
"""

import time
from dataclasses import dataclass

from google import genai
from groq import AsyncGroq
from mistralai.client import Mistral

import config

MISTRAL_MODEL = "mistral-small-latest"
GROQ_MODEL = "llama-3.3-70b-versatile"
GEMINI_MODEL = "gemini-flash-lite-latest"


@dataclass
class Reply:
    provider: str
    model: str
    text: str
    latency_ms: float
    tokens: int


async def ask_mistral(prompt, temperature=None):
    client = Mistral(api_key=config.MISTRAL_API_KEY)
    kwargs = {"temperature": temperature} if temperature is not None else {}

    t0 = time.perf_counter()
    response = await client.chat.complete_async(
        model=MISTRAL_MODEL,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    return Reply(
        provider="Mistral",
        model=response.model,
        text=response.choices[0].message.content,
        latency_ms=latency_ms,
        tokens=response.usage.total_tokens,
    )


async def ask_groq(prompt, temperature=None):
    client = AsyncGroq(api_key=config.GROQ_API_KEY)
    kwargs = {"temperature": temperature} if temperature is not None else {}

    t0 = time.perf_counter()
    response = await client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "user", "content": prompt}],
        **kwargs,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    return Reply(
        provider="Groq (Llama)",
        model=response.model,
        text=response.choices[0].message.content,
        latency_ms=latency_ms,
        tokens=response.usage.total_tokens,
    )


async def ask_gemini(prompt, temperature=None):
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    config_kwargs = {}
    if temperature is not None:
        config_kwargs["temperature"] = temperature

    t0 = time.perf_counter()
    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config_kwargs or None,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    return Reply(
        provider="Gemini",
        model=response.model_version,
        text=response.text,
        latency_ms=latency_ms,
        tokens=response.usage_metadata.total_token_count,
    )
