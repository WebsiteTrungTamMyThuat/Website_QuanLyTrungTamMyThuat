from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import authenticate ,login,logout
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.contrib.auth.hashers import check_password
from PageAdmin.models import *
from .models import *

from django.db.models import Max

from .forms import HocVienForm


# Create your views herede

def user(request):
    username = request.session.get('user_username', None)  # Lấy username từ session
    if username:
        context = {'username': username}
        return render(request, 'pages/user.html', context)
    else:
        messages.error(request, "Bạn chưa đăng nhập!")
        return redirect('dangnhap') 

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

def chinhanh(request):
    return render(request,'pages/chi-nhanh.html')

def giohang(request):
    return render(request, 'pages/gio-hang.html')



#### Đăng nhập


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass_word = request.POST.get("pass_word")

        if username and pass_word:
            try:
                
                nguoidung = TaiKhoanNguoiDung.objects.get(username=username)

                if nguoidung.pass_word == pass_word:
                    
                    request.session['user_username'] = nguoidung.username
                   
                    messages.success(request, f"Chào mừng {nguoidung.username}!")
                    return redirect('user')
                  
                else:
                    messages.error(request, 'Mật khẩu không chính xác!')
            except TaiKhoanNguoiDung.DoesNotExist:
                messages.error(request, 'Người dùng không tồn tại!')
                

    return render(request, 'layout/dangnhap.html')



##Dang xuat
def user_logout(request):
    logout(request)
    return redirect("dangnhap")




    return render(request, 'layout/dangky.html', {'form': form})


## Tạo id tai khoản theo hv
def generate_unique_id():
    last_id = TaiKhoanNguoiDung.objects.aggregate(max_id=Max('idtaikhoan'))['max_id']
    if last_id:
        # Chỉ lấy phần số từ id (vd: "hv003" -> 3), tăng giá trị
        last_number = int(last_id.replace('hv', '').strip())
        new_id = f"hv{last_number + 1:03d}"
    else:
        # Nếu chưa có bản ghi nào, bắt đầu từ "hv001"
        new_id = "hv001"
    return new_id


## Đăng ký
def register(request):
    if request.method == 'POST':
        hoten = request.POST.get('hoten')
        sdt = request.POST.get('sdt')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        # Kiểm tra mật khẩu khớp
        if password != password_confirmation:
            return render(request, 'user/dangky.html', {'error': 'Mật khẩu không khớp!'})

        try:
            # Tạo mã học viên duy nhất
            mahv = generate_unique_id()
            
            # Lưu tài khoản
            TaiKhoanNguoiDung.objects.create(
                idtaikhoan=mahv,
                username=email,
                pass_word=password,
                quyen='hocvien',
                trangthai='active'
            )
            
            # Lưu học viên
            HocVien.objects.create(
                mahv=mahv,
                hoten=hoten,
                email=email,
                gioitinh = "",
                diachi ="",
                sdt=sdt
            )
            return redirect('dangnhap')  # Chuyển hướng sau khi đăng ký thành công
        except Exception as e:
            return render(request, 'layout/dangky.html', {'error': str(e)})

    return render(request, 'layout/dangky.html')

def tthocvien(request):
    return render(request,'pages/thong-tin-hoc-vien.html')

def lichsukh(request):
    return render(request,'pages/lich-su-khoa-hoc.html')

