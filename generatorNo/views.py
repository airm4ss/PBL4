from base64 import b64encode
import base64
from io import BytesIO
import traceback
from django.shortcuts import redirect, render

from config import settings
from .forms import PrivacyPolicyForm

from notion.client import NotionClient
from django.views.decorators.csrf import csrf_exempt
from notion.client import NotionClient
from notion.block import PageBlock, HeaderBlock, SubsubheaderBlock, TextBlock, CodeBlock, BulletedListBlock
import os, qrcode
from django.http import FileResponse, HttpResponse
from datetime import date
from django.conf import settings


# Notion 관련 토큰과 페이지 URL을 상수로 정의
MY_TOKEN = settings.MY_TOKEN
PAGE_URL = 'https://www.notion.so/airmasss/45582212e7994cdaaa84b6a67e519df0?pvs=4'

def gen_no_home(request):
    if request.method == 'POST':
        form = PrivacyPolicyForm(request.POST)
        if form.is_valid():
            # 폼 데이터를 가져옴
            form_data = form.cleaned_data

            # 저장할 개인정보 항목 리스트
            privacy_policies = []

            # form_data에 privacy_policies와 consent_info 추가
            form_data['privacy_policies'] = privacy_policies

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


            # 만약 privacy_policy_date가 date 객체라면, 문자열로 변환
            privacy_policy_date = form_data.get('privacy_policy_date')
            if isinstance(privacy_policy_date, date):
                form_data['privacy_policy_date'] = privacy_policy_date.strftime('%Y년 %m월 %d일')

            # 세션에 저장
            request.session['form_data'] = form_data

            return render(request, 'generatorNo/genNo_mid.html', {'form_data': form_data})
    else:
        form = PrivacyPolicyForm()

    return render(request, 'generatorNo/genNo_home.html', {'form': form})


def no_preview_html(request):
    return render(request, 'generatorNo/genNo_result.html')


