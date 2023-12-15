from django.shortcuts import render
from django.contrib.auth.decorators import login_required



def home(request):
    return render(request, 'beandex/home.html')

def profile(request):
    return render(request, 'beandex/profile.html')