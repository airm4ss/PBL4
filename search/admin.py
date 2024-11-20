from django.contrib import admin
from .models import Hospital  # Hospital 모델을 import

# Hospital 모델을 관리자 페이지에 등록하는 설정
class HospitalAdmin(admin.ModelAdmin):
    # 검색 필드를 병원 이름으로 설정
    search_fields = ['name']  # name 필드로 검색 가능하도록 설정

# Hospital 모델과 설정된 Admin 클래스를 등록
admin.site.register(Hospital, HospitalAdmin)
