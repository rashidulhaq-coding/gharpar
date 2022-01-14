from django.urls import path
from .views import *

urlpatterns = [
    # Common urls
    path('', home_view, name='home'),
    
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('category/', admin_category_view, name='admin_category_view'),
    path('category/create/', admin_category_create, name='admin_category_create'),
    path('category/edit/<int:pk>/', admin_category_edit, name='admin_category_edit'),
    path('category/delete/<int:pk>/', admin_category_delete, name='admin_category_delete'),
    path('package/', admin_package_view, name='admin_package_view'),
    path('package/create/', admin_package_create, name='admin_package_create'),
    path('package/edit/<int:pk>/', admin_package_edit, name='admin_package_edit'),
    path('package/delete/<int:pk>/', admin_package_delete, name='admin_package_delete'),
    path('service/<str:pk>/', admin_service_view, name='admin_service_view'),
    path('service/edit/<str:pk>/', admin_service_edit, name='admin_service_edit'),
    path('service/delete/<str:pk>/', admin_service_delete, name='admin_service_delete'),
    path('service/add/<str:pk>', create_service, name='admin_service_add'),
    path('appoitment/', admin_appoitment_view, name='admin_appoitment_view'),
    path('appointment/status/<int:pk>/', admin_appoitment_status, name='admin_appoitment_status'),
    
    # path('booking/service/<str:pk>/', booking_service, name='booking_service'),
    path('booking/package/<str:pk>/', booking_package, name='booking_package'),
    
    
    
    
    
    # user views
]
