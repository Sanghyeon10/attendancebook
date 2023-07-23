import pandas as pd
import datetime
import making
import re



print('초등부 출석표 파일 맞음?')
tempdf = pd.read_excel(r'C:\Users\User\Downloads\2023 초등부 출석표.xlsx', sheet_name=None)


all_group= making.all_group()

# 출석 정보가 저장된 파일 경로를 입력합니다.
attendance_file_path = 'attendance.txt'

# 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
attendance_dict = {}

# 출석 정보 파일을 읽어서 딕셔너리에 저장합니다.
# 주의사항, 목장 내용인데 사이가 space바여야지, tab(\t)으로 구분되어있으면 오류남
with open(attendance_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # 한 줄씩 읽어서 공백 , .을 기준으로 분리합니다.(정규 표현식 활용했음)
        # fields = line.strip().split()
        fields = [line for line in re.split('\s|,|\.', line) if line]

        # 목장 이름, 출석자 이름1, 출석자 이름2, ...으로 분리합니다.
        farm_name, *attendees = fields

        # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
        attendance_dict[farm_name] = attendees

# 각 목장의 출석 정보 리스트를 출력합니다.
for farm_name, attendees in attendance_dict.items():
    print(f'{farm_name} 목장 출석자: {attendees}', '인원수:' ,len(attendees))

#결석정보 추가 코드
nocome_file_path = 'nocome.txt'

# 결석 사유 정보를 저장할 딕셔너리를 생성합니다.
nocome_dict = {}

# 딕셔너리에 저장합니다.
with open(nocome_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # fields = line.strip().split()
        field = line.split(" ",1)

        # 목장 이름, 출석자 이름1, 출석자 이름2, ...으로 분리합니다.
        farm_name, reason = field

        # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
        nocome_dict[farm_name] = reason





print()
print()

now =datetime.datetime.now()


dff=tempdf[all_group[0]]
print(int(now.strftime("%U"))-1) #오늘은 몇번째 주일?\
N = int(now.strftime("%U"))-1
# N = int(input("오늘은 몇번째 주일꺼 입력?+ upload시 목장if문 체크 input")) #특정 일자 입력할때 쓰는것
print(dff.iloc[N,0])


getnamelist=[] #정보없는 목장 선생님 이름 구하기

#for문 돌리기
for i in range(len(all_group)):
    df=tempdf[all_group[i]] #해당하는 목장 정보 불러오기
    # print(df)
    df.set_index('날짜\이름',inplace=True)
    namelist = df.columns


    check=[]


    if attendance_dict[all_group[i]] !=[] and all_group[i]!='새신자': # 출석 공란이 아닌경우 (정상적인경우) and 새신자가 아니면
        for j in namelist: #기존 엑셀시트에 있는 이름중
            if j in attendance_dict[all_group[i]]: # 오늘 출석정보가 있다면.ex4-3을 넣고 해당하는 출석정보 리스트 얻기
                df.loc[df.index[N],j]='O'
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
            print(all_group[i] , nocome_dict[all_group[i]] ) #strip해줘야 엔터키 삭제됨.


    elif all_group[i] == '새신자': #새신자라면, 비출석이 불출석이 아님.
        for j in namelist: #기존 엑셀시트에 있는 이름중
            if j in attendance_dict[all_group[i]]: # 오늘 출석정보가 있다면 새신자 딕셔너리를 넣고 해당하는 출석정보 리스트 얻기
                df.loc[df.index[N],j]='O'
                check.append(j) #확인된건 넣어두기

            if j in attendance_dict['불출석']: #불출석에 들어있다면,
                df.loc[df.index[N],j]='X'
                check.append(j) #확인된건 넣어두기


        #이름다 체크했다면,

        diff1= list(set(attendance_dict[all_group[i]]+(attendance_dict['불출석'])) -set(check))
        # 오늘 출석 정보에 있는 명단에서 check(출석인원중)을 빼면 누락된 사람 찾아내기 가능
        if diff1 !=[]: # 빈 리스트가 아니라면 누락존재
            print('새신자 이름 누락',all_group[i], diff1)


        #결석사유칸이 존재한다면
        if all_group[i] in nocome_dict: # 즉, 결석정보가 들어있는 목장이 있다면
            df.loc[df.index[N], '기타'] = nocome_dict[all_group[i]].strip() #입력해주기
            print(all_group[i] , nocome_dict[all_group[i]] ) #strip해줘야 엔터키 삭제됨.



    else: #출석정보가 없는경우
        for j in namelist:  # 출석정보가 없으므로 ?표시
            df.loc[df.index[N], j] = '?'
        getnamelist.append(all_group[i]) #정보 없는 목장 리스트 구하기

    #파일로 만들기
    df.to_excel("{}.xlsx".format(all_group[i])) #5-1식으로 출력


getname= making.get_name()
print('정보부재목장')
for l in getnamelist: #목장 별로 하나씩 꺼내서 이름프린트
    print(getname[l])

print()
print()
print()

#여기서는 4-1부터 6-4파일을 가져와 출석율을 계산해줌

for l in range(len(all_group)):
    df = pd.read_excel('{}.xlsx'.format(all_group[l]), sheet_name=None)
    df=df['Sheet1']
    df.set_index('날짜\이름',inplace=True)

    df = making.calculate_o_ratio(df)



    df.to_excel("{}.xlsx".format(all_group[l]),  index=True )  # 5-1식으로 출력
print('통계작성완료')
