import os
import shutil
import asyncio
import requests
import random
import datetime

from app import dp, bot, query, week, time_table, escape_markdown
from config import MYSQL_HOST

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions


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

@dp.message_handler(commands=["exit"])
async def handler(message: types.message):
    if message['from']['id'] not in [780882761, 1058211493]: return
    await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")
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
    if message.text.lower() == "расписание":
        date = datetime.date.today()
        result = time_table(datetime.datetime.today())

        next_date = date + datetime.timedelta(days=1)
        pre_date = date - datetime.timedelta(days=1)

        inline_add = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton('назад', callback_data=f"edit|{pre_date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('обн', callback_data=f"edit|{date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('вперед', callback_data=f"edit|{next_date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('домашняя работа', callback_data=f"home|{date.strftime('%d.%m.%Y')}"),
        )
        await message.reply(result, parse_mode = "Markdown", reply_markup=inline_add)

    if message.text.lower().startswith("+пара "):
        text = message.text[6::]
        data = {}
        for i in text.split("&"):
            split_item = i.strip().split(' ')
            data[split_item[0]] = ' '.join(split_item[1:])

        print(data)

        await message.reply(escape_markdown(text), parse_mode = "Markdown")

@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    if call.data.split("|")[0] == "edit":

        date = datetime.datetime.strptime(call.data.split("|")[1], '%d.%m.%Y')
        result = time_table(date)

        next_date = date + datetime.timedelta(days=1)
        pre_date = date - datetime.timedelta(days=1)

        inline_add = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton('назад', callback_data=f"edit|{pre_date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('обн', callback_data=f"edit|{date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('вперед', callback_data=f"edit|{next_date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('домашняя работа', callback_data=f"home|{date.strftime('%d.%m.%Y')}"),
        )
        try:
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result, parse_mode = "Markdown", reply_markup=inline_add)
        except exceptions.MessageNotModified: await call.answer()
    if call.data.split("|")[0] == "home":
        await call.answer()
