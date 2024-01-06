import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making
import datetime



scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name("C:\\Users\\User\PycharmProjects\pythonProject\\abiding-honor-375915-c16db88a8008.json")

file = gspread.authorize(creds)
# sh = file.open("오류 테스트용")
sh = file.open(making.ThisYearAttendnce) #woorbook = sh
# print(type(sh.worksheets()[1]))

A = input('특정 목장 업로드할지 판단 0이면 전부올리기 input')
uploadlist = making.WhatIsToUpload(A)
print("uploadlist:",uploadlist)


all_group= making.all_group()
worksheet_list = sh.worksheets()

if len(worksheet_list)!= len(all_group): #에러상황일수도? 워크 시트 기준으로해야맞음
    print(worksheet_list)
    print(all_group)
    input('시트와 변수개수가 안맞다!')
    # time.sleep(600)

for i in range(len(all_group)):
    if all_group[i] in uploadlist: #업로드 리스트에 해당하는 것만 업로드하기
        sheet= sh.worksheet(all_group[i]) #구글 스프레드기준 찾기
        print(all_group[i])

        tempdf = pd.read_excel(r'{}.xlsx'.format(all_group[i])) #해당파일찾고 데이터 옮겨오기
        tempdf = tempdf.fillna('')

        sheet.clear()
        sheet.update(making.getrangename(tempdf) ,[tempdf.columns.values.tolist()] +tempdf.values.tolist()) #데이터 덧씌우기
        #6.0.0 버전되면 구문 위치 바뀐다고함.
        time.sleep(5)

        # print(making.getrangename(tempdf))
    else:
        pass


### 백업파일 업로드

now =datetime.datetime.now()
N = int(now.strftime("%U"))% 6
print('N',N)


sh = file.open("백업"+str(N)) #woorbook = sh

print('백업파일 업로드')
uploadlist = making.WhatIsToUpload(A)


all_group= making.all_group()
worksheet_list = sh.worksheets()

if len(worksheet_list)!= len(all_group): #에러상황일수도? 워크 시트 기준으로해야맞음
    print(worksheet_list)
    print(all_group)
    input('시트와 변수개수가 안맞다!')
    # time.sleep(600)

for i in range(len(all_group)):
    if all_group[i] in uploadlist: #업로드 리스트에 해당하는 것만 업로드하기
        sheet= sh.worksheet(all_group[i]) #구글 스프레드기준 찾기
        print(all_group[i])

        tempdf = pd.read_excel(r'{}.xlsx'.format(all_group[i])) #해당파일찾고 데이터 옮겨오기
        tempdf = tempdf.fillna('')

        sheet.clear()
        sheet.update(making.getrangename(tempdf) ,[tempdf.columns.values.tolist()] +tempdf.values.tolist()) #데이터 덧씌우기
        #6.0.0 버전되면 구문 위치 바뀐다고함.
        time.sleep(5)

        # print(making.getrangename(tempdf))
    else:
        pass

print('N',N)