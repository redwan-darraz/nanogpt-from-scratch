# Mistral 7B — loading, inspecting, comparing

Loading a real 7-billion-parameter LLM in 4-bit, poking inside its layers, and comparing it directly against the ~10M-parameter GPT built from scratch in [`lab01_nanogpt`](../lab01_nanogpt).

## Plan

- Load Mistral 7B in 4-bit quantization (fits on a free-tier GPU)
- Inspect the model's layers — architecture, parameter count, attention heads, hidden dimensions
- Generate text at three temperatures (0.0, 0.8, 1.5) and observe the difference in behavior
- Comparison table: nanoGPT vs Mistral 7B — architecture and parameter count side by side

## Why this matters

Everything in `lab01_nanogpt` — token embeddings, causal attention, feedforward blocks, LM head — is exactly what's inside Mistral 7B too. Same architecture, ~650x more parameters. Seeing both side by side turns "Mistral 7B" from a black box into "the same thing I built, just a lot bigger."

## Stack

Python 3.11 · PyTorch · transformers · bitsandbytes (4-bit quantization)
