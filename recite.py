import pandas as pd
import making
import re
from collections import Counter
import datetime
import  openpyxl  as  op
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import time
from collections import Counter

text = making.year + "성경암송 명단"
text = "2026 "+ "성경암송 명단"

scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/dirve'
]
creds = ServiceAccountCredentials.from_json_keyfile_name(making.addrresOfjsonfile)
# 위json파일 주소는 위치바뀌면 수정해줄것.
file = gspread.authorize(creds)
sh = file.open(text)
sheet = sh.worksheet('시트1')
values_list = sheet.col_values(2)[1:]
# print(values_list)


# 2️⃣ 구분자로 분리 (공백 | , | . | / | :)
split_names = [
    re.split(r"\s|,|\.|/|:", x)
    for x in values_list
]

print(split_names)
# 3️⃣ 1차원 리스트로 평탄화 + 공백 제거 + 반 번호 제거
all_names = [
    name.strip()
    for sublist in split_names
    for name in sublist
    if name.strip() != ""
    and not re.fullmatch(r"\d+-\d+", name.strip())  # 4-1, 4-2 제거
]


# 4️⃣ 빈도 계산
name_count = Counter(all_names)

# print(name_count.items())
# 5️⃣ DataFrame으로 변환
result = pd.DataFrame(
    name_count.items(),
    columns=["암송자", "횟수"]
).sort_values("횟수", ascending=False)

# print(result)
result_str = "\n".join(
    f"{row['암송자']}: {row['횟수']}"
    for _, row in result.iterrows()
)

# print(result_str)

sheet.update_acell('C2', result_str)
