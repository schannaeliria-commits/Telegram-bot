import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import ReplyKeyboardBuilder

TELEGRAM_BOT_TOKEN = "8712306634:AAF_plYJuDJscsZbowimVQMtVj5G8ZJxcXo"

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
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum,toncoin&vs_currencies=usd"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    data = await response.json()
                    btc = data.get("bitcoin", {}).get("usd", "—")
                    eth = data.get("ethereum", {}).get("usd", "—")
                    ton = data.get("the-open-network", {}).get("usd", "—")
                    text = f"📊 **Актуальные курсы (USD):**\n\n• Bitcoin: ${btc}\n• Ethereum: ${eth}\n• TON: ${ton}"
                else:
                    text = "Не удалось загрузить курсы, попробуйте чуть позже."
    except Exception:
        text = "Ошибка при получении котировок."
    await message.answer(text, parse_mode="Markdown")

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

async def main():
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
