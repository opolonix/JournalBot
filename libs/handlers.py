import os
import shutil
import asyncio
import requests
import random
import datetime
import subprocess
import traceback
import sys
import string
from ast import literal_eval

from zoneinfo import ZoneInfo

from app import dp, bot, query, week, time_table, escape_markdown, timetableBtn
from config import MYSQL_HOST

from aiogram import Bot, types
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, InputFile
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor, exceptions


work_path = os.path.abspath(os.curdir)

class HMW:
    def __init__(self) -> None:
        self.wait_load_tasks = {}
hmw = HMW()


teacher = """<b>Учителя:</b>
<blockquote>Дикаленко Игорь Андреевич - БОСС
Гапонов Андрей Иванович - Вышмат
Ермоленко Ростислав Александрович - Архитектура
Иванов Алексей Викторович - Дискретная математика
Китаев Артур Владимирович - ПМ.04 
Ковалёва Надежда Сергеевна - Иностранный язык
Когут Виктор Игоревич - Компьютерные сети
Козлов Юрий Васильевич - Физкультура
Лялечкина Зинаида Павловна - Психология
Мельник Александр Геннадьевич - МДК 04.01, МДК 04.02
Опацкая Алла Ивановна - История
Томалак Марина Григорьевна - Физика
Чернышенко Надежда Владимировна - Деловой русский язык, Философии
</blockquote>
"""

student = """<b>Студенты:</b>
<blockquote>1. Бобров Михаил Андреевич
2. Боровик Даниил
3. Быстров Виктор
4. Верещагин Андрей
5. Громов Дмитрий
6. Дятлов Константин
7. Житенко Артем Леонидович
8. Заусаев Илья
9. Клепиков Михаил
10. Ковальчук Денис
11. Король Тимофей
12. Кузнецова Виолетта
13. Мокеев Алексей
14. Новиков Андрей Александрович
15. Ольшанская Доменика
16. Пестряков Максим Геевич
17. Раенко Андрей
18. Рулев Степан Сергеевич
19. Сайдаметов Тимур
20. Смелов Антон
21. Старовойтов Олег
22. Трухачев Артем Александрович
23. Туранский Даниил Александрович
24. Шилова Евгения
</blockquote>
"""

moms = """<b>Мамы:</b>
<blockquote>Бобров Михаил
Боброва Ирина Николаевна
Боровик Людмила Владимировна
Быстрова Яна Владимировна
Верещагина Людмила Анатольевна
Акимова(Громова) Анна Валерьевна
Дятлова Марина Петровна
Житенко Оксана Леонидовна
Заусаева Елена Юрьевна
Клепикова Наталья Николаевна
Ковальчук Алла Владимировна
Король Сергей Владимирович 👎
Кузнецова Оксана Станиславовна
Мокеева Татьяна Сергеевна
Новиков Александр Андреевич 👎
Харитонцева(Ольшанская) Марина Юрьевна
Пестрякова Ольга Александровна
Раенко Галина Васильевна
Рулëва Анастасия Владимировна
Годий(Сайдаметова) Елена Генриковна
Смелова Татьяна Алексеевна
Старовойтова Юлия Николаевна
Трухачева Виктория Викторовна
Туранский Александр Александрович 👎
Шилова Елена Владимировна
</blockquote>
"""


