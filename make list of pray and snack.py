import pandas as pd
import calendar
import making
import datetime
from wcwidth import wcswidth
import tabulate
import matplotlib.pyplot as plt
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time

tabulate.WIDE_CHARS_MODE = False
# tabulate.PRESERVE_WHITESPACE = True


# 변수 설정
start=4# int(input("시작월"))
end=6# int(input("끝나는월"))



daylist= making.index()[:-1]
# 문자열을 datetime 객체로 변환
daylist = [datetime.datetime.strptime(date_str, '%Y-%m-%d') for date_str in daylist]
# print(daylist, type(daylist[3]))

columns= range(start, end+1)

# 데이터프레임 초기화
df = pd.DataFrame(index=range(0, 5), columns=columns)
# df.index.name="주차\월"


all_group=making.all_group()[:-1] #새신자 삭제
praysunsu= sorted(all_group, key=lambda x: (int(x.split('-')[0])) , reverse=True)
snacksunsu= all_group[::-1]+ ["부장님","총무님"]
snacksunsu.remove('6-5')
snacksunsu.remove('6-4')
print(praysunsu)
print(snacksunsu)




#변수설정
startday= datetime.datetime(year=2024,month=4,day=7)
specialday= [datetime.datetime(year=2024,month=5,day=12)]

#기도 ['6-1','6-2', '6-3', '6-4', '6-5', '5-1', '5-2', '5-3', '5-4', '5-5', '4-1', '4-2', '4-3', '4-4']
#간식 ['6-3','6-2','6-1', '5-5', '5-4', '5-3', '5-2', '5-1', '4-4', '4-3', '4-2', '4-1', '부장님', '총무님']
realpraysunsu=['5-2', '5-3', '5-4', '5-5', '4-1', '4-2', '4-3', '4-4']+  praysunsu*10
realsnacksunsu=['5-1', '4-4', '4-3', '4-2', '4-1', '부장님', '총무님'] + snacksunsu*10



# print( ["a","a"]+ [5,4,3]*10)


# 계산
i=0
j=0
for day in daylist:
    if startday<= day and making.getdaydate(day)[0] in columns: #특정 날자 이후 그리고 표를 작성해야하는 달에 해당하면
        if day in specialday:#특이사항인경우
            print(day)
            pandan=int(input("기도pass? 1이면 참 0이면 거짓"))
            if pandan:
                A="공란"
            else:
                A="대표기도,성경봉독:"+realpraysunsu[i]
                i +=1

            pandan= int(input("간식pass? 1이면 참 0이면 거짓"))
            if pandan:
                B="공란"
            else:
                B="간식:"+realsnacksunsu[j]
                j +=1
            text= "\n".join([A, B])

        elif making.getdaydate(day)[1] ==2 : #3주차인경우
            text="\n".join(["대표기도:장로님", "간식:"+realsnacksunsu[j]])
            j += 1

        else: #그외 보통
            text= "\n".join(["대표기도,성경봉독:"+realpraysunsu[i], "간식:"+ realsnacksunsu[j]])
            i += 1
            j += 1

        df.loc[making.getdaydate(day)[1], making.getdaydate(day)[0]]= text



df.index= range(1,6)
df = df.fillna("")
df.columns = [str(col) + '월' for col in df.columns]
df.index= [str(ind) + '주차' for ind in df.index]
df.index.name=""
name="snack"
df.to_excel("{}.xlsx".format(name))
# print(df)

table = tabulate.tabulate(df, headers='keys', tablefmt='grid', showindex="always", stralign='left')

print(table)


##구글 스프레드 시트 업로드

A= input('구글 스프레드 시트 업로드 input')
givenlist=[name] #엑셀파일이름과 구글스프레드시트 이름을 일치시킬것.


scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)


making.upload_data_to_sheets(file,givenlist)

