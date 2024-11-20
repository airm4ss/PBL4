from django import forms

class PrivacyPolicyForm(forms.Form):
    hospital_name = forms.CharField(label='병원 이름', max_length=100)
    privacy_policy_date = forms.DateField(label='개인정보처리방침 시행 날짜', widget=forms.SelectDateWidget)
    department = forms.ChoiceField(
        label='병원 진료과',
        choices=[
            ('비뇨기과', '비뇨기과'),
            ('소아과', '소아(청소년)과'),
            ('외과', '외과'),
            ('안과', '안과'),
            ('산부인과', '산부인과'),
            ('내과', '내과'),
            ('이비인후과', '이비인후과'),
            ('피부과', '피부과'),
            ('성형외과', '성형외과'),
            ('치과', '치과'),
            ('한의원', '한의원'),
        ],
        widget=forms.RadioSelect,
    )
    data_protection_officer = forms.CharField(label='개인정보책임자명', max_length=100)
    position = forms.CharField(label='직위', max_length=100)
    phone_number = forms.CharField(label='휴대전화번호', max_length=20)
    email = forms.EmailField(label='이메일')
    fax_number = forms.CharField(label='팩스번호', required=False, max_length=20)
    has_privacy_officer = forms.ChoiceField(
        label='개인정보 보호 담당부서',
        choices=[('예', '예'), ('아니요', '아니요')],
        widget=forms.RadioSelect,
    )
    privacy_officer_name = forms.CharField(label='개인정보보호 담당부서명', required=False, max_length=100)
    privacy_officer_phone = forms.CharField(label='전화번호', required=False, max_length=20)
    privacy_officer_email = forms.EmailField(label='이메일', required=False)
    privacy_officer_fax = forms.CharField(label='팩스번호', required=False, max_length=20)
    cctv_installed = forms.BooleanField(label='주차장 내 CCTV 설치 여부', required=False)
    website_functions = forms.MultipleChoiceField(
        label='홈페이지에서 운영하는 기능',
        choices=[
            ('회원가입', '회원가입'),
            ('주문처리', '홈페이지 내 주문 및 결제 처리'),
            ('배송', '홈페이지 내 상품 배송'),
            ('이벤트', '이벤트 참여 및 경품 응모 행사 진행'),
            ('마케팅', '마케팅 및 광고에 고객 정보 활용'),
            ('건의함', '고객 건의함 운영'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    data_outsourcing = forms.ChoiceField(
        label='개인정보 위탁 여부',
        choices=[('위탁하지 않음', '위탁하지 않음'), ('위탁하고 있음', '위탁하고 있음')],
        widget=forms.RadioSelect,
    )
    privacy_links = forms.CharField(widget=forms.Textarea, required=False)
