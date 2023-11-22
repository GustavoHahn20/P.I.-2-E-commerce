from django.contrib import admin
from .models import *
from . import models

# Register your models here.

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'id', 'name'
    ordering = 'id',

