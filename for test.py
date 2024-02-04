input_file_path = "full name list.txt"
output_file_path = "full name list.txt"

with open(input_file_path, 'r', encoding='utf-8') as input_file:
    lines = input_file.readlines()

filtered_lines = [line.strip() for line in lines if line.strip() != ""]

with open(output_file_path, 'w', encoding='utf-8') as output_file:
    output_file.write('\n'.join(filtered_lines))

print("텍스트 파일에서 \\n을 제거하여", output_file_path, "에 저장되었습니다.")
