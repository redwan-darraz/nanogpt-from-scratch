# llmplay — LLM Playground CLI

Send the same prompt to three free LLM APIs in parallel — Mistral, Groq (Llama) and Gemini — and compare their responses, latency and token counts side by side. All three calls run concurrently via `asyncio.gather()`, so the total wait time is bounded by the slowest single call, not the sum of all three.

## Usage

```bash
llmplay "explain RAG in 3 lines"
llmplay "tell a short story in 2 sentences" --temp 0.0 0.5 1.0 1.5 --model mistral
llmplay "explain RAG in 3 lines" --judge
```

## Output example — `llmplay "explain RAG in 3 lines"`

```text
┌────────────── Mistral ───────────────┐
│ RAG (Retrieval-Augmented Generation) │
│ combines a retrieval system with a   │
│ generative AI model to improve       │
│ responses by fetching relevant       │
│ context from a knowledge base before │
│ generating an answer. It reduces     │
│ hallucinations by grounding outputs  │
│ in retrieved data, making responses  │
│ more accurate and reliable. This     │
│ approach is widely used in chatbots, │
│ search engines, and enterprise Q&A   │
│ systems.                             │
│                                      │
│ 1677ms — 98 tokens —                 │
│ mistral-small-latest                 │
└──────────────────────────────────────┘
┌──────────── Groq (Llama) ────────────┐
│ RAG (Retrieval, Augment, Generate)   │
│ is an AI framework that combines     │
│ retrieval and generation techniques. │
│ It retrieves relevant information    │
│ from a database or knowledge graph,  │
│ augments it with additional context, │
│ and generates human-like responses.  │
│ This approach enables more accurate  │
│ and informative responses,           │
│ especially for complex and           │
│ open-ended questions.                │
│                                      │
│ 976ms — 108 tokens —                 │
│ llama-3.3-70b-versatile              │
└──────────────────────────────────────┘
┌─────────────── Gemini ───────────────┐
│ RAG (Retrieval-Augmented Generation) │
│ connects a Large Language Model to   │
│ your private or real-time data       │
│ sources.                             │
│ It retrieves relevant information    │
│ from those documents before sending  │
│ it to the model to generate an       │
│ answer.                              │
│ This process grounds the AI in       │
│ facts, significantly reducing        │
│ hallucinations and providing         │
│ verifiable citations.                │
│                                      │
│ 743ms — 71 tokens —                  │
│ gemini-3.1-flash-lite                │
└──────────────────────────────────────┘
```

All three get the core idea right here, with different framing — Mistral leans on concrete use cases, Groq slightly misexpands the acronym ("Retrieval, Augment, Generate" instead of "Retrieval-Augmented Generation") but explains the mechanism correctly, Gemini emphasizes grounding and citations. Small, real differences in emphasis and depth — exactly what this tool is built to surface before committing to a model.

## `--temp` — same model, four temperatures

`llmplay "tell a short story in 2 sentences" --temp 0.0 0.5 1.0 1.5` on Mistral:

```text
┌───────── temperature = 0.0 ──────────┐
│ The old lighthouse keeper swore he   │
│ saw a ghost ship every full moon,    │
│ its tattered sails glowing with an   │
│ eerie light. One night, as he raised │
│ his lantern to guide it safely past  │
│ the rocks, the ghostly vessel        │
│ dissolved into mist—and in its place │
│ stood his long-lost brother, holding │
│ the same lantern he'd carried        │
│ decades ago.                         │
│                                      │
│ 2272ms — 95 tokens                   │
└──────────────────────────────────────┘
┌───────── temperature = 0.5 ──────────┐
│ The old lighthouse keeper swore he   │
│ saw a ghost ship every full moon,    │
│ its tattered sails glowing with      │
│ eerie green light. One night, he     │
│ finally climbed aboard—only to       │
│ discover the ship was his own        │
│ reflection in a shattered mirror     │
│ left behind by a long-lost sailor.   │
│                                      │
│ 1559ms — 82 tokens                   │
└──────────────────────────────────────┘
┌───────── temperature = 1.0 ──────────┐
│ The old lighthouse keeper swore he'd │
│ never leave his post—until one       │
│ stormy night, a child's laughter     │
│ echoed up the spiral stairs,         │
│ beckoning him toward a mystery older │
│ than the sea itself. By dawn, the    │
│ keeper was gone, and in his place    │
│ stood a figure with saltwater in     │
│ their veins, watching the waves roll │
│ in with eyes that had seen the       │
│ future.                              │
│                                      │
│ 1335ms — 101 tokens                  │
└──────────────────────────────────────┘
┌───────── temperature = 1.5 ──────────┐
│ Michel struck gold hammering random  │
│ chimes except for Congol's           │
│ broBundle. retirada cattle ser trava │
│ com obtimum delivery letolithic      │
│ starts tool rods afford piloto       │
│ Wyge ayudé qué política terceroquest │
│ repartovaly hallwayziJoilo surrogate │
│ ele squeeze verts visni gratitude    │
│ arena seam jurid fiecare responde    │
│ directly cream mediario périphrá     │
│ unvalid descendre Kabaut             │
│ backbone.work rock persist dell el   │
│ Roch enam?' καριobu ptrister musul   │
│ kay bitten left bed sobie约 CVs      │
│ 없었며 سُکه什've de آم Venetiaizam    │
│ Kol FuoaGap-F solarrom adapt alguien │
│ fearsn mundoahan erupt seven tob     │
│ lov                                  │
│                                      │
│ 2257ms — 145 tokens                  │
└──────────────────────────────────────┘
```

The first three temperatures tell a coherent, atmospheric two-sentence story with the same lighthouse-keeper premise, gradually adding more unusual imagery. At 1.5 it completely disintegrates into a mix of English, Spanish, Portuguese, Korean, Greek, Arabic and Romanian fragments with no coherent meaning left. A real, reproducible illustration of the temperature/coherence trade-off — the same softmax-sampling mechanism that adds variety also opens the door to total incoherence once stretched too far.

## `--judge` — a fourth model picks a winner

`llmplay "explain RAG in 3 lines" --judge` — Mistral Large (deliberately a different, larger model than the one competing) reads all three responses and picks a winner with a rationale:

```text
┌─────────────────────── Judge verdict — Mistral Large ───────────────────────┐
│ Response 1 (Mistral) is the best. It clearly and concisely explains RAG's   │
│ core mechanism (retrieval + generation), highlights its key benefit         │
│ (reducing hallucinations), and provides a practical example (knowledge      │
│ base) without unnecessary jargon. The structure is direct, informative,     │
│ and easy to understand, making it the most effective of the three. While    │
│ the others are accurate, they either lack specificity (Response 2) or       │
│ overcomplicate the explanation (Response 3).                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

The judge gives a substantive, specific rationale rather than a generic "they're all fine" — useful signal when deciding which model to trust for a given task.

## Real usage

Before picking a model for a project: `llmplay "your prompt" --judge` gives a verdict in a few seconds instead of guessing which model to trust.

## Setup

```bash
cp .env.example .env
# fill in MISTRAL_API_KEY, GROQ_API_KEY, GEMINI_API_KEY — all free tiers
python llmplay.py "your prompt"
```

## Stack

Python 3.11 · asyncio · Mistral API · Groq API · Gemini API · rich
