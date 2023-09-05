from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

week = [
    ["monday", "Понедельник"],
    ["tuesday", "Вторник"],
    ["wednesday", "Среда"],
    ["thursday", "Четверг"],
    ["friday", "Пятница"],
    ["saturday", "Суббота"],
    ["sunday", "Воскресенье"]
]
# timetable = KeyboardButton('Расписание')
# teachers = KeyboardButton('Учителя')
# group = KeyboardButton('Группа')
# timetableBtn = ReplyKeyboardMarkup(resize_keyboard=True)
# timetableBtn.add(timetable).add(teachers, group)
# position = ReplyKeyboardMarkup().row(timetable, teachers, group)

timetable = KeyboardButton('Расписание')
timetableBtn = ReplyKeyboardMarkup(resize_keyboard=True).row(timetable)