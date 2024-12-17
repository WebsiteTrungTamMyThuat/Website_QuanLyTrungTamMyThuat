from django.db import models
import os

class TaiKhoanNguoiDung(models.Model):
    QUYEN_CHOICES = [('GV', 'Giáo Viên'), ('HV', 'Học Viên'),]
    idtaikhoan = models.CharField(max_length=10, primary_key=True, db_column='idtaikhoan', verbose_name="ID")
    username = models.CharField(max_length=50, unique=True, db_column='username', verbose_name="Tên đăng nhập")
    pass_word = models.CharField(max_length=50, db_column='pass')
    quyen = models.CharField(max_length=10, choices=QUYEN_CHOICES, default='GV', verbose_name="Quyền")
    trangthai = models.CharField(max_length=50, verbose_name="Trạng thái")

    class Meta:
        db_table = 'taikhoannguoidung'
        verbose_name = "Tài khoản người dùng"
        verbose_name_plural = "Tài khoản người dùng"


        
class KhoaHoc(models.Model):
    makh = models.CharField(max_length=7, primary_key=True,verbose_name="Mã khóa học")
    tenkh = models.CharField(max_length=255, verbose_name="Tên khóa học")
    mota = models.TextField(verbose_name="Mô tả")
    hinhthuc = models.CharField(max_length=50, verbose_name="Hình thức")
    dotuoi = models.IntegerField(verbose_name="Độ tuổi")
    class Meta:
        db_table = 'khoahoc'
        verbose_name = "Khóa học"
        verbose_name_plural = "Khóa học"
    def __str__(self):
        return self.tenkh

class NoiDungKhoaHoc(models.Model):
    manoidung = models.AutoField(primary_key=True, verbose_name="Mã nội dung")
    tieude = models.CharField(max_length=255, verbose_name="Tiêu đề")
    class Meta:
        db_table = 'noidungkhoahoc'
        verbose_name = "Nội dung khóa học"
        verbose_name_plural = "Nội dung khóa học"
    def __str__(self):
        return self.tieude
    
        
class ChiTietKhoaHoc(models.Model):
    stt = models.IntegerField()
    makh = models.ForeignKey(KhoaHoc, on_delete=models.CASCADE, db_column='makh', verbose_name="Khóa học")
    manoidung = models.ForeignKey(NoiDungKhoaHoc, on_delete=models.CASCADE, db_column='manoidung', verbose_name="Nội dung")
    id = models.AutoField(primary_key=True, db_column='id')
    class Meta:
        db_table = 'chitietkhoahoc'
        verbose_name = "Chi tiết khóa học"
        verbose_name_plural = "Chi tiết khóa học"
    
import os
from django.conf import settings     
def upload_to_pageuser(instance, filename):
    # Đường dẫn lưu file: static/img/PageUser/<tên file>
    return os.path.join('PageUser', 'static', 'img', filename)
class LopHoc(models.Model):
    malop = models.CharField(max_length=7, primary_key=True, db_column='malop', verbose_name="Mã lớp")
    tenlop = models.CharField(max_length=100, verbose_name="Tên lớp")
    siso = models.IntegerField(verbose_name="Sĩ số")
    diadiemhoc = models.CharField(max_length=255, verbose_name="Địa điểm học")
    ngaybatdau = models.DateField(verbose_name="Ngày bắt đầu")
    tonggiohoc = models.IntegerField(verbose_name="Tổng giờ học")
    hocphi = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Học phí")
    makh = models.ForeignKey(KhoaHoc, on_delete=models.CASCADE, db_column='makh', verbose_name="Khóa học")
    magv = models.CharField(max_length=10, db_column='magv', verbose_name="Giáo viên")
    urlhinh = models.FileField(max_length=255, upload_to=upload_to_pageuser, verbose_name="Hình ảnh")
    tinhtrang = models.CharField(max_length=255, verbose_name="Tình trạng")
    class Meta:
        db_table = 'lophoc'
        verbose_name = "Lớp học"
        verbose_name_plural = "Lớp học"
    def __str__(self):
        return self.malop + " - " + self.tenlop
    def clean(self):
        self.malop = self.malop.strip()
        
