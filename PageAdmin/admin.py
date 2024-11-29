from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django import forms
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
    
@admin.register(TaiKhoanNguoiDung)
class TaiKhoanNguoiDungAdmin(admin.ModelAdmin):
    list_display = ('idtaikhoan', 'username', 'quyen', 'trangthai',)
    search_fields = ('username','quyen', 'trangthai', )
    list_filter = ('quyen', 'trangthai')

@admin.register(HocVien)
class HocVienAdmin(admin.ModelAdmin):
    list_display = ('mahv', 'hoten', 'email', 'SDT', 'GioiTinh', 'NgaySinh', 'DiaChi',)
    search_fields = ('hoten', 'DiaChi', 'GioiTinh')
    list_filter = ('DiaChi', 'GioiTinh')
    def save_model(self, request, obj, form, change):
        if not change:
            TaiKhoanNguoiDung.objects.create(
                idtaikhoan=obj.mahv,
                username=obj.email,
                pass_word=obj.mahv,
                quyen='HV',
                trangthai='Mới tạo'
            )
        super().save_model(request,obj,form,change)

@admin.register(GiaoVien)
class GiaoVienAdmin(admin.ModelAdmin):
    
    list_display = ('magv', 'hoten', 'email', 'SDT', 'GioiTinh', 'NgaySinh', 'DiaChi',)
    search_fields = ('hoten', 'DiaChi', 'GioiTinh')
    list_filter = ('DiaChi', 'GioiTinh')
    def save_model(self, request, obj, form, change):
        if not change:
            TaiKhoanNguoiDung.objects.create(
                idtaikhoan=obj.magv,
                username=obj.email,
                pass_word=obj.magv,
                quyen='GV',
                trangthai='Hoạt động'
            )
        super().save_model(request,obj,form,change)
    
    
@admin.register(DanhGia)
class DanhGiaAdmin(admin.ModelAdmin):
    list_display = ('madanhgia', 'mota', 'mahv', 'malop')
    search_fields = ('mahv','malop',)
    
    
@admin.register(ChiTietKhoaHoc)  
class ChiTietKhoaHocAdmin(admin.ModelAdmin):
    list_display = ('id', 'stt', 'manoidung', 'makh')
    list_filter = ('makh','manoidung',)
    autocomplete_fields = ['manoidung']


@admin.register(KhoaHoc)    
class KhoaHocAdmin(admin.ModelAdmin):
    list_display = ('makh', 'tenkh', 'mota', 'hinhthuc')
    search_fields = ('tenkh','hinhthuc',)
    list_filter = ('hinhthuc',)
    
@admin.register(NoiDungKhoaHoc)
class NoiDungKhoaHocAdmin(admin.ModelAdmin):
    list_display = ('manoidung', 'tieude')
    search_fields = ('tieude',)
    
    
@admin.register(PhieuNhap)
class PhieuNhapAdmin(admin.ModelAdmin):
    list_display = ('maphieunhap', 'ngaynhap', 'tongtien', 'ghichu', 'mancc', 'manv')
    search_fields = ('maphieunhap','mancc', 'manv', )
    list_filter = ('mancc','manv','ngaynhap',) 
    
    
from .forms import HoaDonForm
@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    form = HoaDonForm
    list_display = ('sohd','ngaylap','tongtien','trangthai','malop','mahv',)
    search_fields = ('sohd','malop','mahv',)
    list_filter = ('trangthai','malop','mahv',)


@admin.register(LichHoc)
class LichHocAdmin(admin.ModelAdmin):
    list_display = ('malich','ngayhoc','giohoc','sogiohoc','malop',)
    search_fields = ('malich','malop',)
    list_filter = ('giohoc','sogiohoc','malop',)
    
    

        
@admin.register(LopHoc)
class LopHocAdmin(admin.ModelAdmin):
    list_display = ('malop','tenlop','siso','tonggiohoc','hocphi','makh',)
    search_fields = ('tenlop','makh',)
    list_filter = ('tenlop','makh',)
    
    
    
    