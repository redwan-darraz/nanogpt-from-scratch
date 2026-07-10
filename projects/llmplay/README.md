# llmplay — LLM Playground CLI

Send the same prompt to three free LLM APIs in parallel — Mistral, Groq (Llama) and Gemini Flash — and compare their responses, latency and token counts side by side.

## Usage

```bash
llmplay "explain attention in one sentence"
llmplay "explain attention in one sentence" --temp 0.0 0.5 1.0
llmplay "explain attention in one sentence" --judge
```

## Plan

- `ask_mistral`, `ask_groq`, `ask_gemini`: async functions, one per provider, all free-tier APIs
- `asyncio.gather()` to run all three concurrently, results displayed with `rich`
- Per-model output: response, latency (ms), token count, exact model name
- `--temp 0.0 0.5 1.0`: same prompt, same model, three temperatures side by side
- `--judge`: a fourth LLM scores which response is best and explains why

## Real usage

Before picking a model for a project: `llmplay "your prompt" --judge` gives you a verdict in a few seconds instead of guessing.

## Stack

Python 3.11 · asyncio · Mistral API · Groq API · Gemini API · rich
