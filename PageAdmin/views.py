from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse,Http404 
from .models import *
from django.db import transaction, connection
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate ,login,logout

from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.messages import get_messages
from django.views.decorators.cache import never_cache
from datetime import timedelta
from django.utils.timezone import now
from django.db.models import Sum




def checklogin(idtaikhoan, username):
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    if taikhoan is None or taikhoan.username != username:
        raise Http404("Không tìm thấy tài khoản hoặc bạn không có quyền truy cập.")

# Create your views herede
def admin(request, idtaikhoan):
    request.session['idtaikhoan'] = idtaikhoan.strip()
    username = request.session.get('user_username', None)
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    
    today = now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Thứ Hai
    end_of_week = start_of_week + timedelta(days=6) # Chủ Nhật
        
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    request.session['quyen'] = taikhoan.quyen
    
    if taikhoan.quyen == 'GV':
        lop_dang_hoc = LopHoc.objects.filter(magv=idtaikhoan, tinhtrang="Đang học")
        so_luong_lop_dang_hoc = lop_dang_hoc.count()
        
        so_luong_lich_trong_tuan = LichHoc.objects.filter(
            malop__in=lop_dang_hoc,
            ngayhoc__range=[start_of_week, end_of_week]
        ).select_related('malop')
        
        danh_sach_lop = []
        for lich in so_luong_lich_trong_tuan:
            danh_sach_lop.append({
                "malop": lich.malop.malop,
                "tenlop": lich.malop.tenlop,
                "ngayhoc": lich.ngayhoc.strftime("%d-%m-%Y"),
                "giohoc": lich.giohoc.strftime("%H:%M"),
                "diadiem": lich.malop.diadiemhoc,
            })
            
        return render(request, 'pages/admin.html', {
            'so_luong_lop_dang_hoc': so_luong_lop_dang_hoc,
            'so_luong_lich_trong_tuan': so_luong_lich_trong_tuan.count(),
            'taikhoan': taikhoan,
            'dslop' : danh_sach_lop
        })
        
    if taikhoan.quyen == 'HV':
        # Hóa đơn chưa thanh toán
        hoadon_chua_tt = HoaDon.objects.filter(mahv=idtaikhoan, trangthai="Chưa thanh toán")
        hoadon_da_tt = HoaDon.objects.filter(mahv=idtaikhoan, trangthai="Đã thanh toán")
        
        tong_tien_chua_tt = hoadon_chua_tt.aggregate(total=Sum('tongtien'))['total'] or 0

        # Mã lớp từ hóa đơn chưa thanh toán
        ma_lop_chua_tt = hoadon_chua_tt.values_list('malop', flat=True)
        ma_lop_da_tt = hoadon_da_tt.values_list('malop', flat=True)
        
        # Lớp học đang học
        hoadon = HoaDon.objects.filter(mahv=idtaikhoan, trangthai="Đã thanh toán").values_list('malop', flat=True)
        lop_dang_hoc = LopHoc.objects.filter(malop__in=hoadon, tinhtrang="Đang học")
        so_luong_lop_dang_hoc = lop_dang_hoc.count()
        
        
        
        so_luong_lich_trong_tuan = LichHoc.objects.filter(
            malop__in=ma_lop_da_tt,
            ngayhoc__range=[start_of_week, end_of_week]
        ).select_related('malop')
        
        danh_sach_lop = []
        for lich in so_luong_lich_trong_tuan:
            danh_sach_lop.append({
                "malop": lich.malop.malop,
                "tenlop": lich.malop.tenlop,
                "ngayhoc": lich.ngayhoc.strftime("%d-%m-%Y"),
                "giohoc": lich.giohoc.strftime("%H:%M"),
                "diadiem": lich.malop.diadiemhoc,
            })
            
        return render(request, 'pages/admin.html', {
            'tong_tien_chua_tt': tong_tien_chua_tt,
            'so_luong_lop_dang_hoc': so_luong_lop_dang_hoc,
            'so_luong_lich_trong_tuan': so_luong_lich_trong_tuan.count(),
            'taikhoan': taikhoan
        })

    return render(request, '403.html', status=403)
    
    
