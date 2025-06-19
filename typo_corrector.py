from rapidfuzz import process
from db import get_entries

def get_all_words():
    from dotenv import load_dotenv
    import sqlite3, os
    load_dotenv()
    conn = sqlite3.connect(os.getenv("DATABASE_PATH"))
    c = conn.cursor()
    c.execute("SELECT DISTINCT word FROM dictionary")
    words = [r[0] for r in c.fetchall()]
    conn.close()
    return words

def correct_typo(word, threshold=85):
    all_words = get_all_words()
    best, score, _ = process.extractOne(word, all_words)
    return best if score >= threshold else None
