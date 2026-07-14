"""
llmplay — send the same prompt to Mistral, Groq (Llama) and Gemini in parallel.
Usage: python llmplay.py "your prompt here"
"""

import argparse
import asyncio

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

from engines import ask_mistral, ask_groq, ask_gemini

console = Console()

PROVIDERS = [ask_mistral, ask_groq, ask_gemini]


async def run_all(prompt, temperature=None):
    tasks = [fn(prompt, temperature) for fn in PROVIDERS]
    return await asyncio.gather(*tasks, return_exceptions=True)


def render(replies):
    panels = []
    for fn, result in zip(PROVIDERS, replies):
        provider_name = fn.__name__.replace("ask_", "").capitalize()

        if isinstance(result, Exception):
            panels.append(Panel(
                f"[red]{type(result).__name__}[/red]\n{str(result)[:200]}",
                title=f"[bold red]{provider_name} — failed[/bold red]",
                width=40,
            ))
            continue

        body = f"{result.text}\n\n[dim]{result.latency_ms:.0f}ms — {result.tokens} tokens — {result.model}[/dim]"
        panels.append(Panel(body, title=f"[bold]{result.provider}[/bold]", width=40))

    console.print(Columns(panels))


def main():
    parser = argparse.ArgumentParser(prog="llmplay", description="Send a prompt to Mistral, Groq and Gemini in parallel.")
    parser.add_argument("prompt", help="Prompt to send to all three models")
    args = parser.parse_args()

    replies = asyncio.run(run_all(args.prompt))
    render(replies)


if __name__ == "__main__":
    main()
