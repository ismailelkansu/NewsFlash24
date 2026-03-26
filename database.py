import sqlite3
import json

DB_PATH = "newsflash24.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS posted_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            posted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS pending_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT UNIQUE NOT NULL,
            title TEXT,
            summary TEXT,
            hashtags TEXT,
            source TEXT,
            original_link TEXT,
            telegram_message_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def is_posted(url):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM posted_articles WHERE url = ?", (url,))
    result = c.fetchone()
    conn.close()
    return result is not None

def mark_posted(url, title):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO posted_articles (url, title) VALUES (?, ?)", (url, title))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def add_pending(url, title, summary, hashtags, source, original_link):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO pending_articles (url, title, summary, hashtags, source, original_link)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (url, title, summary, hashtags, source, original_link))
        conn.commit()
        pending_id = c.lastrowid
    except sqlite3.IntegrityError:
        pending_id = None
    conn.close()
    return pending_id

def get_pending(pending_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM pending_articles WHERE id = ?", (pending_id,))
    result = c.fetchone()
    conn.close()
    return result

def delete_pending(pending_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM pending_articles WHERE id = ?", (pending_id,))
    conn.commit()
    conn.close()

def update_pending_message_id(pending_id, message_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE pending_articles SET telegram_message_id = ? WHERE id = ?", (message_id, pending_id))
    conn.commit()
    conn.close()
