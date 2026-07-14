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

# Deliberately a different (larger) Mistral model than the one being judged,
# so the judge isn't just grading its own homework.
JUDGE_MODEL = "mistral-large-latest"


@dataclass
class Reply:
    provider: str
    model: str
    text: str
    latency_ms: float
    tokens: int


async def ask_mistral(prompt: str, temperature: float | None = None) -> Reply:
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


async def ask_groq(prompt: str, temperature: float | None = None) -> Reply:
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


async def ask_gemini(prompt: str, temperature: float | None = None) -> Reply:
    client = genai.Client(api_key=config.GEMINI_API_KEY)
    config_kwargs = {"temperature": temperature} if temperature is not None else {}

    t0 = time.perf_counter()
    response = await client.aio.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=config_kwargs or None,
    )
    latency_ms = (time.perf_counter() - t0) * 1000

    return Reply(
        provider="Gemini",
        # model_version reports the concrete model behind the "latest" alias
        # (e.g. gemini-3.1-flash-lite), more informative than the alias name.
        model=response.model_version,
        text=response.text,
        latency_ms=latency_ms,
        tokens=response.usage_metadata.total_token_count,
    )


async def ask_judge(prompt: str, replies: list) -> str:
    """Have Mistral Large pick the best of the three replies and explain why.

    Silently skips replies that came back as exceptions (a provider outage
    shouldn't stop the other two responses from being judged).
    """
    valid = [r for r in replies if isinstance(r, Reply)]
    if not valid:
        return "No successful replies to judge."

    options = "\n\n".join(
        f"Response {i + 1} — {r.provider}:\n{r.text}"
        for i, r in enumerate(valid)
    )

    judge_prompt = (
        f'A user asked the following prompt:\n"{prompt}"\n\n'
        f"Here are {len(valid)} responses from different AI models:\n\n{options}\n\n"
        "Which response is the best, and why? Answer in 3-4 sentences, "
        "and clearly state which response number you picked."
    )

    client = Mistral(api_key=config.MISTRAL_API_KEY)
    response = await client.chat.complete_async(
        model=JUDGE_MODEL,
        messages=[{"role": "user", "content": judge_prompt}],
    )
    return response.choices[0].message.content
