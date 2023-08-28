import json
import making

data = {
    "4-1": [
        "송지율"
    ],
    "4-2": [],
    "4-3": [],
    "4-4": [
        "박서윤"
    ]
}

# 딕셔너리의 리스트 값을 한 줄로 조정하여 저장
for key, value in data.items():
    data[key] = ", ".join(value)

# 조정된 데이터를 JSON 파일로 저장
making.save_dict_to_file(data,"adjusted_data.txt")

print("조정된 데이터가 파일에 저장되었습니다.")
