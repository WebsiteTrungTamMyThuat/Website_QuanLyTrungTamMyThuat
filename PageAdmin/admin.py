from django.contrib import admin
from django.contrib.auth.models import User
from .models import *
from django import forms
from django.forms import PasswordInput

# Register your models here.


admin.site.site_header = "Trang quản trị Mỹ Thuật Bụi"
admin.site.site_title = "Quản trị hệ thống"
admin.site.index_title = "Chào mừng đến với trang quản trị Mỹ Thuật Bụi"

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
  
  
class TaiKhoanNguoiDungForm(forms.ModelForm):
    class Meta:
        model = TaiKhoanNguoiDung
        exclude = ('pass_word',)
        
@admin.register(TaiKhoanNguoiDung)
class TaiKhoanNguoiDungAdmin(admin.ModelAdmin):
    list_display = ('idtaikhoan', 'username', 'quyen', 'trangthai',)
    search_fields = ('username','quyen', 'trangthai', )
    list_filter = ('quyen', 'trangthai')
    readonly_fields = ('username', 'quyen')
    form = TaiKhoanNguoiDungForm
    def has_add_permission(self, request):
        return False

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
    

# class ChiTietPhieuNhapInline(admin.TabularInline):
#     model = ChiTietPhieuNhap
#     extra = 1
#     fields = ('mahoacu', 'soluong', 'dongia', 'thanhtien')
    
@admin.register(PhieuNhap)
class PhieuNhapAdmin(admin.ModelAdmin):
    list_display = ('maphieunhap', 'ngaynhap', 'tongtien', 'ghichu', 'get_mancc', 'get_manv')
    search_fields = ('maphieunhap', 'mancc__tenncc', 'manv__hoten')
    list_filter = ('mancc', 'manv', 'ngaynhap',)

    #inlines = [ChiTietPhieuNhapInline]
    
    def get_mancc(self, obj):
        return obj.mancc.tenncc if obj.mancc else "N/A"
    get_mancc.short_description = 'Nhà cung cấp'

    def get_manv(self, obj):
        return obj.manv.hoten if obj.manv else "N/A"
    get_manv.short_description = 'Nhân viên nhập'
    
    
from .forms import HoaDonForm
@admin.register(HoaDon)
class HoaDonAdmin(admin.ModelAdmin):
    form = HoaDonForm
    list_display = ('sohd','ngaylap','tongtien','trangthai','malop','mahv',)
    search_fields = ('sohd','malop','mahv',)
    list_filter = ('trangthai','malop','mahv',)


@admin.register(LichHoc)
class LichHocAdmin(admin.ModelAdmin):
    list_display = ('malich', 'ngayhoc', 'giohoc', 'sogiohoc', 'get_tenlop',)
    search_fields = ('malich', 'malop__tenlop',)  # Tìm kiếm theo tên lớp học
    list_filter = ('giohoc', 'sogiohoc', 'malop',)  # Lọc theo lớp học
    def get_tenlop(self, obj):
        return obj.malop.tenlop  # Lấy tên lớp từ ForeignKey
    get_tenlop.short_description = 'Tên lớp'  # Đặt tiêu đề cho cột

        
@admin.register(LopHoc)
class LopHocAdmin(admin.ModelAdmin):
    list_display = ('malop','tenlop','siso','tonggiohoc','hocphi','makh',)
    search_fields = ('tenlop','makh',)
    list_filter = ('tenlop','makh',)
    
    def save_model(self, request, obj, form, change):
        if obj.urlhinh:
            # Lấy tên file từ đường dẫn, bỏ tất cả các khoảng trắng
            file_name = os.path.basename(obj.urlhinh.name)
            
            # Lưu lại tên file vào trường urlhinh
            obj.urlhinh.name = file_name  # Đây sẽ là tên file không có đường dẫn
        
        # Gọi phương thức save_model của lớp cha để lưu model
        super().save_model(request, obj, form, change)
    
    