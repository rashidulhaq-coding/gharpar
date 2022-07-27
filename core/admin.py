from django.contrib import admin
from .models import Category, Service, Package, Appointment, OrderService,Review

admin.site.register(Category)
admin.site.register(Service)

admin.site.register(Package)
admin.site.register(OrderService)
admin.site.register(Appointment)
admin.site.register(Review)


admin.site.site_header = 'Salon Admin'
admin.site.site_title = 'Salon Admin'
admin.site.index_title = 'Salon Admin'
admin.site.site_url ='/admin/'