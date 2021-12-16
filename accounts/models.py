from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager

# Create your models here.
class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, blank=False,
                              error_messages={
                                  'unique': "A user with that email already exists.",
                              })

    image = models.ImageField(
        upload_to='profile_pictures',null=True,blank=True)
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ['first_name','last_name']
    is_employee=models.BooleanField(default=False)

    def __unicode__(self):
        return self.email

    objects = UserManager()