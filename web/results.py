import os.path
import sqlite3

from datetime import datetime
from typing import Dict, List, Any

import pandas as pd
import streamlit as st


def show_results(vacancies:  List[Dict | None] , settings: Dict[str, Any]) -> None:
    """Отображение результата поиска на сайте"""
    with st.container():
        st.markdown("<h2 style='text-align: center;'>Скачать результаты</h2>", unsafe_allow_html=True)

        if not vacancies:
            st.warning("Нет вакансий для отображения")
            return

        df = pd.DataFrame(vacancies)
        date = datetime.now().strftime("%Y_%m_%d_%H_%M")
        filename = f'vacancies_{settings['filter_config']['keywords']}_{date}'



        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if "json" in settings["output_formats"]:
                json_data = df.to_json(orient='records', force_ascii=False, indent=2)
                st.download_button(
                    label="Скачать JSON 📥",
                    data=json_data,
                    file_name=f'{filename}.json',
                    mime='application/json',
                    key=f'json_{date}',
                    use_container_width=True
                )

            if "csv" in settings["output_formats"]:
                csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    label="Скачать CSV 📊",
                    data=csv_data,
                    file_name=f'{filename}.csv',
                    mime='text/csv',
                    key=f'csv_{date}',
                    use_container_width=True
                )


            if "sqlite" in settings["output_formats"]:
                try:
                    conn = sqlite3.connect(f'{filename}.db')
                    cursor = conn.cursor()

                    cursor.execute(
                        '''
                        CREATE TABLE IF NOT EXISTS vacancies (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        company TEXT,
                        salary TEXT,
                        skills TEXT,
                        meta TEXT,
                        link TEXT UNIQUE,
                        query TEXT,
                        created_at TEXT DEFAULT CURRENT_TIMESTAMP
                        )
                        '''
                    )
                    conn.commit()

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
                                    ', '.join(settings['filter_config']['keywords']
                                )
                            ))
                        except sqlite3.Error as e:
                            st.error(f"Ошибка сохранения в SQLite '{vacancy.get('title')}': {e}'")

                    conn.commit()
                    conn.close()
                    #if os.path.exists(filename):
                    with open(f'{filename}.db', 'rb') as f:
                        db_bytes = f.read()

                    st.download_button(
                        label="Скачать SQLite 📊",
                        data=db_bytes,
                        file_name=f'{filename}.db',
                        mime='application/octet-stream',
                        key=f'sqlite_{date}',
                        use_container_width=True
                    )
                    os.remove(f'{filename}.db')
                except Exception as e:
                    st.error(f"Общая ошибка SQLite: {e}")

