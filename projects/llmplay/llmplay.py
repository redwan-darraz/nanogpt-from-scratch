"""
llmplay — send the same prompt to Mistral, Groq (Llama) and Gemini in parallel.

Usage:
    python llmplay.py "your prompt here"
    python llmplay.py "your prompt here" --temp 0.0 0.5 1.0 1.5 --model groq
    python llmplay.py "your prompt here" --judge
"""

import argparse
import asyncio

from rich.columns import Columns
from rich.console import Console
from rich.panel import Panel

from engines import Reply, ask_gemini, ask_groq, ask_judge, ask_mistral

console = Console()

PROVIDERS = [ask_mistral, ask_groq, ask_gemini]
PROVIDER_BY_NAME = {"mistral": ask_mistral, "groq": ask_groq, "gemini": ask_gemini}

PANEL_WIDTH = 40


async def run_all(prompt: str) -> list[Reply | Exception]:
    """Query all three providers concurrently. A single provider failing
    (rate limit, outage...) shouldn't take the other two down with it, so
    failures are returned as exceptions rather than raised."""
    tasks = [fn(prompt) for fn in PROVIDERS]
    return await asyncio.gather(*tasks, return_exceptions=True)


async def run_temperatures(prompt: str, provider_fn, temperatures: list[float]) -> list[Reply | Exception]:
    tasks = [provider_fn(prompt, temp) for temp in temperatures]
    return await asyncio.gather(*tasks, return_exceptions=True)


def render(replies: list[Reply | Exception]) -> None:
    panels = []
    for fn, result in zip(PROVIDERS, replies):
        provider_name = fn.__name__.replace("ask_", "").capitalize()

        if isinstance(result, Exception):
            panels.append(Panel(
                f"[red]{type(result).__name__}[/red]\n{str(result)[:200]}",
                title=f"[bold red]{provider_name} — failed[/bold red]",
                width=PANEL_WIDTH,
            ))
            continue

        body = f"{result.text}\n\n[dim]{result.latency_ms:.0f}ms — {result.tokens} tokens — {result.model}[/dim]"
        panels.append(Panel(body, title=f"[bold]{result.provider}[/bold]", width=PANEL_WIDTH))

    console.print(Columns(panels))


def render_temperatures(temperatures: list[float], replies: list[Reply | Exception]) -> None:
    panels = []
    for temp, result in zip(temperatures, replies):
        if isinstance(result, Exception):
            panels.append(Panel(
                f"[red]{type(result).__name__}[/red]\n{str(result)[:200]}",
                title=f"[bold red]temperature={temp} — failed[/bold red]",
                width=PANEL_WIDTH,
            ))
            continue

        body = f"{result.text}\n\n[dim]{result.latency_ms:.0f}ms — {result.tokens} tokens[/dim]"
        panels.append(Panel(body, title=f"[bold]temperature = {temp}[/bold]", width=PANEL_WIDTH))

    console.print(Columns(panels))


def main():
    parser = argparse.ArgumentParser(
        prog="llmplay",
        description="Send a prompt to Mistral, Groq and Gemini in parallel and compare their answers.",
    )
    parser.add_argument("prompt", help="Prompt to send to the model(s)")
    parser.add_argument("--temp", nargs="+", type=float, metavar="T",
                         help="Test the prompt at multiple temperatures on one model, e.g. --temp 0.0 0.5 1.0 1.5")
    parser.add_argument("--model", choices=list(PROVIDER_BY_NAME.keys()), default="mistral",
                         help="Model used with --temp (default: mistral)")
    parser.add_argument("--judge", action="store_true",
                         help="Have a fourth model (Mistral Large) pick the best response and explain why")
    args = parser.parse_args()

    if args.temp:
        provider_fn = PROVIDER_BY_NAME[args.model]
        console.print(f"[bold]Model: {args.model}[/bold]\n")
        replies = asyncio.run(run_temperatures(args.prompt, provider_fn, args.temp))
        render_temperatures(args.temp, replies)
        return

    replies = asyncio.run(run_all(args.prompt))
    render(replies)

    if args.judge:
        verdict = asyncio.run(ask_judge(args.prompt, replies))
        console.print()
        console.print(Panel(verdict, title="[bold yellow]Judge verdict — Mistral Large[/bold yellow]", width=3 * PANEL_WIDTH + 4))


if __name__ == "__main__":
    main()
