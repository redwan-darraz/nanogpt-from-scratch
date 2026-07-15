# Mistral 7B — loading, inspecting, comparing

Loading a real 7-billion-parameter LLM in 4-bit, poking inside its layers, and comparing it directly against the ~10M-parameter GPT built from scratch in [`lab01_nanogpt`](../lab01_nanogpt).

## What it does

- Loads Mistral 7B in 4-bit quantization on a Kaggle T4 — 4.01 GB of VRAM, loaded in 6.2s
- Reads the real architecture straight from `model.config`, no hardcoding
- Reconstructs the parameter count from the architecture formula and checks it against the published figure
- Compares nanoGPT (lab01) against Mistral 7B side by side
- Generates text at temperature 0.0, 0.8 and 1.5 on the same prompt

## Why this matters

Everything in `lab01_nanogpt` — token embeddings, causal attention, feedforward blocks, LM head — is exactly what's inside Mistral 7B too. Same architecture, ~671x more parameters. Seeing both side by side turns "Mistral 7B" from a black box into "the same thing I built, just a lot bigger."

## Results

| Property | nanoGPT (lab01) | Mistral 7B |
| --- | --- | --- |
| Layers | 6 | 32 |
| Attention heads | 6 | 32 (8 key/value heads — grouped-query attention) |
| Embedding dimension | 384 | 4096 |
| Feedforward width | 1536 | 14336 |
| Vocabulary size | 65 (characters) | 32000 (subword) |
| Context length | 256 tokens | 32768 tokens |
| Position encoding | Learned embedding table | RoPE |
| Normalization | LayerNorm | RMSNorm |
| Feedforward | Linear → ReLU → Linear | SwiGLU |
| Parameters | 10.79M | 7.24B (reconstructed from architecture — matches the published figure exactly) |

**671x** more parameters than the model trained in lab01, same core recipe.

### Temperature, side by side

Same prompt, same model, one parameter changed:

- **0.0** (greedy): fell into a repetition loop — *"The attention mechanism is a function of the input sequence"* over and over. A textbook example of why pure greedy decoding is rarely used in production.
- **0.8**: coherent, on-topic, reads like a real explanation of the alignment problem in sequence-to-sequence models.
- **1.5**: still on-topic but visibly looser — more unusual word choices, less predictable phrasing.

Full outputs, architecture dump, and the parameter-count derivation are in [`mistral_inspection.ipynb`](mistral_inspection.ipynb).

## Stack

Python 3.11 · PyTorch · transformers · bitsandbytes (4-bit quantization)

## Recruiter demo

Print `model.model.layers[0]` live, point at `k_proj`/`v_proj` outputting 1024 instead of 4096, and explain grouped-query attention in one sentence. Show the temperature comparison and explain why greedy decoding loops.
