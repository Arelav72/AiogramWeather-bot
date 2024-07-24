import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart,Command
from aiogram.types import Message

import requests
from config import TOKEN
from config import API_KEY

import random

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('help'))
async def help(message: Message):
    await message.answer("Этот бот умеет выполнять команды:\n/start\n/help")

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer("Привет! Я бот оправляю погоду!")

@dp.message(Command('weather'))
async def get_weather(message: Message):
    city = message.text.split()[-1]
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'

    response = requests.get(url)
    data = response.json()

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']

        await message.answer(f'Weather in {city}: {weather_description}, Temperature: {temperature}K')
    else:
        await message.answer('City not found')




async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

# Запрос к API и парсинг ответа имеет сложность, зависящую от времени выполнения сетевого запроса и парсинга JSON.
# Это не алгоритмическая сложность в обычном смысле, но можно сказать,
# что сетевые запросы и обработка данных имеют сложность O(1),
# так как выполняются за постоянное время независимо от размера данных
# (предполагая, что ответ от API имеет фиксированный формат и размер).
# Запуск основного цикла диспетчера зависит от количества получаемых сообщений,
# но каждый цикл обработки сообщения выполняется за постоянное время  O(1),
# если не учитывать время сетевых запросов.
#  Таким образом, основные части кода имеют константную сложность  O(1),
#  за исключением времени, необходимого для выполнения сетевых запросов и ожидания ответа от API,
#  которые зависят от внешних факторов.
