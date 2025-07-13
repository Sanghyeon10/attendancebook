import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making



teacherNameList =["홍세미","김원직","김다혜"]

A= input('extrafile 업로드?  input')
givenlist=[making.Newmembers ]+teacherNameList #엑셀파일이름과 구글스프레드시트 이름을 일치시킬것.

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)

making.upload_data_to_sheets(file,givenlist)