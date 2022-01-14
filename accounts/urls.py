from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import PasswordResetCompleteView,PasswordResetDoneView

from .forms import PwdChangeForm, UserLoginForm, PwdResetForm, PwdResetForm, PwdResetConfirmForm

urlpatterns = [
   path('password_change/',auth_views.PasswordChangeView.as_view(template_name='registration/password_change_form.html',form_class=PwdChangeForm),name='pwdchange'),
   path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
       template_name="registration/password_change_done.html"), name='password_change_done'),
   path('login/', auth_views.LoginView.as_view(template_name='registration/login.html',
        authentication_form=UserLoginForm), name='login'),
   path('logout/', auth_views.LogoutView.as_view(template_name='registration/loggedout.html'), name='logout'),
   path("register/", views.accounts_register, name="register"),
   path("activate/<slug:uidb64>/<slug:token>", views.activate, name="activate"),
   path('password_reset/',auth_views.PasswordResetView.as_view(template_name='registration/password_reset_form.html',form_class=PwdResetForm),name='pwdreset'),
   path('password_reset_confirm/<slug:uidb64>/<slug:token>/',auth_views.PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm.html',form_class=PwdResetConfirmForm),name='pwdresetconfirm'),
   path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),name="password_reset_done"),
   path('password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),name='password_reset_complete'),
   # user edit path view
   path('user_update/', views.user_update, name="user_update"),
   
   # employee view urls
   path('employee/', views.employee_list_view, name="employee_list_view"),
#    path('employee/<int:pk>/', views.employee_detail, name="employee_detail"),
   # create employee view
   path('employee/create/', views.employee_create_view,
        name="employee_create_view"),
   path('employee/<int:id>/update/', views.employee_edit_view,
        name="employee_edit_view"),
   path('employee/<int:id>/delete/', views.employee_delete_view, name="employee_delete_view"),
   
]
