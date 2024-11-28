from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse,Http404 
from .models import *
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views herede
@login_required
def admin(request, idtaikhoan):
    request.session['idtaikhoan'] = idtaikhoan.strip()
    username = request.session.get('user_username', None)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    if taikhoan is None or taikhoan.username != username:
        raise Http404("Không tìm thấy tài khoản hoặc bạn không có quyền truy cập.")
    
    
    if idtaikhoan:
        return render(request, 'pages/admin.html')
    return render(request, '403.html', status=403)
    
    
@api_view(['GET'])   
def lichhoc(request, idtaikhoan):
    
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    
    username = request.session.get('user_username', None)
    taikhoan = TaiKhoanNguoiDung.objects.filter(idtaikhoan=idtaikhoan).first()
    if taikhoan is None or taikhoan.username != username:
        return HttpResponse("Bạn không có quyền truy cập vào tài khoản này.", status=403)
    
    if taikhoan.quyen == 'GV':
        malop_list = LopHoc.objects.filter(magv=idtaikhoan).values_list('malop', flat=True)
        lich_hoc = LichHoc.objects.filter(malop__in=malop_list).select_related('malop')
        if not lich_hoc.exists():
            return Response({"message": "Không có lịch học cho học viên này."}, status=404)
    
    elif taikhoan.quyen == 'HV':
        malop_list = HoaDon.objects.filter(mahv=idtaikhoan).values_list('malop', flat=True)
        lich_hoc = LichHoc.objects.filter(malop__in=malop_list).select_related('malop')
        
        if not lich_hoc.exists():
            return Response({"message": "Không có lịch học cho học viên này."}, status=404)
    
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



def giaovien(request):
    return render(request,'pages/admin-giaovien.html')


def hocvien(request):
    return render(request,'pages/admin-hocvien.html')

def thanhtoan(request):
    return render(request,'pages/admin-thanhtoan.html')


def them_gv(request):
    
    if request.method == 'POST':
        try:
            with transaction.atomic():
                    data = request.POST
                    magv = data.get("magv")
                    hoten = data.get("hoten")
                    email = data.get("email")
                    SDT = data.get("SDT")
                    GioiTinh = data.get("GioiTinh")
                    NgaySinh = data.get("NgaySinh")
                    
                    if magv and hoten and email and SDT and GioiTinh and NgaySinh:
                        TaiKhoanNguoiDung.objects.create(
                            idtaikhoan = magv,
                            username = email,
                            pass_word = "123456",
                            quyen = "GV",
                            trangthai = "Đang hoạt động"
                        )
                        
                        GiaoVien.objects.create(
                        magv=magv,
                        hoten=hoten,
                        email=email,
                        SDT=SDT,
                        GioiTinh=GioiTinh,
                        NgaySinh=NgaySinh
                        )
                        messages.success(request, 'Thêm giáo viên thành công!')
                        return HttpResponseRedirect(reverse('giaovien_admin')) 
                    else:
                        return render(request, 'pages/Them-Xoa-Sua/them-giaovien.html', {
                        'error_message': 'Vui lòng điền đầy đủ thông tin!'
                        })
        except Exception as e:
            return render(request, 'pages/Them-Xoa-Sua/them-giaovien.html', {
                'error_message': f"Đã xảy ra lỗi: {str(e)}"
            })
    
    return render(request,'pages/Them-Xoa-Sua/them-giaovien.html')

def them_hv(request):
    return render(request,'pages/Them-Xoa-Sua/them-hocvien.html')

def them_kh(request):
    return render(request,'pages/Them-Xoa-Sua/them-khoahoc.html')

def them_hd(request):
    return render(request,'pages/Them-Xoa-Sua/them-thanhtoan.html')

def sua_gv(request):
    return render(request,'pages/Them-Xoa-Sua/sua-giaovien.html')

def sua_hv(request):
    return render(request,'pages/Them-Xoa-Sua/sua-hocvien.html')

def sua_kh(request):
    return render(request,'pages/Them-Xoa-Sua/sua-khoahoc.html')

def sua_hd(request):
    return render(request,'pages/Them-Xoa-Sua/sua-thanhtoan.html')