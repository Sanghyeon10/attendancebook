import pandas as pd


all_group=['4-1','4-2','4-3','4-4','4-5','5-1','5-2','5-3','5-4','6-1','6-2','6-3','6-4']
tempdf = pd.read_excel(r'C:\Users\A\Downloads\2023 초등부 출석표.xlsx', sheet_name=None)

a=[]
b=[]
temp=[]


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
    print(all_group[i],temp) #애들 한글 명단 다시 만들때 활용할 코드부분.
    temp=[]
    a=[]
    b=[]

    df.to_excel("{}.xlsx".format(all_group[i]))

# input('목장별로만?')
print("")
for i in all_group:
    print(i)

