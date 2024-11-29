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
    
    if idtaikhoan:
        return render(request, 'pages/admin.html')
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
        lophoc = LopHoc.objects.filter(magv=idtaikhoan).values_list(flat=True)
    if taikhoan.quyen == 'HV':
        so_hoadon = HoaDon.objects.filter(mahv=idtaikhoan).values_list('malop', flat=True)
        lophoc = LopHoc.objects.filter(malop__in=so_hoadon)
        
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
    print(data)
    return render(request,'pages/admin-lophoc.html', {'dslop': data})


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
            "tongtien": hd.tongtien,
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
            "NgaySinh" : thongtincanhan.NgaySinh.strftime("%Y-%m-%d"),
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
            "NgaySinh" : thongtincanhan.NgaySinh.strftime("%Y-%m-%d"),
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


@never_cache
def dangxuat(request,idtaikhoan):
    username = request.session.get('user_username', None)
    checklogin(idtaikhoan, username)
    request.session.flush()  # Xóa toàn bộ session
    logout(request)
    return redirect('logout')