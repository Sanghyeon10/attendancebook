import pandas as pd
import making


all_group = making.all_group()
tempdf = pd.read_excel(r'C:\Users\User\Downloads\2023 초등부 출석표.xlsx', sheet_name=None)

printing= 'yes'#input('명단 프린트할꺼라면 yes라고 치기')

a=[]
b=[]
temp=[]


filtered_data=[] #먼저 빈리스트 정의하기
for i in range(len(all_group)): #인덱스가 같은지 보기 (요류 방지용)
    df = tempdf[all_group[i]]
    df.set_index('날짜\이름', inplace=True)

    namelist = df.columns
    # print(all_group[i], namelist.tolist()) #정렬하기 않고 기존꺼 포현할때 쓰는것

    #프린트 명부에서 제거해야할 명단
    file_name = "class_data.txt"
    loaded_data = making.load_dict_from_file(file_name)

    for j in namelist:  # 기존 엑셀시트에 있는 이름중
        if df[j][(df[j] == 'O') | (df[j] == 'X')].count() >5: # X든 O든 총개수가 5를 넘어야
            a.append( (j,float(df.loc[df.index[-1], j])) )
            # print(all_group[i],j,df.loc[df.index[-1], j])
        else:
            b.append( (j,float(df.loc[df.index[-1], j])) )


    a.sort(key=lambda x: x[1], reverse=True)   #전부 정보획득했으면 정렬하기
    b.sort(key=lambda x: x[1], reverse=True) #(이름, 출석율)의 정보 리스트, a는 출석개수가 많은것 b는적은것
    a= a+b #출석 정보가 작은 애들은 뒤로 빼준 것임.
    a.remove(('기타',0)) #기타는 첫번째로 넣어야되서 일단 삭제
    filtered_data = filtered_data+ [all_group[i]]+ [item for item in a if int(item[1]) < 10 and item not in loaded_data[all_group[i]] ]
    #출석율이 특정숫자보다 낮고 제거명부에 없는 애들은 명부 프린트에서 제거해줄지 검토해야함
    #목장이름+ 리스트형태로 명부 만들어서 마지막에 프린트해줌.

    #칼럼에 넣을 리스트 만들기
    for l in range(len(a)):
        temp.append(a[l][0]) #출석율 높은 순서대로 넣는것임.

    # print(temp)

    temp.insert(0,'기타') #기타 첫번째로 다시 넣어주기
    df=df.loc[:,temp]
    # df=df[[temp]]


    if all_group[i] in loaded_data.keys():# 명단에서 제외해야할 명단이 있다면
        temp = making.gettruelist(temp, loaded_data[all_group[i]]) # 순서에서 제외해서 저장하기


    # print(all_group[i],temp) #애들 한글 명단 다시 만들때 활용할 코드부분. 한줄로 출력할때 사용
    if printing == 'yes': #프린트 하는게 맞으면
        making.make_5line(all_group[i],temp) #5명씩 잘라서 표현할때



    temp=[]
    a=[]
    b=[]

    if all_group[i] != '새신자':
        # df.to_excel("{}.xlsx".format(all_group[i]))
        pass # 정렬화한 후 엑셀출력이 필요가 없어서 주석처리해놓음.
    else: #새신자이면
        print("")
        print("이름:")
        print("전도자(목장):")
        print("인적사항:")
        print("주소 생년월일 학교명 가족관계 핸드폰번호")


if printing =='yes':
    print("")
    for m in all_group:
        print(m)
    print('불출석')
    print('등반자')

print("")
print("")
print(filtered_data)