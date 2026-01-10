import sqlite3
import logging
import os

from cli.config import get_value_from_data


def create_database(file_name) -> None:
    """Создает базу данных"""
    conn = sqlite3.connect(os.path.join(get_value_from_data("path_to_load"), file_name))
    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS vacancies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        company TEXT,
        salary TEXT,
        meta TEXT,
        skills TEXT,
        link TEXT UNIQUE,
        query TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        '''
    )

    conn.commit()
    conn.close()
    logging.info("Успешно создана бд: vacancies.db")


