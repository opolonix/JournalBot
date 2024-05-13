from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

week = [
    ["monday",    "Понедельник", "Понедельник"],
    ["tuesday",   "Вторник",     "Вторник"],
    ["wednesday", "Среда",       "Среду"],
    ["thursday",  "Четверг",     "Четверг"],
    ["friday",    "Пятница",     "Пятницу"],
    ["saturday",  "Суббота",     "Субботу"],
    ["sunday",    "Воскресенье", "Воскресенье"]
]
timetable = KeyboardButton('Расписание')
teachers = KeyboardButton('Учителя')
group = KeyboardButton('Группа')
timetableBtn = ReplyKeyboardMarkup(resize_keyboard=True)
timetableBtn.add(timetable).add(teachers, group)
