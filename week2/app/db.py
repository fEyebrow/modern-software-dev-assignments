from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
DB_PATH = DATA_DIR / "app.db"


@dataclass
class Note:
    """笔记数据模型"""

    id: int
    content: str
    created_at: str


@dataclass
class ActionItem:
    """待办事项数据模型"""

    id: int
    note_id: Optional[int]
    text: str
    done: bool
    created_at: str


def ensure_data_directory_exists() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def get_connection() -> sqlite3.Connection:
    ensure_data_directory_exists()
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def _row_to_note(row: sqlite3.Row) -> Note:
    return Note(id=row["id"], content=row["content"], created_at=row["created_at"])


def _row_to_action_item(row: sqlite3.Row) -> ActionItem:
    return ActionItem(
        id=row["id"],
        note_id=row["note_id"],
        text=row["text"],
        done=bool(row["done"]),
        created_at=row["created_at"],
    )


def init_db() -> None:
    ensure_data_directory_exists()
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            );
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS action_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_id INTEGER,
                text TEXT NOT NULL,
                done INTEGER DEFAULT 0,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (note_id) REFERENCES notes(id)
            );
            """
        )
        connection.commit()


def insert_note(content: str) -> int:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("INSERT INTO notes (content) VALUES (?)", (content,))
        connection.commit()
        last_row_id = cursor.lastrowid
        if last_row_id is None:
            raise ValueError("Failed to retrieve last inserted ID")
        return int(last_row_id)


def list_notes() -> list[Note]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT id, content, created_at FROM notes ORDER BY id DESC")
        rows = cursor.fetchall()
        return [_row_to_note(row) for row in rows]


def get_note(note_id: int) -> Optional[Note]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, content, created_at FROM notes WHERE id = ?",
            (note_id,),
        )
        row = cursor.fetchone()
        return _row_to_note(row) if row else None


def insert_action_items(items: list[str], note_id: Optional[int] = None) -> list[int]:
    with get_connection() as connection:
        cursor = connection.cursor()
        ids: list[int] = []
        for item in items:
            cursor.execute(
                "INSERT INTO action_items (note_id, text) VALUES (?, ?)",
                (note_id, item),
            )
            last_row_id = cursor.lastrowid
            if last_row_id is None:
                raise ValueError("Failed to retrieve last inserted ID")
            ids.append(int(last_row_id))
        connection.commit()
        return ids


def list_action_items(note_id: Optional[int] = None) -> list[ActionItem]:
    with get_connection() as connection:
        cursor = connection.cursor()
        if note_id is None:
            cursor.execute(
                "SELECT id, note_id, text, done, created_at FROM action_items ORDER BY id DESC"
            )
        else:
            cursor.execute(
                "SELECT id, note_id, text, done, created_at FROM action_items WHERE note_id = ? ORDER BY id DESC",
                (note_id,),
            )
        rows = cursor.fetchall()
        return [_row_to_action_item(row) for row in rows]


def get_action_item(action_item_id: int) -> Optional[ActionItem]:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT id, note_id, text, done, created_at FROM action_items WHERE id = ?",
            (action_item_id,),
        )
        row = cursor.fetchone()
        return _row_to_action_item(row) if row else None


def mark_action_item_done(action_item_id: int, done: bool) -> None:
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute(
            "UPDATE action_items SET done = ? WHERE id = ?",
            (1 if done else 0, action_item_id),
        )
        connection.commit()
