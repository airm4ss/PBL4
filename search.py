import os
import django
import pandas as pd

# Django 환경 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # 실제 프로젝트 이름으로 변경
django.setup()

from search.models import Hospital  # search 앱의 Hospital 모델 import

# 엑셀 파일 로드
file_path = '/Users/mingidan/Downloads/1차병원 개인정보 처리방침.xlsx'
df = pd.read_excel(file_path)

# 데이터프레임을 행으로 변환 (전치)
df = df.transpose()

# 열 이름을 첫 번째 행으로 설정
df.columns = df.iloc[0]
df = df[1:]  # 첫 번째 행은 컬럼명이 되었으므로 제외

# 각 열을 병원 정보로 저장
for index, row in df.iterrows():
    Hospital.objects.create(
        name=index,  # 열 이름이 병원 이름으로 사용됨
        address=row.get('주소', ''),
        homepage_url=row.get('처리 방침 URL', ''),
        has_homepage=row.get('홈페이지 유무', 'X'),
        has_policy=row.get('처리방침 유무', 'X'),
        policy_name_use=row.get("'개인정보 처리방침'이라는 명칭 사용", 'X'),
        processing_purpose=row.get('2. 개인정보의 처리 목적', 'X'),
        processed_items=row.get('3. 처리하는 개인정보의 항목', 'X'),
        retention_period=row.get('5. 개인정보의 처리 및 보유기간', 'X'),
        third_party_provision=row.get('7. 개인정보의 제3자 제공에 관한 사항', 'X'),
        consignment=row.get('9. 개인정보 처리업무의 위탁에 관한 사항', 'X'),
        video_processing=row.get('20. 고정형 영상정보처리기기 운영・관리에 관한 사항', 'X'),
        responsible_person=row.get('17. 개인정보책임자 or 부서', 'X'),
        consent_and_legal_basis=row.get("3.1 '동의/비동의' 구분 & 법적 근거 (ox로만)", 'X'),
        destruction_procedure=row.get('6. 개인정보의 파기 절차 및 방법에 관한 사항', 'X'),
        safety_measures=row.get('11. 개인정보의 안전성 확보조치에 관한 사항', 'X'),
        auto_collection_device=row.get('14. 개인정보 자동 수집 장치의 설치・운영 및 거부에 관한 사항', 'X'),
        subject_rights=row.get('16. 정보주체와 법정대리인의 권리・의무 및 행사방법에 관한 사항', 'X'),
        relief_methods=row.get('19. 정보주체의 권익침해에 대한 구제방법', 'X'),
        policy_changes=row.get('23. 개인정보 처리방침의 변경에 관한 사항', 'X')
    )

print("데이터베이스에 데이터가 성공적으로 저장되었습니다.")
