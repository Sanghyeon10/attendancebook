import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making
import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time


pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비

all_group= making.all_group()

attendance_file_path = 'farmnameAndkids.txt' #기존 텍본파일과 다른것 사용하기.
# 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
attendance_dict= making.get_nextyearinfo(attendance_file_path)



df = pd.read_excel(making.destination_folder+"아이들 정보.xlsx", sheet_name='시트1' ,index_col=0 )



df=df[['비고']]
df= df.reset_index()
# print(df)

for i in range(len(df)):
    for farm_name, attendees in attendance_dict.items():
        if df.loc[df.index[i], '이름'] in  attendees:
            df.loc[df.index[i], '목장'] = farm_name

df= df.dropna(subset=['목장'])
df=df[["이름",'목장','비고']].sort_values(by="목장")
# print(df)

df.to_excel('주소원페이지.xlsx')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)

making.upload_data_to_sheets(file,["주소원페이지"])

