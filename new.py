import pandas as pd
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import time
import making


print('초등부 새친구 출석표 파일 맞음?')
tempdf = pd.read_excel(r'C:\Users\User\Downloads\새친구 관리엑셀표.xlsx', sheet_name=None)
df=tempdf['시트1'] # 여러 시트중 시트1을 지정해 저장
df.set_index('날짜\이름', inplace=True)

indexlist = making.index()

for l in range(5): #0~4번까지 돌리기
    indexlist.insert(l,df.index[l]) #앞의 정보는 유지해야함

df.index = indexlist
df.index.name= '날짜\이름'

all_group= making.all_group()

# print(tempdf)
# print(df)


# 혹시나 문자열이 아니라 datetime형태의 정보로 저장하고 있으면 에러나므로 검사하고 만일 맞으면 강제종료
my_list = df.iloc[2].value_counts().index.tolist() + df.iloc[1].value_counts().index.tolist()
# print(my_list)

for item in my_list:
    # datetime 객체인지 확인
    if isinstance(item, datetime.datetime):
        print("리스트에 datetime 객체가 포함되어 있습니다.")
        print(my_list)
        exit()




#엑셀에서 출석정보 가져오기
for i in range(1,len(df.columns.tolist())): #첫번재칸은 통계라 예외
    # print(df.loc[df.index[4], df.columns.tolist()[i]])
    groupname = (df.loc[df.index[4], df.columns.tolist()[i]]).split(" ", 1)[0] # 빈칸을 기준으로 앞의것을 가져오기 즉 목장정보를 가져오기
    name= df.columns.tolist()[i]
    # print(groupname)

    if groupname in all_group or groupname=='새신자': #특정 아이의 목장 출석 정보를 가져와야 한다면 or 새신자문자열을 쓰는경우

        tempdf = pd.read_excel('{}.xlsx'.format(groupname), sheet_name=None) #기록된 출석부에서 정보 가져오기
        tempdf = tempdf['Sheet1']
        tempdf.set_index('날짜\이름', inplace=True)
        # print(tempdf)

        olddata =  pd.read_excel('{}.xlsx'.format("새신자"), sheet_name=None) #새신자 출석부에서 정보 가져오기
        olddata = olddata['Sheet1']
        olddata.set_index('날짜\이름', inplace=True)


        if name in tempdf.columns.tolist() and name in olddata.columns.tolist(): #가져올게 있으면, 데이터프레임형태로 가져오기
            tempdf = tempdf[name]
            olddata = olddata[name]

            for p in range(len(tempdf)):
                # print(olddata.loc[olddata.index[p]])
                if pd.notnull(olddata.loc[olddata.index[p]]):  # 결측치가 아니다. 즉 새신자 정보란에 값이 있다면
                    tempdf.loc[tempdf.index[p]] = olddata.loc[olddata.index[p]]  # tempdf에 값 넣어주기
                    if tempdf.loc[tempdf.index[p]] != olddata.loc[olddata.index[p]]: #혹시 둘의 값이 다르다면 확인해주기.
                        print(name, '정보값 확인하기', tempdf.loc[tempdf.index[p]],olddata.loc[olddata.index[p]] )

            df[name] = pd.concat([df[name].iloc[:5], tempdf]) #합친 것을  데이터로 넣어주기
            df[name]= making.calculate_o_ratio_for_series(df[name]) #출석율 통계 합쳐서 계산하기
            # 합쳐서 통계작성 오류 있음.

        elif name in tempdf.columns.tolist() and name not in olddata.columns.tolist(): #새신자 출석부에 명단이 없는경우
            tempdf = tempdf[name]

            df[name] = pd.concat([df[name].iloc[:5], tempdf])  # 첫 4행까지는 기본정보이므로 그 이후부터 복사함.

        elif name not in tempdf.columns.tolist() and name in olddata.columns.tolist(): #새신자 출석부에만 명단이 있는경우
            olddata = olddata[name]

            df[name] = pd.concat([df[name].iloc[:5], olddata])  # 첫 4행까지는 기본정보이므로 그 이후부터 복사함.

        else:
            print('오류가능성!')

        # df[name] = pd.concat([df[name].iloc[:5], tempdf]) #첫 4행까지는 기본정보이므로 그 이후부터 복사함.
        # print(df[name])




