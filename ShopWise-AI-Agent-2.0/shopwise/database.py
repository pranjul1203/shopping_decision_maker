import sqlite3
from datetime import datetime
DB="shopwise_memory.db"
def conn(): return sqlite3.connect(DB)
def init_db():
    c=conn(); cur=c.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS searches(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT,query TEXT,category TEXT,budget REAL,recommendation TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS snapshots(id INTEGER PRIMARY KEY AUTOINCREMENT,created_at TEXT,product_query TEXT,price REAL,link TEXT)")
    c.commit(); c.close()
def save_search(query,category,budget,recommendation):
    c=conn(); c.execute("INSERT INTO searches VALUES(NULL,?,?,?,?,?)",(datetime.now().isoformat(timespec="seconds"),query,category,budget,recommendation)); c.commit(); c.close()
def get_history():
    c=conn(); rows=c.execute("SELECT created_at,query,category,budget,recommendation FROM searches ORDER BY id DESC").fetchall(); c.close()
    return [{"Date":r[0],"Query":r[1],"Category":r[2],"Budget":f"₹{r[3]:,.0f}","Recommendation":r[4]} for r in rows]
def save_snapshot(query,price,link):
    c=conn(); c.execute("INSERT INTO snapshots VALUES(NULL,?,?,?,?)",(datetime.now().isoformat(timespec="seconds"),query,price,link)); c.commit(); c.close()
def get_snapshots(query):
    c=conn(); rows=c.execute("SELECT created_at,price,link FROM snapshots WHERE product_query=? ORDER BY id",(query,)).fetchall(); c.close()
    return [{"Date":r[0],"Price":f"₹{r[1]:,.0f}","Link":r[2]} for r in rows]
