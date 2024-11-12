from django.shortcuts import render
from django.http import HttpResponse 

# Create your views herede
def admin(request):
    return render(request, 'pages/admin.html')

def giaovien(request):
    return render(request,'pages/admin-giaovien.html')

def khoahoc(request):
    return render(request,'pages/admin-khoahoc.html')

def hocvien(request):
    return render(request,'pages/admin-hocvien.html')

def thanhtoan(request):
    return render(request,'pages/admin-thanhtoan.html')

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