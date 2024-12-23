import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import datetime
import making
import re
import matplotlib.pyplot as plt
from openpyxl import Workbook
import making
import os
from  openpyxl.styles.fonts  import  Font
from  openpyxl.styles  import  Border, Side
import shutil


pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비


#아이들 정보 기입용 코드

df2 = pd.read_excel(making.addressgibon+"아이들 정보.xlsx", sheet_name='시트1' , index_col=0)
df = pd.read_excel(making.addressgibon+"아이들 정보.xlsx", sheet_name='시트1' , index_col=0)

def insert_info(df, insert_position,new_row ,name ):

    # 삽입할 위치 지정 (예: 2번째 인덱스 뒤에 삽입)
    insert_position

    # 데이터프레임을 나눠 새로운 행 삽입
    df_top = df.iloc[:insert_position]
    df_bottom = df.iloc[insert_position:]
    df = pd.concat([df_top, pd.DataFrame([new_row], columns=df.columns), df_bottom])  # .reset_index(drop=True)
    df.index.values[insert_position]=name
    return df

def get_user_input(prompt):
    """
    사용자 입력을 받고, 잘못된 입력이 있을 경우 빈 문자열을 반환하는 함수.
    """
    try:
        key = input(f"{prompt} 0이면 공란 정보 넣으면 입력")
        if key ==0 or key == str(0):
            return ""  # '0'을 입력하면 빈 문자열 반환
        else:
            return key

    except ValueError:
        print("잘못된 입력입니다. 빈 문자열을 반환합니다.")
        return ""  # 예외 발생시 빈 문자열 반환


def getnumberone(given,check):
    if check == 1 or check == str(1):
        return given
    else:
        return  check

def getnumberzero(given,check):
    if check == 0 or check == str(0):
        return given
    else:
        return  check

def change_info(name,df):
    list=['학생연락처', '부모님 연락처','출결','생일','비고']
    for i in range(len(list)):
        df.loc[name, df.columns[i]] = getnumberone(df.loc[name, df.columns[i]],input(list[i]+"기존 이면1"))

    return df


going= int(1)
while going:
    name = input('아이 이름')
    index=df.index.tolist()

    count = index.count(name)

    #동명이인 제거
    if count >= 2:
        print(f"'{name}'가 2개 이상 있습니다. (총 {count}개)")

    #이름이 있으면 수정
    elif name in index:
        try:
            change_info(name,df)

        except Exception as e:
            print(f"오류 발생내용: {e}")

    #이름이 없으면
    else:
        try:
            key=int(input("몇년도생?"))
            indexnumber = index.index(key)+1

            new_row= []
            # new_row = [name]
            new_row.append(get_user_input("학생 연락처"))
            new_row.append(get_user_input("부모님 연락처"))
            new_row.append(get_user_input("출결 정보"))
            new_row.append(get_user_input("생일 정보"))
            new_row.append(get_user_input("비고"))


            df = insert_info(df, indexnumber,new_row,name )


        except Exception as e:
            print(f"오류 발생내용: {e}")



    going= int(input("0넣으면 종료"))


# 결과 출력
print(df)

df.index.name='이름'
name = "아이들 정보"
df.to_excel(name+".xlsx")



# 개인파일 폴더 경로
destination_folder = r'C:\Users\captu\OneDrive\바탕 화면\diary\개인 파일'  # 보관하고 싶은 절대주소를 적으면 됩니다.

# 다룰 엑셀파일 위치
source_folder = r'C:\Users\captu\PycharmProjects\pythonProject' # 다운로드파일에 있는 최신 엑셀파일을 복사합니다.

# 출석부 엑셀 파일 이름
file_name = name + ".xlsx"

# 현재 시각을 추가한 새로운 파일 이름 생성
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")  # "년월일_시분초" 형식
new_file_name = f"{name}_{current_time}.xlsx"

# 출석부 파일 경로
source_path = os.path.join(source_folder, file_name)
destination_path = os.path.join(destination_folder, new_file_name)

# 다운로드 폴더에서 출석부 파일을 개인파일 폴더로 복사
if os.path.exists(source_path):
    shutil.copy(source_path, destination_path)
    print(f'{new_file_name} 파일이 복사 성공.')
else:
    print(f'{file_name} 파일이 존재하지 않습니다.')




scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
#위치 바뀌면 수정해줄것.

file = gspread.authorize(creds)

making.upload_data_to_sheets(file,[name])

