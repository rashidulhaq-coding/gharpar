import uuid
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
    # employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    # shift = models.ForeignKey(Shift, on_delete=models.CASCADE, default=1)
    time_slot = models.TimeField(null=True, blank=True)

    def __str__(self):
        #return self.employee.user.first_name + ' ' + self.shift.name + ' ' + self.time_slot.strftime('%H:%M')
        return self.time_slot.strftime('%H:%M')



class Holiday(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False,null=True, blank=True)
    CHOICES= (
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Pending', 'Pending'),
        )
    created_by = models.ForeignKey(
        User, related_name='Holiday', null=True, blank=True,on_delete=models.SET_NULL)
    date = models.DateField()
    holiday = models.BooleanField(default=False, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    accepted = models.CharField(choices=CHOICES,default='Pending', max_length=100,null=True, blank=True)
    image = models.ImageField(upload_to="holiday_pictures", blank=True, null=True)
    
    def __str__(self):
        return str(self.created_by) + ' ' + self.date.strftime('%Y-%m-%d')
