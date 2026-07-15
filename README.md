# nanogpt-from-scratch

Training a real GPT language model from scratch — character-level, on tiny_shakespeare, watching the loss actually go down.

Builds directly on [transformer-from-scratch](https://github.com/redwan-darraz/transformer-from-scratch), reusing the tokenizer and attention mechanism implemented there, this time assembled into a full trainable model.

## Labs

### LAB 2.1 — nanoGPT: Training a Real LLM from Scratch

Character-level tokenizer, causal self-attention Transformer block, full GPT assembly, training on Kaggle's free T4 GPU, text generation, and a RoPE variant compared against learned positional embeddings. → [`lab01_nanogpt/`](lab01_nanogpt/)

### LAB 2.2 — Mistral 7B: Loading, Inspecting, Comparing

Loading a real 7-billion-parameter LLM in 4-bit on a free Kaggle T4, inspecting its actual architecture (GQA, RoPE, RMSNorm, SwiGLU) straight from `model.config`, and comparing it side by side against the nanoGPT built in lab01. → [`lab02_mistral7b/`](lab02_mistral7b/)

## Projects

### llmplay — LLM Playground CLI

Send the same prompt to Mistral, Groq (Llama) and Gemini Flash in parallel with `asyncio`, compare responses, latency and token counts side by side. → [`projects/llmplay/`](projects/llmplay/)

## Stack

Python 3.11 · PyTorch · transformers · bitsandbytes · NumPy · matplotlib · Jupyter · asyncio · Mistral API · Groq API · Gemini API · rich

## Resources

- [Let's build GPT: from scratch, in code, spelled out (Karpathy)](https://www.youtube.com/watch?v=kCc8FmEb1nY)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding](https://arxiv.org/abs/2104.09864)
- [GQA: Training Generalized Multi-Query Transformer Models from Multi-Head Checkpoints](https://arxiv.org/abs/2305.13245)
- [GLU Variants Improve Transformer (SwiGLU)](https://arxiv.org/abs/2002.05202)
- [Mistral 7B](https://arxiv.org/abs/2310.06825)
