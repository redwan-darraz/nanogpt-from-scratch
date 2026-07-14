# llmplay — LLM Playground CLI

Send the same prompt to three free LLM APIs in parallel — Mistral, Groq (Llama) and Gemini — and compare their responses, latency and token counts side by side. All three calls run concurrently via `asyncio.gather()`, so the total wait time is bounded by the slowest single call, not the sum of all three.

## Usage

```bash
llmplay "explique le RAG en 3 lignes"
llmplay "raconte une histoire en 2 phrases" --temp 0.0 0.5 1.0 1.5 --model mistral
llmplay "explique le RAG en 3 lignes" --judge
```

## Output example — `llmplay "explique le RAG en 3 lignes"`

```text
┌────────────── Mistral ───────────────┐
│ Le RAG (Retrieval-Augmented          │
│ Generation) est une technique qui    │
│ combine la recherche d'informations  │
│ pertinentes (via un retriever) et    │
│ la génération de texte (via un       │
│ LLM), pour améliorer la précision    │
│ des réponses en s'appuyant sur des   │
│ données externes.                    │
│                                      │
│ Il réduit les hallucinations en      │
│ puisant dans des sources fiables     │
│ avant de formuler une réponse, tout  │
│ en restant flexible grâce à          │
│ l'adaptation du modèle.              │
│                                      │
│ Cette approche est utile pour les    │
│ chatbots, la recherche               │
│ d'informations ou les assistants     │
│ spécialisés.                         │
│                                      │
│ 2056ms — 140 tokens —                │
│ mistral-small-latest                 │
└──────────────────────────────────────┘
┌──────────── Groq (Llama) ────────────┐
│ Le RAG (Rouge, Ambre, Vert) est un   │
│ système de codage des risques        │
│ utilisé pour évaluer la criticité    │
│ des problèmes. Il utilise des        │
│ couleurs pour indiquer le niveau de  │
│ risque : rouge pour les problèmes    │
│ critiques, ambre pour les problèmes  │
│ modérés et vert pour les problèmes   │
│ mineurs. Ce système aide à prioriser │
│ les tâches et les ressources en      │
│ fonction du niveau de risque associé │
│ à chaque problème.                   │
│                                      │
│ 1091ms — 147 tokens —                │
│ llama-3.3-70b-versatile              │
└──────────────────────────────────────┘
┌─────────────── Gemini ───────────────┐
│ Le RAG (Retrieval-Augmented          │
│ Generation) consiste à connecter un  │
│ modèle d'IA à vos propres sources de │
│ données privées.                     │
│ Au lieu de se fier uniquement à sa   │
│ mémoire, l'IA cherche d'abord les    │
│ informations pertinentes dans vos    │
│ documents.                           │
│ Elle utilise ensuite ces éléments    │
│ pour générer une réponse précise,    │
│ factuelle et citée.                  │
│                                      │
│ 732ms — 83 tokens —                  │
│ gemini-3.1-flash-lite                │
└──────────────────────────────────────┘
```

Groq/Llama confused "RAG" with an unrelated project-management color code (Red/Amber/Green) — reproducibly, across multiple runs — while Mistral and Gemini both correctly explained Retrieval-Augmented Generation. Same prompt, three different outcomes: exactly the kind of gap this tool is built to expose before committing to a model.

## `--temp` — same model, four temperatures

`llmplay "raconte une histoire en 2 phrases" --temp 0.0 0.5 1.0 1.5` on Mistral:

```text
┌───────── temperature = 0.0 ──────────┐
│ Le Gardien des Ombres                │
│                                      │
│ Chaque nuit, Elias entendait un      │
│ murmure derrière sa porte, mais      │
│ quand il l'ouvrait, il ne trouvait   │
│ que son chat endormi sur le          │
│ paillasson. Un soir, le chuchotement │
│ se transforma en une voix familière  │
│ : "Tu as oublié de me rendre mon     │
│ livre…" — c'était sa sœur, disparue  │
│ dix ans plus tôt.                    │
│                                      │
│ 2437ms — 111 tokens                  │
└──────────────────────────────────────┘
┌───────── temperature = 0.5 ──────────┐
│ Le dernier souffle de l'arbre        │
│                                      │
│ Sous la lune pâle, un vieux chêne    │
│ murmura à l'oreille de la fillette   │
│ qui s'endormait contre son tronc :   │
│ "Je te donne mes feuilles pour tes   │
│ rêves, mais garde-toi des ombres qui │
│ dansent entre mes branches." Au      │
│ matin, elle trouva ses cheveux       │
│ couverts d'or, et l'arbre,           │
│ silencieux, n'était plus qu'un tas   │
│ de cendres.                          │
│                                      │
│ 1991ms — 116 tokens                  │
└──────────────────────────────────────┘
┌───────── temperature = 1.0 ──────────┐
│ Le Gardien des Ombres                │
│                                      │
│ Dès que la lune se levait, Elias     │
│ disparaissait dans la forêt          │
│ interdite, où les arbres             │
│ chuchotaient des formules            │
│ oubliées—sauf cette nuit-là, où il   │
│ découvrit que la seule ombre qui ne  │
│ bougeait pas était la sienne,        │
│ reflétée par quelque chose… autre.   │
│ En courant vers le village, il       │
│ comprit trop tard que l'ombre        │
│ l'avait déjà remplacé.               │
│                                      │
│ 1630ms — 119 tokens                  │
└──────────────────────────────────────┘
┌───────── temperature = 1.5 ──────────┐
│ La dernière lue m'observa avec des   │
│ yeux dorés avant de disparaitre dans │
│ la nuit touffue.                     │
│ Désormais, chaque rayon de lune      │
│ 唤queur相信 fils chien                │
│ m'accompagn значај toujours traites  │
│ elles sp, 'llling VI/ch2 Sect. LS    │
│ Raptor/Chleur区 DK EulOT BOO         │
│ must(await gelang.callback           │
│ OutstandingProf... CongregDigiteux    │
│ HardDu Павел Insp/check              │
│ Fasah重命ÉselFund учуєlov прой       │
│ Beatrice ler 負ùÈ dort.. Alice 향해. │
│                                      │
│ 1840ms — 133 tokens                  │
└──────────────────────────────────────┘
```

Temperature 1.5 doesn't just get "more creative" — it collapses into a mix of Chinese, Korean, Russian, Hebrew and stray code fragments mid-sentence. A real, reproducible illustration of why cranking temperature isn't a free lunch: the same softmax-sampling mechanism that adds variety also opens the door to complete incoherence once it's stretched too far.

## `--judge` — a fourth model picks a winner

`llmplay "explique le RAG en 3 lignes" --judge` — Mistral Large (deliberately a different, larger model than the one competing) reads all three responses and picks a winner with a rationale:

```text
┌─────────────────────── Judge verdict — Mistral Large ───────────────────────┐
│ Response 1 (Mistral) est la meilleure.                                      │
│                                                                              │
│ Elle explique clairement et précisément le RAG (Retrieval-Augmented         │
│ Generation) en trois lignes, en couvrant ses deux étapes clés (recherche    │
│ + génération) et ses avantages (réduction des hallucinations, sources       │
│ fiables). Les réponses 2 et 3 sont soit hors-sujet (Groq confond avec un    │
│ autre acronyme), soit moins complète (Gemini omet des détails techniques    │
│ comme la base de connaissances). Mistral offre un équilibre parfait entre   │
│ concision et exhaustivité.                                                  │
└──────────────────────────────────────────────────────────────────────────────┘
```

The judge caught the Groq mix-up entirely on its own, without being told which response was wrong.

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
