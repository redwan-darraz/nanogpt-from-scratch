# nanogpt-from-scratch

Training a real GPT language model from scratch — character-level, on tiny_shakespeare, watching the loss actually go down.

Builds directly on [transformer-from-scratch](https://github.com/redwan-darraz/transformer-from-scratch), reusing the tokenizer and attention mechanism implemented there, this time assembled into a full trainable model.

## Labs

### LAB 2.1 — nanoGPT: Training a Real LLM from Scratch

Character-level tokenizer, causal self-attention Transformer block, full GPT assembly, training on Kaggle's free T4 GPU, text generation, and a RoPE variant compared against learned positional embeddings. → [`lab01_nanogpt/`](lab01_nanogpt/)

## Projects

### llmplay — LLM Playground CLI

Send the same prompt to Mistral, Groq (Llama) and Gemini Flash in parallel with `asyncio`, compare responses, latency and token counts side by side. → [`projects/llmplay/`](projects/llmplay/)

## Stack

Python 3.11 · PyTorch · NumPy · matplotlib · Jupyter · asyncio

## Resources

- [Let's build GPT: from scratch, in code, spelled out (Karpathy)](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)
