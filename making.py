import re
import json
import pandas as pd
import making
import os
import shutil
import calendar
import datetime
import time
from collections import Counter
import numpy as np


ThisYearAttendnce="2025 초등부 출석표"

nextYearAttendnce="2025 초등부 출석표"

Newmembers = "2025 새친구 관리엑셀표"

addressgibon = 'C:\\Users\\captu\\Downloads\\'

#C:\Users\User\Downloads

addrresOfjsonfile = r"C:\Users\captu\PycharmProjects\pythonProject\abiding-honor-375915-c16db88a8008.json"

def index():
    df=[]
    year = 2025 #년도는 체크하기

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
    # print(df)
    return df




def all_group(): #그룹리스트 가져오기
    A = ['4-1', '4-2', '4-3', '4-4','4-5', '5-1', '5-2', '5-3', '5-4', '6-1', '6-2', '6-3', '6-4','6-5','새신자']

    return A

def next_group(): #그래도 새신자칸 넣어주기.
    A = ['4-1', '4-2', '4-3', '4-4','4-5', '5-1', '5-2', '5-3', '5-4', '6-1', '6-2', '6-3', '6-4','6-5','새신자']
    # A = ['4-1', '4-2', '4-3', '4-4', '5-1', '5-2', '5-3', '5-4','5-5', '6-1', '6-2', '6-3', '6-4','6-5','새신자']

    return A


def next_index():
    df=[]
    year = 2025 #년도는 체크하기

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
    # print(df)
    return df



def get_name(): #정보 부존재 목장의 선생님 이름 구하기
    B={}  # 빈 딕셔너리 생성

    with open("namebook.txt", "r" , encoding="utf-8") as file:
        for line in file:
            farm_name, name = line.strip().split(" ")  # 빈칸으로 구분된 이름과 전화번호 추출
            #예시 4-1 홍길동
            B[farm_name] = name  # 딕셔너리에 추가

    return B

def get_newname(): #정보 부존재 목장의 선생님 이름 구하기
    B={}  # 빈 딕셔너리 생성

    with open("newnamebook.txt", "r" , encoding="utf-8") as file:
        for line in file:
            farm_name, name = line.strip().split(" ")  # 빈칸으로 구분된 이름과 전화번호 추출
            #예시 4-1 홍길동
            B[farm_name] = name  # 딕셔너리에 추가

    return B


