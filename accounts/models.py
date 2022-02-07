from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    image = models.ImageField(
        upload_to='profile_pictures', null=True, blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name', 'last_name']
    is_employee = models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    objects = UserManager()

    def __str__(self):
        return self.email

class Employee(models.Model):
    JOBS = (
        ('Fashion Designer', 'Fashion Designer'),
        ('Beautician', 'Beautician'),
        ('Hair Stylist', 'Hair Stylist'),
        ('Makeup Artist', 'Makeup Artist'),
        ('Nail Artist', 'Nail Artist'),
        ('Other', 'Other'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, choices=JOBS, default='Other')
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        verbose_name = 'employee'
        verbose_name_plural = 'employees'
    
    def __str__(self):
        return self.user.first_name + ' ' + self.user.last_name

class Shift(models.Model):
    name = models.CharField(max_length=100,default='Morning Shift')
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    
    
    def __str__(self):
        #return self.name + ' ' + self.start_time.strftime('%H:%M') + ' - ' + self.end_time.strftime('%H:%M')
        return self.name

# timing model for employee
class Timing(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, default=1)
    time_slot = models.TimeField(null=True, blank=True)

    def __str__(self):
        #return self.employee.user.first_name + ' ' + self.shift.name + ' ' + self.time_slot.strftime('%H:%M')
        return self.shift.name
    

class Holiday(models.Model):
    holiday_date = models.DateField()
    description = models.CharField(max_length=100)
    def __str__(self):
        return self.holiday_date.strftime('%Y-%m-%d') + ' ' + self.description
