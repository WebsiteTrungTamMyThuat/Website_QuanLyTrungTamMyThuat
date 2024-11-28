from django.shortcuts import render,redirect, get_object_or_404
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

import re
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import random
from django.db import transaction
from django.http import JsonResponse
from django.views.decorators.cache import never_cache

from datetime import date

from decimal import Decimal
# Create your views herede

def user(request):
    # Lấy username từ session
    username = request.session.get('user_username', None)

    # Prepare the context dictionary
    context = {
        'username': username,
        'dm_kh': KhoaHoc.objects.all()  # Add the list of courses to the context
    }

    # Render the template with the combined context
    return render(request, 'pages/user.html', context)



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

#def giohang(request):
    gio_hang = GioHang.objects.filter(user=request.user)

    return render(request, 'gio-hang.html', {
        'gio_hang': gio_hang })



#### Đăng nhập


def userlogin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass_word = request.POST.get('pass_word')

     
        # request.session.flush()

        if username and pass_word:
            try:
               
                nguoidung = TaiKhoanNguoiDung.objects.get(username=username)



               
                if nguoidung.pass_word == pass_word:
                    
                    request.session['user_username'] = nguoidung.username
                    request.session['user_idtaikhoan'] = nguoidung.idtaikhoan

                    
                    if nguoidung.quyen == 'GV': 
                        return redirect('giaovien_admin')
                    elif nguoidung.quyen == 'HV':
                        messages.success(request, f"Chào mừng {nguoidung.username}!") 
                        return redirect('user')
                    else:
                        messages.error(request, 'Thông tin đăng nhập không chính xác')
                        return redirect('login')
                else:
                    messages.error(request, 'Mật khẩu không chính xác!')
            except TaiKhoanNguoiDung.DoesNotExist:
                messages.error(request, 'Người dùng không tồn tại!')

    return render(request, 'layout/dangnhap.html')



####

@never_cache
def logout_view(request):
    request.session.flush()  # Xóa toàn bộ session
    logout(request)
    return redirect('/user')


## Tạo id tai khoản theo hv
def generate_unique_id():
    with transaction.atomic():
        while True:
            # Generate a random 5-digit numeric ID
            new_id = f"{random.randint(1000000, 9999999)}"
            
            # Check if the ID already exists in the database
            if not TaiKhoanNguoiDung.objects.filter(idtaikhoan=new_id).exists():
                return new_id


## Đăng ký
def register(request):
    if request.method == 'POST':
        hoten = request.POST.get('hoten')
        email = request.POST.get('email')
        SDT = request.POST.get('SDT')
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        # Kiểm tra mật khẩu khớp
        if password != password_confirmation:
            return render(request, 'user/dangky.html', {'error': 'Mật khẩu không khớp!'})
        

        if not SDT.isdigit():
            return render(request, 'user/dangky.html', {'error': 'Số điện thoại phải là số!'})

        try:
            validate_email(email)
        except ValidationError:
            return render(request, 'user/dangky.html', {'error': 'Email không hợp lệ!'})

        try:
            # Tạo mã học viên duy nhất
            mahv = generate_unique_id()
            
            # Lưu tài khoản
            TaiKhoanNguoiDung.objects.create(
                idtaikhoan=mahv,
                username=email,
                pass_word=password,
                quyen='HV',
                trangthai='Hoạt Động'
            )
            
            # Lưu học viên
            HocVien.objects.create(
                mahv=mahv,
                hoten=hoten,
                email=email,
                SDT=SDT
            )
            messages.success(request, 'Đăng ký thành công!')
            return redirect('dangnhap')  # Chuyển hướng sau khi đăng ký thành công
        except Exception as e:
            return render(request, 'layout/dangky.html', {'error': str(e)})

    return render(request, 'layout/dangky.html')

def tthocvien(request):
    return render(request,'pages/thong-tin-hoc-vien.html')

