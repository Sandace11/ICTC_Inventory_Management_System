from django import template
from django.utils.html import mark_safe
register = template.Library()

from ..models import Item,Categorie,Room


# @register.simple_tag
# def equipment1_name():
#     return equipment[0].__name__
#
# @register.simple_tag
# def equipment2_name():
#     return equipment[1].__name__
#
# @register.simple_tag
# def equipment3_name():
#     return equipment[2].__name__
#
# @register.simple_tag
# def equipment4_name():
#     return equipment[3].__name__
#
# @register.simple_tag
# def equipment5_name():
#     return equipment[4].__name__


@register.simple_tag
def categoryList():
    list = []
    categories = Categorie.objects.all()
    if categories.exists():
        for c in categories:
            list.append(c.category_name)
        return mark_safe(list)
    else:
        return list

@register.simple_tag
def roomList():
    list = []
    rooms = Room.objects.all()
    if rooms.exists():
        for r in rooms:
            list.append(r.room_name)
    return mark_safe(list)

@register.simple_tag
def itemNumberBasedOnCategory():
    list = []
    categories = Categorie.objects.all()
    if categories.exists():
        for c in categories:
           items = Item.objects.filter(category = c)
           count = 0
           if items.exists():
               for i in items:
                   count = count + i.working + i.out_of_order + i.in_maintenance
           list.append(count)
    return [0]

@register.simple_tag
def itemNumberBasedOnRoom():
    list = []
    rooms = Room.objects.all()
    if rooms.exists():
        for r in rooms:
            items = Item.objects.filter(room = r)
            count = 0
            if items.exists():
                for i in items:
                    count = count + i.working + i.out_of_order + i.in_maintenance
            list.append(count)
    return [0]



@register.simple_tag
def total_products_count():
    count = 0
    item = Item.objects.all()
    if item.exists():
        for obj in item:
            count += obj.working + obj.in_maintenance + obj.out_of_order

    return count

@register.simple_tag
def working_count():
    count = 0
    item = Item.objects.all()
    if item.exists():
        for obj in item:
            count += obj.working
    return count


@register.simple_tag
def out_of_order_count():
    count = 0
    item = Item.objects.all()
    if item.exists():
        for obj in item:
            count += obj.out_of_order
    return count


@register.simple_tag
def in_maintenance_count():
    count = 0
    item = Item.objects.all()
    if item.exists():
        for obj in item:
            count += obj.in_maintenance
    return count

@register.simple_tag
def total_categories_count():
    return Categorie.objects.all().count()

@register.simple_tag
def total_item_type_count():
    return Item.objects.all().count()

@register.simple_tag
def working_percentage():
    try:
        percentage = ((working_count() / total_products_count())*100)
    except:
        percentage = 0.0
    return percentage


@register.simple_tag
def out_of_order_percentage():
    try:
        percentage = ((out_of_order_count() / total_products_count())*100)
    except:
        percentage = 0.0
    return percentage

@register.simple_tag
def in_maintenance_percentage():
    try:
        percentage = ((in_maintenance_count() / total_products_count())*100)
    except:
        percentage = 0.0
    return percentage
