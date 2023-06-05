.. Spellchecker documentation master file, created by
   sphinx-quickstart on Sun Apr 23 23:17:54 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Slack-open-data-science-search-system's documentation!
=================================================================
Данный проект - реализация системы информационного поиска по дампу сообщений из канала Slack. Open DS.
Задача - найти посты, которые будут релевантны поисковому запросу пользователя.


Программа состоит из 4 основных модулей:

Часть 1. Спеллчекер
========================================
Задача данной системы - исправление опечаток в запросе пользователя. 
Исправление происходит с использованием оценки вероятности исправленного запроса, рассчитанной с помощью модели языка, и вероятности ошибки из модели ошибок. Поиск кандидатов на исправление генерируется с помощью поиска по префиксному дереву.


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   
1.1. Модель ошибок
------------------

.. automodule:: error_model
    :members:
    :undoc-members:
 
1.2. Модель языка
-----------------
    
.. automodule:: language_models
    :members:
    :undoc-members:
    
1.3. Префиксное дерево
----------------------
    
.. automodule:: prefix_tree
    :members:
    :undoc-members:
    
1.4.  Спеллкоректор
-------------------
    
.. automodule:: spellchecker
    :members:
    :undoc-members:
    
1.5.  Обучение моделей и построение дерева
------------------------------------------
    
.. automodule:: build_models
    :members:
    :undoc-members:
    
1.6.  Вспомогательные функции
-----------------------------
    
.. automodule:: utils
    :members:
    :undoc-members:


Часть 4. Парсер и подготовка данных
========================================

4.1. Парсер
------------------

.. automodule:: parser
    :members:
    :undoc-members:

4.2. Чистка данных
------------------

.. automodule:: clean
    :members:
    :undoc-members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
