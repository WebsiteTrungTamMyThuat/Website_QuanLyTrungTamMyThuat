from django.shortcuts import render
from django.http import HttpResponse 

# Create your views herede
def user(request):
    return render(request, 'pages/user.html')

def dangky(request):
    return render(request,'layout/dangky.html')

def dangnhap(request):
    return render(request,'layout/dangnhap.html')

def quenmk(request):
    return render(request,'layout/quenmk.html')

def dangkytuvan(request):
    return render(request,'pages/dang-ky-tu-van.html')

def gioithieu(request):
    return render(request,'pages/gioithieu.html')

def chinhsachbaomat(request):
    return render(request,'pages/chinh-sach-bao-mat.html')

def hdthanhtoan(request):
    return render(request,'pages/huong-dan-thanh-toan.html')

def chinhsachdichvu(request):
    return render(request,'pages/chinh-sach-dich-vu.html')

def khoahoc(request):
    return render(request,'pages/khoahoc.html')

def ttkhoahoc(request):
    return render(request,'pages/thong-tin-khoa-hoc.html')

def giaovien(request):
    return render(request, 'pages/giao-vien.html')

def chitietgiaovien(request):
    return render(request, 'pages/chi-tiet-giao-vien.html')