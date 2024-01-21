import datetime
import re
import json
import pandas as pd
import making
import os
import shutil

ThisYearAttendnce="2024 초등부 출석표"

Newmembers = "2024 새친구 관리엑셀표"


def index():
    df=[]
    year = 2024 #년도는 체크하기

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

    df.append('비고') #비고에는 출석율 계산할것임.
    return df


def all_group(): #그룹리스트 가져오기
    A = ['4-1', '4-2', '4-3', '4-4', '5-1', '5-2', '5-3', '5-4','5-5', '6-1', '6-2', '6-3', '6-4','6-5','새신자']

    return A

def get_name(): #정보 부존재 목장의 선생님 이름 구하기
    B={}  # 빈 딕셔너리 생성

    with open("namebook.txt", "r" , encoding="utf-8") as file:
        for line in file:
            name, number = line.strip().split(" ")  # 빈칸으로 구분된 이름과 전화번호 추출
            #예시 4-1 홍길동
            B[name] = number  # 딕셔너리에 추가

    return B


def calculate_o_ratio(df):


    # 날짜 열들에 대해 반복하여 'o'의 개수를 세서 리스트에 추가
    for column in df.columns :
        # df[column] = df[column].astype(str)
        o_count = df[column].astype(str).str.contains('O').sum() #0도아니고 o도 아니고 O일것. -> 수정함. O을 포함.
        x_count = df[column].astype(str).str.contains('X').sum()
        total_count = o_count + x_count
        df.loc[df.index[-1],column] = round(o_count / total_count*100)  if total_count > 0 else 0.0
        #맨 아래에 값에 o/(o+x)값 넣어주기



    return df

def calculate_o_ratio_for_series(series):
    start_index = 5  # 6번째 칸까지의 것은 세지 않습니다
    end_index = len(series) - 1  # -1해줘야 인덱스 안벗어남
    selected_data = series[start_index:]


    # 'O'와 'X'의 개수 세기
    o_count = selected_data.astype(str).str.contains('O').sum()
    x_count = selected_data.astype(str).str.contains('X').sum()

    # 'O'의 비율 계산
    total_count = o_count + x_count
    o_ratio = round(o_count / total_count*100) if total_count > 0 else 0.0

    series[end_index] = o_ratio

    return series