@api_view(['GET'])   
def lichhoc(request, idtaikhoan):
    
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    
    username = request.session.get('user_username', None)
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    
    if taikhoan.quyen == 'GV':
        malop_list = LopHoc.objects.filter(magv=idtaikhoan).values_list('malop', flat=True)
        lich_hoc = LichHoc.objects.filter(malop__in=malop_list).select_related('malop')
        
    
    elif taikhoan.quyen == 'HV':
        malop_list = HoaDon.objects.filter(mahv=idtaikhoan, trangthai="Đã thanh toán").values_list('malop', flat=True)
        lich_hoc = LichHoc.objects.filter(malop__in=malop_list).select_related('malop')
    
    data = [
        {
            "date": lich.ngayhoc.strftime("%Y-%m-%d"),
            "time": f"{lich.giohoc.strftime('%H:%M')} - {(lich.giohoc.hour + lich.sogiohoc):02}:00",
            "className": lich.malop.tenlop,
            "room": lich.malop.diadiemhoc,
            "startTime": lich.giohoc.strftime("%H:%M"),
            "totalTime": f"{lich.sogiohoc}h",
            "color": "orange", 
        }
        for lich in lich_hoc
    ]
    #return Response(data)
    return render(request, 'pages/admin-lichhoc.html', {'lich_hoc': data, 'idtaikhoan': idtaikhoan})



def lophoc(request, idtaikhoan):
    request.session['idtaikhoan'] = idtaikhoan.strip()
    username = request.session.get('user_username', None)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    
    if taikhoan.quyen == 'GV':
        lophoc = LopHoc.objects.filter(magv=idtaikhoan)
    if taikhoan.quyen == 'HV':
        so_hoadon = HoaDon.objects.filter(mahv=idtaikhoan, trangthai="Đã thanh toán").values_list('malop', flat=True)
        lophoc = LopHoc.objects.filter(malop__in=so_hoadon)
        
    data = [
        {
            "malop": item.malop,
            "tenlop" : item.tenlop,
            "diadiem" : item.diadiemhoc,
            "hocphi" : f"{item.hocphi} VNĐ",
            "tinhtrang" : item.tinhtrang.strip(),
            "status_btn": item.tinhtrang.strip() if item.tinhtrang.strip() == "Hoàn thành" else None,
            "taikhoan" : taikhoan
        }
        for item in lophoc
    ]
    print(data)
    return render(request,'pages/admin-lophoc.html', {'dslop': data, 'taikhoan': taikhoan})


def thanhtoan(request, idtaikhoan):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    
    if taikhoan.quyen == 'GV':
        return render(request,'pages/admin-thanhtoan.html')
    if taikhoan.quyen == 'HV':
        hoadon = HoaDon.objects.filter(mahv=idtaikhoan).select_related('malop')
        
    data = [
        {
            "sohd" : hd.sohd,
            "ngaylap" : hd.ngaylap.strftime("%d-%m-%Y"),
            "lop": hd.malop.tenlop if hd.malop else "",
            "tongtien": f"{hd.tongtien} VNĐ ",
            "trangthai" : hd.trangthai
        }
        for hd in hoadon
    ]
      
    return render(request,'pages/admin-thanhtoan.html', {'dshd':data})