class HocVien(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nu', 'Nữ'),]
    mahv = models.CharField(max_length=10, primary_key=True, verbose_name="Mã học viên")
    hoten = models.CharField(max_length=40, verbose_name="Tên học viên")
    email = models.CharField(max_length=255, verbose_name="Email")
    SDT = models.CharField(max_length=11, verbose_name="SĐT")
    GioiTinh = models.CharField(max_length=5, choices=GIOI_TINH_CHOICES, default='Nam', verbose_name="Giới tính")
    NgaySinh = models.DateField(verbose_name="Ngày sinh")
    DiaChi = models.CharField(max_length=255, verbose_name="Địa chỉ")
    class Meta:
        db_table = 'hocvien'
        verbose_name = "Học viên"
        verbose_name_plural = "Học viên"
    def __str__(self):
        return self.hoten
    
    
class HoaDon(models.Model):
    sohd = models.AutoField(primary_key=True)
    ngaylap = models.DateField(verbose_name="Ngày lập")
    tongtien = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng tiền")
    trangthai = models.CharField(max_length=20, verbose_name="Trạng thái")
    malop = models.ForeignKey('LopHoc', on_delete=models.CASCADE,db_column='malop', verbose_name="Lớp")
    mahv = models.ForeignKey('HocVien', on_delete=models.CASCADE, db_column='mahv', verbose_name="Học viên")
    class Meta:
        db_table = 'hoadon'
        verbose_name = "Hóa đơn"
        verbose_name_plural = "Hóa đơn"

    def __str__(self):
        return f"Hoa Don {self.sohd} - Học viên: {self.mahv.hoten} - Lớp: {self.malop.tenlop}"


        
class GiaoVien(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nu', 'Nữ'),]
    magv = models.CharField(max_length=10, primary_key=True, verbose_name="Mã giáo viên")
    hoten = models.CharField(max_length=255, verbose_name="Tên giáo viên")
    email = models.CharField(max_length=255, verbose_name="Email")
    SDT = models.CharField(max_length=11, verbose_name="SĐT")
    GioiTinh = models.CharField(max_length=5, choices=GIOI_TINH_CHOICES, default='Nam', verbose_name="Giới tính")
    NgaySinh = models.DateField(verbose_name="Ngày sinh")
    DiaChi = models.CharField(max_length=255, verbose_name="Địa chỉ")
    class Meta:
        db_table = 'giaovien'
        verbose_name = "Giáo viên"
        verbose_name_plural = "Giáo viên"
    def __str__(self):
        return self.hoten
    
        
        
class LichHoc(models.Model):
    malich = models.AutoField(primary_key=True, verbose_name="Mã lịch")
    ngayhoc = models.DateField(verbose_name="Ngày học")
    giohoc = models.TimeField(verbose_name="Giờ học")
    sogiohoc = models.IntegerField(verbose_name="Số giờ học")
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE, db_column='malop', verbose_name="Lớp")
    class Meta:
        db_table = 'lichhoc'
        verbose_name = "Lịch học"
        verbose_name_plural = "Lịch học"
        
class NhaCungCap(models.Model):
    mancc = models.AutoField(primary_key=True, verbose_name="Mã nhà cung cấp")
    tenncc = models.CharField(max_length=255, verbose_name="Tên nhà cung cấp")
    diachi = models.CharField(max_length=255, verbose_name="Địa chỉ")
    sdt = models.CharField(max_length=15, verbose_name="SĐT")
    class Meta:
        db_table = 'nhacc'
        verbose_name = "Nhà cung cấp"
        verbose_name_plural = "Nhà cung cấp"
    def __str__(self):
        return self.tenncc
        
from django.contrib.auth.models import User
class NhanVien(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nu', 'Nữ'),]
    manv = models.CharField(max_length=20, primary_key=True, db_column='manv', verbose_name="Mã nhân viên")
    hoten = models.CharField(max_length=255, verbose_name="Tên nhân viên")
    gioitinh = models.CharField(max_length=5, choices=GIOI_TINH_CHOICES,default='Nam', verbose_name="Giới tính")
    ngaysinh = models.DateField(verbose_name="Ngày sinh")
    diachi = models.CharField(max_length=255,verbose_name="Địa chỉ")
    sdt = models.CharField(max_length=11, verbose_name="SĐT")
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'nhanvien'
        verbose_name = "Nhân viên"
        verbose_name_plural = "Nhân viên"
    def __str__(self):
        return self.hoten

 
class DanhGia(models.Model):
    madanhgia = models.AutoField(primary_key=True, verbose_name="Mã đánh giá")
    mota = models.TextField(verbose_name="Mô tả")
    mahv = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='mahv', verbose_name="Học viên")
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE, db_column='malop', verbose_name="Lớp")
    class Meta:
        db_table = 'danhgia'
        verbose_name = "Đánh giá"
        verbose_name_plural = "Đánh giá"
    
        
