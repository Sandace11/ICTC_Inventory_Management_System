
from django.contrib import admin

from .models import Category, Floor, Product, Room, SubProduct, Type

# Register your models here.
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(Product)
admin.site.register(SubProduct)
