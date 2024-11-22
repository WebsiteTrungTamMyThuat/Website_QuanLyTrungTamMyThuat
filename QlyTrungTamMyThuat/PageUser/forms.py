from django import forms
from PageAdmin.models import HocVien

class HocVienForm(forms.ModelForm):
    class Meta:
        model = HocVien
        fields = ['mahv', 'hoten', 'email', 'gioitinh', 'ngaysinh', 'diachi','sdt']