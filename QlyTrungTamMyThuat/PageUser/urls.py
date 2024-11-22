from django.urls import path
from . import views

urlpatterns = [
    path('', views.user, name='user'),
    path('dangky/',views.register,name='dangky'),
    path('dangnhap/',views.userlogin,name='dangnhap'),
    path("dangxuat/", views.user_logout, name="dangxuat"),
    path('quenmk/',views.quenmk,name='quenmk'),
    path('dangkytuvan/',views.dangkytuvan,name='dangkytuvan'),
    path('gioithieu/',views.gioithieu,name='gioithieu'),
    path('chinhsachbaomat/',views.chinhsachbaomat,name='chinhsachbaomat'),
    path('hdthanhtoan/',views.hdthanhtoan,name='hdthanhtoan'),
    path('chinhsachdichvu/',views.chinhsachdichvu,name='chinhsachdichvu'),
    path('khoahoc/',views.khoahoc,name='khoahoc'),
    path('khoahoc/ttkhoahoc',views.ttkhoahoc,name='ttkhoahoc'),
    path('giaovien/', views.giaovien, name='giaovien'),
    path('chinhanh/',views.chinhanh,name='chinhanh'),
    path('giaovien/chitietgiaovien/', views.chitietgiaovien, name='chitietgiaovien'),
    path('giohang/', views.giohang, name='giohang'),
]
