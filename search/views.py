from django.shortcuts import render, get_object_or_404
from .models import Hospital
from .forms import HospitalSearchForm

def search_hospital(request):
    form = HospitalSearchForm(request.GET or None)
    results = None

    if form.is_valid() and form.cleaned_data['name']:
        name = form.cleaned_data['name']
        results = Hospital.objects.filter(name__icontains=name)

    return render(request, 'search/search_results.html', {'form': form, 'results': results})

def hospital_detail(request, id):
    hospital = get_object_or_404(Hospital, id=id)

    # 벌금 및 위반 항목 추적
    max_fine = 0
    violations = []
    violation_details = []

    # 벌금 범위
    fine_categories = {
        200: [],
        600: []
    }

    # 'o', 'f', 'x' 개수 세기
    fields_to_check = [
        hospital.has_policy,
        hospital.processing_purpose,
        hospital.processed_items,
        hospital.retention_period,
        hospital.destruction_procedure,
        hospital.third_party_provision,
        hospital.consignment,
        hospital.auto_collection_device,
        hospital.subject_rights,
        hospital.responsible_person,
        hospital.video_processing,
        hospital.policy_changes,
        hospital.consent_and_legal_basis,
    ]

    o_count = sum(1 for field in fields_to_check if field.lower() == 'o')
    f_count = sum(1 for field in fields_to_check if field.lower() == 'f')
    x_count = sum(1 for field in fields_to_check if field.lower() == 'x')

    # 필수 기재 항목
    required_fields = [
        'processing_purpose',           # 개인정보처리목적
        'processed_items',              # 처리하는 개인정보의 항목
        'consent_and_legal_basis',      # 동의/비동의 구분 및 법적근거 기재
        'retention_period',             # 개인정보 처리 및 보유기간
        'destruction_procedure',        # 개인정보파기사항
        'security_measures',            # 개인정보안전성확보조치사항
        'subject_rights',               # 정보주체의 권리 의무 및 행사 방법 사항
        'responsible_person',           # 개인정보보호책임자사항
        'remedies_for_infringement',    # 정보주체권익침해구제방법
        'policy_changes'                # 개인정보처리방침변경사항
    ]

    # 해당시 기재사항
    optional_fields = [
        'third_party_provision',        # 개인정보 제3자 제공사항
        'consignment',                  # 개인정보위탁사항
        'pseudonym_processing',         # 가명정보 처리에 관한 사항
        'auto_collection_device',       # 개인정보 자동 수집 장치 사항
        'video_processing'              # 고정형 영상정보처리기 운영 사항
    ]

    # 필수 항목 중 작성되지 않은 항목 (x의 개수)
    missing_required_count = sum(
        1 for field in required_fields if getattr(hospital, field, '').lower() == 'x'
    )

    # 해당시 기재사항 중 작성되지 않은 항목 (x 또는 nan의 개수)
    missing_optional_count = sum(
        1 for field in optional_fields if getattr(hospital, field, '').lower() in ['x', 'nan']
    )

    # 처리방침 유무가 'f' 또는 'x'일 경우 벌금 (200만원)
    if hospital.has_policy in ['x', 'f']:
        fine_categories[200].append('처리방침 유무')
        violation_details.append(('처리방침 유무', hospital.has_policy, [
            "- 제30조 제1항 제1호",
            "- 법 제75조제4항제3호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]))

    # 파기 절차 및 방법이 'f' 또는 'x'일 경우 벌금 (600만원)
    if hospital.destruction_procedure in ['x', 'f']:
        fine_categories[600].append('파기 절차 및 방법')
        violation_details.append(('파기 절차 및 방법', hospital.destruction_procedure, [
            "- 법 제21조제1항",
            "- 법 제75조 제2항 제4호",
            "- 1회 위반: 600, 2회 위반: 1200, 3회 위반: 2400"
        ]))

    # 기타 200만원 벌금 항목들
    violation_fields = [
        ('processing_purpose', '개인정보의 처리 목적', [
            "- 제30조 제1항 제1호",
            "- 법 제75조제4항제3호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('processed_items', '처리하는 개인정보의 항목', [
            "- 제22조(동의를 받는 방법)",
            "- 법 제75조제4항제3호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('retention_period', '개인정보의 처리 및 보유기간', [
            "- 제30조 제1항 제2호",
            "- 법 제75조제4항제8호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('third_party_provision', '개인정보의 제3자 제공', [
            "- 제30조 제1항 제3호",
            "- 법 제75조제4항제8호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('consignment', '개인정보 처리업무의 위탁', [
            "- 제30조 제1항 제4호",
            "- 법 제75조제4항제8호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('auto_collection_device', '개인정보 자동 수집 장치의 설치・운영 및 거부', [
            "- 제30조 제1항 7호",
            "- 법 제75조제4항제8호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('subject_rights', '정보주체와 법정대리인의 권리・의무 및 행사방법', [
            "- 제38조(권리행사의 방법 및 절차), 제30조 제1항 제5호",
            "- 법 제75조제4항제8호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('responsible_person', '개인정보 책임자 or 부서', [
            "- 제31조(개인정보 보호책임자의 지정 등), 제30조 제1항 제6호",
            "- 법 제75조제4항제9호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('video_processing', '고정형 영상정보처리기기 운영・관리', [
            "- 제25조(고정형 영상정보처리기기의 설치ㆍ운영 제한) 제7항"
        ]),
        ('policy_changes', '개인정보 처리방침의 변경', [
            "- 제30조(개인정보 처리방침의 수립 및 공개) 2항",
            "- 법 제75조제4항제8호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ]),
        ('consent_and_legal_basis', '동의/비동의 구분 & 법적 근거', [
            "- 법 제22조제1항부터 제3항까지(법 제26조제8항에 따라 준용되는 경우를 포함한다)를 위반하여 동의를 받은 경우",
            "- 법 제75조제4항제3호",
            "- 1회 위반: 200, 2회 위반: 400, 3회 위반: 800"
        ])
    ]

    for field, label, law_info in violation_fields:
        if getattr(hospital, field) in ['x', 'f']:
            fine_categories[200].append(label)
            violation_details.append((label, getattr(hospital, field), law_info))

    # 가장 높은 벌금 설정
    if fine_categories[600]:
        max_fine = 600
        violations = fine_categories[600]
    elif fine_categories[200]:
        max_fine = 200
        violations = fine_categories[200]

    # 벌금 문구
    fine_text = f"{max_fine}만원" if max_fine > 0 else '-'

    context = {
        'hospital': hospital,
        'fine_text': fine_text,
        'violations': violations,
        'violation_details': violation_details,  # 항목에 따른 법 조항 정보
        'o_count': o_count,
        'f_count': f_count,
        'x_count': x_count,
        'missing_required_count': missing_required_count,
        'missing_optional_count': missing_optional_count,
    }

    return render(request, 'search/hospital_detail.html', context)

