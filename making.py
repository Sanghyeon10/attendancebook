import datetime

def index():
    df=[]
    year = 2023 #년도는 체크하기

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

def all_group(): #그룹리스트 가져오기
    A = ['4-1', '4-2', '4-3', '4-4', '4-5', '5-1', '5-2', '5-3', '5-4', '6-1', '6-2', '6-3', '6-4']

    return A

def get_name(): #정보 부존재 목장의 선생님 이름 구하기
    B={}  # 빈 딕셔너리 생성

    with open("namebook.txt", "r" , encoding="utf-8") as file:
        for line in file:
            name, number = line.strip().split(" ")  # 빈칸으로 구분된 이름과 전화번호 추출
            B[name] = number  # 딕셔너리에 추가

    return B