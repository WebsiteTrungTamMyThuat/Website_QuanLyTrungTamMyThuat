from django.urls import path
from . import views


urlpatterns = [
    path('', views.user, name='user'),
    path('dangky/',views.register,name='dangky'),
    path('dangnhap/',views.userlogin,name='dangnhap'),
    path('dangkytuvan/',views.LoadPhieuDK,name='dangkytuvan'),
    path('gioithieu/',views.gioithieu,name='gioithieu'),
    path('chinhsachbaomat/',views.chinhsachbaomat,name='chinhsachbaomat'),
    path('hdthanhtoan/',views.hdthanhtoan,name='hdthanhtoan'),
    path('chinhsachdichvu/',views.chinhsachdichvu,name='chinhsachdichvu'),
    path('khoahoc/',views.DSKhoaHoc,name='khoahoc'),
    path('khoahoc/DSL/<str:ml>/', views.DSTheoKH, name='DSTheoKH'),
    path('khoahoc/ttkhoahoc/<str:mlop>',views.ChiTietLop,name='ttkhoahoc'),

    path("filter-khoahoc", views.filter_khoahoc, name="filter_khoahoc"),

    path('logout', views.logout_view, name='logout'),
    path('giaovien/', views.giaovien, name='giaovien'),
    path('chinhanh/',views.chinhanh,name='chinhanh'),
    path('giaovien/chitietgiaovien/', views.chitietgiaovien, name='chitietgiaovien'),
    path('tthocvien/',views.thongtinhv,name='tthocvien'),
    path('lichsukh/',views.lichsukh,name='lichsukh'),


    path('giohang/', views.LoadGioHang, name='giohang'),
    path('them-vao-gio-hang/<str:malop>/', views.them_vao_gio_hang, name='them_vao_gio_hang'),
    path('xoa-giỏ-hàng/<str:malop>/', views.xoa_hoan_tat, name='xoa_hoan_tat'),
    path('thanh-toan/', views.thanh_toan, name='thanh_toan'),

   
    path('momo-payment/', views.momo_payment, name='momo_payment'),
    path('thank-you/', views.momo_return, name='thank-you'),
    path('momo-notify/', views.momo_notify, name='momo_notify'),
    path('success/',views.success, name = 'success'),

    path('quenmk/',views.quenmk,name='quenmk'),
    path('forgot-password/', views.forgot_password, name='forgot_password'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),
]
