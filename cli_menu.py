import logging

from cli.config import get_value_from_data, change_quantity_pages
from core.parser.engine import get_habr_vacancies
from cli.filter_config import create_filter_config

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main_loop() -> None:
    """Меню для консоли"""
    while True:
        pages_to_parse = get_value_from_data("quantity_pages")
        print("="*50)
        print("ПАРСЕР ВАКАНСКИЙ ХАБР КАРЬЕРА")
        print("="*50)

        print("1. Начать поиск вакансий")
        print(f"2. Выбрать количество страниц для запроса (опционально, установлено {pages_to_parse})")
        print("0. Выйти")

        # Выбор действия в главном меню
        try:
            user_choice = int(input("Выберите (0-2): "))
        except ValueError:
            print("Ошибка ввода")
            continue

        match user_choice:
            # 1. Поисковой запрос вакансий
            case 1:
                output_format = []
                go_back_to_main_menu = False # отвечает за необходимость выхода в главное меню
                while True:
                    # Выбор формата данных
                    print("\n\n--- Выберите форматы вывода ---")
                    print("1. JSON - для анализа данных:" + (" выбран" if 'json' in output_format else " не выбран"))
                    print("2. CSV - для Excel таблиц:" + (" выбран" if 'csv' in output_format else " не выбран"))
                    print("3. SQLite - для базы данных:" + (" выбран" if 'sqlite' in output_format else " не выбран"))
                    print("4. Продолжить с выбранными форматами")
                    print("5. Вернуться в главное меню (Отмена)")
                    try:
                        choice_format = int(input("Выберите (1-3): "))
                        match choice_format:
                            case 1:
                                if 'json' in output_format:
                                    output_format.remove('json')
                                else:
                                    output_format.append('json')
                                continue
                            case 2:
                                if 'csv' in output_format:
                                    output_format.remove('csv')
                                else:
                                    output_format.append('csv')
                                continue
                            case 3:
                                if 'sqlite' in output_format:
                                    output_format.remove('sqlite')
                                else:
                                    output_format.append('sqlite')
                                continue
                            case 4:
                                if not output_format:
                                    print("Вы не выбрали не один формат")
                                    continue
                                else:
                                    break
                            case 5:
                                go_back_to_main_menu = True
                                break
                            case _:
                                continue
                    except ValueError:
                        print("Ошибка ввода")
                        continue

                if go_back_to_main_menu:
                    continue

                filter_config = create_filter_config() # Настройка фильтра

                try:
                    # Запуск поискового запроса
                    get_habr_vacancies(filter_config, output_format, 'cli')
                except Exception as e:
                    logging.error(f"Ошибка при парсинге: {e}")
                    continue
            case 2:
                # 2. Выбор кол-ва страниц (p.s: хранить значение в json)
                try:
                    pages = int(input("Сколько страниц нужно для анализа? (по умолчанию 10): "))
                    if pages <= 0:
                        print("Количество должно быть больше нуля")
                        continue
                    else:
                        change_quantity_pages(pages)
                        print("Количество страниц для анализа: ", get_value_from_data("quantity_pages"))
                except ValueError:
                    print("Ошибка, введите число")
                    continue
            case 0: # 3. Выход из программы
                break
            case _:
                print("Ошибка ввода")
                continue





if __name__ == "__main__":
    main_loop()
