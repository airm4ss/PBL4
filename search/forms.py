# search/forms.py
from django import forms

class HospitalSearchForm(forms.Form):
    name = forms.CharField(label='병원 이름', max_length=100, required=False)
