from django.contrib import admin
from .models import Categorie, Item, Floor, Room, SubItem
# Register your models here.
admin.site.register(Categorie)
admin.site.register(Item)
admin.site.register(Floor)
admin.site.register(Room)
admin.site.register(SubItem)

