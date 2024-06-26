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
