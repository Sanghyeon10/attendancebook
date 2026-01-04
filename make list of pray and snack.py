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




all_group=making.next_group()[:-1] #새신자 삭제
praysunsu= sorted(all_group, key=lambda x: (int(x.split('-')[0])) , reverse=True)
snacksunsu= all_group[::-1]+ ["부장님","총무님"]
# snacksunsu.remove('6-5')
# snacksunsu.remove('6-4')
print(praysunsu)
print(snacksunsu)


# 변수 설정
start=1# int(input("시작월"))
end=3# int(input("끝나는월"))

startday= datetime.datetime(year=2024,month=1,day=7)
specialday= []# [datetime.datetime(year=2025,month=1,day=5),datetime.datetime(year=2025,month=1,day=12),datetime.datetime(year=2025,month=1,day=19),datetime.datetime(year=2025,month=1,day=26)]

# 기도 ['6-1', '6-2', '6-3', '6-4', '5-1', '5-2', '5-3', '4-1', '4-2', '4-3', '4-4', '4-5']
# 간식 ['6-4', '6-3', '6-2', '6-1', '5-3', '5-2', '5-1', '4-5', '4-4', '4-3', '4-2', '4-1', '부장님']
realpraysunsu =   ['6-1', '6-2', '6-3', '6-4', '5-1', '5-2', '5-3', '4-1', '4-2', '4-3', '4-4', '4-5']+praysunsu*10
realsnacksunsu=[""]+['부장님','6-4', '6-3', '6-2', '6-1', '5-3', '5-2', '4-5', '4-3', '4-2', '4-1', "심상현",'부장님']*20# "홍세미선생님","이윤미 선생님","이성미 선생님","1번 예외"]*10 #+ snacksunsu*10




# df 생성

daylist= making.index()[:-1]
# 문자열을 datetime 객체로 변환
daylist = [datetime.datetime.strptime(date_str, '%Y-%m-%d') for date_str in daylist]
# print(daylist, type(daylist[3]))

columns= range(start, end+1)

# 데이터프레임 초기화
df = pd.DataFrame(index=range(0, 5), columns=columns)
# df.index.name="주차\월"







# print( ["a","a"]+ [5,4,3]*10)

namebook = making.get_name()
# print(namebook)

# 계산
i=0 #기도순서 +1
j=0 # 간식순서 +1
for day in daylist:
    if startday<= day and making.getdaydate(day)[0] in columns: #특정 날자 이후 그리고 표를 작성해야하는 달에 해당하면
        if day in specialday:#특이사항인경우
            print(day)
            pandan=int(input("기도pass? 1이면 참 0이면 거짓"))
            if pandan:
                A="공란"
            else:
                if making.getdaydate(day)[1] !=2 : #3주차가 아닌경우 문제없음.
                    A="대표기도,성경봉독:"+realpraysunsu[i]
                    i +=1
                else:
                    A="대표기도:장로님"
                    #i는 변동없음

            pandan= int(input("간식pass? 1이면 참 0이면 거짓"))
            if pandan:
                B="공란"
            else:
                B="간식:"+realsnacksunsu[j]+" "+namebook.get([realsnacksunsu[j]])
                j +=1


            text= "\n".join([A, B])

        # elif making.getdaydate(day)[1] ==2 : #3주차인경우
        #     text="\n".join(["대표기도:장로님", "간식:"+realsnacksunsu[j]])
        #     j += 1

        else: #그외 보통
            # text= "\n".join(["대표기도,성경봉독:"+realpraysunsu[i], "간식:"+ realsnacksunsu[j],inverse.get([realsnacksunsu[j]]) ])
            text = "\n".join([
                "대표기도,성경봉독:" + realpraysunsu[i],
                "간식: " + realsnacksunsu[j]+" ("+namebook.get(realsnacksunsu[j], "")+")"
            ])
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
print(df.index.name)
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


#업로드 이후 A1 값 수정
making.upload_data_to_sheets(file,givenlist)

spreadsheet = file.open('snack')  # 수정하려는 스프레드시트 이름
worksheet = spreadsheet.sheet1
worksheet.update_acell('A1', making.year+'년')

