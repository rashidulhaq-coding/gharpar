from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

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
    path('booking/<str:pk>/', booking_employee, name='booking_employee'),
    path('booking_employee_confirm/<str:pk>/<str:package>/',booking_package, name='booking_employee_confrim'),
    path('validate_employee/', csrf_exempt(validate_employee),name='validate_employee'),
    path("validate_date/", csrf_exempt(validate_date), name="validate_date"),
    path("validate_time/<str:date>",csrf_exempt(validate_time), name="validate_time"),
    # user dashboard
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    
    
    # employee urls
    path('employee/', employee_dashboard, name='employee_dashboard'),
    path('employee/appointments/', employee_appointment_view, name='employee_appointment_view'),
    path('employee/timings/', employee_timing_view, name='employee_timing_view'),
    path('employee/timings/create/', employee_timing_create, name='employee_timing_create'),
    path('employee/timings/edit/<str:pk>',employee_timing_edit, name='employee_timing_edit'),
    path('employee/timings/delete/<str:pk>',employee_timing_delete, name='employee_timing_delete'),
    
    
    
    
    
    
    
    
    # user views
]
