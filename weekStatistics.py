import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager
import making

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 원하는 한글 폰트 파일 경로로 변경
font_prop = font_manager.FontProperties(fname=font_path)
plt.rcParams["font.family"] = font_prop.get_name()



# 데이터프레임 생성
all_group= making.all_group()
accumulatedDF=pd.DataFrame( index=making.index())

for i in range(len(all_group)):
    if all_group[i] != '새신자': #새신자는 출석 중복카운팅이 되어버려서 제외해야함.
        df = pd.read_excel(r'{}.xlsx'.format(all_group[i]))  # 해당파일찾고 데이터 옮겨오기
        df.set_index('날짜\이름',inplace=True)
        df.drop(columns=['기타'], inplace=True)
        df = df.fillna('')
        accumulatedDF = pd.merge(accumulatedDF, df, left_index=True, right_index=True, how='outer')

    else: #새신자인경우
        df = pd.read_excel(r'{}.xlsx'.format(all_group[i]))  # 해당파일찾고 데이터 옮겨오기
        df.set_index('날짜\이름',inplace=True)
        df.drop(columns=['기타'], inplace=True)
        df = df.fillna('')
        havetoaddlist=list(set(df.columns)-set(accumulatedDF.columns))
        accumulatedDF.update(df,overwrite=True, filter_func=lambda x: x=="X") #목장에 X인경우 새신자에서 정보를 가져와서 확인할 필요가 있음.
        accumulatedDF=accumulatedDF.join(df[havetoaddlist],how='left')#덮어씌울게 없으면 따로 추가해주기.
        print(accumulatedDF)

accumulatedDF['O의 개수'] = accumulatedDF.apply(making.count_os, axis=1)
accumulatedDF=accumulatedDF.iloc[:-1,:] #비고는 필요없음
# accumulatedDF.index = accumulatedDF.index.apply(lambda x: x[-5:])
accumulatedDF.index = range(1,len(accumulatedDF)+1)
# print(accumulatedDF)
# print(accumulatedDF['O의 개수'])

# 주차별 출석 합계 계산
weekly_attendance = accumulatedDF['O의 개수']





# 출석 추이 시각화
weekly_attendance.plot(kind='bar')
plt.xlabel('몇주차')
plt.ylabel('출석수(기타칸 제외)')
plt.title('주별 출석인원수')
# plt.ylim([30,85])
plt.grid(True, axis='y')
plt.savefig('savefig_200dpi.png', dpi=200, facecolor='#eeeeee', edgecolor='blue', bbox_inches='tight')
plt.show()