import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time


input('새친구 엑셀 업로드가 맞는가? input')

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\User\PycharmProjects\pythonProject\\abiding-honor-375915-c16db88a8008.json")

file = gspread.authorize(creds)
sh = file.open('새친구 관리엑셀표') #woorbook = sh

worksheet_name = sh.worksheets()[0]


print(sh.worksheets()[0])
sheet= sh.worksheet('시트1') #구글 스프레드기준 찾기

tempdf = pd.read_excel(r'{}.xlsx'.format('test')) #해당파일찾고 데이터 옮겨오기
tempdf = tempdf.fillna('')


sheet.update([tempdf.columns.values.tolist()] +tempdf.values.tolist()) #데이터 덧씌우기

time.sleep(2)
