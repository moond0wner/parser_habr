from typing import Dict, Any

import streamlit as st

from cli.config import change_quantity_pages, get_value_from_data


def render_sidebar() -> Dict[str, Any]:
    """Отображение бокового меню на сайте"""
    with st.sidebar:
        st.header("Настройки поиска")
        pages = st.slider(
            "Количество страниц:",
            min_value=1,
            max_value=20,
            value=get_value_from_data("quantity_pages"),
            help="Сколько страниц парсить"
        )

        st.subheader("Фильтры")
        filter_type = st.radio(
            "Тип фильтра:",
            ["По должности", "По навыкам", "По описанию", "По навыкам, должности и описанию", "Без фильтра"]
        )

        filter_config = {
            "mode": "",
            "keywords": []
        }

        match filter_type:
            case "По навыкам":
                filter_config["mode"] = "skills"
                skills = '_'.join(st.text_input("Навыки (через пробел):", "python linux fastapi").split())
                if skills:
                    filter_config["keywords"] = skills
            case "По должности":
                filter_config["mode"] = "title"
                title = st.text_input("Должность:", "системный аналитик")
                if title:
                    filter_config["keywords"] = '_'.join(title.lower().split())
            case "По описанию":
                filter_config["mode"] = "meta"
                meta = '_'.join(st.text_input("Описание (через пробел):", "senior москва удаленно").split())
                if meta:
                    filter_config["keywords"] = meta
            case "По навыкам, должности и описанию":
                filter_config["mode"] = "all_conditions"
                all_conditions = '_'.join(st.text_input("Ключевые слова (через пробел):", "python developer senior москва удаленно").split())
                if all_conditions:
                    filter_config["keywords"] = all_conditions
            case "Без фильтра":
                filter_config['mode'] = 'anywhere'
                filter_config['keywords'] = 'общий_поиск'


        output_formats = st.multiselect(
            "Выберите форматы сохранения:",
            options=['json', 'csv', 'sqlite'],
            format_func=lambda x: {
                'json': "JSON (анализ данных)",
                'csv': "CSV (Excel таблицы)",
                'sqlite': "SQLite (база данных)"
            }.get(x)
        )


        run_button = st.button(
            "Начать парсинг",
            type="primary",
            use_container_width=True
        )
    change_quantity_pages(pages)

    return {
        "filter_config": filter_config,
        "output_formats": output_formats,
        "run_button": run_button
    }