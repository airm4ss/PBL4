import pandas as pd

# 엑셀 파일 경로 설정
file_path = '/Users/mingidan/Downloads/1차병원 개인정보 처리방침.xlsx'  # 실제 엑셀 파일 경로로 변경

# 엑셀 파일 로드
df = pd.read_excel(file_path)

# 열 이름 확인
print(df.columns)