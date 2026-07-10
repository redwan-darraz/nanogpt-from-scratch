# nanoGPT — training a real LLM from scratch

Building a full GPT language model — character-level, trained on tiny_shakespeare — and watching it go from random noise to something that reads like Shakespeare (badly, but recognizably).

Unlike the previous repo where every piece was verified in isolation, this one trains end to end. The loss curve is the proof.

## What it does

- Character-level tokenizer, no subword complexity — the point here is the architecture, not the tokenizer
- Full causal Transformer block: LayerNorm → Multi-Head (masked) Attention → residual → LayerNorm → FeedForward → residual
- GPT assembly: token embedding + position embedding, stacked blocks, final LM head
- Trained for 5000 steps on a Kaggle T4 GPU, train/val loss logged every 500 steps
- Text generation with temperature sampling
- A second version swaps learned position embeddings for RoPE (Rotary Position Embedding) and compares perplexity against the baseline

## Why train on Kaggle

This model (6 layers, 384-dim embeddings, ~10M parameters) would take hours on CPU. Kaggle gives 30h/week of free T4 GPU — training the full 5000 steps takes roughly 20-30 minutes there.

## Results

| Model | Steps | Train loss | Val loss | Perplexity |
|---|---|---|---|---|
| Baseline (learned pos. embedding) | 5000 | — | — | — |
| RoPE | 2000 | — | — | — |

*(filled in after training — see the notebook)*

## Stack

PyTorch 2.x · Kaggle T4 GPU · matplotlib

## Recruiter demo

Generate text live, show the loss curve GIF, explain why we divide attention scores by √d_k and why RoPE encodes position differently than a learned embedding table.
