import pandas as pd
import making


all_group = making.all_group()
tempdf = pd.read_excel(r'C:\Users\User\Downloads\2023 초등부 출석표.xlsx', sheet_name=None)

printing= 'yes'#input('명단 프린트할꺼라면 yes라고 치기')

a=[]
b=[]
temp=[]

def make_5line(groupname,my_list):
    print(groupname, end=' ')
    for i, x in enumerate(my_list):
        if i % 5 == 0 and i != 0:
            print()
        elif i >= 5 and i % 10 == 5:
            print()
        else:
            pass


        if i == len(my_list)-1: #마지막
            print(x)
        else: #평상시
            print(x, end=' ')

    return False


for i in range(len(all_group)): #인덱스가 같은지 보기 (요류 방지용)
    df = tempdf[all_group[i]]
    df.set_index('날짜\이름', inplace=True)

    namelist = df.columns
    # print(all_group[i], namelist.tolist()) #정렬하기 않고 기존꺼 포현할때 쓰는것

    for j in namelist:  # 기존 엑셀시트에 있는 이름중
        if df[j][(df[j] == 'O') | (df[j] == 'X')].count() >5: # X든 O든 총개수가 5를 넘어야
            a.append( (j,float(df.loc[df.index[-1], j])) )
            # print(all_group[i],j,df.loc[df.index[-1], j])
        else:
            b.append( (j,float(df.loc[df.index[-1], j])) )


    a.sort(key=lambda x: x[1], reverse=True)   #전부 정보획득했으면 정렬하기
    b.sort(key=lambda x: x[1], reverse=True)
    a= a+b #출석 정보가 작은 애들은 뒤로 빼준 것임.
    a.remove(('기타',0)) #기타는 첫번째로 넣어야되서 일단 삭제

    #칼럼에 넣을 리스트 만들기
    for l in range(len(a)):
        temp.append(a[l][0]) #출석율 높은 순서대로 넣는것임.

    # print(temp)

    temp.insert(0,'기타') #기타 첫번째로 다시 넣어주기
    df=df.loc[:,temp]
    # df=df[[temp]]


    if all_group[i]=='6-4': #안쓰이는 이름은 제거하기
        temp= making.gettruelist(temp,["김현아", "정현영","이가영","조서현","신재은","유하은","서예린"])
        # print(temp)
    # print(all_group[i],temp) #애들 한글 명단 다시 만들때 활용할 코드부분. 한줄로 출력할때 사용
    if printing == 'yes': #프린트 하는게 맞으면


        make_5line(all_group[i],temp) #5명씩 잘라서 표현할때



    temp=[]
    a=[]
    b=[]

    if all_group[i] != '새신자':
        df.to_excel("{}.xlsx".format(all_group[i]))
if printing =='yes':
    print("")
    for m in all_group:
        print(m)
    print('불출석')
    print('등반자')
