import datetime

def make():
    df=[]
    year = 2023

    # 특정 년도의 첫 번째 날
    first_day = datetime.date(year, 1, 1)

    # 특정 년도의 첫 번째 일요일
    first_sunday = first_day + datetime.timedelta(days=(6-first_day.weekday()))

    # 특정 년도의 마지막 날
    last_day = datetime.date(year, 12, 31)

    # 특정 년도의 마지막 일요일
    if last_day.weekday()==6: #마지막날이 일요일이면 마지막날이 마지막 일요일
        last_sunday = last_day
    else:
        last_sunday = last_day - datetime.timedelta(days=last_day.weekday())
    # print(last_sunday)

    # 출력
    day = first_sunday
    while day <= last_sunday:
        if day <= last_day or (day == last_day and day.weekday() == 6):
            df.append(day.strftime("%Y-%m-%d"))
            # print(day.strftime("%Y-%m-%d"))
        day += datetime.timedelta(days=7)

    return df
