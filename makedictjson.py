import json
import making


all_group=making.all_group()

file_name = "class_data.txt"
loaded_data = making.load_dict_from_file(file_name)
print(loaded_data)

#목장별로 돌면서 키 추가해주기.
for i in range(len(all_group)):
    if all_group[i] not in loaded_data.keys():
        loaded_data[all_group[i]] = []

#저장
making.save_dict_to_file(loaded_data, file_name)
print(loaded_data)



# 불러온 데이터를 정렬
sorted_data = dict(sorted(loaded_data.items() ,key=lambda x: (x[0] != "새신자", x[0])))
#새신자를 제일 먼저 앞으로 뺌.
print(sorted_data)
# 정렬된 데이터를 JSON 파일로 저장
making.save_dict_to_file(sorted_data, file_name)

print("정렬된 데이터가 파일에 저장되었습니다.")

