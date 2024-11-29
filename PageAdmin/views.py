from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse,Http404 
from .models import *
from django.db import transaction
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from rest_framework.response import Response
from rest_framework.decorators import api_view




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
        malop_list = HoaDon.objects.filter(mahv=idtaikhoan).values_list('malop', flat=True)
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
            "tinhtrang" : item.tinhtrang
        }
        for item in lophoc
    ]
        
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
    
    if taikhoan.quyen == 'GV':
        return render(request,'pages/admin-thanhtoan.html')
    thongtincanhan = None
    if taikhoan.quyen == 'HV':
        thongtincanhan = HocVien.objects.filter(mahv=idtaikhoan).first()

    if not thongtincanhan:
        return render(request, '404.html', status=404)
    return render(request,'pages/admin-hocvien.html', {'thongtincanhan' : thongtincanhan})


def them_gv(request):
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