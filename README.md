# TelegramBot
Информация
Это Telegram бот, который запоминает ссылки на статьи и выдает их рандомно пользователю по его запросу.
После того, как бот отдал ссылку на прочтение - статья больше не хранится в его базе. Пример ссылки, которую можно передать боту: https://example.com.

Установка
Установите интерпретатор python версии 3.12.2 или выше.
Клонируйте репозиторий.
Создайте виртуальное окружение c помощью команды:
python -m venv {venv name}
Активируйте его для Windows с помощью команды:
venv\Scripts\activate.bat
Или для MacOS и Linux с помощью команды:
source venv/bin/activate
Установите необходимые библиотеки с помощью команды pip install имя библиотеки
Установите PostgreSQL.
Запустите базу данных у себя на компьютере.
Запишите адрес локальной бд в переменную окружения.

Запуск программы
Запустите программу с помощью командной строки:

python main.py 
Используйте команду /start, чтобы начать.
Отправьте ссылку на статью
Используйте команду /get_random_article, чтобы получить ссылку на рандомную статью.
