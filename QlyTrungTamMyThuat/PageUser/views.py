from django.shortcuts import render
from django.http import HttpResponse 

# Create your views herede
def user(request):
    return render(request, 'pages/user.html')

def dangky(request):
    return render(request,'layout/dangky.html')

def dangnhap(request):
    return render(request,'layout/dangnhap.html')

def quenmk(request):
    return render(request,'layout/quenmk.html')

def dangkytuvan(request):
    return render(request,'pages/dang-ky-tu-van.html')