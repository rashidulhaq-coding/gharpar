from email import message
from django.shortcuts import render
from .token import account_activation_token
from django.http.response import HttpResponse, HttpResponseRedirect
from .forms import Employee_User, RegistrationForm,UserEditForm,Employee_form
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.template.loader import render_to_string
from .models import Employee, User
from django.contrib.auth import login
from django.core.mail import send_mail
from .restrictions import *
from django.contrib import messages

# Create your views here.
def accounts_register(request):
    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():
            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])

            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = "Activate you Account"
            message = render_to_string('registration/account_activation_email.html',{
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            user.email_user(subject=subject,message=message)
            messages.success(request, f'Account created successfully. Please check your email to activate your account.')
            return HttpResponse('registered successfully and activation sent.')
    
    else:
        registerForm = RegistrationForm()
    return render(request,'registration/register.html',{'form':registerForm})

def activate(request,uidb64,token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = uid)
    
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user= None
    
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active = True
        user.save()
        login(request,user)
        return redirect('login')
    
    else:
        return render(request,'registration/activation_invalid.html')
    

# user update view

def user_update(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, request.FILES, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('user_update')
    else:
        user_form = UserEditForm(instance=request.user)
    return render(request, 'admin/create_service.html', {'form': user_form,'title':'Update User'})


# Employee creation by admin
@only_admin
def employee_create_view(request):
    # creating employee with user form and employee form
    if request.method == 'POST':
        user_form = Employee_User(request.POST)
        employee_form = Employee_form(request.POST)
        if user_form.is_valid() and employee_form.is_valid():
            user = user_form.save(commit=False)
            user.is_active = True
            user.is_employee= True
            password = User.objects.make_random_password(
                length=14, allowed_chars="abcdefghjkmnpqrstuvwxyz01234567889")  # zvk0hawf8m6394
            user.set_password(password)
            email = user_form.cleaned_data['email']
            send_mail(
                subject='Account Created',
                message='your account has been created with your email and password is '+password,
                from_email="test@gmail.com",
                recipient_list=[email, ],
                fail_silently=False,

            )
            user.save()
            employee = employee_form.save(commit=False)
            employee.user = user
            employee.save()
            messages.success(request, f'Employee created successfully!')
            return redirect('employee_list_view')
    else:
        user_form = Employee_User()
        employee_form = Employee_form()
    return render(request, 'admin/employee_create.html', {'form': user_form, 'employee_form': employee_form, 'title': 'Create Employee'})

# employee edit view
@only_admin
def employee_edit_view(request,id):
    user = get_object_or_404(User, id=id)
    if request.method == 'POST':
        user_form = Employee_User(request.POST, instance=user)
        employee_form = Employee_form(request.POST, instance=user.employee)
        if user_form.is_valid() and employee_form.is_valid():
            user_form.save()
            employee_form.save()
            messages.success(request, f'Employee updated successfully!')
            return redirect('employee_list_view')
    else:
        user_form = Employee_User(instance=user)
        employee_form = Employee_form(instance=user.employee)
    return render(request, 'admin/employee_create.html', {'form': user_form, 'employee_form': employee_form, 'title': 'Edit '+user.first_name+' '+user.last_name})

# employee delete view
@only_admin
def employee_delete_view(request,id):
    user = get_object_or_404(User, id=id)
    employee= get_object_or_404(Employee, user=user)
    if request.method == 'POST':
        user.is_active = False
        employee.delete()
        user.save()
        messages.success(request, f'Employee deleted successfully!')
        return redirect('employee_list_view')
    return render(request, 'admin/delete_view.html', {'delete': user.first_name+' '+user.last_name})


# def admin_package_delete(request, pk):
#     package = get_object_or_404(Package, pk=pk)
#     if request.method == 'POST':
#         package.delete()
#         return redirect('admin_package_view')
#     return render(request, 'admin/delete_view.html', {'delete': package})

# Employee list view
@only_admin
def employee_list_view(request):
    # list of employees
    employees = Employee.objects.all()
    return render(request, 'admin/employee_list.html', {'employees': employees})

