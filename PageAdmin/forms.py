from django import forms
from .models import GiaoVien

class FormGiaoVien(forms.ModelForm):
    class Meta:
        model = GiaoVien
        fields = ['magv', 'hoten', 'email', 'SDT', 'GioiTinh', 'NgaySinh', 'DiaChi']