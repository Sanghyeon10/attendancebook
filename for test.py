import pandas as pd
import datetime
import making
import re


# df = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드 도감"), sheet_name=None)['시트1']
# df= df[["NO1","NO2","Pal"]]
#
# # 데이터프레임이 df라고 가정합니다.
# # df['NO1'] = df['NO1'].str.extract(r'\d+\.\s\d+:\s(.+)$')
# df['NO1'] = df['NO1'].str.split(':').str[1].str.strip()
#
# # 수정된 데이터프레임 출력
# print(df)
#
# df.to_excel("Palworld.xlsx", sheet_name="시트1", engine='openpyxl')
a="""
dfpal = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "Palworld"), sheet_name=None)['시트1'].astype(str)
df1= pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드1"), sheet_name=None)['시트1'].astype(str)
df2= pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드2"), sheet_name=None)['시트1'].astype(str)

print(df1)
print(df2)
print(dfpal)

speed_mapping = {'Excellent': 'S', 'Fast': 'A', 'Good': 'B', 'Okay': 'C', 'Slow': 'D'}
df2['이동속도'] = df2['이동속도'].map(speed_mapping)


for i in range(len(df2)): #df2가 구하는것
    for j in range(len(dfpal)):
        if df2.loc[df2.index[i],"팰이름"]== dfpal.loc[dfpal.index[j],'NO1']:
            df2.loc[df2.index[i],"도감번호"]= str(dfpal.loc[dfpal.index[j],'NO2'])



for i in range(len(df2)): #df2가 구하는것
    for j in range(len(df1)):#인장재료와 이동속도 붙히기
        if df2.loc[df2.index[i],"팰이름"]== df1.loc[df1.index[j],'팰 이름']:
            df2.loc[df2.index[i], "인장재료"]= df1.loc[df1.index[j],'안장 재료']
            df2.loc[df2.index[i], "이동속도"]=  str(df2.loc[df2.index[i], "이동속도"])+"("+str(df1.loc[df1.index[j],'이동 속도'])+")"


df2['해금레벨']=df2['해금레벨'].astype(int)
df2 = df2.sort_values(by='해금레벨', ascending=True)
df2['인장재료'] = df2['인장재료'].str.replace(r'\n', ', ', regex=True).str.strip()


print(df2)
df2.to_excel(r'{}{}.xlsx'.format(making.addressgibon, "업로드용"), sheet_name="시트1", engine='openpyxl')
"""

# dfpal = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "Palworld"), sheet_name=None)['시트1'].astype(str)
# df1= pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드1"), sheet_name=None)['시트1'].astype(str)
# df3= pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드3"), sheet_name=None)['시트1'].astype(str)
#
#
#
# for i in range(len(df3)): #df2가 구하는것
#     for j in range(len(dfpal)):
#         if df3.loc[df3.index[i],"Pal"]== dfpal.loc[dfpal.index[j],'Pal']:
#             df3.loc[df3.index[i], "팰이름"] = str(dfpal.loc[dfpal.index[j], 'NO1'])
#             df3.loc[df3.index[i],"도감번호"]= str(dfpal.loc[dfpal.index[j],'NO2'])
#
#
#
# speed_mapping = {'Excellent': 'S', 'Fast': 'A', 'Good': 'B', 'Okay': 'C', 'Slow': 'D'}
# df3['Ride Tier'] = df3['Ride Tier'].map(speed_mapping)
# df3['Partner Skill / Pal Gear'] = df3['Partner Skill / Pal Gear'].replace(to_replace='[^0-9]', value='', regex=True)
#
# for i in range(len(df3)): #df2가 구하는것
#     for j in range(len(df1)):#인장재료와 이동속도 붙히기
#         if df3.loc[df3.index[i],"팰이름"]== df1.loc[df1.index[j],'팰 이름']:
#             df3.loc[df3.index[i], "인장재료"]= df1.loc[df1.index[j],'안장 재료']
#             df3.loc[df3.index[i], "Ride Tier"]=  str(df3.loc[df3.index[i], "Ride Tier"])+"("+str(df1.loc[df1.index[j],'이동 속도'])+")"
#
#
# df3 = df3.drop('Pal', axis=1)
#
# df3=df3[['도감번호','팰이름', 'Partner Skill / Pal Gear', 'Ride Tier',   '인장재료']]
#
# df3['Partner Skill / Pal Gear']=df3['Partner Skill / Pal Gear'].astype(int)
# df3 = df3.sort_values(by='Partner Skill / Pal Gear', ascending=True)
# df3['인장재료'] = df3['인장재료'].str.replace(r'\n', ', ', regex=True).str.strip()
#
#
#
# df3.to_excel(r'{}{}.xlsx'.format(making.addressgibon, "업로드용"), sheet_name="시트1", engine='openpyxl')
#
# # print(df1)
# print(df3)
# # print(dfpal)


dfpal = pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "Palworld"), sheet_name=None)['시트1'].astype(str)
df1= pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드1"), sheet_name=None)['시트1'].astype(str)
df3= pd.read_excel(r'{}{}.xlsx'.format(making.addressgibon, "팰월드3"), sheet_name=None)['시트1'].astype(str)

print(df3)