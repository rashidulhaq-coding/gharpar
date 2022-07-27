from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.utils import timezone
from django.forms import formset_factory
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from datetime import date, datetime, timedelta
import datetime
from django.core.mail import send_mail

from .models import *
from .forms import *
from core.forms import Service_Form

from accounts.restrictions import *
from accounts.forms import Timing_form, Employee_Holiday, Leave_Status_Form
from accounts.models import *
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


@only_admin
def employee_timing_view(request):
    timing = Timing.objects.all()
    shifts = Shift.objects.all()
    context = {
        'timing': timing,
        'shifts': shifts,
    }
    return render(request, 'employee/timing_view.html', context)


@only_admin
def employee_timing_create(request):

    if request.method == 'POST':
        shift = Shift.objects.get(pk=request.POST['shift'])
        time = request.POST['time']
        time = datetime.datetime.strptime(time, '%H:%M').time()
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


@only_admin
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


@only_admin
def employee_timing_delete(request, pk):
    timing = Timing.objects.get(pk=pk)
    if request.method == 'POST':
        timing.delete()
        return redirect('employee_timing_view')
    return render(request, 'admin/delete_view.html', {'delete': timing.time_slot})

def leave_request(request):
    today = datetime.datetime.today()
    last_30_days = datetime.datetime.now() - datetime.timedelta(days=30)
    leaves = Holiday.objects.filter(holiday=False,accepted='Pending',date__gte=today)
    rejected = Holiday.objects.filter(holiday=False,accepted='Rejected',date__gte=last_30_days)
    accepted = Holiday.objects.filter(holiday=False,accepted='Accepted',date__gte=last_30_days)
    pending = Holiday.objects.filter(holiday=False,accepted='Pending',date__gte=last_30_days)
    context = {'holidays': leaves,
               'accepted': accepted,
               'rejected': rejected,
               }
    return render(request, 'admin/leave.html', context)


def leave_status(request, id):
    leave = get_object_or_404(Holiday, uuid=id)
    if request.method == 'POST':
        form = Leave_Status_Form(request.POST, instance=leave)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.save()
            messages.success(
                request, "Leave status changed to "+leave.accepted)
            return redirect('holiday')
    else:
        form = Leave_Status_Form(instance=leave)
    return render(request, 'admin/create_service.html', {'form': form, 'title': 'Change Status of Leave'})

def leave_delete(request, id):
    leave = get_object_or_404(Holiday, uuid=id)
    if request.method == 'POST':
        leave.delete()
        messages.warning(request, leave+' deleted successfully')
        return redirect('holiday')
    return render(request, 'admin/delete_view.html', {'delete': leave})
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

def employee_holiday_view(request):
    user = request.user
    
    if user.is_authenticated:
        if user.is_employee:
            holidays = Holiday.objects.filter(created_by = user).order_by('-date')
            context ={
                'holidays': holidays,
            }
        elif user.is_superuser:
            holidays = Holiday.objects.filter(
                created_by=user).order_by('-date')
            context = {
                'holidays': holidays,
            }
    else:
        messages.error(request,'You do not have permission to view a holiday')
    return render(request, 'employee/holiday.html', context)



def create_leave(request):
    user = request.user
    if request.method == 'POST':
        form = Employee_Holiday(request.POST, request.FILES)
        if form.is_valid():
            date = form.cleaned_data['date']
            description= form.cleaned_data['description']
            image = form.cleaned_data['image']
            created_by =get_object_or_404(User, pk=request.user.id)
            holiday = False
            accepted = 'Pending'
            if user.is_superuser:
                holiday = True
                accepted = 'Accepted'
            holiday_exist = Holiday.objects.filter(date=date)
            if holiday_exist:
                messages.warning(request, "It already exists.")
                return redirect('holiday_create')
            else:
                Holiday.objects.create(created_by=created_by,date=date,holiday=holiday,description=description,accepted=accepted)
                return redirect('holiday')
    else:
        form = Employee_Holiday()
    
    return render(request, 'employee/create_holiday.html', {'form': form})
            


# user views
def home_view(request):
    services = Service.objects.all()[:10]
    packages = Package.objects.all()[:10]
    categories = Category.objects.all()
    review = Review.objects.all()[:10]
    # rating_list = []
    # for rating in review:
    #     rate = []
    #     services_list=[]
    #     # for service in rating.appointment.package.services.all():
    #     #     services_list.append(service.name)
    #     services_list = [service.name for service in rating.appointment.package.services.all()]
    #     l=[rating.author, services_list,
    #          range(1,rating.stars), rating.comment]
    #     rate.extend(l)
    #     rating_list.append(rate)
    # print(rating_list)

    context = {
        'services': services,
        'packages': packages,
        'categories': categories,
        'rating': review,
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

def about_view(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees
    }
    return render(request, 'core/about.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        msg = request.POST.get('msg', None)
        send_mail(
                subject='Client Contact',
                message="From "+name+"\n"+msg,
                from_email=email,
                recipient_list=['admin@gmail.com', ],
                fail_silently=False,
        )
        messages.success(request,"Message sended successfully")
        return redirect('about')
    else:
        return redirect('about')

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
        date= i.date.strftime("%Y/%m/%d")
        holiday_dates.append(date)
        # convert date to y/m/d format
    data = {
        'is_taken': Employee.objects.filter(id=username).exists(),
        'holidays': holiday_dates
    }
    return JsonResponse(data)


# @only_user
def validate_date(request):
    date = request.POST.get('date', None)
    user = request.POST.get('employee', None)
    holiday = Holiday.objects.filter(date=date).exists()
    leave = Holiday.objects.filter(created_by=user,date=date,accepted='Accepted').exists()
    dat = date.split('-')
    day = int(dat[2])
    date = dat[0]+'-'+dat[1]+'-'+str(day)
    if holiday:
        data = {
            'is_taken': True,
            'times': [],
            'holiday':'holiday',
        }
        return JsonResponse(data)
    elif leave:
        data = {
            'is_taken': True,
            'times': [],
            'holiday': 'Leave',
        }
        return JsonResponse(data)
    else:
        # print('date is ',date)
        appointments = Appointment.objects.filter(date=date)
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

def rate(request, id):
    appointment = Appointment.objects.get(id=id)
    if Review.objects.filter(appointment=appointment).count() > 0:
        review = get_object_or_404(Review,appointment=appointment)
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():  
            form.save()
            return redirect('user_appoitment_view', 'completed')
        form = ReviewForm(instance=review)
        context = {
            "form":form,
            "title":"Review",
        }
        return render(request, 'admin/create_service.html', context)
    else:
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            author = request.user
            stars = request.POST.get('stars')
            comment = request.POST.get('comment')
            review = Review(author=author, stars = stars,  comment=comment , appointment=appointment)
            review.save()
            return redirect('user_appoitment_view','completed')
        form = ReviewForm()
        context = {
                "form":form,
                "title":"Review",
            }
        return render(request, 'admin/create_service.html',context)