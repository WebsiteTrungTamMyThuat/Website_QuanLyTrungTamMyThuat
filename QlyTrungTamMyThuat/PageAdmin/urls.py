from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin, name='admin'),
    path('giaovien_ad/',views.giaovien_ad,name='giaovien_ad'),
    path('khoahoc_ad/',views.khoahoc_ad,name='khoahoc_ad'),
    path('hocvien/',views.hocvien,name='hocvien'),
    path('thanhtoan/',views.thanhtoan,name='thanhtoan'),
    path('giaovien_ad/them_gv/',views.them_gv,name='them_gv'),
    path('hocvien/them_hv/',views.them_hv,name='them_hv'),
    path('khoahoc_ad/them_kh/',views.them_kh,name='them_kh'),
    path('thanhtoan/them_hd/',views.them_hd,name='them_hd'),
    path('giaovien_ad/sua_gv/',views.sua_gv,name='sua_gv'),
    path('hocvien/sua_hv/',views.sua_hv,name='sua_hv'),
    path('khoahoc_ad/sua_kh/',views.sua_kh,name='sua_kh'),
    path('thanhtoan/sua_hd/',views.sua_hd,name='sua_hd'),
]