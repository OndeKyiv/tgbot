import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import asyncio
import nest_asyncio
import pandas as pd
import os

# Дозволяємо вкладені event loops
nest_asyncio.apply()

# Налаштування логування з емодзі
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Зменшуємо рівень логування для telegram.ext
logging.getLogger('telegram.ext').setLevel(logging.WARNING)
# Зменшуємо рівень логування для telegram
logging.getLogger('telegram').setLevel(logging.ERROR)

# Константи
TOKEN = os.getenv('BOT_TOKEN')  # Отримуємо токен з середовища
EXCEL_FILE = 'users_data.xlsx'

# Створюємо Excel файл якщо він не існує
if not os.path.exists(EXCEL_FILE):
    df = pd.DataFrame(columns=['chat_id', 'username'])  # Прибрано 'phone' та 'UsersBox'
    df.to_excel(EXCEL_FILE, index=False)

def save_user_data(chat_id, username):
    """Зберігає дані користувача в Excel"""
    try:
        df = pd.read_excel(EXCEL_FILE)
        if not df[df['chat_id'] == chat_id].empty:
            return False
        
        new_data = pd.DataFrame({
            'chat_id': [chat_id],
            'username': [username]
        })
        df = pd.concat([df, new_data], ignore_index=True)
        df.drop_duplicates(subset=['chat_id'], keep='first', inplace=True)
        df.to_excel(EXCEL_FILE, index=False)
        return True
    except Exception as e:
        logger.error(f"❌ Помилка при збереженні даних: {e}")
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Відправляє початкове повідомлення"""
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    
    # Зберігаємо інформацію про користувача
    save_user_data(chat_id, username)
    
    keyboard = [[InlineKeyboardButton('Перейти у канал', url='https://t.me/+ctj-ly-X2MMyYTAy')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo='http://hromada.media/wp-content/uploads/2024/12/hro2.png',
        caption=(
            '⚡️ Новини та інсайди від влади Броварщини\n'
            '💡 Графіки подачі електропостачання\n'
            '👉 Долучайся та будь у курсі\n'
        ),
        reply_markup=reply_markup
    )

async def main() -> None:
    """Запускає бота"""
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(CommandHandler('start', start))
    
    logger.info("🟢 Бот запущено")
    await application.run_polling(allowed_updates=Update.ALL_TYPES)
    logger.info("🔴 Бот зупинено")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except Exception as e:
        logger.error(f"❌ Помилка: {e}")
