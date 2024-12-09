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

def lienhe(request):
    return render(request,'pages/lien-he.html')

#def giohang(request):
    gio_hang = GioHang.objects.filter(user=request.user)

    return render(request, 'gio-hang.html', {
        'gio_hang': gio_hang })



#### Đăng nhập
from django.urls import reverse

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
                    request.session['quyen'] = nguoidung.quyen
                    
                    if nguoidung.quyen == 'GV': 
                        return redirect(reverse('admin', kwargs={'idtaikhoan': nguoidung.idtaikhoan}))
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
 
    username = request.session.get('user_username')
    if not username:
        messages.error(request, "Bạn cần đăng nhập để xem lịch sử khóa học.")
        return redirect('login')  # Redirect tới trang đăng nhập


    hoc_vien = get_object_or_404(HocVien, email=username)
    

    registered_courses = HoaDon.objects.filter(mahv=hoc_vien, trangthai='Đã thanh toán').select_related('malop')
    

    context = {
        'registered_courses': registered_courses
    }
    return render(request, 'pages/lich-su-khoa-hoc.html', context)
 
    username = request.session.get('user_username')
    if not username:
        messages.error(request, "Bạn cần đăng nhập để xem lịch sử khóa học.")
        return redirect('login')  # Redirect tới trang đăng nhập


    hoc_vien = get_object_or_404(HocVien, email=username)
    

    registered_courses = HoaDon.objects.filter(mahv=hoc_vien, trangthai='Đã thanh toán').select_related('malop')
    

    context = {
        'registered_courses': registered_courses
    }
    return render(request, 'pages/lich-su-khoa-hoc.html', context)

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
# sap xem khoa hoc theo
from datetime import datetime
def filter_khoahoc(request):
    danh_sach_khoa_hoc = KhoaHoc.objects.all()
    danh_sach_lop = LopHoc.objects.all()

    # Lấy thông tin lọc từ request
    selected_date = request.GET.get('ngaybatdau', None)
    sort_option = request.GET.get('sortOptions', None)

    error = None
    has_courses = True

    # Lọc theo ngày bắt đầu
    if selected_date:
        try:
            ngaybatdau = datetime.strptime(selected_date, "%Y-%m-%d").date()
            danh_sach_lop = danh_sach_lop.filter(ngaybatdau=ngaybatdau)
        except ValueError:
            error = "Định dạng ngày không hợp lệ. Vui lòng chọn đúng định dạng YYYY-MM-DD."

    # Sắp xếp theo tùy chọn
    if sort_option == 'priceLowToHigh':
        danh_sach_lop = danh_sach_lop.order_by('hocphi')  # Học phí tăng dần
    elif sort_option == 'priceHighToLow':
        danh_sach_lop = danh_sach_lop.order_by('-hocphi')  # Học phí giảm dần


    
    if not danh_sach_lop.exists():  # Nếu danh sách lớp rỗng
        has_courses = False
    # Truyền dữ liệu vào template
    return render(request, 'pages/khoahoc.html', {
        'ds_lop': danh_sach_lop,
        'dm_kh': danh_sach_khoa_hoc,
        'ctkh': ChiTietKhoaHoc.objects.all(),
        'ndkh': NoiDungKhoaHoc.objects.all(),
        'selected_date': selected_date,
        'sort_option': sort_option,
        'error': error,
        'has_courses': has_courses,
    })
  

### Chi tiet lop hoc

