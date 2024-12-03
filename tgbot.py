from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import asyncio
import nest_asyncio
import pandas as pd
import os

# Токен вашего бота
TOKEN = '7972722854:AAH30y1KhVey_XkQ_V0Cn8QYxgw-RU8jaF4'

# Путь к файлу Excel
EXCEL_FILE = 'users.xlsx'

# Функция для добавления пользователя в Excel
def add_user_to_excel(user_id, username):
    # Проверяем, существует ли файл
    if os.path.exists(EXCEL_FILE):
        df = pd.read_excel(EXCEL_FILE)
    else:
        df = pd.DataFrame(columns=['user_id', 'username'])

    # Создаем DataFrame для нового пользователя
    new_user_df = pd.DataFrame({'user_id': [user_id], 'username': [username]})

    # Объединяем старый и новый DataFrame
    df = pd.concat([df, new_user_df], ignore_index=True)

    # Сохраняем изменения в файл
    df.to_excel(EXCEL_FILE, index=False)

# Обработчик команды /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Створюємо велику кнопку
    keyboard = [[KeyboardButton('РОЗПОЧАТИ')]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Натисніть РОЗПОЧАТИ",
        reply_markup=reply_markup
    )

# Обробник натискання кнопки
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text == 'РОЗПОЧАТИ':
        # Получаем user_id и username
        user_id = update.effective_user.id
        username = update.effective_user.username

        # Добавляем пользователя в Excel
        add_user_to_excel(user_id, username)

        # URL зображення
        image_url = "https://hromada.media/wp-content/uploads/2024/10/brovary.png"
        
        # Кнопки с переходом на каналы
        keyboard = [
            [InlineKeyboardButton("Голос Броварського району", url="https://t.me/+MR8OR4hhNus3OWQy")],
            [InlineKeyboardButton("Маразми Великодимерської громади", url="https://t.me/velykadymerka")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        try:
            await context.bot.send_photo(
                chat_id=update.effective_chat.id,
                photo=image_url,
                caption="""⚡️ Новини та інсайди від влади Броварщини
💌 Зв'язок @info_holos
🧲 Запрошення t.me/+MR8OR4hhNus3OWQy""",
                reply_markup=reply_markup
            )
        except Exception as e:
            print(f"Error sending photo: {e}")
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="""⚡️ Новини та інсайди від влади Броварщини
💌 Зв'язок @info_holos
🧲 Запрошення t.me/+MR8OR4hhNus3OWQy""",
                reply_markup=reply_markup
            )

# Основная функция
async def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button_handler))
    
    await application.run_polling()

if __name__ == "__main__":
    nest_asyncio.apply()
    asyncio.run(main())
