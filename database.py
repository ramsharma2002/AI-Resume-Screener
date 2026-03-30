import sqlite3

def init_db():
    conn = sqlite3.connect("ats.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            resume TEXT,
            role TEXT,
            score REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def save_result(resume, role, score):
    conn = sqlite3.connect("ats.db")
    c = conn.cursor()
    c.execute("INSERT INTO results (resume, role, score) VALUES (?, ?, ?)",
              (resume, role, score))
    conn.commit()
    conn.close()