def get_nextyearinfo(attendance_file_path):
    # 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
    attendance_dict = {}

    # 출석 정보 파일을 읽어서 딕셔너리에 저장합니다.
    with open(attendance_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
            fields = [line for line in re.split(r'\s|,|\.', line) if line]

            # 목장 이름, 출석자 이름1, 출석자 이름2, ...으로 분리합니다.
            farm_name, *attendees = fields

            # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
            attendees = ['기타'] + attendees  # 리스트 맨 앞에 기타 추가해줘야함.
            attendance_dict[farm_name] = attendees

    return attendance_dict


def get_phonenumber(): #정보 부존재 목장의 선생님 이름 구하기
    B={}  # 빈 딕셔너리 생성

    with open("phonenumber.txt", "r" , encoding="utf-8") as file:
        for line in file:
            farm_name, name = line.strip().split(" ")  # 빈칸으로 구분된 이름과 전화번호 추출
            #예시 4-1 홍길동
            B[farm_name] = name  # 딕셔너리에 추가

    return B



def get_keyAndlist(filname):
    # 출석 정보가 저장된 파일 경로를 입력합니다.
    # attendance_file_path = 'famenameAndkids.txt'  # 첫 엑셀표 양식만들때 쓰는거라 같은 텍스트파일을 활용함.
    attendance_file_path=filname

    # 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
    attendance_dict = {}

    # 출석 정보 파일을 읽어서 딕셔너리에 저장합니다.
    with open(attendance_file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
            fields = [line for line in re.split(r'\s|,|\.', line) if line]

            # 목장 이름, 출석자 이름1, 출석자 이름2, ...으로 분리합니다.
            farm_name, *attendees = fields

            # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
            attendance_dict[farm_name] = attendees

    return attendance_dict





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

    # series[end_index] = o_ratio
    series.iloc[end_index] = o_ratio

    return series




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
                split_string = [line for line in re.split(r'\s|,|\.', split_string) if line]
                class_name, *student_names = split_string

                if class_name not in attendance_dict.keys():
                    attendance_dict[class_name] = student_names
                    nocome_dict[class_name] = oneline.split("///")[1] #뒤에꺼는 기타사항 딕셔너리 정보에 추가
                else:
                    print('중복 존재',class_name)

            else:
                split_string = [line for line in re.split(r'\s|,|\.', oneline) if line]
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

def make_line(groupname,my_list, teachername):
    n=100
    print(groupname,end=" ")   #print(groupname,teachername,'선생님',end=' ')
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
    print()

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
        uploadlist = [line for line in re.split(r'\s|,|\.', A) if line]

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

def move_attendance_file(fileToUploadlist):

    for name in fileToUploadlist:

        # 개인파일 폴더 경로
        destination_folder = r'C:\Users\captu\OneDrive\바탕 화면\diary\개인 파일' #보관하고 싶은 절대주소를 적으면 됩니다.

        # 다운로드 폴더 경로
        source_folder = addressgibon #다운로드파일에 있는 최신 엑셀파일을 복사합니다.

        # 출석부 엑셀 파일 이름
        file_name = name+".xlsx"

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
            print(f'{file_name} 파일이 복사 성공.')
        else:
            print(f'{file_name} 실패.')


def getdaydate(day):
    # 특정 날짜 문자열
    date_str = day

    # 문자열을 datetime 객체로 변환
    # date_obj = datetime.datetime.strptime(date_str, '%Y-%m-%d')
    date_obj=day

    # 날짜가 속한 달의 달력을 얻어오기
    _, last_day = calendar.monthrange(date_obj.year, date_obj.month)
    month_calendar = calendar.monthcalendar(date_obj.year, date_obj.month)

    # 날짜가 속한 주차 찾기
    week_of_month = next((week_num for week_num, week in enumerate(month_calendar, start=1) if date_obj.day in week),
                         None)

    week_of_month-=1 #0주차부터 시작해야함
    # # 결과 출력
    # print(f"{date_str}은 {date_obj.month}월의 {week_of_month}주차에 속합니다.")
    return (date_obj.month,week_of_month)



def upload_to_sheet(sheet, dataframe):
    sheet.clear()
    sheet.update(range_name=making.getrangename(dataframe),
                 values=[dataframe.columns.values.tolist()] + dataframe.values.tolist())
    time.sleep(5)

def upload_data_to_sheets(file,givenlist):
    for i in givenlist:  # 새신자파일, 특정목장 파일, 새친구 파일 업로드

        sh = file.open(i)  # woorbook = sh

        print(i)
        sheet = sh.worksheet('시트1')  # 구글 스프레드기준 찾기

        tempdf = pd.read_excel(r'{}.xlsx'.format(i))  # 해당파일찾고 데이터 옮겨오기
        tempdf = tempdf.fillna('')  # 이거 안해주면 업로드시 오류남

        sheet.clear()
        sheet.update(range_name=making.getrangename(tempdf),
                     values=[tempdf.columns.values.tolist()] + tempdf.values.tolist())  # 데이터 덧씌우기

        time.sleep(5)


def upload_data_to_allsheets(file,givenlist,all_group,uploadlist):
    for i in givenlist:  # 새신자파일, 특정목장 파일, 새친구 파일 업로드

        sh = file.open(i)  # woorbook = sh

        print(i)

        worksheet_list = sh.worksheets()


        if len(worksheet_list) < len(all_group):  # 에러상황일수도? 워크 시트 기준으로해야맞음
            print(worksheet_list)
            print(all_group)
            input('시트 개수가 부족해!')
            time.sleep(600)

        for i in range(len(all_group)):
            if all_group[i] in uploadlist:  # 업로드 리스트에 해당하는 것만 업로드하기
                try:
                    sheet = sh.worksheet(all_group[i])  # 구글 스프레드기준 찾기
                    print(all_group[i])

                    tempdf = pd.read_excel(r'{}.xlsx'.format(all_group[i]))  # 해당파일찾고 데이터 옮겨오기
                    tempdf = tempdf.fillna('')

                    sheet.clear()
                    sheet.update(range_name=making.getrangename(tempdf),
                                 values=[tempdf.columns.values.tolist()] + tempdf.values.tolist())  # 데이터 덧씌우기
                    # 6.0.0 버전되면 구문 위치 바뀐다고함.
                    time.sleep(5)

                    # print(making.getrangename(tempdf))
                except Exception as e:
                    print(all_group[i],f"오류 발생: {e}")
            else:
                pass


def find_duplicate_names(names): #중복 된거 찾기.
    count = Counter(names)
    # 출현 횟수가 1보다 큰 이름을 반환
    return [name for name, freq in count.items() if freq > 1]


def getABCD(score):
    if score>=75:
        return "A"
    elif score>=50:
        return "B"
    elif score>=25:
        return "C"
    else:
        return "D"


def merge_sheets_to_dataframe(file_name):
    getscoredic = {}
    file_path = making.addressgibon +  file_name#"2024 초등부 출석표.xlsx"
    #작년 출석자료 파일위치


    # 모든 시트를 데이터프레임으로 읽기
    sheet_dfs = pd.read_excel(file_path, sheet_name=None)  # 모든 시트를 딕셔너리로 읽음


    for sheet_name, df in sheet_dfs.items():
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.set_index(df.columns[0], inplace=True)
        df.drop(columns=['기타'], inplace=True)
        df = df.fillna('')
        # print(sheet_name)

        if sheet_name != '새신자':
            for name in df.columns:
                if name not in getscoredic.keys():
                    getscoredic[name] = getABCD(int(df.loc[df.index[-1],name]))
                else:
                    print("중복출석정보이름",name)

    print(getscoredic)
    return getscoredic

def getTrueScore(calcu, given):
    # print(given,type(given))
    if isinstance(given, str):
        return given
    else:
        return calcu


def SetName(check,file,filename):
    sheet = file.open(filename)
    next_group = making.next_group()

    if check == False:
        print("이름을 초기화하지 않는다.")

    elif len(next_group) <= len(sheet.worksheets()) and check == True:  # 개수가 적어나 같아야 문제없음.
        for i in range(len(next_group)):
            print(str(i), "으로이름수정")
            worksheet = sheet.get_worksheet(i)
            worksheet.update_title(title=str(i))
            time.sleep(1)

        for i in range(len(next_group)):
            print(next_group[i], "으로이름수정")
            worksheet = sheet.get_worksheet(i)
            worksheet.update_title(title=next_group[i])
            time.sleep(1)

    else:
        input("워크시트를 더 복사해야해!")
        time.sleep(1000)

def MakeCorrectLine(check,file,filename,startline):
    startTrue= False
    sheet = file.open(filename)
    next_group= making.next_group()

    worksheet_list = sheet.worksheets()
    print(worksheet_list)

    worksheet = sheet.get_worksheet(0)
    index = worksheet.col_values(1)[1:-1]
    # print(index)
    gijun = ""

    if check == False:
        print("선을 그리지 않는다.")

    elif len(next_group) <= len(sheet.worksheets()) and check == True:

        for j in range(len(next_group)):
            if next_group[j]== startline or startTrue:
                startTrue =True
                worksheet = sheet.get_worksheet(j)
                print(next_group[j], '작업중')
                for i in range(len(index)):
                    try:
                        if gijun != datetime.datetime.strptime(worksheet.cell(i + 2, 1).value, "%Y-%m-%d").month:
                            gijun = datetime.datetime.strptime(worksheet.cell(i + 2, 1).value, "%Y-%m-%d").month
                            worksheet.format("A{}:Z{}".format(str(i + 2), str(i + 2)), {"borders": {"top": {"style": "DOUBLE"}}, })

                        else:
                            worksheet.format("A{}:Z{}".format(str(i + 2), str(i + 2)), {"borders": {"top": {"style": "DOTTED"}}, })


                    except Exception as e:
                        print(next_group[j], f"오류 발생: {e}")

                    time.sleep(1)


            else:
                pass

    else:
        input('시트 개수가 모자라!')
        time.sleep(1000)