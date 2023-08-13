import datetime
import re

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

    df.append('비고')
    return df

def all_group(): #그룹리스트 가져오기
    A = ['4-1', '4-2', '4-3', '4-4', '4-5', '5-1', '5-2', '5-3', '5-4', '6-1', '6-2', '6-3', '6-4','새신자']

    return A

def get_name(): #정보 부존재 목장의 선생님 이름 구하기
    B={}  # 빈 딕셔너리 생성

    with open("namebook.txt", "r" , encoding="utf-8") as file:
        for line in file:
            name, number = line.strip().split(" ")  # 빈칸으로 구분된 이름과 전화번호 추출
            B[name] = number  # 딕셔너리에 추가

    return B


def calculate_o_ratio(df):


    # 날짜 열들에 대해 반복하여 'o'의 개수를 세서 리스트에 추가
    for column in df.columns :
        o_count = df[column].eq('O').sum() #0도아니고 o도 아니고 O일것.
        x_count = df[column].eq('X').sum()
        total_count = o_count + x_count
        df.loc[df.index[-1],column] = round(o_count / total_count*100)  if total_count > 0 else 0.0
        #맨 아래에 값에 o/(o+x)값 넣어주기



    return df

def calculate_o_ratio_for_series(series):
    start_index = 5  # 6번째 칸까지의 것은 세지 않습니다
    end_index = len(series) - 1  # -1해줘야 인덱스 안벗어남
    selected_data = series[start_index:]


    # 'O'와 'X'의 개수 세기
    o_count = selected_data.eq('O').sum()
    x_count = selected_data.eq('X').sum()

    # 'O'의 비율 계산
    total_count = o_count + x_count
    o_ratio = round(o_count / total_count*100) if total_count > 0 else 0.0

    series[end_index] = o_ratio

    return series


def read_attendance_from_file(attendance_file_path):
    # 주의사항, 목장 내용인데 사이가 space바여야지, tab(\t)으로 구분되어있으면 오류남
    attendance_dict = {}

    with open(attendance_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
            fields = [line for line in re.split('\s|,|\.', line) if line]

            # 목장 이름, 출석자 이름1, 출석자 이름2, ...으로 분리합니다.
            farm_name, *attendees = fields
            # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
            attendance_dict[farm_name] = attendees

    return attendance_dict

def read_nocome_from_file(nocome_file_path):
    nocome_dict = {}

    with open(nocome_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 정규 표현식을 사용하여 첫 번째 공백문자로 분리합니다.
            pattern = r'^(\S+)\s(.+)$'
            match = re.match(pattern, line)

            if match:
                # 두 개의 그룹으로 나눈 문자열을 변수에 저장합니다.
                farm_name = match.group(1)
                reason = match.group(2).strip()  # 리스트에서 양쪽 공백 제거
                # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
                nocome_dict[farm_name] = reason

    return nocome_dict


def gettruelist(my_list,remove_items):
    new_list = [item for item in my_list if item not in remove_items]

    return (new_list)