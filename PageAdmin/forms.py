from django import forms
from .models import GiaoVien, HoaDon, HocVien

class FormGiaoVien(forms.ModelForm):
    class Meta:
        model = GiaoVien
        fields = ['magv', 'hoten', 'email', 'SDT', 'GioiTinh', 'NgaySinh', 'DiaChi']

class HoaDonForm(forms.ModelForm):
    class Meta:
        model = HoaDon
        fields = '__all__'

    mahv = forms.ModelChoiceField(
        queryset=HocVien.objects.all(),
        label="Học Viên",
        to_field_name="mahv",  # Lưu giá trị là `mahv`
        widget=forms.Select
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Tùy chỉnh hiển thị trong dropdown
        self.fields['mahv'].label_from_instance = lambda obj: f"{obj.hoten} ({obj.mahv})"