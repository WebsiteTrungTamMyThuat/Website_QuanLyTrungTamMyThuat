from django.contrib import admin
from django.contrib.auth.models import User
from .models import TaiKhoanNhanVien, NhanVien, NhaCungCap, HoaCu, GiaoVien, HocVien, DanhGia
# Register your models here.


@admin.register(NhanVien)
class NhanVienAdmin(admin.ModelAdmin):
    list_display = ('manv', 'hoten', 'gioitinh', 'ngaysinh', 'diachi', 'sdt')  # Hiển thị các trường trong danh sách
    search_fields = ('manv', 'hoten')  # Thêm thanh tìm kiếm theo mã NV và họ tên
    list_filter = ('gioitinh',)  # Thêm bộ lọc theo giới tính
    readonly_fields = ('user',)
    def save_model(self, request, obj, form, change):
        # Tạo người dùng khi lưu một nhân viên mới
        if not obj.user:
            user = User.objects.create_user(username=obj.manv, password='default_password')
            obj.user = user
        super().save_model(request, obj, form, change)
    
    

    
@admin.register(NhaCungCap)
class NhaCungCapAdmin(admin.ModelAdmin):
    list_display = ('mancc', 'tenncc', 'diachi', 'sdt')
    search_fields = ('tenncc', 'diachi')
    list_filter = ('diachi',)
    exclude = ('mancc',) 
    

@admin.register(HoaCu)
class HoaCuAdmin(admin.ModelAdmin):
    list_display = ('mahoacu', 'tenhoacu', 'soluong')
    search_fields = ('tenhoacu',)
    

@admin.register(HocVien)
class HocVienAdmin(admin.ModelAdmin):
    list_display = ('mahv', 'hoten', 'email', 'SDT', 'GioiTinh', 'NgaySinh', 'DiaChi',)
    search_fields = ('hoten', 'DiaChi', 'GioiTinh')
    list_filter = ('DiaChi', 'GioiTinh')

@admin.register(GiaoVien)
class GiaoVienAdmin(admin.ModelAdmin):
    list_display = ('magv', 'hoten', 'email', 'SDT', 'GioiTinh', 'NgaySinh', 'DiaChi',)
    search_fields = ('hoten', 'DiaChi', 'GioiTinh')
    list_filter = ('DiaChi', 'GioiTinh')
    
    
@admin.register(DanhGia)
class DanhGiaAdmin(admin.ModelAdmin):
    list_display = ('madanhgia', 'mota', 'mahv', 'malop')
    search_fields = ('mahv','malop',)