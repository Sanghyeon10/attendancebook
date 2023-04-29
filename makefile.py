import pandas as pd
import datetime
import indexmaking


print('초등부 출석표 파일 맞음?')
tempdf = pd.read_excel(r'C:\Users\A\Downloads\2023 초등부 출석표.xlsx', sheet_name=None)


all_group=['4-1','4-2','4-3','4-4','4-5','5-1','5-2','5-3','5-4','6-1','6-2','6-3','6-4']

# 출석 정보가 저장된 파일 경로를 입력합니다.
attendance_file_path = 'attendance.txt'

# 목장 출석 정보를 저장할 딕셔너리를 생성합니다.
attendance_dict = {}

# 출석 정보 파일을 읽어서 딕셔너리에 저장합니다.
with open(attendance_file_path, 'r', encoding='utf-8') as f:
    for line in f:
        # 한 줄씩 읽어서 공백을 기준으로 분리합니다.
        fields = line.strip().split()

        # 목장 이름, 출석자 이름1, 출석자 이름2, ...으로 분리합니다.
        # print(fields)
        farm_name, *attendees = fields
        # if attendees ==[]:
        #     print('???')

        # 딕셔너리에 목장 이름을 키로, 출석자 이름 리스트를 값으로 저장합니다.
        attendance_dict[farm_name] = attendees

# 각 목장의 출석 정보 리스트를 출력합니다.
for farm_name, attendees in attendance_dict.items():
    print(f'{farm_name} 목장 출석자: {attendees}', '인원수:' ,len(attendees))



test=[]
for i in range(len(all_group)): #인덱스가 같은지 보기 (요류 방지용)
    df = tempdf[all_group[i]]
    df.set_index('날짜\이름', inplace=True)
    test.append(len(df.index))


print(test.count(54))
print('13이면 인덱스에 문제없음')

now =datetime.datetime.now()

N = int(now.strftime("%U"))-1 #오늘은 몇번째 주일?
print(df.index[N])
input('파일, 인덱스, 일자 맞는가?')


#for문 돌리기
for i in range(len(all_group)):
    df=tempdf[all_group[i]] #해당하는 목장 정보 불러오기
    # print(df)
    # df.set_index('날짜\이름',inplace=True)
    namelist = df.columns

    check=[]


    if attendance_dict[all_group[i]] !=[]: # 출석 공란이 아닌경우 (정상적인경우)
        for j in namelist: #기존 엑셀시트에 있는 이름중
            if j in attendance_dict[all_group[i]]: # 오늘 출석정보가 있다면.ex4-3을 넣고 해당하는 출석정보 리스트 얻기
                df.loc[df.index[N],j]='O'
                check.append(j) #확인된건 넣어두기


            else: #에러가능성 고치기 A2에서 시작하는게 좋음
                df.loc[df.index[N],j]='X' #없다면 x표시

        #이름다 체크했다면,
        if len(check) !=len(attendance_dict[all_group[i]]):
            print('누락존재목장')
            diff1= list(set(attendance_dict[all_group[i]]) -set(check)  ) # check(출석인원중) 명부인원을 빼면 누락된 사람 찾아내기 가능
            print(all_group[i], diff1)
            # print(all_group[i], check, attendance_dict[all_group[i]] ) #실제 0입력한 사람수와 아날로그 출석수가 같아야함.,ex. 4-3....

    else:
        for j in namelist:  # 출석정보가 없으므로 ?표시
            df.loc[df.index[N], j] = '?'

    #파일로 만들기
    df.to_excel("{}.xlsx".format(all_group[i])) #5-1식으로 출력




#여기서는 4-1부터 6-4파일을 가져와 출석율을 계산해줌 문제 생기면 아래건 다 날리기
name=0
all_group=['4-1','4-2','4-3','4-4','4-5','5-1','5-2','5-3','5-4','6-1','6-2','6-3','6-4']

for i in range(len(all_group)): #인덱스가 같은지 보기 (요류 방지용)
    name=all_group[i]
    df = pd.read_excel('{}.xlsx'.format(name), sheet_name=None)
    df=df['Sheet1']
    # print(df)
    # df.set_index('날짜\이름', inplace=True)
    # print(df)




numberofO= 0
numberofX= 0
for l in range(len(all_group)):
    df = pd.read_excel('{}.xlsx'.format(all_group[l]), sheet_name=None)
    df=df['Sheet1']
    # print(all_group[l])

    # df.set_index('날짜\이름', inplace=True)
    # print(type(df))
    # print(df)
    df.set_index('날짜\이름',inplace=True)
    # print(df)


    namelist = df.columns
    for i in range(len(namelist)): #이름 뽑기
        for j in range(len(df.index)): #인덱스아래로 가면서 처리하기
            if df.index[j] =='비고':
                pass
            else:
                if df.iat[j,i] =='O':
                    numberofO += 1
                elif df.iat[j,i] =='X': #숫자 카운팅
                    numberofX += 1
                else: #공란이면 무시
                    pass



        if (numberofO + numberofX)==0: #값 정의 안됨
            df.iat[-1, i] = 0 #맨아래에 적기
            # print(namelist[i],0)
        else:
            df.iat[-1, i] = str(round(numberofO /(numberofO+numberofX)*100))
            # print(namelist[i], numberofO /(numberofO+numberofX))
        numberofO=0
        numberofX=0 #값초기화 겸 값작성


    # print(df)
    tempindex= indexmaking.make()
    tempindex.append('비고')

    # print(len(tempindex),len(df.index))

    df.index = tempindex
    df.index.name= '날짜\이름'
    # df.index = pd.to_datetime(df.index)




    df.to_excel("{}.xlsx".format(all_group[l]),  index=True )  # 5-1식으로 출력
print('통계작성완료')