def lichsukh(request):
    return render(request,'pages/lich-su-khoa-hoc.html')

## thông tin học viên
def thongtinhv(request):
    if not request.session.get('user_username'):
        return redirect('dangnhap')


    username = request.session['user_username']
    

    hoc_vien = get_object_or_404(HocVien, email=username)
    tai_khoan = get_object_or_404(TaiKhoanNguoiDung, username=username)
    

    if request.method == 'POST':
        hoten = request.POST.get('hoten')
        SDT = request.POST.get('SDT')
        email = request.POST.get('email')
        NgaySinh = request.POST.get('NgaySinh')

       
        hoc_vien.hoten = hoten
        hoc_vien.SDT = SDT
        hoc_vien.email = email
        hoc_vien.NgaySinh = NgaySinh

        try:
           
            hoc_vien.save()

           
            if tai_khoan.username != email:
                tai_khoan.username = email
                tai_khoan.save()

            request.session['user_username'] = email
            request.session.flush()
            messages.success(request, 'Cập nhật thông tin thành công!')
            return redirect('dangnhap')

        except Exception as e:
            print("Error:", str(e))
            messages.error(request, 'Đã xảy ra lỗi, vui lòng thử lại!')

    return render(request, 'pages/thong-tin-hoc-vien.html', {'form': HocVienForm(instance=hoc_vien)})




## Danh sách lớp theo khóa học

def DSTheoKH(request , ml):

    Lop = LopHoc.objects.filter(makh=ml)
    dskh = KhoaHoc.objects.all()
    data = {
        'ds_lop': Lop,
        'dm_kh': dskh, 
        'ctkh': ChiTietKhoaHoc.objects.all(),
        'ndkh': NoiDungKhoaHoc.objects.all(),
    }
    return render(request, 'pages/khoahoc.html', data)

from datetime import datetime
def filter_khoahoc(request):
   
    dskh = KhoaHoc.objects.all()
    ds_lop = LopHoc.objects.all()

    selected_date = request.GET.get('ngaybatdau', None)


    if selected_date:
        try:
            ngaybatdau = datetime.strptime(selected_date, "%Y-%m-%d").date()
            ds_lop = ds_lop.filter(ngaybatdau=ngaybatdau)
        except ValueError:
         
            return render(request, 'pages/khoahoc.html', {
                'error': "Định dạng ngày không hợp lệ. Vui lòng chọn đúng định dạng YYYY-MM-DD.",
                'ds_lop': ds_lop,
                'dm_kh': dskh,

                'selected_date': selected_date
            })

    # Truyền dữ liệu vào template
    return render(request, 'pages/khoahoc.html', {
        'ds_lop': ds_lop,
        'dm_kh': dskh,
        'ctkh': ChiTietKhoaHoc.objects.all(),
        'ndkh': NoiDungKhoaHoc.objects.all(),
        'selected_date': selected_date
    })

  

### Chi tiet lop hoc

def ChiTietLop(request,mlop):

    lop = get_object_or_404(LopHoc, malop=mlop)

   
    khoa_hoc = lop.makh 
    giaovien = get_object_or_404(GiaoVien, magv=lop.magv)

    lich_hoc = LichHoc.objects.filter(malop=mlop)
    lich_hoc_list = [
        {
            'ngayhoc': lh.ngayhoc.strftime("%d/%m/%Y"),
            'giohoc': lh.giohoc.strftime("%H:%M"),
            'sogiohoc': lh.sogiohoc
        }
        for lh in lich_hoc
    ]

    data = {
        'single_lop': lop,
        'khoa_hoc': khoa_hoc,  
        'giaovien': giaovien,
        'lichhoc': lich_hoc_list,
    }

    return render(request, 'pages/thong-tin-khoa-hoc.html', data)


### 