class LichSuGiaoDich(models.Model):
    magiaodich = models.IntegerField(primary_key=True, verbose_name="Mã giao dịch")
    ngaygiaodich = models.DateField(verbose_name="Ngày giao dịch")
    sotien = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Số tiền")
    loaigiaodich = models.CharField(max_length=20, verbose_name="Loại giao dịch")
    ghichu = models.TextField(verbose_name="Ghi chú")

    class Meta:
        db_table = 'lichsugiaodich'
        verbose_name = "Lịch sử giao dịch"
        verbose_name_plural = "Lịch sử giao dịch"

    @classmethod
    def get_next_magiaodich(cls):
        last_entry = cls.objects.all().order_by('-magiaodich').first()
        if last_entry:
            return last_entry.magiaodich + 1
        return 1  # Nếu chưa có dữ liệu, bắt đầu từ 1
    
    def save(self, *args, **kwargs):
        if not self.magiaodich:  # Chỉ tự động gán giá trị khi magiaodich chưa có
            self.magiaodich = self.get_next_magiaodich()
        super().save(*args, **kwargs)


class HoaCu(models.Model):
    mahoacu = models.AutoField(primary_key=True, verbose_name="Mã họa cụ")
    tenhoacu = models.CharField(max_length=255, verbose_name="Tên họa cụ")
    soluong = models.IntegerField(verbose_name="Số lượng")
    class Meta:
        db_table = 'hoacu'
        verbose_name = "Họa cụ"
        verbose_name_plural = "Họa cụ"
    def __str__(self):
        return self.tenhoacu
          
class PhieuNhap(models.Model):
    maphieunhap = models.AutoField(primary_key=True,verbose_name="Mã phiếu nhập")
    ngaynhap = models.DateField(verbose_name="Ngày nhập")
    tongtien = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Tổng tiền")
    ghichu = models.TextField(verbose_name="Ghi chú")
    mancc = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, db_column="mancc",verbose_name="Nhà cung cấp")
    manv = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column="manv", verbose_name="Nhân viên nhập")
    class Meta:
        db_table = 'phieunhap'
        verbose_name = "Phiếu nhập"
        verbose_name_plural = "Phiếu nhập"
        
class ChiTietPhieuNhap(models.Model):
    soluong = models.IntegerField(verbose_name="Số lượng")
    dongia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Đơn giá")
    thanhtien = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Thành tiền")
    maphieunhap = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE, verbose_name="Phiếu nhập", primary_key=True)
    mahoacu = models.ForeignKey(HoaCu, on_delete=models.CASCADE, verbose_name="Họa cụ")
    class Meta:
        db_table = 'chitietphieunhap'
        verbose_name = "Chi tiết phiếu nhập"
        verbose_name_plural = "Chi tiết phiếu nhập"
        unique_together = ('maphieunhap', 'mahoacu')
        
    


class ChiTietPhieuNhap(models.Model):
    soluong = models.IntegerField(verbose_name="Số lượng")
    dongia = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Đơn giá")
    thanhtien = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Thành tiền")
    maphieunhap = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE, db_column='maphieunhap',verbose_name="Phiếu nhập")
    mahoacu = models.ForeignKey(HoaCu, on_delete=models.CASCADE, db_column='mahoacu', verbose_name="Họa cụ")
    class Meta:
        db_table = 'chitietphieunhap'
        verbose_name = "Chi tiết phiếu nhập"
        verbose_name_plural = "Chi tiết phiếu nhập"
        constraints = [
            models.UniqueConstraint(fields=['maphieunhap', 'mahoacu'], name='unique_maphieunhap_mahoacu')
        ]


