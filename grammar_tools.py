from rich import print
from llm_fallback import call_llm

def grammar_correct(text):
    result = call_llm(f"Correct the grammar and suggest vocabulary or syntax improvements for:\n{text}")
    print(f"[green]Grammar Suggestion:[/green]\n{result}")
