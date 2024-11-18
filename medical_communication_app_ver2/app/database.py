import sqlite3
import os
import json  # json 모듈 추가

DB_PATH = "data/database.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        conversation_text TEXT,
        analysis_result TEXT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

def save_conversation(conversation_text, analysis_result):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # analysis_result를 JSON 문자열로 변환
    if not isinstance(analysis_result, str):
        analysis_result = json.dumps(analysis_result, ensure_ascii=False)
    cursor.execute("""
    INSERT INTO conversations (conversation_text, analysis_result)
    VALUES (?, ?)
    """, (conversation_text, analysis_result))
    conn.commit()
    conn.close()