def ChiTietLop(request,mlop):

    lop = get_object_or_404(LopHoc, malop=mlop)

   
    khoa_hoc = lop.makh 
    giaovien = get_object_or_404(GiaoVien, magv=lop.magv)

    lichhoc = LichHoc.objects.filter(ngayhoc=lop.ngaybatdau)

    lichhoc = LichHoc.objects.filter(ngayhoc=lop.ngaybatdau)


    data = {
        'single_lop': lop,
        'khoa_hoc': khoa_hoc,  
        'giaovien': giaovien,
        'lichhoc': lichhoc,
        'lichhoc': lichhoc,
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
    today = date.today()
    dskh = {
        'dm_kh' : KhoaHoc.objects.all().order_by('tenkh'),
        'ds_lop': LopHoc.objects.filter(tinhtrang="Chưa bắt đầu",ngaybatdau__gt=today).order_by('ngaybatdau'),
        'ds_lop': LopHoc.objects.filter(tinhtrang="Chưa bắt đầu",ngaybatdau__gt=today).order_by('ngaybatdau'),
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


    gio_hang = request.session.get('gio_hang', {})

    # Kiểm tra xem lớp đã thanh toán chưa
    lop_hoc = get_object_or_404(LopHoc, malop=malop)
    is_paid = HoaDon.objects.filter(
        mahv=hoc_vien,
        malop=lop_hoc,
        trangthai='Đã thanh toán'
    ).exists()

    if is_paid:
        messages.error(request, "Bạn đã thanh toán lớp học này trước đó.")
        return redirect('giohang')

    mahv = hoc_vien.mahv.strip()

    if request.method == "POST":
        gio_hang = request.session.get('gio_hang', {})

        gio_hang[malop] = {
            'tenlop': lop_hoc.tenlop,
            'hocphi': str(lop_hoc.hocphi),
            'so_luong': 1,
            'malop': malop,
            'mahv': mahv,

        }

        # Lưu giỏ hàng vào session
        request.session['gio_hang'] = gio_hang

        messages.success(request, f"Lớp học {lop_hoc.tenlop} đã được thêm vào giỏ hàng!")
        return redirect('giohang')

    return redirect('ttkhoahoc', mlop=malop)

####

def is_conflict_schedule_and_paid(gio_hang, hoc_vien):
    """
    Kiểm tra xem có lịch học trùng hoặc lớp đã thanh toán trong giỏ hàng không.
    Trả về True nếu có trùng lặp hoặc đã thanh toán, ngược lại trả về False.
    """
    schedule_set = set()

    for malop, item in gio_hang.items():
        lichhoc = item.get('lichhoc', {})
        ngayhoc = lichhoc.get('ngayhoc')
        giohoc = lichhoc.get('giohoc')

        if not ngayhoc or not giohoc:
            continue  

        ngay_gio = (ngayhoc, giohoc)

        # Kiểm tra lịch học trùng
        if ngay_gio in schedule_set:
            return True
        schedule_set.add(ngay_gio)

        # Kiểm tra xem lớp đã được thanh toán chưa
        try:
            lop_hoc = LopHoc.objects.get(malop=malop)
            is_paid = HoaDon.objects.filter(
                mahv=hoc_vien,
                malop=lop_hoc,
                trangthai='Đã thanh toán'
            ).exists()
            if is_paid:
                return True
        except LopHoc.DoesNotExist:
            continue  # Nếu lớp học không tồn tại, bỏ qua kiểm tra

    return False

import hmac
import hashlib
import json
import requests ,time
from django.conf import settings
from django.shortcuts import redirect, render
from django.http import HttpResponse



def momo_payment(request):
    if request.method == 'POST':
        # Lấy thông tin từ form
        payment_method = request.POST.get('payment_method', 'captureWallet')  # Phương thức thanh toán
        amount = request.POST.get('amount', '10000')  # Số tiền thanh toán
        order_id = f"ORDER{int(time.time())}"  # Mã đơn hàng
        request_id = f"REQUEST{int(time.time())}"  # Mã yêu cầu
        order_info = "Thanh toán khóa học"  # Thông tin đơn hàng

        # Dữ liệu yêu cầu gửi tới Momo API
        data = {
            "partnerCode": settings.MOMO_PARTNER_CODE,
            "accessKey": settings.MOMO_ACCESS_KEY,
            "requestId": request_id,
            "amount": amount,
            "orderId": order_id,
            "orderInfo": order_info,
            "redirectUrl": settings.MOMO_RETURN_URL,
            "ipnUrl": settings.MOMO_NOTIFY_URL,
            "extraData": "",  # Dữ liệu bổ sung, có thể để trống
            "requestType": payment_method  # Phương thức thanh toán được chọn
        }

        # Tạo signature để xác thực yêu cầu
        raw_signature = (
            f"accessKey={settings.MOMO_ACCESS_KEY}&"
            f"amount={amount}&"
            f"extraData=&"
            f"ipnUrl={settings.MOMO_NOTIFY_URL}&"
            f"orderId={order_id}&"
            f"orderInfo={order_info}&"
            f"partnerCode={settings.MOMO_PARTNER_CODE}&"
            f"redirectUrl={settings.MOMO_RETURN_URL}&"
            f"requestId={request_id}&"
            f"requestType={payment_method}"  # Đảm bảo phương thức thanh toán được truyền đúng
        )
        signature = hmac.new(
            settings.MOMO_SECRET_KEY.encode('utf-8'),
            raw_signature.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        data["signature"] = signature

        # Gửi yêu cầu đến Momo
        response = requests.post(settings.MOMO_ENDPOINT, json=data)
        response_data = response.json()

        # Kiểm tra phản hồi từ Momo
        if response_data.get('payUrl'):
            return redirect(response_data['payUrl'])  # Chuyển hướng tới trang thanh toán Momo
        else:
            return HttpResponse(f"Lỗi khi tạo yêu cầu thanh toán: {response_data.get('message', 'Unknown error')}")
    else:
        return render(request, 'pages/payment.html')


####
def thanh_toan(request):
    if not request.session.get('user_username'):
        messages.error(request, "Vui lòng đăng nhập để tiếp tục!")
        return redirect('dangnhap')

    gio_hang = request.session.get('gio_hang', {})
    username = request.session.get('user_username')
    hoc_vien = get_object_or_404(HocVien, email=username)

    if is_conflict_schedule_and_paid(gio_hang, hoc_vien):
        messages.error(request, "Lịch học bị trùng hoặc lớp học đã được thanh toán.")
        return redirect('khoahoc')
        return redirect('khoahoc')

    if not gio_hang:
        messages.error(request, "Giỏ hàng không có lớp học nào.")
        return redirect('giohang')

    total_price = Decimal(0)
    try:
        # Tính tổng tiền
        # Tính tổng tiền
        for malop, item in gio_hang.items():
            malop_cleaned = malop.strip()
            lop_hoc = get_object_or_404(LopHoc, malop=malop_cleaned)
            total_price += Decimal(item['hocphi']) * item['so_luong']

    except Exception as e:
        messages.error(request, f"Lỗi khi lấy lớp học từ giỏ hàng: {e}")
        return redirect('giohang')

    if request.method == 'POST':
        try:
            created_invoices = []  # Danh sách hóa đơn đã tạo
            created_invoices = []  # Danh sách hóa đơn đã tạo
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
                    created_invoices.append(hoa_don.sohd)  # Thêm mã hóa đơn vào danh sách

                # Tiếp tục xử lý thanh toán MoMo
                payment_method = request.POST.get('payment_method', 'captureWallet')
                amount = request.POST.get('amount', '10000')
                order_id = f"ORDER{int(time.time())}"  # Mã đơn hàng chung cho giao dịch
                request_id = f"REQUEST{int(time.time())}"
                created_invoices.append(hoa_don.sohd)  # Thêm mã hóa đơn vào danh sách

                # Tiếp tục xử lý thanh toán MoMo
                payment_method = request.POST.get('payment_method', 'captureWallet')
                amount = request.POST.get('amount', '10000')
                order_id = f"ORDER{int(time.time())}"  # Mã đơn hàng chung cho giao dịch
                request_id = f"REQUEST{int(time.time())}"
                order_info = "Thanh toán khóa học"

                # Lưu danh sách hóa đơn vào session để sử dụng sau
                request.session['created_invoices'] = created_invoices

                # Chuẩn bị chữ ký
                # Lưu danh sách hóa đơn vào session để sử dụng sau
                request.session['created_invoices'] = created_invoices

                # Chuẩn bị chữ ký
                raw_signature = (
                    f"accessKey={settings.MOMO_ACCESS_KEY}&"
                    f"amount={amount}&"
                    f"extraData=&"
                    f"ipnUrl={settings.MOMO_NOTIFY_URL}&"
                    f"orderId={order_id}&"
                    f"orderInfo={order_info}&"
                    f"partnerCode={settings.MOMO_PARTNER_CODE}&"
                    f"redirectUrl={settings.MOMO_RETURN_URL}&"
                    f"requestId={request_id}&"
                    f"requestType={payment_method}"
                )

                signature = hmac.new(
                    settings.MOMO_SECRET_KEY.encode('utf-8'),
                    raw_signature.encode('utf-8'),
                    hashlib.sha256
                ).hexdigest()

                data = {
                    "partnerCode": settings.MOMO_PARTNER_CODE,
                    "accessKey": settings.MOMO_ACCESS_KEY,
                    "requestId": request_id,
                    "amount": amount,
                    "orderId": order_id,
                    "orderInfo": order_info,
                    "redirectUrl": settings.MOMO_RETURN_URL,
                    "ipnUrl": settings.MOMO_NOTIFY_URL,
                    "extraData": "",
                    "requestType": payment_method,
                    "signature": signature,
                    "signature": signature,
                }

                response = requests.post(settings.MOMO_ENDPOINT, json=data)
                response_data = response.json()

                if response_data.get('payUrl'):
                    return redirect(response_data['payUrl'])  # Redirect to Momo payment page
                else:
                    return HttpResponse(f"Lỗi khi tạo yêu cầu thanh toán: {response_data.get('message', 'Unknown error')}")

        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi khi thanh toán: {e}")
            return redirect('giohang')

    else:
        messages.error(request, "Vui lòng gửi yêu cầu thanh toán.")
        return redirect('giohang')
####

###
def momo_return(request):
    if request.method == 'GET':
        data = request.GET
        order_id = data.get('orderId')
        amount = data.get('amount')
        result_code = data.get('resultCode')
        message = data.get('message')
        mahv = request.session.get('user_username')

        created_invoices = request.session.get('created_invoices', [])


        created_invoices = request.session.get('created_invoices', [])

        if result_code == '0':  # Thanh toán thành công
            try:
                with transaction.atomic():
                    hoc_vien = HocVien.objects.get(email=mahv)
                    for sohd in created_invoices:
                        hoa_don = HoaDon.objects.filter(sohd=sohd, mahv=hoc_vien, trangthai='Chưa thanh toán').first()
                        if hoa_don:
                            hoa_don.trangthai = 'Đã thanh toán'
                            hoa_don.save()

                            LichSuGiaoDich.objects.create(
                                magiaodich=sohd,
                                ngaygiaodich=date.today(),
                                sotien=hoa_don.tongtien,
                                loaigiaodich="Thanh toán qua Momo",
                                ghichu=f"Giao dịch thành công: {message}"
                            )
                    for sohd in created_invoices:
                        hoa_don = HoaDon.objects.filter(sohd=sohd, mahv=hoc_vien, trangthai='Chưa thanh toán').first()
                        if hoa_don:
                            hoa_don.trangthai = 'Đã thanh toán'
                            hoa_don.save()

                            LichSuGiaoDich.objects.create(
                                magiaodich=sohd,
                                ngaygiaodich=date.today(),
                                sotien=hoa_don.tongtien,
                                loaigiaodich="Thanh toán qua Momo",
                                ghichu=f"Giao dịch thành công: {message}"
                            )

                    request.session['gio_hang'] = {}
                    return redirect('success')

            except Exception as e:
                return HttpResponse(f"Đã xảy ra lỗi: {str(e)}")
        else:
            # Thanh toán thất bại
            # Thanh toán thất bại
            try:
                with transaction.atomic():
                    hoc_vien = HocVien.objects.get(email=mahv)
                    for sohd in created_invoices:
                        hoa_don = HoaDon.objects.filter(sohd=sohd, mahv=hoc_vien, trangthai='Chưa thanh toán').first()
                        if hoa_don:
                            hoa_don.trangthai = 'Đã hủy'
                            hoa_don.save()

                            LichSuGiaoDich.objects.create(
                                magiaodich=sohd,
                                ngaygiaodich=date.today(),
                                sotien=hoa_don.tongtien,
                                loaigiaodich="Thanh toán qua Momo",
                                ghichu=f"Giao dịch thất bại: {message}"
                            )

                    # Lấy hóa đơn cần cập nhật khi thanh toán thất bại
                    hoa_don = HoaDon.objects.filter(
                        mahv=hoc_vien, 
                        tongtien=Decimal(amount), 
                        trangthai='Chưa thanh toán'
                    ).first()
                    print("Hello")
                    # Kiểm tra nếu hóa đơn không tồn tại
                    if not hoa_don:
                        return HttpResponse("Hóa đơn không tồn tại hoặc đã được xử lý.")

                    # Cập nhật trạng thái hóa đơn là "Đã hủy"
                    hoa_don.trangthai = 'Đã hủy'
                    hoa_don.save()

                    LichSuGiaoDich.objects.create(
                        magiaodich=sohd,
                        ngaygiaodich=date.today(),
                        sotien=hoa_don.tongtien,
                        loaigiaodich="Thanh toán qua Momo",
                        ghichu=f"Giao dịch thất bại: {message}"
                    )
                    LichSuGiaoDich.objects.create(
                        magiaodich=sohd,
                        ngaygiaodich=date.today(),
                        sotien=hoa_don.tongtien,
                        loaigiaodich="Thanh toán qua Momo",
                        ghichu=f"Giao dịch thất bại: {message}"
                    )

                    return HttpResponse(f"Thanh toán thất bại: {message}")

            except Exception as e:
                return HttpResponse(f"Đã xảy ra lỗi khi xử lý thanh toán thất bại: {str(e)}")
        
def success(request):
     return render(request, 'pages/paymey_succesful.html')


from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def momo_notify(request):
    
    
    if request.method == 'POST':
        data = json.loads(request.body)
        order_id = data.get('orderId')
        result_code = data.get('resultCode')

        try:
            hoa_don = HoaDon.objects.get(mahd=order_id)
            if result_code == 0:
                hoa_don.trangthai = 'Đã thanh toán'
                hoa_don.save()
                print(f"Đơn hàng {order_id} đã thanh toán thành công.")
            else:
                hoa_don.trangthai = 'Thanh toán thất bại'
                hoa_don.save()
                print(f"Đơn hàng {order_id} thanh toán thất bại.")
        except HoaDon.DoesNotExist:
            print(f"Đơn hàng {order_id} không tồn tại trong hệ thống.")

        return HttpResponse("Received", status=200)
    


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
#from .models import  OTPRequest
from django.utils.timezone import now, timedelta

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # Kiểm tra email có tồn tại trong hệ thống không
        try:
            hoc_vien = HocVien.objects.get(email=email)

            # Tạo mã OTP
            otp_code = get_random_string(length=6, allowed_chars='0123456789')

            # Lưu OTP vào session
            request.session['otp_code'] = otp_code
            request.session['otp_email'] = email
            request.session['otp_expiry'] = (now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')  # Lưu thời gian hết hạn

            # Gửi email với mã OTP
            send_mail(
                'Khôi phục mật khẩu',
                f'Mã OTP để khôi phục mật khẩu của bạn là: {otp_code}',
                'no-reply@example.com',  # Email người gửi
                [email],
                fail_silently=False,
            )

            messages.success(request, "Mã OTP đã được gửi tới email của bạn.")
            return redirect('verify_otp')  # Redirect tới trang nhập OTP

        except HocVien.DoesNotExist:
            messages.error(request, "Email không tồn tại trong hệ thống.")
            return redirect('forgot_password')

    return render(request, 'pages/forgot_password.html')
###
from django.utils.timezone import now, make_aware
def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp_code = request.POST.get('otp_code')

        # Kiểm tra OTP từ session
        saved_otp_code = request.session.get('otp_code')
        saved_otp_email = request.session.get('otp_email')
        otp_expiry_str = request.session.get('otp_expiry')

        # Kiểm tra email và OTP có khớp không


        if saved_otp_code != otp_code:
            messages.error(request, "Mã OTP không hợp lệ.")
            return redirect('verify_otp')

        # Kiểm tra thời gian hết hạn của OTP
        if otp_expiry_str:
            otp_expiry_time = make_aware(datetime.strptime(otp_expiry_str, '%Y-%m-%d %H:%M:%S'))
            if now() > otp_expiry_time:
                messages.error(request, "Mã OTP đã hết hạn.")
                return redirect('forgot_password')

        # OTP hợp lệ, lưu trạng thái xác nhận vào session
        request.session['verified_email'] = email
        messages.success(request, "OTP xác nhận thành công. Vui lòng đặt lại mật khẩu.")
        return redirect('reset_password')

    return render(request, 'pages/verify_otp.html')

###
from django.contrib.auth.hashers import make_password

def reset_password(request):
    if request.method == "POST":
        username = request.session.get('verified_email')
        if not username:
            messages.error(request, "Yêu cầu không hợp lệ.")
            return redirect('forgot_password')

        # Lấy mật khẩu mới từ form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin.")
            return redirect('reset_password')

        if new_password != confirm_password:
            messages.error(request, "Mật khẩu xác nhận không khớp.")
            return redirect('reset_password')

        # Lấy tài khoản người dùng từ cơ sở dữ liệu
        user = get_object_or_404(TaiKhoanNguoiDung, username=username)

        # Cập nhật mật khẩu mới (đã mã hóa)
        user.pass_word = new_password  # Đổi 'pass_field' thành tên cột chứa mật khẩu
        user.save()

        # Xóa session đã xác thực
        del request.session['verified_email']

        # Hiển thị thông báo thành công
        messages.success(request, "Mật khẩu đã được thay đổi thành công.")
        return redirect('dangnhap')  # Chuyển hướng về trang đăng nhập

    return render(request, 'pages/reset_password.html')
    


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
#from .models import  OTPRequest
from django.utils.timezone import now, timedelta

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        # Kiểm tra email có tồn tại trong hệ thống không
        try:
            hoc_vien = HocVien.objects.get(email=email)

            # Tạo mã OTP
            otp_code = get_random_string(length=6, allowed_chars='0123456789')

            # Lưu OTP vào session
            request.session['otp_code'] = otp_code
            request.session['otp_email'] = email
            request.session['otp_expiry'] = (now() + timedelta(minutes=10)).strftime('%Y-%m-%d %H:%M:%S')  # Lưu thời gian hết hạn

            # Gửi email với mã OTP
            send_mail(
                'Khôi phục mật khẩu',
                f'Mã OTP để khôi phục mật khẩu của bạn là: {otp_code}',
                'no-reply@example.com',  # Email người gửi
                [email],
                fail_silently=False,
            )

            messages.success(request, "Mã OTP đã được gửi tới email của bạn.")
            return redirect('verify_otp')  # Redirect tới trang nhập OTP

        except HocVien.DoesNotExist:
            messages.error(request, "Email không tồn tại trong hệ thống.")
            return redirect('forgot_password')

    return render(request, 'pages/forgot_password.html')
###
from django.utils.timezone import now, make_aware
def verify_otp(request):
    if request.method == "POST":
        email = request.POST.get('email')
        otp_code = request.POST.get('otp_code')

        # Kiểm tra OTP từ session
        saved_otp_code = request.session.get('otp_code')
        saved_otp_email = request.session.get('otp_email')
        otp_expiry_str = request.session.get('otp_expiry')

        # Kiểm tra email và OTP có khớp không
        if email != saved_otp_email:
            messages.error(request, "Email không khớp với yêu cầu trước.")
            return redirect('verify_otp')

        if saved_otp_code != otp_code:
            messages.error(request, "Mã OTP không hợp lệ.")
            return redirect('verify_otp')

        # Kiểm tra thời gian hết hạn của OTP
        if otp_expiry_str:
            otp_expiry_time = make_aware(datetime.strptime(otp_expiry_str, '%Y-%m-%d %H:%M:%S'))
            if now() > otp_expiry_time:
                messages.error(request, "Mã OTP đã hết hạn.")
                return redirect('forgot_password')

        # OTP hợp lệ, lưu trạng thái xác nhận vào session
        request.session['verified_email'] = email
        messages.success(request, "OTP xác nhận thành công. Vui lòng đặt lại mật khẩu.")
        return redirect('reset_password')

    return render(request, 'pages/verify_otp.html')


###
from django.contrib.auth.hashers import make_password

def reset_password(request):
    if request.method == "POST":
        username = request.session.get('verified_email')
        if not username:
            messages.error(request, "Yêu cầu không hợp lệ.")
            return redirect('forgot_password')

        # Lấy mật khẩu mới từ form
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not new_password or not confirm_password:
            messages.error(request, "Vui lòng nhập đầy đủ thông tin.")
            return redirect('reset_password')

        if new_password != confirm_password:
            messages.error(request, "Mật khẩu xác nhận không khớp.")
            return redirect('reset_password')

        # Lấy tài khoản người dùng từ cơ sở dữ liệu
        user = get_object_or_404(TaiKhoanNguoiDung, username=username)

        # Cập nhật mật khẩu mới (đã mã hóa)
        user.pass_word = new_password  # Đổi 'pass_field' thành tên cột chứa mật khẩu
        user.save()

        # Xóa session đã xác thực
        del request.session['verified_email']

        # Hiển thị thông báo thành công
        messages.success(request, "Mật khẩu đã được thay đổi thành công.")
        return redirect('dangnhap')  # Chuyển hướng về trang đăng nhập

    return render(request, 'pages/reset_password.html')