import os
import shutil
import asyncio
import requests
import random
import datetime

from app import dp, bot, query, week, time_table
from config import MYSQL_HOST

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


work_path = os.path.abspath(os.curdir)

if requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST: # Необходимо, потому что команда /git и /restar работает только на хостинге
    @dp.message_handler(commands=["git"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        os.system("git pull https://github.com/opolonix/JournalBot")
        await message.reply("🪛 Команда на клонирование гит репозитория отправлена")
        await message.reply("🪛 Рестарт бота")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()


        os.system(f"python {work_path}/app.py &")
        exit()

    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await message.reply("🪛 Рестарт бота")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()


        os.system(f"python {work_path}/app.py &")
        exit()

@dp.message_handler(commands=["export", "exp"])
async def handler(message: types.message):
    """
        Экспорт файлов из бота команда /export <путь к файлу>
        Просто /export создает архив всего бота
    """
    if message['from']['id'] not in [780882761, 1058211493]: return
    message.text = message.text.split(" ")
    message.text.pop(0)
    message.text = ' '.join(message.text).replace("\\", "/").replace(" ", "")
    if message.text == '' or message.text == '/':
        print(message)
        await bot.send_document(message.chat.id,  InputFile(shutil.make_archive("files", 'zip', work_path), filename='BioAttacker.zip'))
        os.remove(work_path + "/files.zip")
    else:
        if not message.text.startswith('/'): message.text = "/" + message.text
        if os.path.exists(work_path + message.text):
            if not os.path.isfile(work_path + message.text):
                await bot.send_document(message.chat.id,  InputFile(shutil.make_archive("files", 'zip', work_path + message.text),  filename=message.text + ".zip"))
                os.remove(work_path + "/files.zip")
            else:
                await bot.send_document(message.chat.id,  InputFile(work_path + message.text, filename=message.text))
        else: await message.reply(f"🪛 Путь `{message.text}` не найден")


@dp.message_handler(content_types=['text']) 
async def handler(message: types.message):
    print(message)
    if message.text.lower() == "расписание":
        result = time_table(datetime.date.today())
        await message.reply(result, parse_mode = "Markdown")

    if message.text.lower().startswith("+пара "):
        text = message.text[6::]
        print(text)
        await message.reply(text, parse_mode = "Markdown")