from typing import Optional, Any, Dict, List

from bs4 import Tag


def get_safe_text(card: Tag, selector: str, class_name: str, separator: Optional[str] = None) -> str:
    """Вспомогательная функция для безопасного извлечения текста"""
    tag = card.find(selector, class_=class_name)
    if not tag: return "Не указано"
    return tag.get_text(separator, strip=True) if separator else tag.get_text(strip=True)


def extract_skills(card: Tag) -> str:
    """Извлекает навыки указанные в вакансии"""
    skills_tag = get_safe_text(card, 'div', 'vacancy-card__skills')
    return skills_tag


def extract_title(card: Tag) -> str:
    """Извлекает должность указанная в вакансии"""
    title_tag = get_safe_text(card, 'div', 'vacancy-card__title')
    return title_tag


def extract_meta(card: Tag) -> str:
    """Извлекает описание указанное в вакансии"""
    meta_tag = get_safe_text(card, 'div', 'vacancy-card__meta', " | ")
    return meta_tag


def extract_salary(card: Tag) -> str:
    """Извлекает зарплату указанную в вакансии"""
    salary = get_safe_text(card, 'div', 'vacancy-card__salary', " ")
    if "Похожие специалисты" in salary:
        salary = salary.replace("Похожие специалисты", "\n(Похожие специалисты") + ")"
    return salary


def extract_company(card: Tag) -> str:
    """Извлекает название компании указанное в вакансии"""
    company_tag = card.find('div', class_='vacancy-card__company')
    company_name = company_tag.find('a').get_text(strip=True) if company_tag and company_tag.find(
        'a') else "Компания не указана"
    return company_name


def extract_rating(card: Tag) -> str:
    """Извлекает рейтинг компании"""
    rating = get_safe_text(card, 'span', 'company-rating__value')
    return rating


def extract_date(card: Tag) -> str:
    """Извлекает дату создания вакансии"""
    date = get_safe_text(card, 'div', 'vacancy-card__date')
    return date


def extract_link(card: Tag) -> str:
    """Извлекают ссылку на вакансию"""
    link = "https://career.habr.com" + card.find('a', class_='vacancy-card__title-link').get('href')
    return link


def filter_vacancy(card: Tag, filter_config: Dict[str, Any], keywords_list: List[str]) -> bool:
    """Проверка вакансии на соответствующие фильтры"""
    if filter_config["mode"] != "anywhere" and keywords_list:
        # проверка на наличие хотя бы одного ключевого слова
        match filter_config["mode"]:
            case "skills":
                search_area = extract_skills(card).lower()

            case "title":
                search_area = extract_title(card).lower()

            case "meta":
                search_area = extract_meta(card).lower()

            case "all_conditions":
                search_area = f"{extract_skills(card)} {extract_title(card)} {extract_meta(card)}".lower()

            case _:
                search_area = ""

        if not any(word.lower() in search_area for word in keywords_list):
            return False

    return True


def parse_vacancy_card(card: Tag, page: int, vacancy_index: int, keywords_str: str) -> Dict[str, str | int]:
    """Возвращает готовые данные о вакансии"""
    return {
        "id": vacancy_index,
        "page": page,
        "date": extract_date(card),
        "company": extract_company(card),
        "rating": extract_rating(card),
        "title": extract_title(card),
        "salary": extract_salary(card),
        "meta": extract_meta(card),
        "skills": extract_skills(card),
        "link": extract_link(card),
        "query": keywords_str
    }
