import logging
import random
import time
from typing import Optional, List, Dict, Any

import requests
from bs4 import BeautifulSoup

from cli.config import get_value_from_data
from core.outputs.csv.save import save_to_csv
from core.outputs.json.save import save_to_json
from core.outputs.sqlite.save import save_to_sqlite
from core.parser.functions import filter_vacancy, parse_vacancy_card

def fetch_page(url) -> Optional[requests.Response]:
    """
    Выполняет GET-запрос по указанному URL и возвращает объект ответа.
    В случае ошибки логирует её и возвращает None.
    """
    try:
        response = requests.get(url, headers=get_value_from_data("headers"))
        response.raise_for_status()
        return response
    except Exception as e:
        logging.error(f"Ошибка сети: {e}")
        return None

def get_habr_vacancies(filter_config: dict, output_format: str, type_application: str = 'cli') -> List[Dict | None]:
    """Парсинг"""

    # Инициализация параметров
    all_data = [] # все релевантные вакансии
    total_vacancy = 0 # кол-во всех вакансий
    total_target_vacancy = 0 # кол-во только релевантных вакансий
    keywords_str = " ".join(filter_config.get("keywords", [])) # строчка ключевых слов через пробел
    keywords_list = filter_config.get("keywords", []) # список ключевых слов
    max_pages = get_value_from_data("quantity_pages") # достаем максимальное кол-во страниц из json

    # Вспомогательная функция для вывода только в CLI
    def cli_log(message: str, is_info: bool = True):
        if type_application == 'cli':
            if is_info:
                logging.info(message)
            else:
                print(message)

    cli_log(f'Страниц для анализа: {max_pages}')
    cli_log('-' * 50, is_info=False)

    for page in range(1, max_pages + 1):
        page_vacancy_counter = 0

        cli_log(f'Парсинг страницы: {page}', is_info=True)

        if filter_config["mode"] == "anywhere": # если фильтр отключен, то парсим любые вакансии
            url = f"https://career.habr.com/vacancies?type=all&page={page}"

            cli_log(f"Поиск вакансий на career.habr", is_info=True)
        else:
            url = f"https://career.habr.com/vacancies?q={keywords_str}&type=all&page={page}"

            cli_log(f"Поиск вакансий на career.habr по запросу: {keywords_str}", is_info=True)

        response = fetch_page(url)
        if not response:
            break

        soup = BeautifulSoup(response.text, 'html.parser')

        if soup.find('div', class_='no-content'):
            cli_log(f"Вакансии по запросу '{keywords_str}' не найдены.", is_info=True)
            break

        vacancies = soup.find_all('div', class_='vacancy-card')
        total_vacancy += len(vacancies)

        for i, card in enumerate(vacancies, start=1):
            if not filter_vacancy(card, filter_config, keywords_list):
                continue
            else:
                vacancy_data = parse_vacancy_card(card, page, i, keywords_str)
                all_data.append(vacancy_data)

                page_vacancy_counter += 1
                cli_log(f"Обработано: {i}/{len(vacancies)}", is_info=True)

        total_target_vacancy += page_vacancy_counter
        cli_log(f"Страница {page}: найдено {len(vacancies)}, сохранено релевантных: {page_vacancy_counter}", is_info=True)

        # Если на целой странице не нашлось ни одной подходящей вакансии
        if filter_config["mode"] != "anywhere" and page_vacancy_counter == 0:
            cli_log("Релевантные вакансии закончились на этой странице. Прекращаем поиск.", is_info=True)
            break

        if page < max_pages:
            delay = random.uniform(*get_value_from_data("request_delay"))
            cli_log(f"Пауза {delay} перед следующей страницей", is_info=True)
            time.sleep(delay)

    cli_log("-"*50)

    if type_application == 'cli':
        if all_data:
            save_results(all_data, filter_config, output_format)
        else:
            search_target = "общий поиск" if filter_config["mode"] == "anywhere" else f"запрос '{keywords_str}'"
            cli_log(f'По запросу "{search_target}" не найдено релевантных вакансий. Файлы не созданы.')

    return all_data


def save_results(
        all_data: List[Dict[str, Any]],
        filter_config: Dict[str, Any],
        output_formats: List[str],
        type_application: str = 'cli'
) -> None:
    """
    Определяет имя файла и сохраняет данные в выбранных форматах.
    """
    if not all_data:
        # Логика для пустых данных
        if filter_config["mode"] == "anywhere":
            search_target = "общий поиск"
        else:
            search_target = f"запрос '{'_'.join(filter_config.get('keywords', []))}'"

        if type_application == 'cli':
            logging.info(f'Релевантных вакансий по запросу "{search_target}" не найдено. Файлы не будут созданы.')
        return

    # 1. Определяем префикс названия файла
    if filter_config["mode"] == "anywhere":
        file_prefix = "общий_поиск"
    else:
        # Берем ключевые слова
        keywords = filter_config.get("keywords", [])
        file_prefix = "_".join(keywords)

    # 2. Сохраняем, если это CLI-приложение
    if type_application == 'cli':
        save_functions = {
            'json': save_to_json,
            'csv': save_to_csv,
            'sqlite': save_to_sqlite
        }

        for fmt in output_formats:
            if fmt in save_functions:
                logging.info(f"Сохраняем данные в {fmt.upper()}...")
                save_functions[fmt](all_data, file_prefix)

        logging.info("Парсинг и сохранение завершены.")
