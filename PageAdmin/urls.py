from django.urls import path
from . import views



urlpatterns = [
    path('<str:idtaikhoan>/', views.admin, name='admin'),
    path('lichhoc/<str:idtaikhoan>/',views.lichhoc,name='lichhoc_admin'),
    
    path('giaovien/',views.giaovien, name='giaovien_admin'),
    path('hocvien/',views.hocvien,name='hocvien'),
    path('thanhtoan/',views.thanhtoan,name='thanhtoan'),
    
    path('giaovien/them_gv/',views.them_gv,name='them_gv'),
    path('hocvien/them_hv/',views.them_hv,name='them_hv'),
    path('khoahoc/them_kh/',views.them_kh,name='them_kh'),
    path('thanhtoan/them_hd/',views.them_hd,name='them_hd'),
    path('giaovien/sua_gv/',views.sua_gv,name='sua_gv'),
    path('hocvien/sua_hv/',views.sua_hv,name='sua_hv'),
    path('khoahoc/sua_kh/',views.sua_kh,name='sua_kh'),
    path('thanhtoan/sua_hd/',views.sua_hd,name='sua_hd'),
]