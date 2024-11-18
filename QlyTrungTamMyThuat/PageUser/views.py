from django.shortcuts import render
from django.http import HttpResponse 

# Create your views herede
def user(request):
    return render(request, 'layout/layout-user.html')