def thongtincanhan(request, idtaikhoan):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    thongtincanhan = None
    
    if taikhoan.quyen == 'GV':
        thongtincanhan = GiaoVien.objects.filter(magv=idtaikhoan).first()
        data = {
            "mahv" : thongtincanhan.magv,
            "tenhv" : thongtincanhan.hoten,
            "email" : thongtincanhan.email,
            "SDT"   : thongtincanhan.SDT,
            "GioiTinh": thongtincanhan.GioiTinh,
            "NgaySinh" : thongtincanhan.NgaySinh.strftime("%Y-%m-%d") if thongtincanhan.NgaySinh else None,
            "DiaChi" : thongtincanhan.DiaChi
        }
    
    if taikhoan.quyen == 'HV':
        thongtincanhan = HocVien.objects.filter(mahv=idtaikhoan).first()
        data = {
            "mahv" : thongtincanhan.mahv,
            "tenhv" : thongtincanhan.hoten,
            "email" : thongtincanhan.email,
            "SDT"   : thongtincanhan.SDT,
            "GioiTinh": thongtincanhan.GioiTinh,
            "NgaySinh" : thongtincanhan.NgaySinh.strftime("%Y-%m-%d") if thongtincanhan.NgaySinh else None,
            "DiaChi" : thongtincanhan.DiaChi
        }
    if not thongtincanhan:
        return render(request, '404.html', status=404)
    
    
    return render(request,'pages/admin-hocvien.html', {'thongtincanhan' : data})


def luuthongtincanhan(request, idtaikhoan):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    if request.method == "POST":
        # Lấy thông tin từ form
        
        gioitinh = request.POST.get('gioitinh')
        sodienthoai = request.POST.get('sdt')
        ngaysinh = request.POST.get('ngaysinh')
        diachi = request.POST.get('diachi')
        
        print(f"Dữ liệu POST: {gioitinh}, {sodienthoai}, {ngaysinh}, {diachi}")
        if taikhoan.quyen == 'GV':
            giaovien = GiaoVien.objects.filter(magv=idtaikhoan).first()
            if giaovien:
                    giaovien.GioiTinh = gioitinh
                    giaovien.SDT = sodienthoai
                    giaovien.NgaySinh = ngaysinh
                    giaovien.DiaChi = diachi
                    giaovien.save()
                    connection.commit()
                    messages.success(request, "Cập nhật thông tin thành công.")
                    return redirect('thongtincanhan', idtaikhoan=idtaikhoan)
            else:
                    # Nếu không tìm thấy học viên
                    messages.error(request, "Không tìm thấy thông tin giáo viên.")
                    return render(request, '404.html', status=404)
                
        if taikhoan.quyen == 'HV':
            hocvien = HocVien.objects.filter(mahv=idtaikhoan).first()
            if hocvien:
                    hocvien.GioiTinh = gioitinh
                    hocvien.SDT = sodienthoai
                    hocvien.NgaySinh = ngaysinh
                    hocvien.DiaChi = diachi
                    hocvien.save()
                    connection.commit()
                    messages.success(request, "Cập nhật thông tin thành công.")
                    return redirect('thongtincanhan', idtaikhoan=idtaikhoan)
            else:
                    # Nếu không tìm thấy học viên
                    messages.error(request, "Không tìm thấy thông tin học viên.")
                    return render(request, '404.html', status=404)
            
     # Xóa các messages còn tồn tại
    storage = get_messages(request)
    for _ in storage:
        pass  # Xóa tất cả các messages
    
    return redirect('thongtincanhan', idtaikhoan=idtaikhoan)

def doimatkhau(request, idtaikhoan):
     # Xóa các messages còn tồn tại
    storage = get_messages(request)
    for _ in storage:
        pass  # Xóa tất cả các messages
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    if request.method == "POST":
        mkcu = request.POST.get('matkhaucu')
        mkmoi = request.POST.get('matkhaumoi')
            
        if taikhoan and taikhoan.pass_word == mkcu:
            taikhoan.pass_word = mkmoi
            taikhoan.save()
            connection.commit()
            messages.success(request, "Đổi mật khẩu thành công.")
            return redirect('thongtincanhan', idtaikhoan=idtaikhoan)
        else:
            messages.error(request, "Mật khẩu cũ không trùng khớp")
            
    
    return render(request,'pages/doimatkhau.html')


