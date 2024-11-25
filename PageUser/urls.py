from django.urls import path
from . import views

urlpatterns = [
    path('', views.user, name='user'),
    path('dangky/',views.register,name='dangky'),
    path('dangnhap/',views.userlogin,name='dangnhap'),
    path('quenmk/',views.quenmk,name='quenmk'),
    path('dangkytuvan/',views.LoadPhieuDK,name='dangkytuvan'),
    path('gioithieu/',views.gioithieu,name='gioithieu'),
    path('chinhsachbaomat/',views.chinhsachbaomat,name='chinhsachbaomat'),
    path('hdthanhtoan/',views.hdthanhtoan,name='hdthanhtoan'),
    path('chinhsachdichvu/',views.chinhsachdichvu,name='chinhsachdichvu'),
    path('khoahoc/',views.DSKhoaHoc,name='khoahoc'),
    path('khoahoc/DSL/<str:ml>/', views.DSTheoKH, name='DSTheoKH'),

    path('khoahoc/ttkhoahoc/<str:mlop>',views.ChiTietLop,name='ttkhoahoc'),
    path('logout', views.logout_view, name='logout'),
    path('giaovien/', views.giaovien, name='giaovien'),
    path('chinhanh/',views.chinhanh,name='chinhanh'),
    path('giaovien/chitietgiaovien/', views.chitietgiaovien, name='chitietgiaovien'),
    path('giohang/', views.giohang, name='giohang'),
    path('tthocvien/',views.thongtinhv,name='tthocvien'),
    path('lichsukh/',views.lichsukh,name='lichsukh')
]
