from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from core.forms import Service_Form
from .models import *
from .forms import *
from django.utils import timezone
# import datetime
from datetime import datetime, timedelta
# import timedelta

from accounts.forms import Timing_form
from accounts.models import *
from django.forms import formset_factory

from django.http import HttpResponse, JsonResponse
from accounts.restrictions import *
from django.contrib import messages
# Admin views


@only_admin
def admin_dashboard(request):
    appointments = Appointment.objects.all()
    pending = appointments.filter(status='Pending').count()
    confirmed = appointments.filter(status='Confirmed').count()
    completed = appointments.filter(status='Completed').count()
    canceled = appointments.filter(status='Canceled').count()

    context = {
        'appointments': appointments.count(),
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
        'canceled': canceled,
    }
    return render(request, 'admin/admin_dashboard.html', context)
# creating category view


@only_admin
def admin_category_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'admin/category_view.html', context)

# category create view


@only_admin
def admin_category_create(request):
    if request.method == 'POST':
        form = Category_Form(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, 'Category created successfully')
            return redirect('admin_category_view')
    else:
        form = Category_Form()
    return render(request, 'admin/create_service.html', {'form': form,'title':'Create Category'})

# category edit view


@only_admin
def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = Category_Form(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            messages.success(request, 'Category updated successfully')
            return redirect('admin_category_view')
    else:
        form = Category_Form(instance=category)
    return render(request, 'admin/create_service.html', {'form': form,'title':'Edit Category'})

# category delete view


@only_admin
def admin_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        messages.warning(request, 'Category deleted successfully')
        return redirect('admin_category_view')
    return render(request, 'admin/delete_view.html', {'delete': category})


@only_admin
def admin_service_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    services = Service.objects.filter(category=category)
    context = {
        'services': services,
        'category': category,
    }
    return render(request, 'admin/service_view.html', context)

# service edit view


@only_admin
def admin_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = Service_Form(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            messages.success(request, service.name+' service updated successfully')
            return redirect('admin_service_view', service.category.pk)
    else:
        form = Service_Form(instance=service)
    return render(request, 'admin/create_service.html', {'form': form,'title':'Edit Service'})

# service delete view


@only_admin
def admin_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        messages.warning(request, service.name+'service deleted successfully')
        return redirect('admin_service_view', service.category.pk)
    return render(request, 'admin/delete_view.html', {'delete': service})


@only_admin
def create_service(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = Service_Form(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created = timezone.now()
            service.category = category
            service.save()
            messages.success(request, service.name+' service created successfully')
            return redirect('admin_service_view', pk=pk)
    else:
        form = Service_Form()
    return render(request, 'admin/create_service.html', {'form': form,'title':'Create Service'})


@only_admin
def admin_package_view(request):
    packages = Package.objects.all()
    context = {
        'packages': packages
    }
    return render(request, 'admin/service_view.html', context)


@only_admin
def admin_package_create(request):
    if request.method == 'POST':
        form = Package_Form(request.POST, request.FILES)
        if form.is_valid():
            package = form.save(commit=False)
            services = form.cleaned_data['services']
            discount = form.cleaned_data['discount']
            package.created_by = request.user
            # retrieve services from form
            duration = 0
            price = 0
            for service in services:
                duration += service.duration
                price += service.price
            package.duration = duration
            package.price = float(price) - (float(price)
                                            * float(discount) / 100)
            package.image = services[0].image
            package.save()
            messages.success(request, 'Package created successfully')
            return redirect('admin_package_view')
    else:
        form = Package_Form()
    return render(request, 'admin/create_service.html', {'form': form ,'title':'Create Package'})


@only_admin
def admin_package_edit(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        form = Package_Form(request.POST, request.FILES, instance=package)
        if form.is_valid():
            package = form.save(commit=False)
            services = form.cleaned_data['services']
            discount = form.cleaned_data['discount']
            # retrieve services from form
            duration = 0
            price = 0
            for service in services:
                duration += service.duration
                price += service.price
            package.duration = duration
            package.price = float(price) - (float(price)
                                            * float(discount) / 100)
            package.image = services[0].image
            package.save()
            messages.success(request, 'Package updated successfully')
            return redirect('admin_package_view')
    else:
        form = Package_Form(instance=package)
    return render(request, 'admin/create_service.html', {'form': form,'title':'Edit Package'})


@only_admin
def admin_package_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        package.delete()
        messages.warning(request, 'Package deleted successfully')
        return redirect('admin_package_view')
    return render(request, 'admin/delete_view.html', {'delete': package})

# appoitment view


@only_admin
def admin_appoitments_list_view(request, name):
    appointments = Appointment.objects.all()
    
    if name == 'pending':
        cancelled = appointments.filter(status='Cancelled')
        pending = appointments.filter(status='Pending')
        context = {
            'cancelled': cancelled,
            'pending': pending,
        }
    else:
        confirmed = appointments.filter(status='Confirmed')
        context = {
            'confirmed': confirmed,
        }
    return render(request, 'admin/appointment_view.html', context)

@only_admin
def admin_appoitment_view(request):
    appointments = Appointment.objects.all()
    # get the appointments where status is pending
    confirmed = appointments.filter(status='Confirmed')
    cancelled = appointments.filter(status='Cancelled')
    pending = appointments.filter(status='Pending')
    context = {
        'appointments': appointments,
        'confirmed': confirmed,
        'cancelled': cancelled,
        'pending': pending,
    }
    return render(request, 'core/admin/appointment_view.html', context)

# appointment staus change view


def admin_appoitment_status(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    if request.method == 'POST':
        form = Appointment_Form(request.POST, instance=appointment)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.save()
            # if request.user.employee:
            #     return redirect('employee_appointment_view')
            # else:
            messages.success(
                request, "Appointment status changed to "+appointment.status)
            return redirect('admin_appoitment_list_view', appointment.status)
    else:
        form = Appointment_Form(instance=appointment)
    return render(request, 'admin/create_service.html', {'form': form,'title':'Change Status'})

# employee view


@only_employee
def employee_dashboard(request):
    appointments = Appointment.objects.filter(employee=request.user.employee)
    pending = appointments.filter(status='Pending').count()
    confirmed = appointments.filter(status='Confirmed').count()
    completed = appointments.filter(status='Completed').count()
    canceled = appointments.filter(status='Canceled').count()
    context = {
        'appointments': appointments.count(),
        'pending': pending,
        'confirmed': confirmed,
        'completed': completed,
        'canceled': canceled,
    }
    return render(request, 'admin/admin_dashboard.html', context)


@only_employee
def employee_appointment_view(request,name):
    appointments = Appointment.objects.filter(employee=request.user.employee)
    if name == 'pending':
        cancelled = appointments.filter(status='Cancelled')
        pending = appointments.filter(status='Pending')
        context = {
            'cancelled': cancelled,
            'pending': pending,
        }
    else:
        confirmed = appointments.filter(status='Confirmed')
        context = {
            'confirmed': confirmed,
        }
    return render(request, 'admin/appointment_view.html', context)

# timing set up by employee


@only_employee
def employee_timing_view(request):
    timing = Timing.objects.all()
    shifts = Shift.objects.all()
    context = {
        'timing': timing,
        'shifts': shifts,
    }
    return render(request, 'employee/timing_view.html', context)


@only_employee
def employee_timing_create(request):

    if request.method == 'POST':
        shift = Shift.objects.get(pk=request.POST['shift'])
        time = request.POST['time']
        time = datetime.strptime(time, '%H:%M').time()
        start_time = shift.start_time
        end_time = shift.end_time
        forms = Timing_form(request.POST)
        if forms.is_valid():
            timing = forms.save(commit=False)
            # timing.employee = request.user.employee
            if time > start_time and time < end_time:
                timing.time_slot = time
                timing.shift = shift
                timing.save()
                return redirect('employee_timing_view')
            else:
                messages.error(request, 'Time slot is not in shift time')
                return redirect('employee_timing_create')
    else:
        forms = Timing_form()

    return render(request, 'employee/create_timing.html', {'forms': forms, 'shifts': Shift.objects.all(), 'title': 'Create Timing'})


@only_employee
def employee_timing_edit(request, pk):

    timing = Timing.objects.get(pk=pk)
    if request.method == 'POST':
        forms = Timing_form(request.POST, instance=timing)
        shift = Shift.objects.get(pk=request.POST['shift'])
        time = request.POST['time']
        time = datetime.strptime(time, '%H:%M').time()
        start_time = shift.start_time
        end_time = shift.end_time
        if forms.is_valid():
            timing = forms.save(commit=False)
            # timing.employee = request.user.employee
            if time > start_time and time < end_time:
                timing.time_slot = time
                # timing.shift = shift
                timing.save()
                return redirect('employee_timing_view')
    else:
        forms = Timing_form(instance=timing)
    return render(request, 'employee/create_timing.html', {'forms': forms, 'shifts': Shift.objects.all()})


@only_employee
def employee_timing_delete(request, pk):
    timing = Timing.objects.get(pk=pk)
    if request.method == 'POST':
        timing.delete()
        return redirect('employee_timing_view')
    return render(request, 'admin/delete_view.html', {'delete': timing.time_slot})


# user views
def home_view(request):
    services = Service.objects.all()[:10]
    packages = Package.objects.all()[:10]
    categories = Category.objects.all()

    context = {
        'services': services,
        'packages': packages,
        'categories': categories,
    }
    return render(request, 'core/home.html', context)

def services_view(request):
    categories = Category.objects.all()
   
    services=[]
    for category in categories:
        service = Service.objects.filter(category=category)
        services.append({'category': category, 'services': service})
    context = {
        'categories': categories,
        'services': services,
    }
    return render(request, 'core/services.html', context)

@only_user
def service_booking_view(request, pk):
    service = Service.objects.get(pk=pk)
    user = request.user
    order_service = OrderService.objects.filter(
        user=user, service=service, ordered=False)
    if order_service.exists():
        messages.error(request, 'Service is already booked')
        return redirect('services')
    else:
        order_service = OrderService.objects.create(user= user,service=service)
        services_by_user = OrderService.objects.filter(user=request.user)
        messages.success(request, 'Service is booked')
        return redirect('services')


@only_user
def cart_view(request):
    order_services = OrderService.objects.filter(user=request.user, ordered=False)
    total_price = 0
    total_duration = 0
    for order_service in order_services:
        # calculate total price and time
        total_price += order_service.service.price  
        total_duration += order_service.service.duration
    
    return render(request, 'core/cart.html', {'order_services': order_services, 'total_price': total_price, 'total_duration': total_duration})


@only_user
def cart_delete(request, pk):
    order = OrderService.objects.get(pk=pk)
    order.delete()
    return redirect('cart')


@only_user
def booking_services(request):
    order_services= OrderService.objects.filter(user=request.user, ordered=False)
    
    duration = 0
    price = 0
    for order in order_services:
        duration += order.service.duration
        price += order.service.price
    package = Package.objects.create(
        duration=duration, price=price, created_by=request.user)
    for order in order_services:
        package.services.add(order.service)
    package.save()
    order_services.update(ordered=True)
    order_services.delete()
    return redirect('booking_employee', pk=package.pk)

# @only_user


@only_user
def booking_employee(request, pk):
    employees = Employee.objects.all()
    package = get_object_or_404(Package, pk=pk)

    if request.method == 'POST':
        package = package
        customer = request.user
        date = request.POST.get('date', None)
        time = request.POST.get('time', None)
        employee = Employee.objects.get(id=request.POST.get('employee'))
        date_only = date.replace('/', '-')
        date = date_only
        duration = package.duration
        t = time.split(':')
        h = int(t[0])
        minute = int(t[1])
        start_date = timedelta(hours=h, minutes=minute)
        total_minute = minute + duration
        if total_minute > 60:
            total_minute = total_minute - 60
            h = h + 1
        end_date = timedelta(hours=h, minutes=int(total_minute))
        booking = Appointment(employee=employee, customer=customer, package=package, date=date,
                              start_time=str(start_date), end_time=str(end_date))
        booking.save()
        messages.success(request, 'Booking is successful')
        return redirect('cart')
    context = {
        'package': package.id,
        'employees': employees,
    }
    return render(request, 'core/booking_employee.html', context)


# @only_user
def validate_employee(request):
    username = request.POST.get('employee', None)
    holiday = Holiday.objects.all()
    holiday_dates = []
    for i in holiday:
        date= i.holiday_date.strftime("%Y/%m/%d")
        holiday_dates.append(date)
        # convert date to y/m/d format
        print(date)
    data = {
        'is_taken': Employee.objects.filter(id=username).exists(),
        'holidays': holiday_dates
    }
    print(data['holidays'])
    return JsonResponse(data)


# @only_user
def validate_date(request):
    date = request.POST.get('date', None)
    holiday = Holiday.objects.filter(holiday_date=date).exists()
    
    dat = date.split('-')
    day = int(dat[2])
    date = dat[0]+'-'+dat[1]+'-'+str(day)
    if holiday:
        data = {
            'is_taken': True,
            'times': []
        }
        return JsonResponse(data)
    else:
        # print('date is ',date)
        appointments = Appointment.objects.filter(date=date)
        print(appointments)
        times = Timing.objects.all()
        available_times = []
        if appointments.exists():
            
            for time in times:
                for apointment in appointments:
                    if apointment.start_time == time.time_slot:
                        pass
                    elif time.time_slot > apointment.start_time and time.time_slot < apointment.end_time:
                        pass
                    else:
                        available_times.append(time.time_slot)
        else:
            for time in times:
                available_times.append(time.time_slot)
        print(available_times)
        data = {
            'is_taken': False,
            'times': available_times,
        }
        return JsonResponse(data)


# @only_user
def validate_time(request, date):
    time = request.POST.get('time', None)
    data = {
        'is_taken': Timing.objects.filter(time=time).exists(),
    }
    return JsonResponse(data)


# @only_user
# def booking_package(request, pk, package):
#     package = get_object_or_404(Package, pk=package)
#     employee = get_object_or_404(Employee, pk=pk)
#     if request.method == 'POST':
#         package = package
#         customer = request.user
#         date = request.POST['time']
#         print(date)
#         splitting = date.split()
#         date_only = splitting[0]
#         time_only = splitting[1]
#         date_only = date_only.replace('/', '-')
#         time = time_only
#         date = date_only
#         duration = package.duration
#         t = time.split(':')
#         h = int(t[0])
#         minute = int(t[1])
#         start_date = timedelta(hours=h, minutes=minute)
#         total_minute = minute + duration
#         if total_minute > 60:
#             total_minute = total_minute - 60
#             h = h + 1
#         end_date = timedelta(hours=h, minutes=int(total_minute))
#         booking = Appointment(employee=employee, customer=customer, package=package, date=date,
#                               start_time=str(start_date), end_time=str(end_date))
#         print(booking)
#         booking.save()
#         return redirect('home')
#     context = {
#         'package': package.id,
#         'employee': employee.id,
#     }
#     return render(request, 'core/user/booking_package.html', context)


# user dashboard
@only_user
def user_dashboard(request):
    appointments = Appointment.objects.filter(customer=request.user)
    pending = appointments.filter(status='Pending').count()
    completed = appointments.filter(status='Completed').count()
    confirmed = appointments.filter(status='Confirmed').count()

    return render(request, 'user/user_dashboard.html', {'appointments': appointments.count(), 'pending': pending, 'completed': completed, 'confirmed': confirmed})


@only_user
def user_appointments(request,name):
    appointments = Appointment.objects.filter(customer=request.user)
    
    if name == 'pending':
        cancelled = appointments.filter(status='Cancelled')
        pending = appointments.filter(status='Pending')
        context = {
            'cancelled': cancelled,
            'pending': pending,
        }
    elif name == 'completed':
        completed = appointments.filter(status='Completed')
        context = {
            'completed': completed,
        }
    else:
        confirmed = appointments.filter(status='Confirmed')
        context = {
            'confirmed': confirmed,
        }
    return render(request, 'user/appointment_view.html', context)
        

@only_user
def edit_booking(request, pk):
    appointment = get_object_or_404(Appointment, pk=pk)
    package = appointment.package
    package_id = package.id
    appointment.delete()
    return redirect(booking_employee, pk=package_id)

    # if request.method == 'POST':
    #     # booking_package(request, appointment.employee.id, appointment.package.id)
    #     return redirect('user_dashboard')
    # return render(request, 'core/user/edit_booking.html', {'appointment': appointment})

# def cancel_booking(request, pk):
#     appointment = get_object_or_404(Appointment, pk=pk)
#     if request.method == 'POST':
#         appointment.delete()
#         return redirect('user_dashboard')
#     return render(request, 'core/user/cancel_booking.html', {'appointment': appointment})
