import pandas as pd
import datetime
import making
import re




input('누락명단이 정상이면 넘어가기 input')

# tempdf = pd.read_excel(r'C:\Users\User\Downloads\{}.xlsx'.format(making.ThisYearAttendnce), sheet_name=None)
tempdf = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, making.ThisYearAttendnce), sheet_name=None)


all_group= making.all_group()

# attendance_dict = making.read_attendance_from_file("attendance.txt") #텍스트 파일 읽어오기
attendance_dict, nocome_dict = making.make_data_from_file("attendance.txt")

toinputdict={}


print("")
try:
    for i in range(int(input("(코드로 이름 추가할 목장 수)반복 횟수를 입력하세요: "))):
        line= input('목장과 새로 기입할 명단을 복붙해 입력(숫자 리스트형태로) input')
        farm_name, attendees = line.split(" ",1) # 4-3은 key로 ,뒤 리스트는 value로 저장
        # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
        toinputdict[farm_name] = eval(attendees)
except: #중간에 잘못입력해도 잘 입력한건 들어감.

    print('형식이 잘못되었음')

print('명단에 추가할 이름:',toinputdict)



# # 각 목장의 출석 정보 리스트를 출력합니다.
# for farm_name, attendees in attendance_dict.items():
#     print(f'{farm_name} 목장 출석자: {attendees}', '인원수:' ,len(attendees))


#비고칸에 채울 결석 관련 정보를 딕셔너리 형태로 저장
# nocome_dict = making.read_nocome_from_file('nocome.txt')

# 잘 저장되었는지 출력
# print(nocome_dict)



print()
print()

now =datetime.datetime.now()



dff=tempdf[all_group[0]]
print(int(now.strftime("%U"))-1) #오늘은 몇번째 주일?\
N = int(now.strftime("%U"))-1
# N = int(input("오늘은 몇번째 주일꺼 입력?+ upload시 목장if문 체크 input")) #특정 일자 입력할때 쓰는것
print(dff.iloc[N,0])

print()

getnamelist=[] #정보없는 목장 선생님 이름 구하기

#for문 돌리기
for i in range(len(all_group)):
    df=tempdf[all_group[i]] #해당하는 목장 정보 불러오기
    # print(df)
    df.set_index('날짜\이름',inplace=True)

    if all_group[i] in toinputdict.keys():  # 명단 추가해야하면
        df = making.AddNewMembers(df , toinputdict[all_group[i]])


    namelist = df.columns
    check=[] #출석인원 수 초기화


    if attendance_dict[all_group[i]] !=[] and all_group[i]!='새신자': # 출석 공란이 아닌경우 (정상적인경우) and 새신자가 아니면

        for j in namelist: #기존 엑셀시트에 있는 이름중
            if j in attendance_dict[all_group[i]]: # 오늘 출석정보가 있다면.ex4-3을 넣고 해당하는 출석정보 리스트 얻기
                df.loc[df.index[N],j]='O'+making.checkO(j,attendance_dict['등반자'])
                check.append(j) #확인된건 넣어두기


            else:
                df.loc[df.index[N],j]='X' #없다면 x표시

        #이름다 체크했다면,
        if len(check) !=len(attendance_dict[all_group[i]]):

            diff1= list(set(attendance_dict[all_group[i]]) -set(check)  ) # check(출석인원중) 명부인원을 빼면 누락된 사람 찾아내기 가능
            print('누락존재 목장',all_group[i], diff1)


        #결석사유칸이 존재한다면
        if all_group[i] in nocome_dict: # 즉, 결석정보가 들어있는 목장이 있다면
            df.loc[df.index[N], '기타'] = nocome_dict[all_group[i]].strip() #입력해주기
            # print(all_group[i] , nocome_dict[all_group[i]] ) #strip해줘야 엔터키 삭제됨.



    elif all_group[i] == '새신자': #새신자라면, 비출석이 불출석이 아님.
        for j in namelist: #기존 엑셀시트에 있는 이름중
            if j in attendance_dict[all_group[i]]: # 오늘 출석정보가 있다면 새신자 딕셔너리를 넣고 해당하는 출석정보 리스트 얻기
                df.loc[df.index[N],j]='O'+making.checkO(j,attendance_dict['등반자'])
                check.append(j) #확인된건 넣어두기

            if j in attendance_dict['불출석']: #불출석에 들어있다면,
                df.loc[df.index[N],j]='X'
                check.append(j) #확인된건 넣어두기


        #이름다 체크했다면,

        diff1= list(set(attendance_dict[all_group[i]]+attendance_dict['불출석'] +attendance_dict['등반자'] ) -set(check))
        # 오늘 출석 정보에 있는 명단에서 check(출석인원중)을 빼면 누락된 사람 찾아내기 가능
        if diff1 !=[]: # 빈 리스트가 아니라면 누락존재
            print('새신자 이름 누락',all_group[i], diff1)


        #결석사유칸이 존재한다면
        if all_group[i] in nocome_dict: # 즉, 결석정보가 들어있는 목장이 있다면
            df.loc[df.index[N], '기타'] = nocome_dict[all_group[i]].strip() #입력해주기
            # print(all_group[i] , nocome_dict[all_group[i]] ) #strip해줘야 엔터키 삭제됨.




    else: #출석정보가 없는경우
        for j in namelist:  # 출석정보가 없으므로 ?표시
            df.loc[df.index[N], j] = '?'
        getnamelist.append(all_group[i]) #정보 없는 목장 리스트 구하기

        #결석사유칸이 존재한다면
        if all_group[i] in nocome_dict: # 즉, 결석정보가 들어있는 목장이 있다면
            df.loc[df.index[N], '기타'] = nocome_dict[all_group[i]].strip() #입력해주기
            # print(all_group[i] , nocome_dict[all_group[i]] ) #strip해줘야 엔터키 삭제됨.

        # 파일로 만들기
    df.to_excel("{}.xlsx".format(all_group[i]))  # 5-1식으로 출력
    # 출력해야지 그 출력된 결과물에서 다시 통계작성함.

