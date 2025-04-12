import sqlite3
from src.utils.logger import Logger
import time

class DebateDB:
    def __init__(self):
        self.db_path = "debates.db"
        self.logger = Logger()
        self._init_db()

    def _init_db(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("""
                    CREATE TABLE IF NOT EXISTS debates (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        topic TEXT,
                        arguments TEXT,
                        rebuttals TEXT,
                        consensus TEXT,
                        date TEXT
                    )
                """)
                conn.commit()
        except Exception as e:
            self.logger.log(f"Error initializing database: {e}")

    def save_debate(self, topic, arguments, rebuttals, consensus):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute(
                    "INSERT INTO debates (topic, arguments, rebuttals, consensus, date) VALUES (?, ?, ?, ?, ?)",
                    (
                        topic,
                        str(arguments),
                        str(rebuttals),
                        consensus,
                        time.ctime()
                    )
                )
                conn.commit()
        except Exception as e:
            self.logger.log(f"Error saving debate: {e}")

    def get_debates(self):
        try:
            with sqlite3.connect(self.db_path) as conn:
                c = conn.cursor()
                c.execute("SELECT topic, arguments, rebuttals, consensus, date FROM debates")
                return [
                    {
                        "topic": row[0],
                        "arguments": row[1],
                        "rebuttals": row[2],
                        "consensus": row[3],
                        "date": row[4]
                    }
                    for row in c.fetchall()
                ]
        except Exception as e:
            self.logger.log(f"Error retrieving debates: {e}")
            return []