@csrf_exempt
def create(request):
    # 세션에서 form_data 불러오기
    form_data = request.session.get('form_data')

    if not form_data:
        return HttpResponse("No form data found in session", status=400)

    # Notion 클라이언트 설정
    client = NotionClient(token_v2=MY_TOKEN)
    page = client.get_block(PAGE_URL)

    # form_data에서 가져오기
    hospital_name = form_data.get('hospital_name', 'Default Hospital Name')
    privacy_policy_date = form_data.get('privacy_policy_date', 'Default Date')
    privacy_manager = form_data.get('privacy_manager', 'Default Manager')
    position = form_data.get('position', 'Default Position')
    phone = form_data.get('phone', 'Default Phone')
    email = form_data.get('email', 'default@example.com')
    fax = form_data.get('fax', 'Default Fax')
    department = form_data.get('department', 'Default Department')
    has_privacy_department = form_data.get('has_privacy_department', False)
    privacy_department = form_data.get('privacy_department', 'Default Privacy Department')
    department_phone = form_data.get('department_phone', 'Default Department Phone')
    department_email = form_data.get('department_email', 'default@department.com')
    department_fax = form_data.get('department_fax', 'Default Department Fax')

    third_party_data = form_data.get('third_party_data', [])
    outsourcing_provision = form_data.get('outsourcing_provision', '위탁하지 않음')
    outsourcing_data = form_data.get('outsourcing_data', [])


    # 고정형 영상정보처리기기 관련 데이터 가져오기
    installation_count = form_data.get('installation_count', 'Unknown')
    installation_location = form_data.get('installation_location', 'Unknown Location')
    shooting_range = form_data.get('shooting_range', 'Unknown Range')
    manager_name = form_data.get('manager_name', 'Default Manager')
    manager_phone = form_data.get('manager_phone', 'Default Phone')
    recording_time = form_data.get('recording_time', 'Default Time')
    retention_period = form_data.get('retention_period', 'Default Period')
    storage_location = form_data.get('storage_location', 'Default Location')
    contractor = form_data.get('contractor', 'Default Contractor')
    contractor_contact = form_data.get('contractor_contact', 'Default Contact')
    contractor_phone = form_data.get('contractor_phone', 'Default Phone')

    # 제목
    new_page = page.children.add_new(PageBlock)
    new_page.title = hospital_name

    # 설명
    new_page.children.add_new(TextBlock,
                              title=f"{hospital_name}(이하 병원 이라 함)은(는) 정보주체의 자유와 권리 보호를 위해 「개인정보 보호법」 및 관계 법령이 정한 바를 준수하여, 적법하게 개인정보를 처리하고 안전하게 관리하고 있습니다. 이에 「개인정보 보호법」 제30조에 따라 정보주체에게 개인정보 처리에 관한 절차 및 기준을 안내하고, 이와 관련한 고충을 신속하고 원활하게 처리할 수 있도록 하기 위하여 다음과 같이 개인정보처리방침을 수립·공개합니다.")

    # 목차
    new_page.children.add_new(HeaderBlock, title="목차")
    code_block = new_page.children.add_new(CodeBlock, language="plain text")
    code_block.title = "1. 개인정보의 처리 목적, 수집 항목, 보유 및 이용기간\n2.14세 미만 아동의 개인정보 처리\n3.개인정보의 파기 절치 및 방법\n4.개인정보의 제3자 제공\n5.개인정보 처리업무의 위탁\n6.개인정보의 안전성 확보조치\n7.정보주체와 법정대리인의 권리, 의무 및 행사방법\n8.개인정보 보호책임자의 성명 또는 개인정보 업무 담당부서 및 고충사항을 처리하는 부서\n9.정보주체의 권익침해에 대한 구제방법\n10.고정형 영상정보처리기기 운영, 관리\n11.개인정보 처리방침의 변경"

    # 배경색 지정
    background_color = "blue_background"

    # 1
    new_page.children.add_new(HeaderBlock, title="1. 개인정보의 처리 목적, 수집 항목, 보유 및 이용기간")
    new_page.children.add_new(TextBlock, title="병원은 다음과 같이 정보주체의 개인정보를 처리합니다. 「개인정보 보호법」에 따라 서비스 제공을 위해 필요한 최소한의 범위에서 개인정보를 수집・이용합니다.")

    new_page.children.add_new(SubsubheaderBlock, title="a. 정보주체의 동의를 받지 않고 처리하는 개인정보 항목")
    new_page.children.add_new(TextBlock, title="병원은 다음의 개인정보 항목을 정보주체의 동의 없이 처리하고 있습니다.")

    new_page.children.add_new(TextBlock, title="구분: 진료서비스 제공 및 환자 명부 관리")
    new_page.children.add_new(TextBlock, title="법적 근거: 개인정보보호법 제15조 제1항 제2호(법률에 특별한 규정) 의료법 제22조 (진료기록부 등)")
    new_page.children.add_new(TextBlock, title="수집 목적: 환자 진료 및 의료법에 따른 환자명부의 보존")
    new_page.children.add_new(TextBlock, title="수집 항목: 주소, 성명, 휴대전화번호, 주민등록번호")
    new_page.children.add_new(TextBlock, title="보유 및 이용기간: 5년 (의료법 시행규칙 제15조)")
    new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가

    new_page.children.add_new(TextBlock, title="구분: 진료기록부 관리")
    new_page.children.add_new(TextBlock, title="법적 근거: 의료법 제22조 (진료기록부 등)")
    new_page.children.add_new(TextBlock, title="수집 목적: 의료법에 따른 진료기록의 작성 및 보존")
    new_page.children.add_new(TextBlock, title="수집 항목: 주소, 성명, 휴대전화번호, 주민등록번호, 병력 및 가족력, 주된 증상, 진단 결과 또는 진단명, 진료 경과, 치료내용(주사・투약・처치 등), 진료일시")
    new_page.children.add_new(TextBlock, title="보유 및 이용기간: 10년 (의료법 시행규칙 제15조)")
    new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가

    new_page.children.add_new(TextBlock, title="구분: 보험청구신청자 정보")
    new_page.children.add_new(TextBlock, title="법적 근거: 국민건강보험법 제96조")
    new_page.children.add_new(TextBlock, title="수집 목적: 보험청구")
    new_page.children.add_new(TextBlock, title="수집 항목: 성명, 주민번호, 보험청구정보")
    new_page.children.add_new(TextBlock, title="보유 및 이용기간: 10년(1회 연장 시 20년)")
    new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가

    new_page.children.add_new(TextBlock, title="구분: 의무기록사본 발급 정보")
    new_page.children.add_new(TextBlock, title="법적 근거: 의료법 제21조 제2항 및 동법 시행규칙 제13조의3")
    new_page.children.add_new(TextBlock, title="수집 목적: 의무기록사본 발급")
    new_page.children.add_new(TextBlock, title="수집 항목: 성명, 주민번호")
    new_page.children.add_new(TextBlock, title="보유 및 이용기간: 3년")
    new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가

    new_page.children.add_new(TextBlock, title="구분: 원무 서비스")
    new_page.children.add_new(TextBlock, title="법적 근거: 개인정보보호법 제15조 제1항 제4호 (계약의 이행)")
    new_page.children.add_new(TextBlock, title="수집 목적: 진료비 수납 등 원무 서비스 제공")
    new_page.children.add_new(TextBlock, title="수집 항목: 카드 결제 승인 정보 (성명, 카드사 명, 카드 종류, 카드 번호, 유효기간)")
    new_page.children.add_new(TextBlock, title="보유 및 이용기간: 5년 (전자상거래법 제6조)")
    new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가
    

    new_page.children.add_new(SubsubheaderBlock, title="b. 정보주체의 동의를 받아 처리하는 개인정보 항목")
    new_page.children.add_new(TextBlock, title="병원은 다음의 개인정보 항목을 「개인정보 보호법」 제15조 제1항 제1호 및 제22조 제1항 제7호에 따라 정보주체의 동의를 받아 처리하고 있습니다.")
    new_page.children.add_new(TextBlock, title="수집 목적: 신약개발을 위한 인간대상 연구")
    new_page.children.add_new(TextBlock, title="수집 항목: 생년월일, 성별, 진단기호, 진단명")
    new_page.children.add_new(TextBlock, title="보유 및 이용기간: 연구종료 시 까지")
    new_page.children.add_new(TextBlock, title="비고: 생명윤리법 제16조 (인간대상연구의 동의)")


    new_page.children.add_new(TextBlock, title="관련 법령의 규정에 의하여 보존할 필요가 있는 경우 병원은 아래와 같이 관련 법령에서 정한 일정 기간 동안 회원정보를 보관합니다.")
    new_page.children.add_new(BulletedListBlock, title="소비자의 불만 또는 분쟁처리에 관한 기록 : 3년 (전자상거래 등에서의 소비자보호에 관한 법률)")
    new_page.children.add_new(BulletedListBlock, title="신용정보의 수집/처리 및 이용 등에 관한 기록 : 3년 (신용정보의 이용 및 보호에 관한 법률)")
    new_page.children.add_new(BulletedListBlock, title="본인 확인에 관한 기록 : 6개월 (정보통신망 이용촉진 및 정보보호 등에 관한 법률)")

    new_page.children.add_new(SubsubheaderBlock, title="개인정보 수집방법")
    new_page.children.add_new(TextBlock, title="다음과 같은 방법으로 개인정보를 수집합니다.")
    new_page.children.add_new(BulletedListBlock, title="서면양식, 팩스, 전화, 전화, 이메일")
    
    new_page.children.add_new(SubsubheaderBlock, title="동의를 거부할 권리가 있다는 사실과 동의 거부에 따른 불이익")
    new_page.children.add_new(TextBlock, title="이용자는 홈페이지에서 수집하는 개인정보에 대해 동의를 거부할 권리가 있으며 동의 거부 시에는 회원가입 및 인터넷 진료예약, 예약조회 등의 홈페이지 서비스가 일부 제한됩니다.")


    # 2
    new_page.children.add_new(HeaderBlock, title="2. 14세 미만 아동의 개인정보 처리에 관한 사항")

    new_page.children.add_new(TextBlock, title="① 병원은 만 14세 미만 아동(이하 ‘아동’이라 함)의 개인정보를 처리하기 위하여 동의가 필요한 경우에는 해당 아동의 법정대리인으로부터 동의를 받습니다.")
    new_page.children.add_new(TextBlock, title="② 병원은 아동의 개인정보 처리에 관하여 그 법정대리인의 동의를 받을 때에는 아동에게 법정대리인의 성명, 휴대전화번호 등 필요한 최소한의 정보를 요구할 수 있으며 적법한 법정대리인이 동의하였는지를 확인합니다.")
    new_page.children.add_new(TextBlock, title="③ 법정대리인의 동의를 얻기 위하여 수집한 법정대리인의 개인정보를 해당 법정대리인의 동의 여부를 확인하는 목적 외의 용도로 이를 이용하거나 제3자에게 제공하지 않습니다.")

    # 3
    new_page.children.add_new(HeaderBlock, title="3. 개인정보의 파기절차 및 방법에 관한 사항")

    new_page.children.add_new(TextBlock, title="① 병원은 만 14세 미만 아동(이하 ‘아동’이라 함)의 개인정보를 처리하기 위하여 동의가 필요한 경우에는 해당 아동의 법정대리인으로부터 동의를 받습니다.")
    new_page.children.add_new(TextBlock, title="② 정보주체로부터 동의받은 개인정보 보유기간이 경과하거나 처리목적이 달성되었음에도 불구하고 다른 법령에 따라 개인정보를 계속 보존하여야 하는 경우에는 해당 개인정보를 별도의 데이터베이스(DB)로 옮기거나 보관장소를 달리하여 보존합니다.")
    new_page.children.add_new(TextBlock, title="③ 병원은 폐업 또는 휴업 신고를 할 때에는 기록・보존하고 있는 진료기록부, 조산기록부, 간호기록, 그 밖의 진료에 관한 기록을 관할 보건소장에게 이관합니다.")
    new_page.children.add_new(TextBlock, title="④ 개인정보 파기의 절차 및 방법은 다음과 같습니다.")

    new_page.children.add_new(TextBlock, text="")
    new_page.children.add_new(TextBlock, title="[파기절차]\n병원은 파기 사유가 발생한 개인정보를 확인하고, 병원의 개인정보 보호책임자의 승인을 받아 개인정보를 파기합니다.")
    new_page.children.add_new(TextBlock, text="")
    new_page.children.add_new(TextBlock, title="[파기방법]\n병원은 전자적 파일 형태로 기록・저장된 개인정보는 기록을 재생할 수 없도록 파기하며, 종이 문서에 기록・저장된 개인정보는 분쇄기로 분쇄하거나 소각하여 파기합니다.")


    # 4
    new_page.children.add_new(HeaderBlock, title="4. 개인정보의 제3자 제공에 관한 사항")
    if third_party_data:
        # 제3자 제공 정보가 있을 경우 텍스트 형식으로 추가
        new_page.children.add_new(TextBlock, title="병원은 다음과 같이 개인정보를 제3자에게 제공하고 있습니다.")
        
        for data in third_party_data:
            recipient = data.get('recipient', 'Unknown Recipient')
            purpose = data.get('purpose', 'Unknown Purpose')
            items = data.get('items', 'Unknown Items')
            legal_basis = data.get('legal_basis', 'Unknown Legal Basis')

            # 각 제3자 제공 정보 텍스트로 추가
            new_page.children.add_new(TextBlock, title=f"제공받는 자: {recipient}")
            new_page.children.add_new(TextBlock, title=f"제공목적: {purpose}")
            new_page.children.add_new(TextBlock, title=f"제공항목: {items}")
            new_page.children.add_new(TextBlock, title=f"제공 근거 및 보유/이용 기간: {legal_basis}")
            new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가

    else:
        # 제3자 제공 정보가 없을 경우 메시지 추가
        new_page.children.add_new(TextBlock, title="병원은 귀하의 동의가 있거나 관련법령의 규정에 의한 경우를 제외하고는 어떠한 경우에도 귀하의 개인정보를 수집 및 이용목적에서 고지한 범위를 넘어 귀하의 개인정보를 이용하거나 타인 또는 타기업, 기관에 제공하지 않습니다.")
        new_page.children.add_new(TextBlock, title="다만, 아래의 경우에는 예외로 합니다.")
        
        # 예외 사항 목록 추가
        new_page.children.add_new(BulletedListBlock, title="이용자들이 사전에 공개에 동의한 경우")
        new_page.children.add_new(BulletedListBlock, title="법령의 규정에 의거하거나, 수사 목적으로 법령에 정해진 절차와 방법에 따라 수사기관의 요구가 있는 경우")
        new_page.children.add_new(BulletedListBlock, title="통계작성, 학술연구 또는 시장조사를 위하여 필요한 경우로서 특정 개인을 알아볼 수 없는 형태로 가공하여 제공하는 경우")


    # 5
    new_page.children.add_new(HeaderBlock, title="5. 개인정보 처리업무의 위탁에 관한 사항")
    if outsourcing_provision == "위탁하고 있음" and outsourcing_data:
        # 위탁 정보가 있을 경우
        new_page.children.add_new(TextBlock, title="병원은 다음과 같이 개인정보 처리업무를 위탁하고 있습니다.")

        # 위탁 데이터 추가
        for row in outsourcing_data:
            company = row.get('company', 'Unknown Company')
            purpose = row.get('purpose', 'Unknown Purpose')

            new_page.children.add_new(TextBlock, title=f"위탁받는 자(수탁자): {company}")
            new_page.children.add_new(TextBlock, title=f"위탁업무: {purpose}")
            new_page.children.add_new(TextBlock, title="")  # 빈 줄 추가

    else:
        # 위탁 정보가 없을 경우 메시지 추가
        new_page.children.add_new(TextBlock, title="병원은 고객님의 동의없이 고객님의 정보를 외부 업체에 위탁하지 않습니다.")
        new_page.children.add_new(TextBlock, title="향후 그러한 필요가 생길 경우, 위탁 대상자와 위탁 업무 내용에 대해 고객님에게 통지하고 필요한 경우 사전 동의를 받도록 하겠습니다.")


    # 6
    new_page.children.add_new(HeaderBlock, title="6. 개인정보의 안전성 확보조치에 관한 사항")
    new_page.children.add_new(TextBlock, title="병원은 개인정보의 안전성 확보를 위해 다음과 같은 조치를 취하고 있습니다.")
    new_page.children.add_new(BulletedListBlock, title="관리적 조치 : 내부관리계획 수립・시행, 전담조직 운영, 정기적 직원 교육")
    new_page.children.add_new(BulletedListBlock, title="기술적 조치 : 개인정보처리시스템 등의 접근권한 관리, 접근통제시스템 설치, 개인정보의 암호화, 보안프로그램 설치 및 갱신")
    new_page.children.add_new(BulletedListBlock, title="물리적 조치 : 전산실, 자료보관실 등의 접근통제")

    # 7
    new_page.children.add_new(HeaderBlock, title="7. 정보주체와 법정대리인의 권리・의무 및 행사방법에 관한 사항")

    new_page.children.add_new(TextBlock, title="정보주체(혹은 해당주체의 법정대리인)는 병원에 대해 언제든지 다음 각 호의 권리를 행사할 수 있습니다.")

    new_page.children.add_new(TextBlock, title="정보주체")
    new_page.children.add_new(BulletedListBlock, title="환자(본인)에 관한 기록 열람, 정정, 삭제, 처리정지 요구")
    new_page.children.add_new(BulletedListBlock, title="그 외 개인정보 열람·정정·삭제·처리정지 요구")
    new_page.children.add_new(TextBlock, title="※ 만 14세 미만 아동에 관한 개인정보의 열람 등 요구는 법정대리인이 직접 해야 하며, 만 14세 이상의 미성년자인 정보주체는 정보주체의 개인정보에 관하여 미성년자 본인이 권리를 행사하거나 법정대리인을 통하여 권리를 행사할 수도 있습니다. ")

    new_page.children.add_new(TextBlock, title="")
    new_page.children.add_new(TextBlock, title="법정대리인, 위임을 받은 자")
    new_page.children.add_new(TextBlock, title="제1항 각 호에 따른 권리 행사는 정보주체의 법정대리인이나 위임을 받은 자 등 대리인을 통하여 하실 수도 있습니다. 이 경우 “개인정보 처리 방법에 관한 고시” 별지 제11호 서식에 따른 위임장을 제출하셔야 합니다.")

    new_page.children.add_new(TextBlock, title="")
    new_page.children.add_new(TextBlock, title="행사방법")
    new_page.children.add_new(TextBlock, title="환자(본인)에 관한 기록 열람, 정정, 삭제, 처리정지 요구: 환자가 지정하는 대리인이 환자 본인의 동의서와 대리권이 있음을 증명하는 서류를 첨부하는 등 보건복지부령으로 정하는 요건을 갖추어 요청한 경우, 다음 서류를 제출")
    new_page.children.add_new(TextBlock, title="① 기록열람이나 사본발급을 요청하는 자의 신분증 사본")
    new_page.children.add_new(TextBlock, title="② 환자가 자필 서명한 「의료법 시행규칙」 별지 제9호의2서식의 동의서 및 별지 제9호의3서식의 위임장\n- 이 경우 환자가 만 14세 미만의 미성년자인 경우에는 환자의 법정대리인이 작성하여야 하며, 가족관계증명서 등 법정대리인임을 확인할 수 있는 서류를 첨부하여야 한다.")
    new_page.children.add_new(TextBlock, title="③ 환자의 신분증 사본\n- 다만, 환자가 만 17세 미만으로 「주민등록법」 제24조제1항에 따른 주민등록증이 발급되지 아니한 자는 제외한다.")
    new_page.children.add_new(TextBlock, title="· 그 외 개인정보 열람, 정정, 삭제, 처리정지 요구 : “개인정보 처리 방법에 관한 고시(제2020-7호)” 별지 제11호 서식에 따른 위임장)")

    new_page.children.add_new(TextBlock, title="")
    new_page.children.add_new(TextBlock, title="제한")
    new_page.children.add_new(TextBlock, title="제1항 각 호에 따른 권리 행사는 다음의 경우에는 제한될 수 있습니다.")
    new_page.children.add_new(BulletedListBlock, title="환자(본인)에 관한 기록 열람, 정정, 삭제, 처리정지 요구: 국가안보에 긴요한 사안으로 “다른 법률에 따라 진행 중인 감사 및 조사에 관한 업무”를 수행하는데 지장을 초래할 때")
    new_page.children.add_new(BulletedListBlock, title="그 외 개인정보 열람, 정정, 삭제, 처리정지 요구 : 「개인정보 보호법」 제35조 제4항 각 호, 제37조 제2항 각 호에 해당되는 경우 ")

    new_page.children.add_new(TextBlock, title="")
    new_page.children.add_new(TextBlock, title="동의 철회")
    new_page.children.add_new(TextBlock, title="귀하는 진료접수 시 개인정보의 수집⋅이용 및 제공에 대해 동의하신 내용을 언제든지 철회하실 수 있습니다. 철회방법은 병원에 서면, 전화 등으로 연락하시면 본인확인을 거쳐 개인정보 동의철회 등 필요한 조치를 합니다.")


    # 8
    new_page.children.add_new(HeaderBlock, title="8. 개인정보 보호책임자에 관한 사항")
    new_page.children.add_new(TextBlock, title="병원은 개인정보 처리에 관한 업무를 총괄해서 책임지고, 개인정보 처리와 관련한 정보주체의 불만처리 및 피해구제 등을 위하여 아래와 같이 개인정보 보호책임자를 지정하고 있습니다.")

    new_page.children.add_new(TextBlock, title="")
    new_page.children.add_new(TextBlock, title="개인정보 보호책임자")
    new_page.children.add_new(BulletedListBlock, title=f"성명 : {privacy_manager}")
    new_page.children.add_new(BulletedListBlock, title=f"직위 : {position}")
    new_page.children.add_new(BulletedListBlock, title=f"연락처 : {phone}, {email}, {fax}")

    if has_privacy_department:
        new_page.children.add_new(TextBlock, title="")
        new_page.children.add_new(TextBlock, title="개인정보보호 담당부서")
        new_page.children.add_new(BulletedListBlock, title=f"부서명 : {privacy_department}")
        new_page.children.add_new(BulletedListBlock, title=f"연락처 : {department_phone}, {department_email}, {department_fax}")

    new_page.children.add_new(TextBlock, title="")
    new_page.children.add_new(TextBlock, title="정보주체는 병원의 서비스를 이용하시면서 발생한 모든 개인정보보호 관련 문의, 불만처리, 피해구제 등에 관한 사항을 개인정보 보호책임자 및 담당부서로 문의할 수 있습니다. 병원은 정보주체의 문의에 대해 지체없이 답변 및 처리해드릴 것입니다.")


    # 9
    new_page.children.add_new(HeaderBlock, title="9. 정보주체의 권익침해에 대한 구제방법")
    new_page.children.add_new(TextBlock, title="정보주체는 개인정보침해로 인한 구제를 받기 위하여 개인정보분쟁조정위원회, 한국인터넷진흥원 개인정보침해신고센터 등에 분쟁해결이나 상담 등을 신청할 수 있습니다. \n이 밖에 기타 개인정보침해의 신고, 상담에 대하여는 아래의 기관에 문의하시기 바랍니다.")
    new_page.children.add_new(TextBlock, title="(아래의 기관은 병원과는 별개의 기관으로서, 병원의 자체적인 개인정보 불만처리, 피해구제 결과에 만족하지 못하시거나 보다 자세한 도움이 필요하시면 문의하여 주시기 바랍니다.)")

    new_page.children.add_new(BulletedListBlock, title="개인정보분쟁조정위원회 : (국번없이) 1833-6972 (www.kopico.go.kr)")
    new_page.children.add_new(BulletedListBlock, title="개인정보침해신고센터 : (국번없이) 118 (privacy.kisa.or.kr)")
    new_page.children.add_new(BulletedListBlock, title="대검찰청 : (국번없이) 1301 (www.spo.go.kr)")
    new_page.children.add_new(BulletedListBlock, title="경찰청 : (국번없이) 182 (ecrm.police.go.kr/minwon/main)")


    # 10
    new_page.children.add_new(HeaderBlock, title="10. 고정형 영상정보처리기기 운영 및 관리 방침")

    new_page.children.add_new(SubsubheaderBlock, title="고정형 영상정보처리기기 설치 및 운영 정보")
    new_page.children.add_new(TextBlock, title=f"설치대수: {installation_count}대")
    new_page.children.add_new(TextBlock, title=f"설치 위치: {installation_location}")
    new_page.children.add_new(TextBlock, title=f"촬영 범위: {shooting_range}")
    
    new_page.children.add_new(SubsubheaderBlock, title="관리책임자 정보")
    new_page.children.add_new(TextBlock, title=f"이름: {manager_name}")
    new_page.children.add_new(TextBlock, title=f"전화번호: {manager_phone}")
    
    new_page.children.add_new(SubsubheaderBlock, title="촬영시간 및 보관 정보")
    new_page.children.add_new(TextBlock, title=f"촬영시간: { recording_time}")
    new_page.children.add_new(TextBlock, title=f"보관기간: 촬영일로부터 {retention_period}일")
    new_page.children.add_new(TextBlock, title=f"보관장소: {storage_location}")

    new_page.children.add_new(SubsubheaderBlock, title="위탁 정보")
    new_page.children.add_new(TextBlock, title=f"수탁업체: {contractor}")
    new_page.children.add_new(TextBlock, title=f"담당자: {contractor_contact}")
    new_page.children.add_new(TextBlock, title=f"연락처: {contractor_phone}")

    new_page.children.add_new(SubsubheaderBlock, title="정보주체의 개인영상정보 열람 등 요구에 대한 조치")
    new_page.children.add_new(TextBlock, title="귀하는 개인영상정보에 관하여 열람 또는 존재확인・삭제를 원하는 경우 언제든지 고정형영상정보처리기기운영자에게 요구하실 수 있습니다. 단, 귀하가 촬영된 개인영상정보에 한정됩니다.")
    new_page.children.add_new(TextBlock, title="병원은 개인영상정보에 관하여 열람 또는 존재확인・삭제를 요구한 경우 지체없이 필요한 조치를 하겠습니다.")
    new_page.children.add_new(SubsubheaderBlock, title="개인영상정보의 안전성 확보조치")
    new_page.children.add_new(TextBlock, title="병원에서 처리하는 개인영상정보는 암호화 조치 등을 통하여 안전하게 관리되고 있습니다. 또한 병원은 개인영상정보보호를 위한 관리적 대책으로서 개인정보에 대한 접근권한을 차등 부여하고 있고, 개인영상정보의 위・변조 방지를 위하여 개인영상정보의 생성 일시, 열람 시 열람 목적・열람자・열람 일시 등을 기록하여 관리하고 있습니다. 이 외에도 개인영상정보의 안전한 물리적 보관을 위하여 잠금장치를 설치하고 있습니다.")
    new_page.children.add_new(SubsubheaderBlock, title="고정형 영상정보처리기기 운영・관리방침 변경에 관한 사항")
    new_page.children.add_new(TextBlock, title=f"이 고정형 영상정보처리기기 운영・관리방침은 {privacy_policy_date}에 제정되었으며 법령・정책 또는 보안기술의 변경에 따라 내용의 추가ㆍ삭제 및 수정이 있을 시에는 시행하기 최소 7일 전에 홈페이지를 통해 변경사유 및 내용 등을 공지하도록 하겠습니다.")


    # 11
    new_page.children.add_new(HeaderBlock, title="11. 개인정보 처리방침의 변경에 관한 사항")
    new_page.children.add_new(TextBlock, title=f"이 개인정보 처리 방침은 {privacy_policy_date}부터 적용 됩니다.")
    new_page.children.add_new(TextBlock, title="이 개인정보 처리방침은 법령·정책 또는 보안기술의 변경에 따라 내용의 추가·삭제 및 수정이 있을 시에는 변경되는 개인정보 처리방침을 시행하기 전에 변경 이유 및 내용 등을 공지하도록 하겠습니다.")

    # 생성된 페이지 URL 가져오기
    new_page_url = new_page.get_browseable_url()

    # QR 코드 생성
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(new_page_url)
    qr.make(fit=True)