print()

getname= making.get_name()
if getnamelist!=[]: #명단이 빈 리스트가 아니면
    print('정보부재목장') #출력해주기
for l in getnamelist: #목장 별로 하나씩 꺼내서 이름프린트
    print(getname[l])



print()

#여기서는 4-1부터 6-4파일을 가져와 출석율을 계산해줌

for l in range(len(all_group)):
    df = pd.read_excel('{}.xlsx'.format(all_group[l]), sheet_name=None)
    df=df['Sheet1']
    df.set_index('날짜\이름',inplace=True)

    df = making.calculate_o_ratio(df)



    df.to_excel("{}.xlsx".format(all_group[l]),  index=True )  # 5-1식으로 출력
# print('통계작성완료') #통계 작성완료도 큰 의미가 없어서 출력안함.



#새로운 사람 추가시 새친구파일에 업데이트할것
if toinputdict!={}: #빈 딕녀서리가 아니라면 입력할것이 있다.
    checkcheck = input("새친구 관리 엑셀표에 추가할지 여부no이면 안함 input")
    if checkcheck !='no':
        # tempdf = pd.read_excel(r'C:\Users\User\Downloads\{}.xlsx'.format(making.Newmembers), sheet_name=None)
        tempdf = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, making.Newmembers), sheet_name=None)
        df=tempdf['시트1'] # 여러 시트중 시트1을 지정해 저장
        df.set_index('날짜\이름', inplace=True)

        indexlist = making.index()

        for l in range(5): #0~4번까지 돌리기
            indexlist.insert(l,df.index[l]) #앞의 정보는 유지해야함

        df.index = indexlist
        df.index.name= '날짜\이름'

        for mokjang in toinputdict.keys():  # 명단 추가해야하면
            for name in toinputdict[mokjang]: #toinputdict[mokjang]은 리스트형태,["홍길동"], 여기서 하나씩 칼럼에 추가
                df[name] = None
                df.loc[df.index[0], name] = "X"
                df.loc[df.index[1], name] = making.index()[N] #이번주 일요일 날짜.
                df.loc[df.index[2], name] = "X"
                df.loc[df.index[3], name] = "X"
                df.loc[df.index[4], name] = mokjang + " "+ "목장" #ex. 4-3 목장

        df.to_excel(r'C:\Users\User\Downloads\{}.xlsx'.format(making.Newmembers), sheet_name="시트1", engine='openpyxl')
        #다운로드 파일의 파일을 업데이트해야 new 파일돌릴때 인식제대로함.



