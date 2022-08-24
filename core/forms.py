from django import forms
from django.forms import widgets
from django.utils.http import MONTHS
from .models import *
from django.utils import timezone
import datetime

# category model form for salon


class Category_Form(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(
       attrs={
           'placeholder': 'name',
           'class': 'form-control',
       }
   ),
       error_messages={
           'required': "This field is required",
           'invalid': "This field is invalid",
   })
    description=forms.CharField(widget=forms.Textarea(
       attrs={
           'placeholder': 'Description',
           'class': 'form-control',
       }
   ),
       error_messages={
           'required': "This field is required",
           'invalid': "This field is invalid",
   })
    image = forms.ImageField(widget=forms.FileInput(
       attrs={
           'placeholder': 'Image',
           'class': 'form-control',
       }))

    class Meta:
       model = Category
       fields = ['name', 'description', 'image',]

# creating Service model form
class Service_Form(forms.ModelForm):
   name= forms.CharField(widget=forms.TextInput(
       attrs = {
           'placeholder':'name',
           'class':'form-control',
       }
   ),
       error_messages = {
           'required' : "This field is required",
           'invalid' : "This field is invalid",
   })
   description=forms.CharField(widget=forms.Textarea(
       attrs={
           'placeholder': 'Description',
           'class': 'form-control',
       }
   ),
       error_messages={
           'required': "This field is required",
           'invalid': "This field is invalid",
   })
   image = forms.ImageField(widget=forms.FileInput(
       attrs={
           'placeholder': 'Image',
           'class': 'form-control',
       }))
#    category = forms.ModelChoiceField(queryset=Category.objects.all(), widget=forms.Select(
#        attrs={
#            'placeholder': 'Category',
#            'class': 'form-control',
#        }
#    ))
   price = forms.CharField(widget=forms.TextInput(
       attrs={
           'placeholder': 'Price',
           'class': 'form-control',
       }
   ),
       error_messages={
           'required': "This field is required",
           'invalid': "This field is invalid",
   })
   duration = forms.CharField(widget=forms.TextInput(
       attrs={
           'placeholder': 'Duration',
           'class': 'form-control',
       }
   ),
       error_messages={
           'required': "This field is required",
           'invalid': "This field is invalid",
   })

   # Metadata
   class Meta:
       model = Service
       fields = ['name', 'description','image','price', 'duration']

# package model form
class Package_Form(forms.ModelForm):
   name = forms.CharField(widget=forms.TextInput(
       attrs = {
           'placeholder':'name',
           'class':'form-control',
       }
   ),
       error_messages = {
           'required' : "This field is required",
           'invalid' : "This field is invalid",
   })
   description=forms.CharField(widget=forms.Textarea(
       attrs={
           'placeholder': 'Description',
           'class': 'form-control',
         }
   ))
   services = forms.ModelMultipleChoiceField(queryset=Service.objects.all(), widget=forms.SelectMultiple(
       attrs = {
           'placeholder':'Services',
           'class':'form-control',
         }
   ))
   image = forms.ImageField(widget=forms.FileInput(attrs = {
       'placeholder': 'Image',
       'class': 'form-control',
   }))
   discount = forms.CharField(widget=forms.TextInput(
       attrs= {
           'placeholder':'Discount',
           'class':'form-control',
         }
    ))
   
   # Metadata
   class Meta:
       model = Package
       fields = ['name', 'description','services','image','discount']
       
# appointment model form
class Appointment_Form(forms.ModelForm):
    # years = range(datetime.date.today().year, datetime.date.today().year+1)
    # m = list(range(datetime.date.today().month-1,datetime.date.today().month+1))
    # months = []
    # for month in m:
    #     months.append(MONTHS[month])
    
    # zip_iterator = zip(m, months)
    # a_dictionary = dict(zip_iterator)
    # dob = forms.DateField(
    #     label='What is your birth date?',
    #     # change the range of the years from 1980 to currentYear - 5
    #     widget=forms.SelectDateWidget(
            
    #         months=a_dictionary,
    #         years=years,
    #         attrs={
    #             'placeholder': 'Date',
    #             'class': 'form-control my-2',
    #         }
        
    #     )
        # widget=forms.SplitDateTimeWidget(
        #     # months=a_dictionary,
        #     years=years,
            
        # )
    # )
    class Meta:
       model = Appointment
       fields = ['status',]
       widgets = {
           'status': forms.Select(
                attrs={
                    'class': 'form-control',
                }
            ),
        }

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ["stars","comment"]
        widgets = {
            'stars': forms.Select(
                attrs={
                    'class': 'form-control mb-3', 'placeholder':'stars',
                }
            ),
            'comment': forms.Textarea(
                attrs={
                    'placeholder': 'Comments',
                    'class': 'form-control mb-3',
                }
            )
        }
