# Mistral 7B — loading, inspecting, comparing

Loading a real 7-billion-parameter LLM in 4-bit, poking inside its layers, and comparing it directly against the ~10M-parameter GPT built from scratch in [`lab01_nanogpt`](../lab01_nanogpt).

## Plan

- Load Mistral 7B in 4-bit quantization (fits on a free-tier GPU)
- Inspect the model's layers — architecture, parameter count, attention heads, hidden dimensions
- Generate text at three temperatures (0.0, 0.8, 1.5) and observe the difference in behavior
- Comparison table: nanoGPT vs Mistral 7B — architecture and parameter count side by side

## Why this matters

Everything in `lab01_nanogpt` — token embeddings, causal attention, feedforward blocks, LM head — is exactly what's inside Mistral 7B too. Same architecture, ~650x more parameters. Seeing both side by side turns "Mistral 7B" from a black box into "the same thing I built, just a lot bigger."

## nanoGPT vs Mistral 7B

| Property | nanoGPT (lab01) | Mistral 7B |
| --- | --- | --- |
| Layers | 6 | 32 |
| Attention heads | 6 | 32 (8 key/value heads — grouped-query attention) |
| Embedding dimension | 384 | 4096 |
| Feedforward width | 1536 (4x embedding) | 14336 |
| Vocabulary size | 65 (characters) | 32000 (subword) |
| Context length | 256 tokens | 32768 tokens |
| Position encoding | Learned embedding table | RoPE |
| Normalization | LayerNorm | RMSNorm |
| Feedforward activation | Linear → ReLU → Linear | SwiGLU (gated, 3 matrices) |
| Parameters | 10.79M | ~7.24B |

Mistral 7B has roughly **670x** more parameters than the model trained in lab01 — same core recipe (embeddings, causal attention, feedforward, LM head), scaled up with a handful of engineering refinements for efficiency: RoPE instead of a learned position table (implemented from scratch in lab01), grouped-query attention instead of giving every head its own key/value projection, RMSNorm instead of LayerNorm, and a gated SwiGLU feedforward instead of a plain ReLU MLP.

Full derivation of the parameter count, live inspection of `model.config`, and temperature comparisons (0.0 / 0.8 / 1.5) are in [`mistral_inspection.ipynb`](mistral_inspection.ipynb).

## Stack

Python 3.11 · PyTorch · transformers · bitsandbytes (4-bit quantization)
