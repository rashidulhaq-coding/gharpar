from django.shortcuts import get_object_or_404, redirect, render

from core.forms import Service_Form
from .models import *
from .forms import *
from django.utils import timezone
# import datetime
from datetime import datetime, timedelta
# import timedelta

# Admin views


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
    return render(request, 'core/admin/index.html', context)
# creating category view


def admin_category_view(request):
    categories = Category.objects.all()
    context = {
        'categories': categories
    }
    return render(request, 'core/admin/category_view.html', context)

# category create view


def admin_category_create(request):
    if request.method == 'POST':
        form = Category_Form(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('admin_category_view')
    else:
        form = Category_Form()
    return render(request, 'core/admin/create_service.html', {'form': form})

# category edit view


def admin_category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = Category_Form(request.POST, request.FILES, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.save()
            return redirect('admin_category_view')
    else:
        form = Category_Form(instance=category)
    return render(request, 'core/admin/create_service.html', {'form': form})

# category delete view


def admin_category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('admin_category_view')
    return render(request, 'core/admin/delete_view.html', {'delete': category})


def admin_service_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    services = Service.objects.filter(category=category)
    context = {
        'services': services,
        'category': category,
    }
    return render(request, 'core/admin/service_view.html', context)

# service edit view


def admin_service_edit(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        form = Service_Form(request.POST, request.FILES, instance=service)
        if form.is_valid():
            service = form.save(commit=False)
            service.save()
            return redirect('admin_service_view', service.category.pk)
    else:
        form = Service_Form(instance=service)
    return render(request, 'core/admin/create_service.html', {'form': form})

# service delete view


def admin_service_delete(request, pk):
    service = get_object_or_404(Service, pk=pk)
    if request.method == 'POST':
        service.delete()
        return redirect('admin_service_view', service.category.pk)
    return render(request, 'core/admin/delete_view.html', {'delete': service})


def create_service(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = Service_Form(request.POST, request.FILES)
        if form.is_valid():
            service = form.save(commit=False)
            service.created = timezone.now()
            service.category = category
            service.save()
            return redirect('admin_service_view', pk=pk)
    else:
        form = Service_Form()
    return render(request, 'core/admin/create_service.html', {'form': form})


def admin_package_view(request):
    packages = Package.objects.all()
    context = {
        'packages': packages
    }
    return render(request, 'core/admin/package_view.html', context)


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
            print(price)
            package.save()
            return redirect('admin_package_view')
    else:
        form = Package_Form()
    return render(request, 'core/admin/create_service.html', {'form': form})


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
            return redirect('admin_package_view')
    else:
        form = Package_Form(instance=package)
    return render(request, 'core/admin/create_service.html', {'form': form})


def admin_package_delete(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        package.delete()
        return redirect('admin_package_view')
    return render(request, 'core/admin/delete_view.html', {'delete': package})

# appoitment view
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
            return redirect('admin_appoitment_view')
    else:
        form = Appointment_Form(instance=appointment)
    return render(request, 'core/admin/create_service.html', {'form': form})




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
    return render(request, 'core/user/home.html', context)


def booking_package(request, pk):
    package = get_object_or_404(Package, pk=pk)
    if request.method == 'POST':
        package = package
        customer = request.user
        date = request.POST['date']
        time = request.POST['time']
        duration = package.duration
        t = time.split(':')
        h= int(t[0])
        minute = int(t[1])
        start_date = timedelta(hours=h, minutes=minute)
        total_minute = minute + duration
        if total_minute > 60:
            total_minute = total_minute - 60
            h = h + 1
        end_date = timedelta(hours=h, minutes=int(total_minute))
        booking = Appointment(customer=customer, package=package, date= date,
                              start_time=str(start_date), end_time=str(end_date))
        booking.save()
        return redirect('home')
    context = {
        'package': package.id,
    }
    return render(request, 'core/user/booking.html', context)
