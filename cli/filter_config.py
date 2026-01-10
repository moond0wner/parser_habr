import logging
from typing import Dict, List

def create_filter_config() -> Dict[str, List | str]:
    """Фильтрация поиска"""
    print("\n\n--- Настройка фильтра ---")
    filter_config = {
        "mode": "",
        "keywords": [],
    }
    while True:
        print("Где искать ключевые слова?")
        print("1. В навыках - для поиска по языкам программирования")
        print("2. В названии вакансии - для поиска по должности")
        print("3. В описании - для поиска по квалификации, месту работы, возможности удаленной работы и т.д")
        print("4. В навыках, вакансиях и описании - широкий поиск")
        print("5. Без фильтра - искать всё подряд")

        try:
            choice = int(input("Выбрать (1-5): "))
            match choice:
                case 1:
                    filter_config["mode"] = "skills"
                    keywords = input("Введите ключевые слова через пробел (например: python linux fastapi kafka): ")
                    if not keywords:
                        print("Запрос не должен быть пустым")
                        continue
                    filter_config['keywords'] = [k.strip().lower() for k in keywords.split()]
                    break
                case 2:
                    filter_config["mode"] = "title"
                    keyword = input("Введите должность (например: системный аналитик)")
                    if not keyword:
                        print("Запрос не должен быть пустым")
                        continue
                    filter_config['keywords'] = [keyword]
                    break
                case 3:
                    filter_config["mode"] = "meta"
                    keywords = input("Введите ключевые слова через пробел (например: junior москва удаленно): ")
                    if not keywords:
                        print("Запрос не должен быть пустым")
                        continue
                    filter_config['keywords'] = [k.strip().lower() for k in keywords.split()]
                    break
                case 4:
                    filter_config["mode"] = "all_conditions"
                    keywords = input("Введите ключевые слова через пробел (например: python senior удаленно москва): ")
                    if not keywords:
                        print("Запрос не должен быть пустым")
                        continue
                    filter_config['keywords'] = [k.strip().lower() for k in keywords.split()]
                    break
                case 5:
                    filter_config["mode"] = "anywhere"
                    break
        except ValueError:
            logging.error("Ошибка ввода")
            continue

    return filter_config