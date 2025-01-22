import pandas as pd
import making

pd.set_option('display.max_rows', None)  # 모든 행 출력
pd.set_option('display.max_columns', None)  # 모든 열 출력
pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비


df = pd.read_excel(making.addressgibon+"책 리스트.xlsx", sheet_name='시트1' , index_col=0)
df = df[~df.index.isna()]
# df = pd.concat([df_top, pd.DataFrame([new_row], columns=df.columns), df_bottom]).reset_index(drop=True)

df.to_excel("책 리스트"+".xlsx")
print(df)
print(len(df))
