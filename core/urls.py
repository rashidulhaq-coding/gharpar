from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    # Common urls
    path('', home_view, name='home'),
    path('services/', services_view, name='services'),
    path('about/',about_view, name='about'),
    path('contact/',contact_view, name='contact'),
    path('services/book/<int:pk>',
         service_booking_view, name='book_service'),
    path('cart/', cart_view, name='cart'),
    path('cart/delete/<int:pk>', cart_delete, name='cart_delete'),
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
    path('appointment/<str:name>/', admin_appoitments_list_view, name='admin_appoitment_list_view'),
    path('appointment/status/<int:pk>/', admin_appoitment_status, name='admin_appoitment_status'),
    path('leaves/',leave_request, name='leaves'),
    path('reviews/',review_list_view, name='reviews'),
    
    
    
    path('booking/services', booking_services, name='booking_services'),
    path('booking/<str:pk>/', booking_employee, name='booking_employee'),
    # path('booking_employee_confirm/<str:pk>/<str:package>/',booking_package, name='booking_employee_confrim'),
    path('validate_employee/', csrf_exempt(validate_employee),name='validate_employee'),
    path("validate_date/", csrf_exempt(validate_date), name="validate_date"),
    path("validate_time/<str:date>",csrf_exempt(validate_time), name="validate_time"),
    # user dashboard
    path('user/dashboard/', user_dashboard, name='user_dashboard'),
    path('user/appoitment/<str:name>/',
         user_appointments, name='user_appoitment_view'),
    path('user/appointment/<int:pk>/',edit_booking, name='edit_booking'),
    path('user/invoice/<int:pk>/', invoice, name='invoice'),
    path('rate/<int:id>', rate, name="rate"),
    
    
    
    # employee urls
    path('employee/', employee_dashboard, name='employee_dashboard'),
    path('employee/appointments/<str:name>', employee_appointment_view, name='employee_appointment_view'),
    path('employee/timings/', employee_timing_view, name='employee_timing_view'),
    path('employee/timings/create/', employee_timing_create, name='employee_timing_create'),
    path('employee/timings/edit/<str:pk>',employee_timing_edit, name='employee_timing_edit'),
    path('employee/timings/delete/<str:pk>',employee_timing_delete, name='employee_timing_delete'),
    
    
    path('holiday/', employee_holiday_view, name='holiday'),
    path('holiday_create/', create_leave, name='holiday_create'),
    path('leave_status/<str:id>', leave_status, name='leave_status'),
    path('holiday/delete/<str:id>', leave_delete, name='holiday_delete'),
    
    
    
    
    
    
    
    # user views
]
