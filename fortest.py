import json

def save_dict_to_file(data, file_name):
    with open(file_name, 'w') as file:
        json.dump(data, file)

def load_dict_from_file(file_name):
    with open(file_name, 'r') as file:
        loaded_data = json.load(file)
    return loaded_data

# 예시 딕셔너리
data = {
    "6-4": ["김현아", "정현영", "이가영", "조서현", "신재은", "유하은", "서예린"],
    "5-1": ["김동혁", "김해진", "서시우", "고연우"],
    "6-1": ["김건우(1)"],
    "새신자": ["김아정",	"설민주"	,"설우진"]
}


# file_name = "class_data.txt"
# save_dict_to_file(data, file_name)


file_name = "class_data.txt"
loaded_data = load_dict_from_file(file_name)
print(loaded_data)