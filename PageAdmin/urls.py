from django.urls import path
from . import views



urlpatterns = [
    path('<str:idtaikhoan>/', views.admin, name='admin'),
    path('lichhoc/<str:idtaikhoan>/',views.lichhoc,name='lichhoc_admin'),
    
    path('lophoc/<str:idtaikhoan>/',views.lophoc, name='lophoc_admin'),
    
    path('thongtincanhan/<str:idtaikhoan>/',views.thongtincanhan,name='thongtincanhan'),
    
    path('thanhtoan/<str:idtaikhoan>/',views.thanhtoan,name='thanhtoan'),
    
    path('luuthongtincanhan/<str:idtaikhoan>/',views.luuthongtincanhan,name='luuthongtincanhan'),
    
    path('doimatkhau/<str:idtaikhoan>/',views.doimatkhau,name='doimatkhau'),
]