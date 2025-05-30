# app_name/urls.py
from django.urls import path
from . import views

app_name = "verify"

urlpatterns = [
    path('', views.home, name='home'),
    path('input_page/',views.input_page,name='input_page'),
    path('register/',views.signin,name='signin'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('upload/', views.upload_certificate, name='upload_certificate'),
    #path('result/',views.output_page,name='output_page'),
]
