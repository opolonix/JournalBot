from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
import sys
import asyncio
import time

from config import BOT_TOKEN, OWNER_ID

from libs.mysql_connect import query
from libs.handlers import *
from libs.days_data import week
from libs.time_table import time_table

sys.path.append(os.path.abspath(os.curdir) + "/libs")

bot = Bot(
    token = BOT_TOKEN
)
dp = Dispatcher(bot)

async def on_startup(dp):
    await dp.bot.send_message(OWNER_ID, "Бот запущен")

if __name__ == '__main__':
    from libs.handlers import dp
    executor.start_polling(dp, on_startup=on_startup, skip_updates=True)



