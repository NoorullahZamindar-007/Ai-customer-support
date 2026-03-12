import os
import sqlite3
from contextlib import closing
from typing import Any, Dict, List, Optional


CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS chat_logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_message TEXT NOT NULL,
    bot_reply TEXT,
    created_at TEXT NOT NULL,
    status TEXT NOT NULL,
    error_message TEXT,
    ip_address TEXT
);
"""


class Database:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)

    def get_connection(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def init_db(self) -> None:
        with closing(self.get_connection()) as connection:
            connection.execute(CREATE_TABLE_SQL)
            connection.commit()

    def save_chat_log(
        self,
        user_message: str,
        bot_reply: Optional[str],
        status: str,
        error_message: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> int:
        query = """
        INSERT INTO chat_logs (user_message, bot_reply, created_at, status, error_message, ip_address)
        VALUES (?, ?, datetime('now'), ?, ?, ?)
        """

        with closing(self.get_connection()) as connection:
            cursor = connection.execute(
                query,
                (user_message, bot_reply, status, error_message, ip_address),
            )
            connection.commit()
            return int(cursor.lastrowid)

    def fetch_recent_logs(self, limit: int = 20) -> List[Dict[str, Any]]:
        query = """
        SELECT id, user_message, bot_reply, created_at, status, error_message, ip_address
        FROM chat_logs
        ORDER BY id DESC
        LIMIT ?
        """

        with closing(self.get_connection()) as connection:
            rows = connection.execute(query, (limit,)).fetchall()
            return [dict(row) for row in rows]
