# Slack-open-data-science-search-system

Есть дамп сообщений из канала open data science (блог про data science) из Слака.
Описание: Веб-приложение, позволяющее осуществлять поиск по этому блогу

Постановка задачи:

1. Распарсить данные, предобработать их
2. Построить поисковый индекс и сжать его для эффективного хранения информации
3. Разработать веб-приложение, к которому пользователи могут слать поисковые вопросы/запросы, а на выходе получать топ N релевантных ответов
4. Предусмотреть исправление опечаток в пользовательском запросе

Используемые инструменты:

1. Для парсинга: библиотека re
2. Для предобработки, токенизации - библиотека nltk
3. Для построения системы исправления опечаток: возможно sklearn(для обучения моделей)

![image](https://user-images.githubusercontent.com/74496817/228052382-f99e3c1e-601c-480c-a888-cd6e71f91712.png)

## How to run app

0. `pybabel compile -D app -d src/locales/ -l ru`

   `pybabel compile -D app -d src/locales/ -l en`

1. `export PYTHONPATH="${PYTHONPATH}:{pwd}/src"`

2. `streamlit run src/app/MainPage.py`

## How to run ui tests

0. `pip install -r requirements.dev.txt`

1. `playwright install`

2. `pytest tests/`
