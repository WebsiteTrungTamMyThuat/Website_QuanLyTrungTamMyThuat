from django.db import models
import os

class TaiKhoanNguoiDung(models.Model):
    QUYEN_CHOICES = [('GV', 'Giáo Viên'), ('HV', 'Học Viên'),]
    idtaikhoan = models.CharField(max_length=10, primary_key=True, db_column='idtaikhoan')
    username = models.CharField(max_length=50, unique=True, db_column='username')
    pass_word = models.CharField(max_length=50, db_column='pass')
    quyen = models.CharField(max_length=10, choices=QUYEN_CHOICES, default='GV')
    trangthai = models.CharField(max_length=50)

    class Meta:
        db_table = 'taikhoannguoidung'


        
class KhoaHoc(models.Model):
    makh = models.CharField(max_length=7, primary_key=True)
    tenkh = models.CharField(max_length=255)
    mota = models.TextField()
    hinhthuc = models.CharField(max_length=50)
    dotuoi = models.IntegerField()
    class Meta:
        db_table = 'khoahoc'
    def __str__(self):
        return self.tenkh

class NoiDungKhoaHoc(models.Model):
    manoidung = models.AutoField(primary_key=True)
    tieude = models.CharField(max_length=255)
    class Meta:
        db_table = 'noidungkhoahoc'
    def __str__(self):
        return self.tieude
        
class ChiTietKhoaHoc(models.Model):
    stt = models.IntegerField()
    makh = models.ForeignKey(KhoaHoc, on_delete=models.CASCADE, db_column='makh')
    manoidung = models.ForeignKey(NoiDungKhoaHoc, on_delete=models.CASCADE, db_column='manoidung')
    id = models.IntegerField(primary_key=True, db_column='id')
    class Meta:
        db_table = 'chitietkhoahoc'
    
        
class LopHoc(models.Model):
    malop = models.CharField(max_length=7, primary_key=True, db_column='malop')
    tenlop = models.CharField(max_length=100)
    siso = models.IntegerField()
    diadiemhoc = models.CharField(max_length=255)
    ngaybatdau = models.DateField()
    tonggiohoc = models.IntegerField()
    hocphi = models.DecimalField(max_digits=10, decimal_places=2)
    makh = models.ForeignKey(KhoaHoc, on_delete=models.CASCADE, db_column='makh')
    magv = models.CharField(max_length=10, db_column='magv')
    urlhinh = models.CharField(max_length=255)
    tinhtrang = models.CharField(max_length=255)
    class Meta:
        db_table = 'lophoc'
    def __str__(self):
        return self.malop + " - " + self.tenlop
    def clean(self):
        self.malop = self.malop.strip()
    def save(self, *args, **kwargs):
        if self.urlhinh:
            self.urlhinh.name = os.path.basename(self.urlhinh.name)
        super().save(*args, **kwargs)
        
