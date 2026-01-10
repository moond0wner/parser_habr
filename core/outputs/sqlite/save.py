import sqlite3
import logging
import os
from datetime import datetime

from cli.config import get_value_from_data
from core.outputs.sqlite.create_db import create_database


def save_to_sqlite(vacancies, target_name):
    file_name = f'vacancies_{target_name}_{datetime.now().strftime("%Y_%m_%d_%H_%M")}.db'
    create_database(file_name)
    conn = sqlite3.connect(os.path.join(get_value_from_data("path_to_load"), file_name))
    cursor = conn.cursor()

    saved_count = 0
    skipped_count = 0

    for vacancy in vacancies:
        try:
            cursor.execute(
                '''
                INSERT OR IGNORE INTO vacancies
                (title, company, salary, meta, skills, link, query)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    vacancy.get('title', ''),
                    vacancy.get('company', ''),
                    vacancy.get('salary', ''),
                    vacancy.get('meta', ''),
                    vacancy.get('skills', ''),
                    vacancy.get('link', ''),
                    target_name
                )
            )
            if cursor.rowcount > 0:
                saved_count += 1
            else:
                skipped_count += 1
        except sqlite3.Error as e:
            logging.error(f'Ошибка сохранения {vacancy.get('title')}: {e}')

    conn.commit()
    conn.close()
    logging.info(f'Готово! Данные сохранены в {file_name} \nСохранено: {saved_count}, пропущено дубликатов: {skipped_count}')
