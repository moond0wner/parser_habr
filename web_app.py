"""Отображение сайта"""
# web_app.py
import streamlit as st

from core.parser.engine import get_habr_vacancies
from web.results import show_results
from web.sidebar import render_sidebar

st.markdown("""
    <style>
    .stDownloadButton {
        display: flex;
        justify-content: center;
    }
    h1 {
        text-align: center;
    }
    h2 {
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title='Парсер вакансий',
    layout="wide"
)

st.markdown("<h1>Парсер вакансий с <a href='https://career.habr.com/'>Хабр Карьера</h1>", unsafe_allow_html=True)
st.markdown("---")


settings = render_sidebar()
if 'vacancies_data' not in st.session_state:
    st.session_state['vacancies_data'] = None

if settings["run_button"]:
    try:
        with st.spinner("Парсим..."):
            vacancies = get_habr_vacancies(
                filter_config=settings['filter_config'],
                output_format=settings['output_formats'],
                type_application='web'
            )

            st.session_state['vacancies_data'] = vacancies

    except Exception as e:
        st.error(f"Ошибка: {e}")
        st.code(str(e))
        st.stop()

if st.session_state['vacancies_data'] is not None:
    show_results(st.session_state['vacancies_data'], settings)

    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        if st.button("Очистить результаты", use_container_width=True):
            st.session_state['vacancies_data'] = None
            st.rerun()