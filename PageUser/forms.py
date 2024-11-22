from django import forms
from PageAdmin.models import HocVien

class HocVienForm(forms.ModelForm):
    class Meta:
        model = HocVien
        fields = ['mahv', 'hoten', 'email','SDT', 'GioiTinh', 'NgaySinh', 'DiaChi']
        widgets = {
            'hoten': forms.TextInput(attrs={'placeholder': 'Họ tên', 'class': 'input-field'}),
            'SDT': forms.TextInput(attrs={'placeholder': 'Số điện thoại', 'class': 'input-field'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'input-field'}),
            'NgaySinh': forms.DateInput(attrs={
                'type': 'date',
                'class': 'input-field',
                'placeholder': 'Ngày sinh',
                'required': True
            }),
        }