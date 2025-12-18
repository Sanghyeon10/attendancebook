import pandas as pd
import making

# # 파일 불러오기
# df = pd.read_excel(making.addressgibon+"뒤집기.xlsx",index_col= '날짜\이름')
# print(df)
# # 전치 (행과 열 바꾸기)
# df_transposed = df.T
# print(df_transposed)
# # df_transposed["등록날짜"]=df_transposed["등록날짜"].strftime("%Y-%m-%d")
# # df_transposed["등반날짜"]=df_transposed["등반날짜"].strftime("%Y-%m-%d")
#
# # 새로운 파일로 저장
# df_transposed.to_excel("뒤집기.xlsx", index=True)

import pandas as pd
import re
from collections import Counter

# 예시 데이터
df = pd.DataFrame({
    "암송자": [
        "김철수, 이영희 / 박민수",
        "이영희.김철수",
        "박민수 / 김철수",
        None
    ]
})



# 1️⃣ 암송자 컬럼에서 문자열만 가져오기
names_series = df["암송자"].dropna()

# 2️⃣ 구분자로 분리 (. , /)
split_names = names_series.apply(
    lambda x: re.split(r"[.,/]", x)
)

# 3️⃣ 1차원 리스트로 평탄화 + 공백 제거
all_names = [
    name.strip()
    for sublist in split_names
    for name in sublist
    if name.strip() != ""
]

# 4️⃣ 빈도 계산
name_count = Counter(all_names)

print(name_count.items())
# 5️⃣ DataFrame으로 변환
result = pd.DataFrame(
    name_count.items(),
    columns=["암송자", "횟수"]
).sort_values("횟수", ascending=False)

print(result)
result_str = "\n".join(
    f"{row['암송자']}: {row['횟수']}"
    for _, row in result.iterrows()
)

print(result_str)