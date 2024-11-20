from django.shortcuts import render
from .forms import PrivacyPolicyForm

def gen_have_home(request):
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)
        if form.is_valid():
            # 폼 데이터를 가져옴
            form_data = form.cleaned_data

            # 저장할 개인정보 항목 리스트
            privacy_policies = []

            # '회원가입' 체크박스가 체크되었는지 확인
            if '회원가입' in form_data.get('website_functions', []):
                membership_data = {
                    'title': '회원 서비스 운영',
                    'legal_basis': '개인정보 보호법 제15조 제1항 제4호 (계약의 이행)',
                    'purpose': '회원 가입의사 확인, 회원제 서비스 제공에 따른 본인 식별・인증, 회원자격 유지・관리, 서비스 부정이용 방지',
                    'info': 'ID, 비밀번호, 성명, 생년월일, 주소, 휴대전화번호, 이메일 주소',
                    'retention': '회원 탈퇴 시까지',
                }
                privacy_policies.append(membership_data)

            # '주문 및 결제 처리' 체크박스가 체크되었는지 확인
            if '주문처리' in form_data.get('website_functions', []):
                order_data = {
                    'title': '주문 및 결제 처리',
                    'legal_basis': '개인정보 보호법 제15조 제1항 제4호 (계약의 이행)',
                    'purpose': '주문 처리 및 결제 관리',
                    'info': 'ID, 주문내역, 결제정보',
                    'retention': '5년 (전자상거래법 제6조)',
                }
                privacy_policies.append(order_data)

            # '상품 배송' 체크박스가 체크되었는지 확인
            if '배송' in form_data.get('website_functions', []):
                delivery_data = {
                    'title': '상품 배송',
                    'legal_basis': '개인정보 보호법 제15조 제1항 제4호 (계약의 이행)',
                    'purpose': '물품 배송, 반품 처리',
                    'info': '성명, 휴대전화번호, 주소, 결제번호',
                    'retention': '물품 배송 및 재화 공급 완료시까지',
                }
                privacy_policies.append(delivery_data)

            # 추가된 부분: '이벤트', '마케팅', '건의함' 항목 처리
            consent_info = []

            # '이벤트 참여 및 경품 응모 행사' 체크박스가 체크되었는지 확인
            if '이벤트' in form_data.get('website_functions', []):
                consent_info.append({
                    'purpose': '이벤트 참여 및 경품 응모',
                    'info': '성명, 주소, 휴대전화번호, 이메일 주소',
                    'retention': '이벤트 종료 시 즉시 파기',
                    'remarks': ''
                })

            # '마케팅 및 광고' 체크박스가 체크되었는지 확인
            if '마케팅' in form_data.get('website_functions', []):
                consent_info.append({
                    'purpose': '마케팅, 광고에 활용',
                    'info': '성명, 휴대전화번호',
                    'retention': '6개월',
                    'remarks': ''
                })

            # '고객 건의함' 체크박스가 체크되었는지 확인
            if '건의함' in form_data.get('website_functions', []):
                consent_info.append({
                    'purpose': '고객 건의함 운영',
                    'info': '성명, 이메일, 휴대전화번호',
                    'retention': '정보주체 요청 시 파기',
                    'remarks': ''
                })

            # form_data에 privacy_policies와 consent_info 추가
            form_data['privacy_policies'] = privacy_policies
            form_data['consent_info'] = consent_info

            # 주차장 내 CCTV 설치 여부 처리
            form_data['cctv_installed'] = form_data.get('cctv_installed', False)

             # 제3자 제공 데이터 처리
            third_party_provision = request.POST.get('third_party_provision')

            third_party_data = []
            if third_party_provision == '예':
                recipients = request.POST.getlist('recipient[]')
                purposes = request.POST.getlist('purpose[]')
                items = request.POST.getlist('items[]')
                legal_bases = request.POST.getlist('legal_basis[]')

                for i in range(len(recipients)):
                    third_party_data.append({
                        'recipient': recipients[i],
                        'purpose': purposes[i],
                        'items': items[i],
                        'legal_basis': legal_bases[i],
                    })
            
            form_data['third_party_data'] = third_party_data

            # 위탁 데이터 수집
            outsourcing_provision = form_data.get('data_outsourcing')
            outsourcing_data = []

            if outsourcing_provision == '위탁하고 있음':
                companies = request.POST.getlist('outsourced_company[]')
                purposes = request.POST.getlist('outsourced_purpose[]')

                for company, purpose in zip(companies, purposes):
                    if company and purpose:
                        outsourcing_data.append({
                            'company': company,
                            'purpose': purpose,
                        })

            form_data['outsourcing_provision'] = outsourcing_provision
            form_data['outsourcing_data'] = outsourcing_data

            # 고정형 영상정보처리기기 관련 데이터 처리
            form_data['installation_count'] = request.POST.get('installation_count')
            form_data['installation_location'] = request.POST.get('installation_location')
            form_data['shooting_range'] = request.POST.get('shooting_range')
            form_data['manager_name'] = request.POST.get('manager_name')
            form_data['manager_phone'] = request.POST.get('manager_phone')
            form_data['recording_time'] = request.POST.get('recording_time')
            form_data['retention_period'] = request.POST.get('retention_period')
            form_data['storage_location'] = request.POST.get('storage_location')
            form_data['contractor'] = request.POST.get('contractor')
            form_data['contractor_contact'] = request.POST.get('contractor_contact')
            form_data['contractor_phone'] = request.POST.get('contractor_phone')


            # 개인정보 처리방침 링크 리스트 처리
            privacy_links = request.POST.getlist('privacy_link[]')
            # 공백을 제거한 유효한 링크만 필터링 및 http 추가
            valid_links = []
            for link in privacy_links:
                clean_link = link.strip()
                if clean_link:
                    if not (clean_link.startswith('http://') or clean_link.startswith('https://')):
                        clean_link = 'http://' + clean_link
                    valid_links.append(clean_link)

            form_data['privacy_links'] = valid_links

            return render(request, 'generatorHave/genHave_mid.html', {'form_data': form_data})
    else:
        form = PrivacyPolicyForm()

    return render(request, 'generatorHave/genHave_home.html', {'form': form})


def yes_preview_html(request):
    context = {
        'name': 'Example Title',
        'description': 'This is an example description.',
        'color': '#3498db'  # 배경색
    }
    return render(request, 'generatorHave/genHave_result.html', context)