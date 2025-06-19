import sqlite3, os
from dotenv import load_dotenv

load_dotenv()
DB_PATH = os.getenv("DATABASE_PATH")

def get_entries(word):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM dictionary WHERE word = ?", (word,))
    rows = c.fetchall()
    conn.close()
    return rows
