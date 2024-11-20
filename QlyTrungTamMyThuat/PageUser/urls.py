from django.urls import path
from . import views

urlpatterns = [
    path('', views.user, name='user'),
    path('dangky/',views.dangky,name='dangky'),
    path('dangnhap/',views.dangnhap,name='dangnhap'),
    path('quenmk/',views.quenmk,name='quenmk'),
    path('dangkytuvan/',views.dangkytuvan,name='dangkytuvan')
]
