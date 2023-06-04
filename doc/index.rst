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
    
.. automodule:: support_functions
    :members:
    :undoc-members:

Часть 2. Web app
========================================

Pages elements:

.. automodule:: elements/common
    :members:
    :undoc-members:

.. automodule:: elements/main_page
    :members:
    :undoc-members:

.. automodule:: elements/result_page
    :members:
    :undoc-members:

.. automodule:: elements/utils
    :members:
    :undoc-members:

Elements templates:

.. automodule:: templates/common
    :members:
    :undoc-members:

.. automodule:: templates/main_page
    :members:
    :undoc-members:

.. automodule:: templates/result_page
    :members:
    :undoc-members:

Часть 3. Поисковый индекс
========================================
Задачи - хранение для каждого токена индексов документов, в которых он содержится; булев поиск множества документов по запросу пользователя.
Для имеющихся данных строится обратный поисковый индекс и сжимается с помощью метода VarByte encoding. Булев поиск осуществляется с помощью перевода запроса пользователя в форму польской инверсной нотации и вычисления конечного множества документов на её основе.

    
2.1. Поисковый индекс
---------------------

.. automodule:: index
    :members:
    :undoc-members:
 
2.2. VarByte кодирование
------------------------
    
.. automodule:: varbyte_encoding
    :members:
    :undoc-members:
    
2.3. Обработка запроса
----------------------
    
.. automodule:: query_processing
    :members:
    :undoc-members:

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
