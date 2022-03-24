from django.contrib.postgres.fields import JSONField
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Model, CharField
from django.utils.translation import gettext_lazy as _


# DONE
# VISUAL TEST PASSED
class Category(Model):
    categoryName = CharField(max_length=64, default='Uncategorized',
                             help_text='Enter category of the product',
                             unique=True)

    def __str__(self):
        return str(self.categoryName)


# DONE
class Type(Model):
    typeName = CharField(
        max_length=64, unique=True, default='No Type', help_text='Enter type of the product')
    category = models.ForeignKey(
        'Category', on_delete=models.PROTECT, related_name='types')

    def __str__(self) -> str:
        return self.typeName

# DONE
class Product(Model):
    type = models.ForeignKey('Type', on_delete=models.PROTECT,
                             help_text='Select type of the product')
    name = CharField(max_length=64,
                     help_text='Enter the name of the item')
    unitCost = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, blank=True, help_text='Enter unit price of the item', validators=[MinValueValidator(0)])
    room = models.ForeignKey('Room', on_delete=models.PROTECT,
                             help_text='Select the room of the prodcut')

    donor = models.ForeignKey('Donor', related_name='products', null=True, blank=True)
    firstAddedDate = models.DateTimeField(null=True)
    lastModifiedDate = models.DateField(
        help_text='Enter the date of acquire', auto_now=True)
    working = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    inMaintenance = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    damaged = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    properties = JSONField(blank=True, null=True, default=dict)
    remarks = CharField(max_length=400, default='',
                        help_text='Enter remarks')

    def __str__(self):
        return self.name

    def count(self):
        return self.working + self.inMaintenance + self.outOfOrder


# DONE
class SubProduct(Model):
    product = models.ForeignKey('Product', on_delete=models.PROTECT,
                                help_text='Select product of this subproduct', related_name='subProducts')
    name = CharField(max_length=64,
                     help_text='Enter the name of the subproduct')
    unitCost = models.DecimalField(
        decimal_places=2,
        max_digits=10,
        null=True,
        blank=True,
        help_text='Enter unit price of the item',
        validators=[MinValueValidator(0)])
    firstAddedDate = models.DateTimeField(auto_now_add=True, null=True)
    lastModifiedDate = models.DateField(
        help_text='Enter the date of acquire', auto_now=True)
    working = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    inMaintenance = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    damaged = models.IntegerField(
        default=0, validators=[MinValueValidator(0)])
    properties = JSONField(blank=True, null=True, default=dict)
    remarks = CharField(max_length=400, default='',
                        help_text='Enter remarks')

    def __str__(self):
        return "{} -> {}".format(self.product.name, self.name)

    def count(self):
        return self.working + self.inMaintenance + self.outOfOrder


# DONE
class Floor(Model):
    floorNumber = models.IntegerField(
        help_text='Enter the floor number', unique=True, validators=[MinValueValidator(0)])

    def __str__(self):
        return str(self.floorNumber)


# DONE
class Room(Model):
    roomNumber = models.IntegerField(
        unique=True, help_text='Enter the room number', validators=[MinValueValidator(0)])
    roomName = CharField(max_length=64, default='Unnamed',
                         help_text='Enter room name', unique=True)
    floor = models.ForeignKey(
        'Floor', help_text='In which floor is this room?', on_delete=models.PROTECT, related_name='rooms')

    def __str__(self):
        return "Room No. {}: {}".format(self.roomNumber, self.roomName)


# DONE
class Donor(Model):
    name = CharField(max_length=64)

    def __str__(self) -> str:
        return self.name