def danhsachhocvien(request, idtaikhoan, malop):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    
    so_hoadon = HoaDon.objects.filter(malop=malop).values_list('mahv', flat=True)
    hocvien = HocVien.objects.filter(mahv__in=so_hoadon)
    
    return render(request,'pages/admin-danhsachhocvien.html', {'dshv' : hocvien})

def danhgia(request, idtaikhoan, malop):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    
    danhgia_list = DanhGia.objects.filter(mahv=idtaikhoan, malop=malop)
    if danhgia_list.exists():
        messages.error(request, "Bạn đã đánh giá lớp học này rồi!")
        return redirect('lophoc_admin', idtaikhoan=idtaikhoan)   
     
    if request.method == "POST":
        danhgia = request.POST.get('danhgia')
        
        try:
            hocvien = HocVien.objects.get(mahv=idtaikhoan)  
        except HocVien.DoesNotExist:
            return HttpResponse("Học viên không tồn tại", status=404)

        try:
            lop = LopHoc.objects.get(malop=malop) 
        except LopHoc.DoesNotExist:
            return HttpResponse("Lớp học không tồn tại", status=404)
            
        DanhGia.objects.create(
                mahv=hocvien,
                malop=lop,  
                mota=danhgia
            )
        messages.success(request, "Đánh giá lớp học thành công.")
        return redirect('lophoc_admin', idtaikhoan=idtaikhoan)
    return render(request,'pages/danhgia.html', {'idtaikhoan':idtaikhoan, 'malop':malop})
    
@never_cache
def dangxuat(request,idtaikhoan):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    request.session.flush()  # Xóa toàn bộ session
    logout(request)
    return redirect('logout')


def search_dslop(request, idtaikhoan):
    from django.db.models import Q
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    
    if request.method == "POST":
        tenlop = request.POST.get('search_ten')

    if taikhoan.quyen == 'GV':
        lophoc = LopHoc.objects.filter(magv=idtaikhoan)
    if taikhoan.quyen == 'HV':
        so_hoadon = HoaDon.objects.filter(mahv=idtaikhoan).values_list('malop', flat=True)
        lophoc = LopHoc.objects.filter(malop__in=so_hoadon)
    else:
        lophoc = LopHoc.objects.none()
    
    if tenlop != None:
        lophoc = LopHoc.objects.filter(Q(tenlop__icontains=tenlop))
    data = [
        {
            "malop": item.malop,
            "tenlop" : item.tenlop,
            "diadiem" : item.diadiemhoc,
            "hocphi" : f"{item.hocphi} VNĐ",
            "tinhtrang" : item.tinhtrang.strip(),
            "status_btn": item.tinhtrang.strip() if item.tinhtrang.strip() == "Hoàn thành" else None
        }
        for item in lophoc
    ]
    return render(request,'pages/admin-lophoc.html', {'dslop': data, 'taikhoan': taikhoan})


def search_lsgd(request, idtaikhoan):
    from django.db.models import Q
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    if request.method == "POST":
        tenlop = request.POST.get('seach_lsgd')
        
    if taikhoan.quyen == 'GV':
        return render(request,'pages/admin-thanhtoan.html')
    if taikhoan.quyen == 'HV':
        hoadon = HoaDon.objects.filter(mahv=idtaikhoan).select_related('malop')
        
    if tenlop:
        hoadon = hoadon.filter(malop__tenlop__icontains=tenlop)
    data = [
        {
            "sohd" : hd.sohd,
            "ngaylap" : hd.ngaylap.strftime("%d-%m-%Y"),
            "lop": hd.malop.tenlop if hd.malop else "",
            "tongtien": f"{hd.tongtien} VNĐ ",
            "trangthai" : hd.trangthai
        }
        for hd in hoadon
    ]
      
    return render(request,'pages/admin-thanhtoan.html', {'dshd':data})