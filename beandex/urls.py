from django.urls import path
from beandex import views

urlpatterns = [
    path('', views.home, name='home'),
]
