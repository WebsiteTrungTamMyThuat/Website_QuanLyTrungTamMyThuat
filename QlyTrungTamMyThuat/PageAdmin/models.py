from django.db import models

class TaiKhoanNguoiDung(models.Model):
    idtaikhoan = models.CharField(max_length=10, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    pass_word = models.CharField(max_length=50)
    sdt = models.CharField(max_length=11)
    gioitinh = models.CharField(max_length=5)
    ngaysinh = models.DateField()
    diachi = models.CharField(max_length=255)
    quyen = models.CharField(max_length=10)
    trangthai = models.CharField(max_length=50)

class TaiKhoanNhanVien(models.Model):
    username = models.CharField(max_length=5, primary_key=True)
    pass_word = models.CharField(max_length=50)
    quyen = models.CharField(max_length=50)
    trangthai = models.CharField(max_length=50)

class KhoaHoc(models.Model):
    makh = models.CharField(max_length=7, primary_key=True)
    tenkh = models.CharField(max_length=255)
    mota = models.TextField()
    hinhanh = models.CharField(max_length=50)

class LopHoc(models.Model):
    malop = models.CharField(max_length=7, primary_key=True)
    tenlop = models.CharField(max_length=100)
    siso = models.IntegerField()
    diadiemhoc = models.CharField(max_length=255)
    ngaybatdau = models.DateField()
    tonggiohoc = models.IntegerField()
    hocphi = models.DecimalField(max_digits=10, decimal_places=2)
    makh = models.ForeignKey(KhoaHoc, on_delete=models.CASCADE)
    magv = models.CharField(max_length=10)

class HocVien(models.Model):
    mahv = models.CharField(max_length=10, primary_key=True)
    hoten = models.CharField(max_length=40)
    gioitinh = models.CharField(max_length=5)
    ngaysinh = models.DateField()
    diachi = models.CharField(max_length=255)
    sdt = models.CharField(max_length=11)
    cccd = models.CharField(max_length=12)

class HoaDon(models.Model):
    mahd = models.CharField(max_length=5, primary_key=True)
    ngaylap = models.DateField()
    tongtien = models.DecimalField(max_digits=10, decimal_places=2)
    trangthai = models.CharField(max_length=20)
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE)
    mahv = models.ForeignKey(HocVien, on_delete=models.CASCADE)

class GiaoVien(models.Model):
    magv = models.CharField(max_length=10, primary_key=True)
    hoten = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class LichHoc(models.Model):
    malich = models.AutoField(primary_key=True)
    ngayhoc = models.DateField()
    giohoc = models.TimeField()
    sogiohoc = models.IntegerField()
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE)

class NhaCungCap(models.Model):
    mancc = models.CharField(max_length=5, primary_key=True)
    tenncc = models.CharField(max_length=255)
    diachi = models.CharField(max_length=255)
    sdt = models.CharField(max_length=15)

class NhapVien(models.Model):
    manv = models.CharField(max_length=5, primary_key=True)
    hoten = models.CharField(max_length=255)
    gioitinh = models.CharField(max_length=5)
    ngaysinh = models.DateField()
    diachi = models.CharField(max_length=255)
    sdt = models.CharField(max_length=11)

class DanhGia(models.Model):
    madanhgia = models.AutoField(primary_key=True)
    mota = models.TextField()
    mahv = models.ForeignKey(HocVien, on_delete=models.CASCADE)
    malop = models.ForeignKey(LopHoc, on_delete=models.CASCADE)

class LichSuGiaoDich(models.Model):
    magiaodich = models.AutoField(primary_key=True)
    ngaygiaodich = models.DateField()
    sotien = models.DecimalField(max_digits=10, decimal_places=2)
    loaigiaodich = models.CharField(max_length=20)
    ghichu = models.TextField()
    mahv = models.ForeignKey(HocVien, on_delete=models.CASCADE)

class PhieuNhap(models.Model):
    maphieunhap = models.AutoField(primary_key=True)
    ngaynhap = models.DateField()
    tongtien = models.DecimalField(max_digits=10, decimal_places=2)
    ghichu = models.TextField()
    mancc = models.ForeignKey(NhaCungCap, on_delete=models.CASCADE)
    manv = models.ForeignKey(NhapVien, on_delete=models.CASCADE)

class ChiTietPhieuNhap(models.Model):
    soluong = models.IntegerField()
    dongia = models.DecimalField(max_digits=10, decimal_places=2)
    thanhtien = models.DecimalField(max_digits=10, decimal_places=2)
    maphieunhap = models.ForeignKey(PhieuNhap, on_delete=models.CASCADE)
    mahoacu = models.ForeignKey('HoaCu', on_delete=models.CASCADE)

class HoaCu(models.Model):
    mahoacu = models.AutoField(primary_key=True)
    tenhoacu = models.CharField(max_length=255)
    soluong = models.IntegerField()
