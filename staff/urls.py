from django.urls import path
from . import views

app_name = 'staff'

urlpatterns = [
    path('', views.home, name='home'),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/create/', views.staff_create, name='staff_create'),
    path('staff/<uuid:uuid>/', views.staff_detail, name='staff_detail'),
    path('staff/<uuid:uuid>/edit/', views.staff_edit, name='staff_edit'),
    path('staff/<uuid:uuid>/qr-sticker/', views.download_qr_sticker, name='download_qr_sticker'),
    path('verify/<uuid:uuid>/', views.verify_staff, name='verify'),
    path('print/<uuid:uuid>/', views.print_card, name='print_card'),
]