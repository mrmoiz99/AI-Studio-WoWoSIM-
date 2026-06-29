import sqlite3
from contextlib import contextmanager
from datetime import datetime
from config import DB_PATH

DB_PATH.parent.mkdir(parents=True, exist_ok=True)

@contextmanager
def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    finally:
        conn.close()

def init_db():
    with get_conn() as conn:
        conn.executescript('''
        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS trends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            source TEXT,
            url TEXT,
            score INTEGER DEFAULT 0,
            status TEXT DEFAULT 'new',
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            trend_id INTEGER,
            platform TEXT,
            title TEXT,
            caption TEXT,
            hashtags TEXT,
            image_prompt TEXT,
            status TEXT DEFAULT 'draft',
            created_at TEXT NOT NULL,
            FOREIGN KEY(trend_id) REFERENCES trends(id)
        );
        CREATE TABLE IF NOT EXISTS images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER,
            path TEXT,
            prompt TEXT,
            created_at TEXT NOT NULL,
            FOREIGN KEY(post_id) REFERENCES posts(id)
        );
        CREATE TABLE IF NOT EXISTS campaigns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            brief TEXT,
            output TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_type TEXT,
            item_id INTEGER,
            action TEXT,
            created_at TEXT NOT NULL
        );
        ''')

def now():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def upsert_setting(key, value):
    with get_conn() as conn:
        conn.execute('INSERT OR REPLACE INTO settings(key,value) VALUES(?,?)', (key, value))

def get_setting(key, default=None):
    with get_conn() as conn:
        row = conn.execute('SELECT value FROM settings WHERE key=?', (key,)).fetchone()
        return row['value'] if row else default

def insert_trend(title, source='', url='', score=0):
    with get_conn() as conn:
        conn.execute('INSERT INTO trends(title,source,url,score,created_at) VALUES(?,?,?,?,?)', (title, source, url, score, now()))

def list_trends(limit=100):
    with get_conn() as conn:
        return conn.execute('SELECT * FROM trends ORDER BY id DESC LIMIT ?', (limit,)).fetchall()

def insert_post(trend_id, platform, title, caption, hashtags, image_prompt):
    with get_conn() as conn:
        cur = conn.execute('''INSERT INTO posts(trend_id,platform,title,caption,hashtags,image_prompt,created_at)
                              VALUES(?,?,?,?,?,?,?)''', (trend_id, platform, title, caption, hashtags, image_prompt, now()))
        return cur.lastrowid

def list_posts(limit=100, search=''):
    with get_conn() as conn:
        if search:
            q = f'%{search}%'
            return conn.execute('''SELECT p.*, t.title AS trend_title FROM posts p LEFT JOIN trends t ON p.trend_id=t.id
                                   WHERE p.caption LIKE ? OR p.hashtags LIKE ? OR p.title LIKE ? OR t.title LIKE ?
                                   ORDER BY p.id DESC LIMIT ?''', (q,q,q,q,limit)).fetchall()
        return conn.execute('''SELECT p.*, t.title AS trend_title FROM posts p LEFT JOIN trends t ON p.trend_id=t.id
                               ORDER BY p.id DESC LIMIT ?''', (limit,)).fetchall()

def update_post_status(post_id, status):
    with get_conn() as conn:
        conn.execute('UPDATE posts SET status=? WHERE id=?', (status, post_id))

def insert_image(post_id, path, prompt):
    with get_conn() as conn:
        conn.execute('INSERT INTO images(post_id,path,prompt,created_at) VALUES(?,?,?,?)', (post_id, path, prompt, now()))

def list_images(limit=100):
    with get_conn() as conn:
        return conn.execute('SELECT * FROM images ORDER BY id DESC LIMIT ?', (limit,)).fetchall()

def insert_campaign(name, brief, output):
    with get_conn() as conn:
        conn.execute('INSERT INTO campaigns(name,brief,output,created_at) VALUES(?,?,?,?)', (name, brief, output, now()))

def list_campaigns(limit=50):
    with get_conn() as conn:
        return conn.execute('SELECT * FROM campaigns ORDER BY id DESC LIMIT ?', (limit,)).fetchall()
