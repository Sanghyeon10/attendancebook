import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making

A= input('no입력하면 extrafile 업로드 안함 input')
givenlist=[making.Newmembers,"6-3" ] #엑셀파일이름과 구글스프레드시트 이름을 일치시킬것.

if A =='no':
    givenlist=[]
else:
    pass

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)

making.upload_data_to_sheets(file,givenlist)

# for i in givenlist: #새신자파일, 특정목장 파일, 새친구 파일 업로드
#
#     sh = file.open(i) #woorbook = sh
#
#     worksheet_name = sh.worksheets()[0]
#
#
#     print(i)
#     sheet= sh.worksheet('시트1') #구글 스프레드기준 찾기
#
#     tempdf = pd.read_excel(r'{}.xlsx'.format(i)) #해당파일찾고 데이터 옮겨오기
#     tempdf = tempdf.fillna('') #이거 안해주면 업로드시 오류남
#
#     sheet.clear()
#     sheet.update(range_name=making.getrangename(tempdf) ,values=[tempdf.columns.values.tolist()] +tempdf.values.tolist()) #데이터 덧씌우기
#
#     time.sleep(5)
