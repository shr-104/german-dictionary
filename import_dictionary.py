import sqlite3, json, os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH", "data/dictionary.db")

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS dictionary")
c.execute("""
CREATE TABLE dictionary (
    word TEXT,
    pos TEXT,
    gloss TEXT,
    example TEXT,
    example_en TEXT
)
""")

with open("/home/dtth/shr104/german-dictionary-v3/cache/kaikki.org-dictionary-German-words.jsonl", "r", encoding="utf-8") as f:
    for line in f:
        entry = json.loads(line)
        word = entry.get("word", "")
        pos = entry.get("pos", "")
        for sense in entry.get("senses", []):
            gloss = sense.get("glosses", [""])[0]
            for ex in sense.get("examples", [])[:1]:
                text = ex.get("text", "")
                english = ex.get("english", "")
                c.execute("INSERT INTO dictionary VALUES (?, ?, ?, ?, ?)",
                          (word, pos, gloss, text, english))

conn.commit()
conn.close()
