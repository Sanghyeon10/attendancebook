import pandas as pd
import datetime
import making
import re



print('초등부 출석표 파일 맞음?')
tempdf = pd.read_excel(r'C:\Users\User\Downloads\2023 초등부 출석표.xlsx', sheet_name=None)


all_group= making.all_group()

attendance_dict = making.read_attendance_from_file("attendance.txt") #텍스트 파일 읽어오기




# 각 목장의 출석 정보 리스트를 출력합니다.
for farm_name, attendees in attendance_dict.items():
    print(f'{farm_name} 목장 출석자: {attendees}', '인원수:' ,len(attendees))


print()
print()


getnamelist=[] #정보없는 목장 선생님 이름 구하기

#for문 돌리기
for i in range(len(all_group)):
    df=tempdf[all_group[i]] #해당하는 목장 정보 불러오기
    # print(df)
    df.set_index('날짜\이름',inplace=True)
    namelist = df.columns


    if attendance_dict[all_group[i]] !=[] and all_group[i]!='새신자': # 출석 공란이 아닌경우 (정상적인경우) and 새신자가 아니면


        diff1= list(set(attendance_dict[all_group[i]]) -set(namelist)  ) # check(출석인원중) 명부인원을 빼면 누락된 사람 찾아내기 가능
        if diff1 !=[]: #빈칸이면 pass
            print('누락존재 목장',all_group[i], diff1)


    elif all_group[i] == '새신자': #새신자라면, 비출석이 불출석이 아님.

        diff1= list(set(attendance_dict[all_group[i]]+(attendance_dict['불출석'])) -set(namelist))
        # 오늘 출석 정보에 있는 명단에서 check(출석인원중)을 빼면 누락된 사람 찾아내기 가능
        if diff1 !=[]: # 빈 리스트가 아니라면 누락존재
            print('새신자 이름 누락',all_group[i], diff1)

print()
print()

#비고칸에 채울 결석 관련 정보를 딕셔너리 형태로 저장
nocome_dict = making.read_nocome_from_file('nocome.txt')
# 잘 저장되었는지 출력
print("nocome_dict", nocome_dict)

input('누락명단이 정상이면 넘어가기 input')
