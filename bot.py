import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

# ==================== ТВОИ ДАННЫЕ ====================
TELEGRAM_BOT_TOKEN = "8712306634:AAG18XtryOhDLOfMU1Qxv1_uxuT8iPWpNXg"
GEMINI_API_KEY = "YOUR_GEMINI_KEY"
# =====================================================

bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📊 Узнать курсы")
    builder.button(text="💡 Шпаргалка: Спот и Фьючерсы")
    builder.button(text="📰 Свежие крипто-новости")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}! 👋\n"
        "Я твой обучающий крипто-ассистент. Выбери действие в меню ниже:",
        reply_markup=main_keyboard()
    )

async def main():
    print("Бот запускается...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
