from django.contrib import admin
from .models import Category, Service, Package, Appointment

admin.site.register(Category)
admin.site.register(Service)
admin.site.register(Package)
admin.site.register(Appointment)

# filter by category


admin.site.site_header = 'Salon Admin'
admin.site.site_title = 'Salon Admin'
admin.site.index_title = 'Salon Admin'
admin.site.site_url ='/admin/'