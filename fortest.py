import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making




scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\User\PycharmProjects\pythonProject\\abiding-honor-375915-c16db88a8008.json")

file = gspread.authorize(creds)
sh = file.open('5-3 목장 출석표') #woorbook = sh

worksheet_name = sh.worksheets()[0]


print(sh.worksheets()[0])
sheet= sh.worksheet('시트1') #구글 스프레드기준 찾기

tempdf = pd.read_excel(r'{}.xlsx'.format('5-3')) #해당파일찾고 데이터 옮겨오기
tempdf = tempdf.fillna('')

rangename=making.getrangename(tempdf)
print(rangename, type(rangename))
simplelist=[tempdf.columns.values.tolist()] +tempdf.values.tolist()
print(simplelist)

sheet.update( simplelist,rangename) #데이터 덧씌우기
# sheet.update('A2:B4', [[42,'33'], [43]]) #알아낸건 주어진 첫번째 row부터 첫번째 리스트각 요쇼별로 넣는다는것.
time.sleep(2)


