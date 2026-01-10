import json
import logging
import os
from datetime import datetime

from cli.config import get_value_from_data


def save_to_json(data, target_name):
    filename = f'vacancies_{target_name}_{datetime.now().strftime('%Y_%m_%d_%H_%M')}.json'
    file_path = os.path.join(get_value_from_data("path_to_load"), filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    logging.info(f"Готово! Данные сохранены в {file_path}")