import pandas as pd

df = pd.read_excel(r'C:\Users\User\Downloads\{}.xlsx'.format('엔비디아'), sheet_name=None)
df=df['시트1']
df.set_index("Breakdown", inplace=True)
selected_index=["총매출","매출원가","매출총이익","판매관리비 총계","연구개발비","영업이익","세전 당기 순이익"]
df = df.loc[df.index.isin(selected_index)]
df = df.drop('Unnamed: 1', axis=1, errors='ignore')
# print(df)

df_change = df.pct_change(axis=1, periods=-1)*100
df_change= df_change.dropna(axis=1)
print(df_change)