class HocVien(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nu', 'Nữ'),]
    mahv = models.CharField(max_length=10, primary_key=True)
    hoten = models.CharField(max_length=40)
    email = models.CharField(max_length=255)
    SDT = models.CharField(max_length=11)
    GioiTinh = models.CharField(max_length=5, choices=GIOI_TINH_CHOICES, default='Nam')
    NgaySinh = models.DateField()
    DiaChi = models.CharField(max_length=255)
    class Meta:
        db_table = 'hocvien'
    def __str__(self):
        return self.hoten
    
    
class HoaDon(models.Model):
    sohd = models.AutoField(primary_key=True)
    ngaylap = models.DateField()
    tongtien = models.DecimalField(max_digits=10, decimal_places=2)
    trangthai = models.CharField(max_length=20)
    malop = models.ForeignKey('LopHoc', on_delete=models.CASCADE,db_column='malop')
    mahv = models.ForeignKey('HocVien', on_delete=models.CASCADE, db_column='mahv')
    class Meta:
        db_table = 'hoadon'

    def __str__(self):
        return f"Hoa Don {self.sohd} - Học viên: {self.mahv.hoten} - Lớp: {self.malop.tenlop}"


        
class GiaoVien(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nu', 'Nữ'),]
    magv = models.CharField(max_length=10, primary_key=True)
    hoten = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    SDT = models.CharField(max_length=11)
    GioiTinh = models.CharField(max_length=5, choices=GIOI_TINH_CHOICES, default='Nam')
    NgaySinh = models.DateField()
    DiaChi = models.CharField(max_length=255)
    class Meta:
        db_table = 'giaovien'
    def __str__(self):
        return self.hoten
    
        
        
class LichHoc(models.Model):
    malich = models.AutoField(primary_key=True)
    ngayhoc = models.DateField()
    giohoc = models.TimeField()
    sogiohoc = models.IntegerField()
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE, db_column='malop')
    class Meta:
        db_table = 'lichhoc'
        
class NhaCungCap(models.Model):
    mancc = models.AutoField(primary_key=True)
    tenncc = models.CharField(max_length=255)
    diachi = models.CharField(max_length=255)
    sdt = models.CharField(max_length=15)
    class Meta:
        db_table = 'nhacc'
    def __str__(self):
        return self.tenncc
        
from django.contrib.auth.models import User
class NhanVien(models.Model):
    GIOI_TINH_CHOICES = [('Nam', 'Nam'), ('Nu', 'Nữ'),]
    manv = models.CharField(max_length=20, primary_key=True, db_column='manv')
    hoten = models.CharField(max_length=255)
    gioitinh = models.CharField(max_length=5, choices=GIOI_TINH_CHOICES,default='Nam')
    ngaysinh = models.DateField()
    diachi = models.CharField(max_length=255)
    sdt = models.CharField(max_length=11)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    class Meta:
        db_table = 'nhanvien'
    def __str__(self):
        return self.hoten

class TaiKhoanNhanVien(models.Model):
    username = models.CharField(max_length=20, primary_key=True)
    pass_word = models.CharField(max_length=50, db_column='pass')
    quyen = models.CharField(max_length=50)
    trangthai = models.CharField(max_length=50)
    class Meta:
        db_table = 'taikhoannhanvien'

 
class DanhGia(models.Model):
    madanhgia = models.AutoField(primary_key=True)
    mota = models.TextField()
    mahv = models.ForeignKey(HocVien, on_delete=models.CASCADE, db_column='mahv')
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE, db_column='malop')
    class Meta:
        db_table = 'danhgia'
    
        
class LichSuGiaoDich(models.Model):
    magiaodich = models.IntegerField(primary_key=True)
    ngaygiaodich = models.DateField()
    sotien = models.DecimalField(max_digits=10, decimal_places=2)
    loaigiaodich = models.CharField(max_length=20)
    ghichu = models.TextField()

    class Meta:
        db_table = 'lichsugiaodich'

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
class PhieuNhap(models.Model):
    maphieunhap = models.AutoField(primary_key=True)
    ngaynhap = models.DateField()
    tongtien = models.DecimalField(max_digits=10, decimal_places=2)
    ghichu = models.TextField()
    mancc = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE, db_column="mancc")
    manv = models.ForeignKey(NhanVien, on_delete=models.CASCADE, db_column="manv")
    class Meta:
        db_table = 'phieunhap'
        
class ChiTietPhieuNhap(models.Model):
    soluong = models.IntegerField()
    dongia = models.DecimalField(max_digits=10, decimal_places=2)
    thanhtien = models.DecimalField(max_digits=10, decimal_places=2)
    maphieunhap = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE)
    mahoacu = models.ForeignKey('HoaCu', on_delete=models.CASCADE)
    class Meta:
        db_table = 'chitietphieunhap'
        
class HoaCu(models.Model):
    mahoacu = models.AutoField(primary_key=True)
    tenhoacu = models.CharField(max_length=255)
    soluong = models.IntegerField()
    class Meta:
        db_table = 'hoacu'
    def __str__(self):
        return self.tenhoacu



class ChiTietPhieuNhap(models.Model):
    soluong = models.IntegerField()
    dongia = models.DecimalField(max_digits=10, decimal_places=2)
    thanhtien = models.DecimalField(max_digits=10, decimal_places=2)
    maphieunhap = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE, db_column='maphieunhap')
    mahoacu = models.ForeignKey(HoaCu, on_delete=models.CASCADE, db_column='mahoacu')
    class Meta:
        db_table = 'chitietphieunhap'
        constraints = [
            models.UniqueConstraint(fields=['maphieunhap', 'mahoacu'], name='unique_maphieunhap_mahoacu')
        ]


