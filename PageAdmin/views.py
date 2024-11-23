from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse 
from .models import *
from django.db import transaction
from django.contrib import messages
from django.urls import reverse

# Create your views herede
def admin(request):
    return render(request, 'pages/admin.html')

def giaovien(request):
    dsgv = GiaoVien.objects.all()
    dstk = TaiKhoanNguoiDung.objects.all()
    
    data = [
        {
            'magv': gv.magv,
            'hoten': gv.hoten,
            'email': gv.email,
            'GioiTinh':gv.GioiTinh,
            'NgaySinh':gv.NgaySinh,
            'SDT': gv.SDT,
            'taikhoan': dstk.filter(idtaikhoan=gv.magv).values('trangthai').first()
        }
        for gv in dsgv
    ]
    
    return render(request,'pages/admin-giaovien.html',{'ds_gv': data})

def lichhoc(request):
    return render(request,'pages/admin-khoahoc.html')

def hocvien(request):
    dshv = HocVien.objects.all()
    dstk = TaiKhoanNguoiDung.objects.all()
    
    data = [
        {
            'magv':hv.mahv,
            'hoten': hv.hoten,
            'email': hv.email,
            'GioiTinh':hv.GioiTinh,
            'NgaySinh':hv.NgaySinh,
            'SDT': hv.SDT,
            'taikhoan': dstk.filter(idtaikhoan=hv.mahv).values('trangthai').first()
        }
        for hv in dshv
    ]
    return render(request,'pages/admin-hocvien.html', {'ds_hv':data})

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