# QR 코드 이미지를 메모리에 저장하고 base64로 인코딩
    img = qr.make_image(fill='black', back_color='white')
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    qr_code_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # 세션에 QR 코드 이미지(base64)와 URL 저장
    request.session['qr_code_data'] = qr_code_base64
    request.session['qr_code_url'] = new_page_url

    # QR 코드 미리보기 페이지로 리다이렉트
    return redirect('generatorNo:qr_preview')

def qr_preview(request):
    # 세션에서 QR 코드 데이터와 URL 가져오기
    qr_code_base64 = request.session.get('qr_code_data')
    qr_code_url = request.session.get('qr_code_url')

    if not qr_code_base64 or not qr_code_url:
        return HttpResponse("QR 코드 정보가 없습니다.", status=400)

    # QR 코드를 Base64 인코딩하여 HTML 이미지로 표시
    return render(request, 'generatorNo/qr_preview.html', {
        'qr_code_url': qr_code_url,
        'qr_code_base64': qr_code_base64,
    })


def download_qr_image(request):
    # 세션에서 Base64로 인코딩된 QR 코드 가져오기
    qr_code_base64 = request.session.get('qr_code_data')

    if not qr_code_base64:
        return HttpResponse("QR 코드 이미지 데이터가 없습니다.", status=400)

    # Base64 데이터를 바이너리 데이터로 변환
    qr_code_binary = base64.b64decode(qr_code_base64)

    # 메모리에 파일 생성
    buffer = BytesIO(qr_code_binary)

    # HTTP 응답으로 PNG 파일 제공
    response = HttpResponse(buffer, content_type="image/png")
    response['Content-Disposition'] = 'attachment; filename="privacy_policy.png"'
    return response