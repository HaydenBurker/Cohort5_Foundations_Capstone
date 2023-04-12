from datetime import datetime, date

def get_current_date():
    return datetime.now().date()

def get_current_datetime():
    return datetime.now().replace(microsecond=0)

def to_date(date_str):
    if not date_str:
        return None
    return datetime.fromisoformat(date_str).date()

def to_datetime(date_str):
    if not date_str:
        return None
    return datetime.fromisoformat(date_str)

def input_year(message):
    while True:
        year = input(message)
        if not year:
            return None
        if not year.isnumeric():
            continue
        year = int(year)
        if year < 1 or year > 9999:
            continue
        return year
    
def input_month(message, year):
    while True:
        month = input(message)
        if not month:
            return None
        if not month.isnumeric():
            continue
        month = int(month)
        if month < 1 or month > 12:
            continue
        try:
            date(year, month, 1)
        except:
            continue
        return month

def input_day(message, year, month):
    while True:
        day = input(message)
        if not day:
            return None
        if not day.isnumeric():
            continue
        day = int(day)
        try:
            date(year, month, day)
        except Exception:
            continue
        return day

def input_hour(message):
    while True:
        hour = input(message)
        if not hour:
            return None
        if not hour.isnumeric():
            continue
        hour = int(hour)
        if hour < 0 or hour > 23:
            continue
        return hour

def input_minute(message):
    while True:
        minute = input(message)
        if not minute:
            return None
        if not minute.isnumeric():
            continue
        minute = int(minute)
        if minute < 0 or minute > 59:
            continue
        return minute

def input_second(message):
    while True:
        second = input(message)
        if not second:
            return None
        if not second.isnumeric():
            continue
        second = int(second)
        if second < 0 or second > 59:
            continue
        return second

def input_date(message):
    print(message)
    year = input_year("Year: ")
    if year == None:
        return None
    month = input_month("Month: ", year)
    if month == None:
        return None
    day = input_day("Day: ", year, month)
    if day == None:
        return None
    return date(year, month, day)

def input_datetime(message):
    print(message)
    year = input_year("Year: ")
    if year == None:
        return None
    month = input_month("Month: ", year)
    if month == None:
        return None
    day = input_day("Day: ", year, month)
    if day == None:
        return None
    hour = input_hour("Hour: ")
    if hour == None:
        return None
    minute = input_minute("Minute: ")
    if minute == None:
        return None
    second = input_second("Second: ")
    if second == None:
        return None
    return datetime(year, month, day, hour, minute, second)
