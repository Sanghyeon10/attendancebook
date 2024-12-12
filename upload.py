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
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
#위치 바뀌면 수정해줄것.

file = gspread.authorize(creds)
# sh = file.open("오류 테스트용")
sh = file.open(making.ThisYearAttendnce) #woorbook = sh
# print(type(sh.worksheets()[1]))


A = input('특정 목장 업로드할지 판단 0이면 전부올리기 input')
uploadlist = making.WhatIsToUpload(A)
print("uploadlist:", uploadlist)

#파일업로드

now =datetime.datetime.now()
N = int(now.strftime("%U"))% 6
making.upload_data_to_allsheets(file,[making.ThisYearAttendnce,"백업"+str(N)], making.all_group(), uploadlist )