def LoadPhieuDK(request):

    if not request.session.get('user_username'):
        messages.error(request, "Vui lòng đăng nhập để tiếp tục!")
        return redirect('dangnhap')

   
    username = request.session['user_username']

    try:
       
        tai_khoan = get_object_or_404(TaiKhoanNguoiDung, username=username)
        hoc_vien = get_object_or_404(HocVien, email=tai_khoan.username)
    except Exception:
        messages.error(request, "Không tìm thấy thông tin tài khoản hoặc học viên.")
        return redirect('dangnhap')


    if request.method == 'POST':
        form = HocVienForm(request.POST, instance=hoc_vien)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Thông tin đã được cập nhật thành công!")
                return redirect('giohang')  # Điều hướng tới trang khác (nếu cần)
            except Exception as e:
                messages.error(request, f"Có lỗi khi lưu dữ liệu: {e}")
        else:
            messages.error(request, "Thông tin nhập vào không hợp lệ. Vui lòng kiểm tra lại!")
    else:
        form = HocVienForm(instance=hoc_vien)

    return render(request, 'pages/dang-ky-tu-van.html', {
        'form': form,
        'ds_lop': LopHoc.objects.all() 
    })

### Danh sách khóa học - lớp
def DSKhoaHoc(request):
    dskh = {
        'dm_kh' : KhoaHoc.objects.all(),
        'ds_lop': LopHoc.objects.all(),
        'ctkh': ChiTietKhoaHoc.objects.all(),
        'ndkh': NoiDungKhoaHoc.objects.all(),
    }
    return render(request,'pages/khoahoc.html',dskh)

### xoa gio hang

def xoa_hoan_tat(request, malop):
 
    gio_hang = request.session.get('gio_hang', {})

   
    if malop in gio_hang:
       
        del gio_hang[malop]
        request.session['gio_hang'] = gio_hang  

        messages.success(request, "Lớp học đã được xóa khỏi giỏ hàng.")
    else:
        messages.error(request, "Lớp học không tồn tại trong giỏ hàng.")

    return redirect('giohang') 
### Load Gio Hang 
def LoadGioHang(request):
    if not request.session.get('user_username'):
        messages.error(request, "Vui lòng đăng nhập để tiếp tục!")
        return redirect('dangnhap')

    username = request.session['user_username']

    try:
        tai_khoan = get_object_or_404(TaiKhoanNguoiDung, username=username)
        hoc_vien = get_object_or_404(HocVien, email=tai_khoan.username)
    except Exception:
        messages.error(request, "Không tìm thấy thông tin tài khoản hoặc học viên.")
        return redirect('dangnhap')

    gio_hang = request.session.get('gio_hang', {})
    total_price = 0

    gio_hang_display = [
        {
            'malop': malop,
            'tenlop': item['tenlop'],
            'hocphi': float(item['hocphi']),
            'so_luong': item['so_luong'],
            'mahv': item.get('mahv', ''),
            'lichhoc': item['lichhoc']  # Lịch học đã chọn
        }
        for malop, item in gio_hang.items()
    ]

    for item in gio_hang.values():
        total_price += float(item['hocphi'])

    return render(request, 'pages/gio-hang.html', {
        'hoc_vien': hoc_vien,
        'gio_hang': gio_hang,
        'total_price': total_price,
        'gio_hang_display': gio_hang_display
    })

