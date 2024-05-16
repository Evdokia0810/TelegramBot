import psycopg2
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import re

# Токен бота и данные для подключения к базе данных
TOKEN = '6580465417:AAFy9A-X4mKYTfzeT9eUgBSj_SG_rC9S1d8'
DB_URL = 'postgresql://test_user:test123@localhost/postgres'

# Подключаемся к базе данных
def connect_to_db():
    return psycopg2.connect(DB_URL)

# Создаем таблицу в базе данных, если ее первоначально не существовало
def create_database_table():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS saved_articles (
            id SERIAL PRIMARY KEY,
            url TEXT NOT NULL,
            user_id INTEGER NOT NULL
        );
    """)
    conn.commit()
    cursor.close()
    conn.close()

# Получение курсора и соединение с базой данных
def get_cursor():
    conn = connect_to_db()
    return conn.cursor(), conn

# Закрываем соединения с базой данных
def close_connection(cursor, conn):
    cursor.close()
    conn.close()

# Команда /start
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я бот, который поможет тебе сохранять статьи для чтения :)\n\n"
                              "- Просто отправь мне ссылку на статью, и я ее сохраню.\n\n"
                              "- Чтобы получить случайную сохраненную статью, введи /get_random_article.\n\n"
                              "Приятного чтения!")

# Сохраненяем статью в базе данных
def save(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    article_url = update.message.text.strip()

    # Проверяем на корректность ссылки
    if not re.match(r'^https?://\S+$', article_url):
        update.message.reply_text("Ошибка! Пожалуйста, введите корректную ссылку на статью.")
        return

    try:
        cursor, conn = get_cursor()
        cursor.execute("SELECT url FROM saved_articles WHERE user_id = %s AND url = %s;", (user_id, article_url))
        existing_article = cursor.fetchone()
        if existing_article:
            update.message.reply_text("Упс, эта статья уже была сохранена :)")
        else:
            cursor.execute("INSERT INTO saved_articles (url, user_id) VALUES (%s, %s);", (article_url, user_id))
            conn.commit()
            update.message.reply_text("Статья успешно сохранена!")
    except Exception as e:
        logger.error(f"Ошибка при сохранении статьи: {e}")
    finally:
        close_connection(cursor, conn)

# Получаем случайную сохраненную статью из базы данных
def get_random_article(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id
    try:
        cursor, conn = get_cursor()
        cursor.execute("SELECT url FROM saved_articles WHERE user_id = %s ORDER BY RANDOM() LIMIT 1;", (user_id,))
        article = cursor.fetchone()
        if article:
            update.message.reply_text(f"Вот случайная статья для тебя: {article[0]}\nПриятного чтения!")
            cursor.execute("DELETE FROM saved_articles WHERE user_id = %s AND url = %s;", (user_id, article[0]))
            conn.commit()
        else:
            update.message.reply_text("У вас пока нет сохраненных статей :(\nЕсли найдете что-то интересное, отправьте мне ссылку!")
    except Exception as e:
        logger.error(f"Ошибка при получении статьи: {e}")
    finally:
        close_connection(cursor, conn)

# неизвестные команды
def unknown(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Извините, я не понимаю вашу команду. Пожалуйста, попробуйте еще раз.")

# Основная функция, которая запускает бота
def main() -> None:
    create_database_table()
    updater = Updater(TOKEN)    
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, save))
    dispatcher.add_handler(CommandHandler("get_random_article", get_random_article))
    dispatcher.add_handler(MessageHandler(Filters.command, unknown))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
