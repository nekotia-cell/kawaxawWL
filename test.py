import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command  # Добавляем фильтр для команд

# --- КОНФИГУРАЦИЯ ---
BOT_TOKEN = "7533873451:AAGbVm39RUCvTPwQuZ6m3Fsccny8t8HsnBg"
BASE_URL = "https://telegram-auto-clicker--jah08664.replit.app"

# --- HTML КОД АВТОКЛИКЕРА ---
HTML_PAGE = """
<!DOCTYPE html>
<html lang="ru">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Auto Clicker</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body {
            font-family: sans-serif;
            background-color: var(--tg-theme-bg-color, #fff);
            color: var(--tg-theme-text-color, #000);
            display: flex; flex-direction: column;
            align-items: center; justify-content: center;
            height: 100vh; margin: 0; user-select: none;
        }
        h1 { font-size: 48px; margin: 0; }
        .counter { font-size: 64px; font-weight: bold; color: var(--tg-theme-button-color, #3390ec); margin: 20px 0; }
        button {
            padding: 15px 30px; font-size: 18px; border: none;
            border-radius: 12px; background-color: var(--tg-theme-button-color, #3390ec);
            color: var(--tg-theme-button-text-color, #fff); cursor: pointer; margin: 10px;
        }
        .auto-btn { background-color: var(--tg-theme-secondary-bg-color, #f0f0f0); color: var(--tg-theme-text-color, #000); }
        .auto-btn.active { background-color: #4caf50; color: white; }
    </style>
</head>
<body>
    <h1>Монеты</h1>
    <div class="counter" id="score">0</div>
    <button onclick="manualClick()">Клик!</button>
    <button class="auto-btn" id="autoBtn" onclick="toggleAuto()">Авто: ВЫКЛ</button>
    <script>
        const tg = window.Telegram.WebApp;
        tg.ready(); tg.expand();
        let score = 0;
        let autoInterval = null;
        const scoreEl = document.getElementById('score');
        const autoBtn = document.getElementById('autoBtn');
        function updateScore() {
            score++; scoreEl.innerText = score;
            tg.HapticFeedback.impactOccurred('light');
        }
        function manualClick() { updateScore(); }
        function toggleAuto() {
            if (autoInterval) {
                clearInterval(autoInterval); autoInterval = null;
                autoBtn.innerText = "Авто: ВЫКЛ"; autoBtn.classList.remove('active');
            } else {
                autoInterval = setInterval(updateScore, 100);
                autoBtn.innerText = "Авто: ВКЛ"; autoBtn.classList.add('active');
            }
        }
    </script>
</body>
</html>
"""

# --- ИНИЦИАЛИЗАЦИЯ ---
logging.basicConfig(level=logging.INFO)

# aiogram 3.x: Dispatcher() без аргументов
dp = Dispatcher()
bot = Bot(token=BOT_TOKEN)

# --- ОБРАБОТЧИК ---
@dp.message(Command("start"))  # Новый синтаксис фильтра
async def cmd_start(message: types.Message):
    kb = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🎮 Открыть Кликер", web_app=types.WebAppInfo(url=f"{BASE_URL}/"))]
    ])
    await message.answer("Привет! Нажми на кнопку ниже 👇", reply_markup=kb)

# --- ВЕБ СЕРВЕР ---
async def handle_webapp(request):
    return web.Response(text=HTML_PAGE, content_type='text/html')

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_webapp)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    print(f"✅ Сервер запущен: {BASE_URL}")

# --- ЗАПУСК ---
async def main():
    await asyncio.gather(
        start_web_server(),
        dp.start_polling(bot)  # Передаем bot в start_polling
    )

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот остановлен")