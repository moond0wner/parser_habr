import logging
import os
from datetime import datetime

import pandas as pd

from cli.config import get_value_from_data


def save_to_csv(data, target_name):
    df = pd.DataFrame(data)
    filename = f'vacancies_{target_name}_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.csv'
    file_path = os.path.join(get_value_from_data("path_to_load"), filename)
    logging.info(f'Создана таблица с {len(df)} строками и {len(df.columns)} столбцами')
    df.to_csv(file_path, index=False, encoding="utf-8-sig")
    logging.info(f"Готово! Данные сохранены в {file_path}")