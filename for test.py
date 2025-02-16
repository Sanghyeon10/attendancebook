import pandas as pd
import making

# pd.set_option('display.max_rows', None)  # 모든 행 출력
# pd.set_option('display.max_columns', None)  # 모든 열 출력
# pd.set_option('display.width', 1000)  # 한 줄에 출력할 수 있는 최대 너비
#
#
# df = pd.read_excel(making.addressgibon+"책 리스트.xlsx", sheet_name='시트1' , index_col=0)
# df = df[~df.index.isna()]
# # df = pd.concat([df_top, pd.DataFrame([new_row], columns=df.columns), df_bottom]).reset_index(drop=True)
#
# df.to_excel("책 리스트"+".xlsx")
# print(df)
# print(len(df))

import os
import filecmp


def compare_folders(folder1, folder2):
    dcmp = filecmp.dircmp(folder1, folder2)

    if dcmp.left_only:
        print("파일이 옜것에만 있음:", dcmp.left_only)
    if dcmp.right_only:
        print("파일이 오늘것에만 있음:", dcmp.right_only)
    if dcmp.diff_files:
        print("내용이 다른 파일:", dcmp.diff_files)
    if dcmp.common_files:
        for file in dcmp.common_files:
            path1 = os.path.join(folder1, file)
            path2 = os.path.join(folder2, file)
            if file.endswith(".txt") and not filecmp.cmp(path1, path2, shallow=False):
                print(f"텍스트 파일 {file}의 내용이 다름")

    for sub_dcmp in dcmp.subdirs.values():
        compare_folders(os.path.join(folder1, sub_dcmp.left), os.path.join(folder2, sub_dcmp.right))


# 사용 예제
folder1 = r"C:\Users\captu\Desktop\old diary"
folder2 = r"C:\Users\captu\Desktop\diary"
compare_folders(folder1, folder2)
