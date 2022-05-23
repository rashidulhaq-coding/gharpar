from django.db import models
from accounts.models import User
from accounts.models import Employee

# category model for salon
class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    image = models.ImageField(upload_to='categories/', blank=True)
    
    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    image = models.ImageField(verbose_name='Image', upload_to='services')
    category = models.ForeignKey('Category', on_delete=models.CASCADE, verbose_name='Category')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Duration')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    
    class Meta:
        verbose_name = 'service'
        verbose_name_plural = 'services'
        ordering = ['-created']
    
    def __str__(self):
        return self.name

# package model for salon
class Package(models.Model):
    name = models.CharField(max_length=200, verbose_name='Name')
    description = models.TextField(verbose_name='Description')
    services = models.ManyToManyField(Service, verbose_name='Services')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Created by')
    duration = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Duration')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Price')
    discount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Discount', default=0)
    image = models.ImageField(verbose_name='Image', upload_to='packages')
    
    def __str__(self):
        return self.name

# Appoitment model 


class OrderService(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} ordered {self.service.name}"

class Appointment(models.Model):
    OPTIONS = (
        ('Pending','Pending'),
        ('Confirmed','Confirmed'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name='Employee',default=2)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Customer')
    package = models.ForeignKey(Package, on_delete=models.CASCADE, verbose_name='Package', blank=True, null=True)
    service = models.ManyToManyField(Service, verbose_name='Service', blank=True)
    status  = models.CharField(max_length=100,choices= OPTIONS,verbose_name='Status', default='Pending')
    date = models .DateField(verbose_name='Date')
    start_time = models.TimeField(verbose_name='Start Time')
    end_time = models.TimeField(verbose_name='End Time')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Created at')
    
    class Meta:
        verbose_name = 'appointment'
        verbose_name_plural = 'appointments'
        ordering = ['-created']
    
    def __str__(self):
        return self.customer.first_name + ' ' + self.customer.last_name
