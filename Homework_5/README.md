## Домашнее задание №5

Файл с результатом выполнения скрипта помещается в папку `temporary_files`  
Имя файла с результатом: `{название_скрипта}_answer_[py,sh].[txt,json]`  
Python скрипты поддерживают флаг `--json`  
В папке с ДЗ есть скрипт `run_all_scripts.sh`, который запускает все bash и python скрипты (и с флагом `--json`, и без него)

1. ### Общее количество запросов
    * #### Bash script `number_of_requests.sh`
        * Считает количество строк в файле при помощи `wc -l`
        * Записывает решение в `number_of_requests_answer_sh.txt`
    * #### Python script `number_of_requests.py`
        * Считает количество строк в файле при помощи `len`
        * Если есть флаг `--json`:
            * Записывает решение в `number_of_requests_answer_py.json`
        * Иначе:
            * Преобразует словарь с решением в строку
            * Записывает решение в `number_of_requests_answer_py.txt`
    
2. ### Общее количество запросов по типу
    * #### Bash script `number_of_requests_by_type.sh`
        * Извлекает метод запроса из каждой записи. Игнорирует невалидные записи
        * Сортирует получившийся список
        * Извлекает уникальные значения и подсчитывает количество повторений каждого значения
        * Сортирует получившийся список по количеству повторений
        * Форматирует каждую запись в нужный формат
        * Записывает решение в `number_of_requests_by_type_answer_sh.txt`
    * #### Python script `number_of_requests_by_type.py`
        * Извлекает метод запроса из каждой записи. Игнорирует невалидные записи
        * Извлекает уникальные значения и подсчитывает количество повторений каждого значения. Записывает значения и количество их повторений в словари
        * Сортирует получившийся список словарей по количеству повторений
        * Если есть флаг `--json`:
            * Записывает решение в `number_of_requests_by_type_answer_py.json`
        * Иначе:
            * Преобразует словарь с решением в строку
            * Записывает решение в `number_of_requests_by_type_answer_py.txt`
    
3. ### Топ 10 самых частых запросов
    * #### Bash script `most_frequent_requests.sh`
        * Извлекает URL из каждой записи
        * Сортирует получившийся список
        * Извлекает уникальные значения и подсчитывает количество повторений каждого значения
        * Сортирует получившийся список по количеству повторений
        * Извлекает первые 10 записей
        * Форматирует каждую запись в нужный формат
        * Записывает решение в `most_frequent_requests_answer_sh.txt`
    * #### Python script `most_frequent_requests.py`
        * Извлекает URL из каждой записи
        * Извлекает уникальные значения и подсчитывает количество повторений каждого значения. Записывает значения и количество их повторений в словари
        * Сортирует получившийся список словарей по количеству повторений
        * Извлекает первые 10 записей
        * Если есть флаг `--json`:
            * Записывает решение в `most_frequent_requests_answer_py.json`
        * Иначе:
            * Преобразует словарь с решением в строку
            * Записывает решение в `most_frequent_requests_answer_py.txt`
    
4. ### Топ 5 самых больших по размеру запросов, которые завершились клиентской (4ХХ) ошибкой
    * #### Bash script `largest_requests.sh`
        * Извлекает URL, статус код, размер запроса и IP адрес из записей, статус код которых начинается на 4
        * Форматирует каждую запись в нужный формат
        * Сортирует получившийся список и оставляет только уникальные значения
        * Сортирует получившийся список по размеру запроса
        * Извлекает первые 5 записей
        * Записывает решение в `largest_requests_answer_sh.txt`
    * #### Python script `largest_requests.py`
        * Фильтрует записи и оставляет только те, статус код которых начинается на 4
        * Сортирует получившийся список записей сначала по всем полям, кроме размера, а затем по размеру в обратном порядке
        * Создает словари с URL, статус кодом, размером запроса и IP адресом
        * Если поднят флаг `remove_repeats`:
            * Записывает в решение только уникальные записи
        * Если есть флаг `--json`:
            * Записывает решение в `largest_requests_answer_py.json`
        * Иначе:
            * Преобразует словарь с решением в строку
            * Записывает решение в `largest_requests_answer_py.txt`
    
5. ### Топ 5 пользователей по количеству запросов, которые завершились серверной (5ХХ) ошибкой
    * #### Bash script `users_by_number_of_requests.sh`
        * Извлекает IP из записей, статус код которых начинается на 5
        * Сортирует получившийся список
        * Извлекает уникальные значения и подсчитывает количество повторений каждого значения
        * Сортирует получившийся список количеству повторений
        * Извлекает первые 5 записей
        * Форматирует каждую запись в нужный формат
        * Записывает решение в `users_by_number_of_requests_answer_sh.txt`
    * #### Python script `users_by_number_of_requests.py`
        * Фильтрует записи и оставляет только те, статус код которых начинается на 5
        * Извлекает IP из каждой записи
        * Извлекает уникальные значения и подсчитывает количество повторений каждого значения. Записывает значения и количество их повторений в словари
        * Сортирует получившийся список словарей по количеству повторений
        * Извлекает первые 5 записей
        * Если есть флаг `--json`:
            * Записывает решение в `users_by_number_of_requests_answer_py.json`
        * Иначе:
            * Преобразует словарь с решением в строку
            * Записывает решение в `users_by_number_of_requests_answer_py.txt`
   

### Решение на Bash
* #### Плюсы:
    * Скрипт меньше по объему и писать его быстрее чем аналогичный скрипт на Python. Большая часть нужных инструменты уже есть, нужно лишь подобрать верные команды, аргументы и флаги
    * Скорость работы выше, чем у аналогичного скрипта на Python
* #### Минусы:
    * Нужно знать, как пользоваться командами. У некоторых команд (например, awk) свой синтаксис, с которым нужно научиться работать, прежде чем писать скрипты
    * Работает только на Linux (на Windows можно запускать Bash скрипты через WSL, но его нужно устанавливать отдельно)
    * Скрипты (в особенности, однострочники) не отличаются гибкостью. Добавление доп. условий (если это вообще будет возможно) может сильно сказаться на простоте, размере скрипта и скорости его работы. На Python можно добиться гораздо большей гибкости

### Решение на Python
* #### Плюсы:
    * Кроссплатформенность. Скрипт работает везде, где есть Python 
    * Гибкость. Доступны все Python библиотеки, можно получать данные из БД и использовать их при анализе логов, записывать результат анализа логов в БД, делать графики при помощи matplotlib, передавать данные по сети, сделать целое приложение для анализа логов и красивого представления проанализированной информации и т.д. 
    * Проще работать со строками, чем на Bash
* #### Минусы:
    * Выполняется медленнее, чем скрипты на Bash
    * Нужно знать Python