import sqlite3
from datetime import datetime

DB_NAME = "retail_intelligence.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            customer_count INTEGER,
            dominant_mood TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_visit_data(count, mood):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute("""
        INSERT INTO customer_analytics (timestamp, customer_count, dominant_mood)
        VALUES (?, ?, ?)
    """, (current_time, count, mood))
    
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print("Database ready!")