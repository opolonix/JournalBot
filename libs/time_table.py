import datetime
from time import mktime
from app import week, query, ZoneInfo
import json

def this_day(text):
    return datetime.datetime.now().strftime('%d.%m.%Y') == text

def time_table(date, next):

    free = date.weekday() >= 5
    skip_free = True
    result = None

    events = query(f"SELECT * FROM `events` WHERE `type` LIKE 'skip'")
    for i in events:
        i['data'] = json.loads(i['data'])
        if eval(i['data']['if']):
            if next: date += datetime.timedelta(days=1)
            else: date -= datetime.timedelta(days=1)
            result, date = time_table(date, next)

    if result == None:
        result = ""
        result += week[date.weekday()][1]
        result += ' ' + date.strftime('%d.%m.%Y')
        even = date.isocalendar()[1] % 2 == 1
        timestamp = int(date.timestamp()) - 10800
        red = not even
        blue = even
        free = date.weekday() >= 5
        skip_free = True

        if even: result += " 🔵"
        else: result += " 🔴"
        day = query(f"SELECT * FROM `{week[date.weekday()][0]}` ORDER BY `{week[date.weekday()][0]}`.`pos` ASC")
        for i in day:
            if eval(i['if']):
                time_start = datetime.datetime.fromtimestamp(i['subj_start']-10800)
                time_end = time_start + datetime.timedelta(seconds=i['subj_end'])
                result += f"\n*{i['subj_name']}*\n  _{i['cabinet']}_ | _{time_start.strftime('%H:%M')} - {time_end.strftime('%H:%M')}_"
    return result, date