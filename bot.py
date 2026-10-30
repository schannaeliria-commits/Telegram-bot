import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TELEGRAM_BOT_TOKEN = os.getenv("BOT_TOKEN")


bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

def main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="📊 Узнать курсы")
    builder.button(text="💡 Шпаргалка: Спот и USDT")
    builder.button(text="📰 Свежие крипто-новости")
    builder.adjust(2, 1)
    return builder.as_markup(resize_keyboard=True)

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    await message.answer(
        f"Привет, {message.from_user.first_name}!\nЯ твой обучающий крипто-ассистент.",
        reply_markup=main_keyboard()
    )

@dp.message(F.text == "💡 Шпаргалка: Спот и USDT")
async def cheat_sheet(message: types.Message):
    text = (
        "💡 **Шпаргалка для новичка:**\n\n"
        "• **USDT (Tether)** — цифровой аналог доллара США (стейблкоин). Курс всегда стремится к $1.\n"
        "• **Спот (Спотовый рынок)** — покупка реальной криптовалюты. Купили монету — она ваша, хранится на кошельке без риска ликвидации при падении."
    )
    await message.answer(text, parse_mode="Markdown")

@dp.message(F.text == "📊 Узнать курсы")
async def crypto_rates(message: types.Message):
    url = "https://data-api.binance.vision/api/v3/ticker/price"

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params={"symbols": '["BTCUSDT","ETHUSDT","TONUSDT"]'}, timeout=5) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    prices = {item['symbol']: float(item['price']) for item in data}
                    text = (
                        "📊 **Актуальные курсы криптовалют:**\n\n"
                        f"• **Bitcoin (BTC):** `${prices.get('BTCUSDT', 0):,.2f}`\n"
                        f"• **Ethereum (ETH):** `${prices.get('ETHUSDT', 0):,.2f}`\n"
                        f"• **Toncoin (TON):** `${prices.get('TONUSDT', 0):,.2f}`\n"
                    )
                    await message.answer(text, parse_mode="Markdown")
                else:
                    await message.answer("⚠️ Не удалось получить курсы. Попробуйте позже.")
    except Exception as e:
        await message.answer("⚠️ Ошибка соединения с биржей.")


@dp.message(F.text == "📰 Свежие крипто-новости")
async def crypto_news(message: types.Message):
    text = (
        "📰 **Главное на крипторынке сегодня:**\n\n"
        "• Биткоин удерживает ключевые уровни поддержки.\n"
        "• Экосистема TON продолжает расширять число активных пользователей.\n"
        "• Институциональный интерес к криптоактивам стабильно растет."
    )
    await message.answer(text, parse_mode="Markdown")

import os
from aiohttp import web

async def handle(request):
    return web.Response(text="Bot is running!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

@dp.message(F.text)
async def ai_assistant(message: types.Message):
    # Проверяем наличие ключа API
    if not GEMINI_API_KEY:
        await message.answer("⚠️ Ключ GEMINI_API_KEY не настроен на сервере.")
        return

    # Показываем статус "печатает..." в чате
    await message.bot.send_chat_action(chat_id=message.chat.id, action="typing")
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-3.0-flash:generateContent?key={GEMINI_API_KEY}"

    
    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": f"Ты дружелюбный крипто-помощник для новичков. Ответь кратко, понятно и по делу на сообщение пользователя: {message.text}"
                    }
                ]
            }
        ]
    }
    
    try:
        # Устанавливаем тайм-аут 20 секунд на случай задержек сети
        timeout = aiohttp.ClientTimeout(total=20)
        async with aiohttp.ClientSession(timeout=timeout) as session:
            async with session.post(url, json=payload, headers=headers) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    try:
                        reply = data["candidates"][0]["content"]["parts"][0]["text"]
                        await message.answer(reply)
                    except (KeyError, IndexError):
                        # Срабатывает, если ответ был заблокирован фильтрами контента
                        await message.answer("⚠️ Не удалось сформировать ответ, попробуйте переформулировать вопрос.")
                else:
                    error_text = await resp.text()
                    print(f"Ошибка Gemini API {resp.status}: {error_text}")
                    await message.answer("⚠️ ИИ сейчас перегружен, попробуйте позже.")
    except asyncio.TimeoutError:
        print("Ошибка: Превышено время ожидания ответа от Gemini API")
        await message.answer("⚠️ Сервер нейросети отвечает слишком долго. Попробуйте еще раз.")
    except Exception as e:
        print(f"Ошибка связи: {e}")
        await message.answer("⚠️ Ошибка связи с нейросетью.")

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":


    
    asyncio.run(main())