def read_attendance_from_file(attendance_file_path):
    attendance_dict = {}

    with open(attendance_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
            # fields = [line for line in re.split('\s|,|\.', line) if line]
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


def make_data_from_file(attendance_file_path):
    #출석정보, 비고 한번에 생성.

    # 결과를 저장할 딕셔너리들
    attendance_dict = {}
    nocome_dict = {}

    with open(attendance_file_path, 'r', encoding='utf-8') as f:
        for oneline in f:
            # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
            # "///"을 포함하는지 확인
            if "///" in oneline:
                # 딕셔너리를 생성 (///이 있는 경우)
                split_string = oneline.split("///")[0] #앞의것을 쪼개서 정보저장
                split_string = [line for line in re.split('\s|,|\.', split_string) if line]
                class_name, *student_names = split_string

                if class_name not in attendance_dict.keys():
                    attendance_dict[class_name] = student_names
                    nocome_dict[class_name] = oneline.split("///")[1] #뒤에꺼는 기타사항 딕셔너리 정보에 추가
                else:
                    print('중복 존재',class_name)

            else:
                split_string = [line for line in re.split('\s|,|\.', oneline) if line]
                # 딕셔너리를 생성 (///이 없는 경우)
                class_name, *student_names = split_string

                if class_name not in attendance_dict.keys():
                    attendance_dict[class_name] = student_names
                    nocome_dict[class_name] = "X"  # 기타사항이 없는 경우 X으로 처리
                else:
                    print('중복 존재',class_name)

    return attendance_dict, nocome_dict

def gettruelist(my_list,remove_items):
    new_list = [item for item in my_list if item not in remove_items]
    #순서를 유지하는체로 리스트 중복을 제거하는 코드
    return (new_list)


def checkO(name, list):
    if name in list:
        A="(등반)"
    else:
        A=""

    return A

# ##json형태로 쓰는건 너무 불편해서 폐기함.
# def save_dict_to_file(data, file_name):
#     with open(file_name, "w", encoding="utf-8") as file:
#         json.dump(data, file, indent=4, ensure_ascii=False)
#
# def load_dict_from_file(file_name):
#     with open(file_name, 'r', encoding="utf-8") as file:
#         loaded_data = json.load(file)
#     return loaded_data

def make_line(groupname,my_list):
    n=6
    print(groupname, end=' ')
    for i, x in enumerate(my_list):
        if i ==0: #4-1 같은건 따로 빼기 위해서 4-1 출력후 바로 한칸 내림
            print()
        elif i % n == 0 and i != 0:
            print()
        else:
            pass


        if i == len(my_list)-1: #마지막
            print(x)
        else: #평상시
            print(x, end=' ')

    return False

def AddNewMembers(df,columns):
    for new_column_name in columns:
        df[new_column_name] = None

    return  df


def getrangename(df):
    num_rows, num_cols = df.shape
    start_cell = "A1"

    # Calculate the end cell column label
    end_col_label = ""
    while num_cols > 0:
        num_cols, remainder = divmod(num_cols - 1, 26)
        end_col_label = chr(65 + remainder) + end_col_label

    end_cell = end_col_label + str(num_rows + 1)

    range_name = f"{start_cell}:{end_cell}"

    return range_name


def makedictfromtxt(file_name):
    # 텍스트 파일을 딕셔너리로 불러오기
    # value는 리스트 형태일것.
    loaded_data = {}
    with open(file_name, 'r', encoding='UTF-8') as txt_file:
        for line in txt_file:
            key, value = line.strip().split(': ')
            loaded_data[key] = eval(value)

    return loaded_data

def savedicttotxt(file_name, data ):
    # 딕셔너리를 텍스트 파일로 저장
    with open(file_name, 'w', encoding='UTF-8') as txt_file:
        for key, value in data.items():
            txt_file.write(f"{key}: {value}\n")

def WhatIsToUpload(A):
    if A==0 or A=="0":
        return making.all_group()
    else:
        # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
        uploadlist = [line for line in re.split('\s|,|\.', A) if line]

        return uploadlist


def count_os(row): #가로줄 O세어보기
    if row is not None:
        return row.astype(str).str.contains('O').sum()
    else:
        return None


def removingexcel(file_path):
    if os.path.exists(file_path):
        # 파일 제거
        os.remove(file_path)
        print(file_path,"파일이 성공적으로 제거되었습니다.")
    else:
        print(file_path,"파일이 존재하지 않습니다.")

def move_attendance_file():

    # 개인파일 폴더 경로
    destination_folder = r'C:\Users\User\Desktop\diary\개인 파일' #보관하고 싶은 절대주소를 적으면 됩니다.

    # 다운로드 폴더 경로
    source_folder = r'C:\Users\User\Downloads' #다운로드파일에 있는 최신 엑셀파일을 복사합니다.

    # 출석부 엑셀 파일 이름
    file_name = ThisYearAttendnce+".xlsx"

    # 출석부 파일 경로
    source_path = os.path.join(source_folder, file_name)
    destination_path = os.path.join(destination_folder, file_name)

    # 개인파일 폴더에 있는 출석부 파일 제거
    if os.path.exists(destination_path):
        os.remove(destination_path)
        print(f'{file_name} 파일이 개인파일 폴더에서 제거되었습니다.')

    # 다운로드 폴더에서 출석부 파일을 개인파일 폴더로 복사
    if os.path.exists(source_path):
        shutil.copy(source_path, destination_folder)
        print(f'{file_name} 파일이 다운로드 폴더에서 개인파일 폴더로 복사되었습니다.')
    else:
        print(f'{file_name} 파일을 다운로드 폴더에서 찾을 수 없습니다.')

