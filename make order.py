import pandas as pd
import making
import numpy as np
import datetime

attendance_dict, nocome_dict = making.make_data_from_file("attendance.txt")

all_group = making.all_group()
# tempdf = pd.read_excel(r'C:\Users\User\Downloads\{}.xlsx'.format(making.ThisYearAttendnce), sheet_name=None)

printing= 'yes'#input('명단 프린트할꺼라면 yes라고 치기')

a=[]
b=[]
temp=[]
getname= making.get_name()
farmnameAndkids=""

filtered_data=[] #먼저 빈리스트 정의하기
for i in range(len(all_group)): #인덱스가 같은지 보기 (요류 방지용)
    df =pd.read_excel(r'{}.xlsx'.format(all_group[i])) #새로이 만든 파일 기준으로 명단출력
    # df = tempdf[all_group[i]]
    df.set_index('날짜\이름', inplace=True)
    # print(df)

    if int(datetime.datetime.now().strftime("%U"))==0 and df.loc[df.index[-1],'기타']!=0 : #엑셀파일 처음만들었때의 주에서만 작동하는 코드
        # print("처음 파일 생성")
        df.loc[df.index[-1],:]=0 #엑셀 파일 처음 만들면 기타의 출석율이 0이 아님. 0으로 다 채워줌. 안 채우면 오류남

    namelist = df.columns
    # print(all_group[i], namelist.tolist())

    #프린트 명부에서 제거해야할 명단의 딕셔너리
    file_name = "except_data.txt"
    loaded_data = making.makedictfromtxt(file_name)

    for j in namelist:  # 기존 엑셀시트에 있는 이름중
        if df[j][(df[j] == 'O') | (df[j] == 'X')].count() >5: # X든 O든 총개수가 5를 넘어야
            a.append( (j,float(df.loc[df.index[-1], j])) )
            # print(all_group[i],j,df.loc[df.index[-1], j])
        else:
            b.append( (j,float(df.loc[df.index[-1], j])) )


    a.sort(key=lambda x: x[1], reverse=True)   #전부 정보획득했으면 정렬하기
    b.sort(key=lambda x: x[1], reverse=True) #(이름, 출석율)의 정보 리스트, a는 출석개수가 많은것 b는적은것
    a= a+b #출석 정보가 작은 애들은 뒤로 빼준 것임.
    # print(a)
    a.remove(('기타',0)) #기타는 첫번째로 넣어야되서 일단 삭제
    # print('dd',[item for item in a if (int(item[1]) < 10 and item[0] not in loaded_data[all_group[i]])])
    filtered_data = filtered_data+ [all_group[i]]+ [item for item in a if int(item[1]) <= 10 and item[0] not in loaded_data[all_group[i]] ]
    #출석율이 특정숫자보다 낮고 제거명부에 없는 애들은 명부 프린트에서 제거해줄지 검토해야함
    #목장이름+ 리스트형태로 명부 만들어서 마지막에 프린트해줌.

    #칼럼에 넣을 리스트 만들기
    for l in range(len(a)):
        temp.append(a[l][0]) #출석율 높은 순서대로 넣는것임.

    # print(temp)

    temp.insert(0,'기타') #기타 첫번째로 다시 넣어주기
    # print(temp)
    temp = making.gettruelist(temp, loaded_data[all_group[i]]) +loaded_data[all_group[i]]
    #기존의 명부에서 제외해야하는 아이들 이름 제외한 리스트를 구하고 뒤에 제외리스트를 추가함.

    # print(df)
    # print(temp)
    #새신자 목장이 없어서, 새신자 정상등록이 되지 않아서, 예외처리하는 코드 만듬.
    df = df.loc[:, temp]
    # if len(df.columns) == len(temp): #정상적인경우
    #     df=df.loc[:,temp] #데이터 프레임에 주어진 명단순서대로 넣기(기타+ 출석율순 명단+ 제외 명단)
    # else: #등반자로 등록되면 temp의 목록에서 삭제되니까 일반목장에서도 삭제되서 에러남. 다시 넣어줌.
    #     df=df.loc[:,temp+attendance_dict['등반자']]



    if all_group[i] != '새신자': #새신자만 아니면
        df.to_excel("{}.xlsx".format(all_group[i])) #엑셀파일 출력


    if all_group[i] in loaded_data.keys():# 명단에서 제외해야할 명단이 있다면
        temp = making.gettruelist(temp, loaded_data[all_group[i]]+['기타']) # 순서에서 제외해서 저장하기


    # print(all_group[i],temp) #애들 한글 명단 다시 만들때 활용할 코드부분. 한줄로 출력할때 사용
    if printing == 'yes': #프린트 하는게 맞으면
        making.make_line(all_group[i],temp, getname[all_group[i]]) #n명씩 잘라서 표현할때
        # print(all_group[i]+" "+' '.join(temp))
        farmnameAndkids= farmnameAndkids+ (all_group[i]+" "+' '.join(temp)) + '\n'

    #변수 초기화
    temp=[]
    a=[]
    b=[]

    if all_group[i] != '새신자':
        pass
    else: #새신자이면
        # print("")
        print("불출석")
        print("등반자")
        print("")
        print("이름:")
        print("전도자(목장):")
        print("인적사항:")
        print("주소 생년월일 학교명 가족관계 핸드폰번호")




print("")
print("")
print(filtered_data)

with open('farmnameAndkids.txt', 'w', encoding='utf-8') as file:
    file.write(farmnameAndkids)
