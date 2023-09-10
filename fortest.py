import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making

# #딕셔너리 생성
# data = {
#     'name': 'John',
#     'friends': ['홍길동' ,'안철수', '문제인', '죽음']
# }
#
# # 딕셔너리를 텍스트 파일로 저장
# with open('data.txt', 'w', encoding='UTF-8') as txt_file:
#     for key, value in data.items():
#         txt_file.write(f"{key}: {value}\n")

# 텍스트 파일을 딕셔너리로 불러오기
loaded_data = {}
with open('data.txt', 'r',encoding='UTF-8') as txt_file:
    for line in txt_file:
        key, value = line.strip().split(': ')
        loaded_data[key] = eval(value)

# 불러온 데이터 출력
print(loaded_data)
print(loaded_data['friends'][-1])




####
# scopes = [
#     'https://www.googleapis.com/auth/spreadsheets',
#     'https://www.googleapis.com/auth/dirve'
# ]
# creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\User\PycharmProjects\pythonProject\\abiding-honor-375915-c16db88a8008.json")
#
# file = gspread.authorize(creds)
# sh = file.open('5-3 목장 출석표') #woorbook = sh
#
# worksheet_name = sh.worksheets()[0]
#
#
# print(sh.worksheets()[0])
# sheet= sh.worksheet('시트1') #구글 스프레드기준 찾기
#
# tempdf = pd.read_excel(r'{}.xlsx'.format('5-3')) #해당파일찾고 데이터 옮겨오기
# tempdf = tempdf.fillna('')
#
# rangename=making.getrangename(tempdf)
# print(rangename, type(rangename))
# simplelist=[tempdf.columns.values.tolist()] +tempdf.values.tolist()
# print(simplelist)
#
# sheet.update( simplelist,rangename) #데이터 덧씌우기
# # sheet.update('A2:B4', [[42,'33'], [43]]) #알아낸건 주어진 첫번째 row부터 첫번째 리스트각 요쇼별로 넣는다는것.
# time.sleep(2)
#
#
