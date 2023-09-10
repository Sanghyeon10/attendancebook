import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time


def upload(name1,name2):

    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/dirve'
    ]
    creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\User\PycharmProjects\pythonProject\\abiding-honor-375915-c16db88a8008.json")

    file = gspread.authorize(creds)
    sh = file.open(name1) #woorbook = sh

    print(sh.worksheets()[0])   # worksheet_name = sh.worksheets()[0]
    sheet= sh.worksheet('시트1') #구글 스프레드기준 찾기

    tempdf = pd.read_excel(r'{}.xlsx'.format(name2)) #해당파일찾고 데이터 옮겨오기
    tempdf = tempdf.fillna('')# 이거 없으면 오류남


    sheet.update([tempdf.columns.values.tolist()] +tempdf.values.tolist()) #데이터 덧씌우기

    time.sleep(2)

    print(name1)
