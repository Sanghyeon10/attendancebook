import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making
import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 원하는 한글 폰트 파일 경로로 변경
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()


pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비

# 데이터프레임 생성
all_group= making.all_group()
accumulatedDF=pd.DataFrame( index=making.index())

for i in range(len(all_group)):
    df = pd.read_excel(r'{}.xlsx'.format(all_group[i]))  # 해당파일찾고 데이터 옮겨오기
    df.set_index('날짜\이름',inplace=True)
    df.drop(columns=['기타'], inplace=True)
    df = df.rename(columns=lambda x: f"{x}({all_group[i]})")
    df = df.fillna('')
    accumulatedDF = pd.merge(accumulatedDF, df, left_index=True, right_index=True, how='outer')


accumulatedDF['이번주 출석인원'] = accumulatedDF.apply(making.count_os, axis=1)
print(accumulatedDF)
accumulatedDF.to_excel('원페이지.xlsx')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)

making.upload_data_to_sheets(file,["원페이지"])

spreadsheet = file.open('원페이지')  # 수정하려는 스프레드시트 이름
worksheet = spreadsheet.sheet1
worksheet.update_acell('A1', '날짜\이름')