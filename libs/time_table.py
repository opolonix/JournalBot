import datetime
from app import week, query

def this_day(text):
    return datetime.datetime.now().strftime('%d.%m.%Y') == text

def time_table(date):
    
    result = ""
    result += week[date.weekday()][1]
    result += ' ' + date.strftime('%d.%m.%Y')
    even = date.isocalendar()[1] % 2 == 1
    
    if even: result += " 🔵"
    else: result += " 🔴"
    day = query(f"SELECT * FROM `{week[date.weekday()][0]}` ORDER BY `{week[date.weekday()][0]}`.`pos` ASC")
    added = 0
    for i in day:
        if eval(i['if']):
            time_start = datetime.datetime.fromtimestamp(i['subj_start'])
            time_end = datetime.datetime.fromtimestamp(i['subj_end'])
            result += f"\n*{i['subj_name']}*\n  _{i['cabinet']}_ | _{time_start.strftime('%H:%M')} - {time_end.strftime('%H:%M')}_"
            added += 1

    return result