if requests.get('https://ip.beget.ru/').text.replace(' ', '').replace('\n', '') == MYSQL_HOST: # Необходимо, потому что команда /git и /restar работает только на хостинге
    @dp.message_handler(commands=["git"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        git_message = await message.reply("🪛 *Ожидаем клонирования...*", parse_mode="Markdown")

        pull_result = subprocess.Popen(["git", "pull", "https://github.com/opolonix/JournalBot"], stdout=subprocess.PIPE, text=True, stderr=subprocess.PIPE)
        output, errors = pull_result.communicate(input="Hello from the other side!")
        pull_result.wait()
        await bot.edit_message_text(f"🪛 *Ожидаем клонирования...\nРезультат:*\n`{output}`", git_message.chat.id, git_message.message_id, parse_mode="Markdown")
        if "Already up to date.\n" != output:
            await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")
            try:
                dp.stop_polling()
                await dp.wait_closed()
                await bot.close()
            except: pass

            os.system(f"python {work_path}/app.py &")
            sys.exit(0)
        else: await message.reply(f"*Файлы не затронуты, перезагрузка не требуется!*", parse_mode="Markdown")
    @dp.message_handler(commands=["restart"])
    async def handler(message: types.message):
        if message['from']['id'] not in [780882761, 1058211493]: return

        await message.reply("🪛 Рестарт бота")

        dp.stop_polling()
        await dp.wait_closed()
        await bot.close()


        os.system(f"python {work_path}/app.py &")
        sys.exit(0)

@dp.message_handler(commands=["exit"])
async def handler(message: types.message):
    if message['from']['id'] not in [780882761, 1058211493]: return
    await message.reply(f"*Выход!* _(⏰{datetime.datetime.now().strftime('%d.%m.%Y %H:%M:%S')})_", parse_mode="Markdown")
    exit(0)

@dp.message_handler(commands=["start"])
async def handler(message: types.message):
    await message.reply("**Приветсвую! Это бот для контроля расписания и домашки!!**", parse_mode = "Markdown", reply_markup=timetableBtn)

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
    if message.text.lower() in ["расписание", "р", "/timetable@msg_72997_bot", "/timetable"]:
        date = datetime.datetime.now()
        result, date = time_table(date, next=True)

        next_date = date + datetime.timedelta(days=1)
        pre_date = date - datetime.timedelta(days=1)

        tasks = 0
        for i in query("SELECT * FROM `events` WHERE `type` LIKE 'home' ORDER BY `events`.`id` ASC"):
           
            data = literal_eval(i['data'])
            print(data['date'], date.strftime('%d.%m.%Y'), data['date'] == date.strftime('%d.%m.%Y'))
            if data['date'] == date.strftime('%d.%m.%Y'): tasks += 1

        inline_add = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton('назад', callback_data=f"edit|{pre_date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('обн', callback_data=f"edit|{date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('вперед', callback_data=f"edit|{next_date.strftime('%d.%m.%Y')}|n"),
            InlineKeyboardButton(f"домашняя работа{' ▫️' if tasks != 0 else ''}", callback_data=f"home|{date.strftime('%d.%m.%Y')}"),
        )
        await message.reply(result, parse_mode = "Markdown", reply_markup=inline_add)

    if message.text.lower().startswith("ученики"):
        inline_add = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton('скрыть', callback_data=f"del")
        )
        await message.reply(student, parse_mode = "HTML", reply_markup=inline_add)

    if message.text.lower().startswith("учителя"):
        inline_add = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton('скрыть', callback_data=f"del")
        )
        await message.reply(teacher, parse_mode = "HTML", reply_markup=inline_add)
        
    if message.text.lower().startswith("мамы"):
        inline_add = InlineKeyboardMarkup(row_width=1).add(
            InlineKeyboardButton('скрыть', callback_data=f"del")
        )
        await message.reply(moms, parse_mode = "HTML", reply_markup=inline_add)

    if message.text.lower().startswith("+пара "):
        text = message.text[6::]
        data = {}
        for i in text.split("&"):
            split_item = i.strip().split(' ')
            data[split_item[0]] = ' '.join(split_item[1:])

        await message.reply(escape_markdown(text), parse_mode = "Markdown")
    elif message.text.startswith("+") and not message.text.startswith("+ "):
        text = message.text[2::].lower()
        text = message.text[1].upper() + text

        syns = {
            "ПРАКТИКА":                             ["практика"],
            "МДК":                                  ["мдк"],
            "Классный час":                         ["классный час"],
            "Элементы высшей математики":           ["вышмат", "высшая математика"],
            "Компьютерные сети":                    ["кс", "компьютерные сети"],
            "Деловой русский язык и культура речи": ["культура речи", "деловой русский и культура речи"],
            "Деловой русский язык":                 ["деловой русский"],
            "Английский":                           ["английский"],
            "Физика":                               ["физика"],
            "Архитектура аппаратных средств":       ["апп. средства", "архитектура аппаратных средств", "апп средства"],
            "Физкультура":                          ["физра", "физкультура", "физ ра"],
            "История":                              ["история"],
            "Дискретная математика":                ["дискретная математика", "дискрет"]
        }

        day = None

        if message.reply_to_message and message.reply_to_message.from_user.id in [6636195294, 5438548972]:
            day = message.reply_to_message.reply_markup.inline_keyboard[1][0]['callback_data'].split("|")[1]

        task = None

        subj = text.split(' ')[0] if len(text.split(' ')) != 1 else None
        task = ' '.join(text.split(' ')[1::]) if len(text.split(' ')) != 1 else None
        is_syn = False
        for i in syns:
            for j in syns[i]:
                if text.lower().startswith(j + " "):
                    task = text[len(j + " ")::]
                    subj = i
                    is_syn = True
                    break
        
        

        if subj != None and day != None and task != None:
            key = ''.join(random.choice(string.ascii_lowercase) for i in range(6))
            inline_hmw = InlineKeyboardMarkup(row_width=3).add(
                InlineKeyboardButton('Загрузить дз', callback_data=f"add_home|{key}"),
                InlineKeyboardButton('Отмена', callback_data=f"remove_home|{key}")
            )
            tasks = []
            for i in query("SELECT * FROM `events` WHERE `type` LIKE 'home' ORDER BY `events`.`id` ASC"):
                data = literal_eval(i['data'])
                if data['date'] == day and data['subj_name'].lower() == subj.lower():
                    tasks.append(data['task'])

            text_tasks = '\n'.join(tasks)
            new_task = ""
            for i in task.split("\n"):
                new_task += f"\n+>{i}"

            hmw.wait_load_tasks[key] = {
                "task": task,
                "subj": subj,
                "date": day
            }

            if is_syn or text_tasks != "": result = f"Хотите _добавить дз_ по предменту *{subj.lower()}* на _{day}_?\n\nТекст задания:\n{text_tasks}{new_task}"
            else: result = f"Предмет не найден в синонимах, уверены, что ходите добавить дз для предмета *{subj.lower()}* на _{day}_?\n\nТекст задания:\n{text_tasks}{new_task}"
            await message.reply(result, parse_mode = "Markdown", reply_markup=inline_hmw)
        


@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    
    if call.data.split("|")[0] == "add_home":
        if call.data.split("|")[1] in hmw.wait_load_tasks:
            data = hmw.wait_load_tasks[call.data.split("|")[1]]
            task_data = f'{{"date": "{data["date"]}", "task": "{data["task"]}", "subj_name": "{data["subj"]}"}}'.replace('"', '\\"').replace("'", "\\'").replace("\n", "&%&")

            query(f"INSERT INTO `events` (`id`, `type`, `date_from`, `date_until`, `data`) VALUES (NULL, 'home', NULL, NULL, '{task_data}')")
            await call.answer("Дз загружено!")
            inline_add = InlineKeyboardMarkup()
            await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Дз успешно обновлено!", parse_mode = "Markdown", reply_markup=inline_add)
        else: await call.answer("Кнопка устарела!")
    if call.data.split("|")[0] == "remove_home":
        try: 
            del hmw.wait_load_tasks[call.data.split("|")[1]]
            await call.answer("Дз удалено!")
        except: await call.answer("Кнопка устарела!")
        inline_add = InlineKeyboardMarkup()
        await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=call.message.text, parse_mode = "Markdown", reply_markup=inline_add)
    if call.data.split("|")[0] == "edit":

        date = datetime.datetime.strptime(call.data.split("|")[1], '%d.%m.%Y')
        result, date = time_table(date, next=len(call.data.split("|")) == 3 and call.data.split("|")[2] == 'n')

        next_date = date + datetime.timedelta(days=1)
        pre_date = date - datetime.timedelta(days=1)

        tasks = 0
        for i in query("SELECT * FROM `events` WHERE `type` LIKE 'home' ORDER BY `events`.`id` ASC"):

            data = literal_eval(i['data'])
            if data['date'] == date.strftime('%d.%m.%Y'): tasks += 1

        inline_add = InlineKeyboardMarkup(row_width=3).add(
            InlineKeyboardButton('назад', callback_data=f"edit|{pre_date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('обн', callback_data=f"edit|{date.strftime('%d.%m.%Y')}"),
            InlineKeyboardButton('вперед', callback_data=f"edit|{next_date.strftime('%d.%m.%Y')}|n"),
            InlineKeyboardButton(f"домашняя работа{' ▫️' if tasks != 0 else ''}", callback_data=f"home|{date.strftime('%d.%m.%Y')}"),
        )
        try: await bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=result, parse_mode = "Markdown", reply_markup=inline_add)
        except exceptions.MessageNotModified: await call.answer()
    if call.data.split("|")[0] == "home":
        date = datetime.datetime.strptime(call.data.split("|")[1], '%d.%m.%Y')
        tasks = {}
        for i in query("SELECT * FROM `events` WHERE `type` LIKE 'home' ORDER BY `events`.`id` ASC"):
            data = literal_eval(i['data'])
            if data['date'] == call.data.split("|")[1]:
                if data['subj_name'].lower() in tasks: tasks[data['subj_name'].lower()] += '\n' + data['task'].replace("&%&", "\n")
                else: tasks[data['subj_name'].lower()] = data['task'].replace("&%&", "\n")
        result = f"Дз на {call.data.split('|')[1]}"
        for i in tasks:
            result += f"\n *{i[0].upper() + i.lower()[1::]}*\n"
            result += tasks[i]
        if len(tasks) != 0:
            await call.answer()
            await call.message.reply(result, parse_mode = "Markdown")
        else:
            await call.answer("Дз не найдено")

    if call.data == "del":
        await call.message.delete()