# 통계 작성
total =len(df.columns)-1 # 전체인원수 구하기
failnumber = df.iloc[2].value_counts()["X"] #등반 미달자 수
up = total - failnumber #등반 성공자 수

df.loc['등록날짜','통계']= total

df.loc['등반날짜','통계']= str(round(up/total*100))+'%' # 등반 인원수/ 전체 인원
#등반율 구하기

numrberofO=0
numrberofX=0

for i in range(1,len(df.columns.tolist())): #애들 이름 순대로 하기 첫번째 칸은 통계임
    # print(df.columns.tolist()[i])
    numrberofO = 0
    numrberofX = 0 #변수 초기화
    # print(type(df.loc[df.index[2], df.columns.tolist()[i]]))

    if df.loc[df.index[2], df.columns.tolist()[i]]!= "X" and i!=0 :#날짜 값이 있는경우 즉 등반날짜가 있는경우.
        # print(df.loc[df.index[2], df.columns.tolist()[i]])
        # print(type(df.loc[df.index[2], df.columns.tolist()[i]]))
        date = datetime.datetime.strptime(df.loc[df.index[2], df.columns.tolist()[i]], "%Y-%m-%d") #날짜를 datetime화
        target_date=  date + datetime.timedelta(weeks=12) #12주후 출석율
        # print(target_date)

        for j in range(len(df.index)-1): #출석율 계산, 마지막은 비고이므로 생략
            # print((df.index[j]))
            if j >4 : #년월일 인덱스인 부분만 계산해야함.
                # print(df.index[j], type(df.index[j]))
                if datetime.datetime.strptime(df.index[j], "%Y-%m-%d") >= target_date: #이미 datetime.datetime형
                # 12주 후부터 세기, 또한 마지막은 비고라서 패스

                    if df.loc[df.index[j],df.columns.tolist()[i]] == 'O':
                        numrberofO = numrberofO+1

                    elif df.loc[df.index[j],df.columns.tolist()[i]] == 'X':
                        numrberofX = numrberofX +1
                    else:
                        pass

                if (numrberofO) == 0:
                    result = 'X'
                elif (numrberofO+numrberofX) == 0:
                    result = "X"

                else:
                    result= round(numrberofO / (numrberofO+ numrberofX)*100)

                # print(df.loc[df.index[3],df.columns.tolist()[i]])
                df.iat[3,i]= result

    else: #등반날짜가 없는 경우
        # 2번째칸에 있는 등록날짜기준으로 날자 세는거임.
        date = datetime.datetime.strptime(df.loc[df.index[1], df.columns.tolist()[i]], "%Y-%m-%d") #날짜를 datetime화
        target_date=  date + datetime.timedelta(weeks=12) #12주후 출석율
        # print(target_date,datetime.datetime.now())
        if datetime.datetime.now()> target_date:#등록이후 12주가 지나도 등반이 안돼면 등반여부체크
            df.iat[3, i] ="등반?"
        else:
            df.iat[3, i] ="" # 아니면 빈칸기입



counts = df.iloc[3].value_counts()["X"]

under=(len(df.columns)-1 - df.iloc[2].value_counts()["X"]) # 전체인원수 -등반실패인원 = 등반인원 수

# print( df.iloc[3].value_counts()[100])
positive_counts =  str(round((under- df.iloc[3].value_counts()["X"] )/ under *100)) + '%' # 3개월후 출석율이 찍힘수(=등반인원수 - 실패율) / 등반 인원수

df.iat[3,0]= positive_counts


df.iloc[1] = df.iloc[1].apply(lambda x: x.strftime('%Y-%m-%d') if type(x)== datetime.datetime else x )
df.iloc[2] = df.iloc[2].apply(lambda x: x.strftime('%Y-%m-%d') if type(x)== datetime.datetime else x )
#datetime형태로 들어가면 업로드에 문제생김 다 통계 작성하고 바꿔주기

df.to_excel("{}.xlsx".format('test'), index=True)













