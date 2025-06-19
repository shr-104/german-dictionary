from db import get_entries
from typo_corrector import correct_typo
from grammar_tools import grammar_correct
from llm_fallback import get_conjugation, get_semantics
from rich import print

def print_entry(entries, word):
    for i, (w, pos, gloss, example, example_en) in enumerate(entries):
        print(f"[cyan]{i+1}. {gloss}[/cyan] ({pos})")
        if example:
            print(f"    • {example}")
        if example_en:
            print(f"      (EN: {example_en})")
    if any(pos == "verb" for _, pos, *_ in entries):
        print(get_conjugation(word))
        # print("\n")
    print(get_semantics(word))

def run_cli():
    print("[bold magenta]German Dictionary CLI – Press Enter to Exit[/bold magenta]")
    while True:
        q = input("\nWord or sentence: ").strip()
        if not q:
            break
        if " " in q:
            grammar_correct(q)
            continue
        entries = get_entries(q)
        if not entries:
            corrected = correct_typo(q)
            if corrected:
                print(f"[yellow]Did you mean:[/yellow] {corrected}?")
                entries = get_entries(corrected)
        if entries:
            print_entry(entries, q)
        else:
            print(f"[red]No entry found for '{q}'[/red]")
            print(get_semantics(q))
