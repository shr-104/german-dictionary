import json, os, time
from openai import OpenAI, APIError
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=os.getenv("OPENROUTER_API_KEY"))

# os.makedirs("cache", exist_ok=True)

def load_cache(path):
    if not os.path.exists(path):
        with open(path, "w") as f: json.dump({}, f)
    with open(path, "r") as f: return json.load(f)

def save_cache(path, cache):
    with open(path, "w") as f: json.dump(cache, f, indent=2, ensure_ascii=False)

# def call_llm(prompt):
#     response = client.chat.completions.create(
#         model="deepseek/deepseek-r1-distill-qwen-14b:free",
#         extra_headers={"X-Title": "GermanDictionaryCLI"},
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content.strip()

def call_llm(prompt, retries=3, wait=3):
    for attempt in range(retries):
        try:
            response = client.chat.completions.create(
                model="deepseek/deepseek-prover-v2:free",
                extra_headers={"X-Title": "GermanDictionaryCLI"},
                messages=[{"role": "user", "content": prompt}]
            )
            return response.choices[0].message.content.strip()
        except APIError as e:
            print(f"[red]LLM API error:[/red] {e}")
        except Exception as e:
            print(f"[yellow]Retrying LLM call... ({attempt+1}/{retries})[/yellow]")
            time.sleep(wait)
    return "[LLM ERROR: Model unavailable]"

def get_conjugation(word):
    # cache = load_cache(CONJ_PATH)
    # if word in cache: return cache[word]
    prompt = f"""
Conjugate the German verb "{word}" in all major tenses (Präsens, Präteritum, Perfekt, Plusquamperfekt), and include:

- Imperativ (du, ihr, Sie)
- Partizip I and II
- Konjunktiv I and II

for Perfekt and Plusquamperfekt, only output haben or sein with the correct form without the verb in Partizip II form.

Output the result as a Markdown table with the following format:

| Tense/Mode        | ich      | du       | er/sie/es | wir      | ihr      | sie/Sie   |
|-------------------|----------|----------|-----------|----------|----------|-----------|
| Präsens           | ...      | ...      | ...       | ...      | ...      | ...       |
| Präteritum        | ...      | ...      | ...       | ...      | ...      | ...       |
| Perfekt           | ...      | ...      | ...       | ...      | ...      | ...       |
| Plusquamperfekt   | ...      | ...      | ...       | ...      | ...      | ...       |
| Konjunktiv I      | ...      | ...      | ...       | ...      | ...      | ...       |
| Konjunktiv II     | ...      | ...      | ...       | ...      | ...      | ...       |
| Imperativ         | -        | [du]     | -         | -        | [ihr]    | [Sie]     |
| Partizip I        | -        | -        | [form]    | -        | -        | -         |
| Partizip II       | -        | -        | [form]    | -        | -        | -         |

create the table with perfectly aligned | (use more space to match | if needed).

No coloring, highlight, bold, explanation, comments, notes, etc.
Use only markdown table format and nessesary information output. 
    """.strip()

    result = call_llm(prompt)
    if "LLM ERROR" in result:
        return "[LLM unavailable]"
    # cache[word] = result
    # save_cache(CONJ_PATH, cache)
    # return cache[word]
    return result

def get_semantics(word):
    # cache = load_cache(SEM_PATH)
    # if word in cache: return cache[word]
    prompt = f"""
Give the **word family**, **synonyms** and **antonyms** of the German word "{word}" with their **English translations**, **other forms** of word (**singular, plural, Genitiv, Dativ, Akkusativ, additional related words except conjugation and imperative**).

Output the result as 2 Markdown tables with the following format:

| Type      | German Word   | English Translation   |
|-----------|---------------|------------------------|
| Synonym   | synonym1      | translation1           |
| Synonym   | synonym2      | translation2           |

| Type      | German Word   | English Translation   |
|-----------|---------------|------------------------|
| Antonym   | antonym1      | translation1           |
| Antonym   | antonym2      | translation2           |

create the table with perfectly aligned | (use more space to match | if needed).

use more columns if needed.

No coloring, highlight, bold, explanation, comments, notes, etc.
Use only markdown table format and nessesary information output. 
    """.strip()

    result = call_llm(prompt)
    if "LLM ERROR" in result:
        return "[LLM unavailable]"
    # cache[word] = result + "\n[LLM GENERATED]"
    # save_cache(SEM_PATH, cache)
    return result
