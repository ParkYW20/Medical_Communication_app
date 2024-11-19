import sqlite3
import os
import json

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


def save_conversation(conversation_text, analysis_result, timestamp):
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # 분석 결과를 JSON 문자열로 변환
        if not isinstance(analysis_result, str):
            analysis_result = json.dumps(analysis_result, ensure_ascii=False)

        cursor.execute("""
        INSERT INTO conversations (conversation_text, analysis_result, timestamp)
        VALUES (?, ?, ?)
        """, (conversation_text, analysis_result, timestamp))
        conn.commit()
    except sqlite3.Error as e:
        print(f"데이터베이스 저장 중 오류 발생: {e}")
    finally:
        conn.close()