### them gio hang
def them_vao_gio_hang(request, malop):
    malop = malop.strip()

    try:
        lop_hoc = LopHoc.objects.get(malop=malop)
    except LopHoc.DoesNotExist:
        messages.error(request, "Lớp học không tồn tại.")
        return redirect('khoahoc')

    if not request.session.get('user_username'):
        messages.error(request, "Vui lòng đăng nhập để thêm lớp vào giỏ hàng.")
        return redirect('dangnhap')

    username = request.session['user_username']
    tai_khoan = get_object_or_404(TaiKhoanNguoiDung, username=username)
    hoc_vien = get_object_or_404(HocVien, email=tai_khoan.username)

    mahv = hoc_vien.mahv.strip()

    if request.method == "POST":
        selected_lich = request.POST.get('selected_lichhoc', None)
        if not selected_lich:
            messages.error(request, "Vui lòng chọn ít nhất một lịch học trước khi đăng ký.")
            return redirect('ttkhoahoc', mlop=malop)

       
        ngayhoc, giohoc = selected_lich.split('|')

        
        gio_hang = request.session.get('gio_hang', {})

       
        gio_hang[malop] = {
            'tenlop': lop_hoc.tenlop,
            'hocphi': str(lop_hoc.hocphi),
            'so_luong': 1,
            'malop': malop,
            'mahv': mahv,
            'lichhoc': {  # Lưu lịch học đã chọn
                'ngayhoc': ngayhoc,
                'giohoc': giohoc
            }
        }

        # Lưu giỏ hàng vào session
        request.session['gio_hang'] = gio_hang

        messages.success(request, f"Lớp học {lop_hoc.tenlop} đã được thêm vào giỏ hàng!")
        return redirect('giohang')

    return redirect('ttkhoahoc', mlop=malop)

####

def is_conflict_schedule(gio_hang):
    """
    Kiểm tra xem có lịch học trùng trong giỏ hàng không.
    Trả về True nếu có trùng lặp, ngược lại trả về False.
    """
    schedule_set = set()

    for item in gio_hang.values():
        lichhoc = item.get('lichhoc', {})  
        ngayhoc = lichhoc.get('ngayhoc')
        giohoc = lichhoc.get('giohoc')

        if not ngayhoc or not giohoc:
            continue  

       
        ngay_gio = (ngayhoc, giohoc)

       
        if ngay_gio in schedule_set:
           
            return True

        schedule_set.add(ngay_gio)

    return False
###
def thanh_toan(request):
   
    if not request.session.get('user_username'):
        messages.error(request, "Vui lòng đăng nhập để tiếp tục!")
        return redirect('dangnhap')

    gio_hang = request.session.get('gio_hang', {})

   
    if is_conflict_schedule(gio_hang):
        messages.error(request, "Lịch học bị trùng lặp. Vui lòng kiểm tra lại.")
        return redirect('giohang')


    if not gio_hang:
        messages.error(request, "Giỏ hàng không có lớp học nào.")
        return redirect('giohang')

    username = request.session['user_username']
    hoc_vien = get_object_or_404(HocVien, email=username)

    total_price = Decimal(0)

    try:
        # Tính tổng học phí cho giỏ hàng
        for malop, item in gio_hang.items():
            malop_cleaned = malop.strip()
            lop_hoc = get_object_or_404(LopHoc, malop=malop_cleaned)
            total_price += Decimal(item['hocphi']) * item['so_luong']  # Tính tổng tiền

    except Exception as e:
        messages.error(request, f"Lỗi khi lấy lớp học từ giỏ hàng: {e}")
        return redirect('giohang')

  
    if request.method == 'POST':
        try:
            with transaction.atomic():  
               
                for malop, item in gio_hang.items():
                    malop_cleaned = malop.strip()
                    lop_hoc = get_object_or_404(LopHoc, malop=malop_cleaned)
             
                    total_price_per_class = Decimal(item['hocphi']) * item['so_luong']

                
                    hoa_don = HoaDon.objects.create(
                        mahv=hoc_vien,  
                        malop=lop_hoc,  
                        ngaylap=date.today(), 
                        tongtien=total_price_per_class, 
                        trangthai='Chưa thanh toán'  
                    )

                
                request.session['gio_hang'] = {}

              
                messages.success(request, "Thanh toán thành công! Bạn đã đăng ký các lớp học.")
                return redirect('user')  

        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi khi thanh toán: {e}")
            return redirect('giohang')

    else:
        messages.error(request, "Vui lòng gửi yêu cầu thanh toán.")
        return redirect('giohang')