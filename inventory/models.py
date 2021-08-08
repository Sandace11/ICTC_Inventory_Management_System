# Create your models here.

from django.db import models
import datetime
from django.contrib.postgres.fields import JSONField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy
from django.core.validators import MinValueValidator


def validate_single_word(value):
     if (' ' in value) == True:
        raise ValidationError(
            ('%(value)s contains space '),
            params={'value': value},
        )

# Create your models here.


class Categorie(models.Model):
    category_name = models.CharField(max_length=50, default='Generic',
                                     help_text='Enter the category of the item',
                                     unique=True, validators=[validate_single_word])
    # extra_fields = JSONField(blank=True, null=True, default=True)
    def __str__(self):
        return str(self.category_name)

class Item(models.Model):
    category = models.ForeignKey('Categorie', on_delete=models.CASCADE,
                                 help_text='Select the category of the equipment', null=True)
    name = models.CharField(max_length=50, default='Generic',
                            help_text='Enter the brand name of the item')
    model = models.CharField(max_length=50, default='Generic',
                             help_text='Enter the model of the item', blank=True, null=True)
    cost_per_item = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, help_text='Enter the cost per item',blank=True,validators=[MinValueValidator(0)])
    room = models.ForeignKey('Room', null=True, on_delete=models.SET_NULL,
                             help_text='Select room where it is kept')
    date_of_acquire = models.DateField(
        default=datetime.date.today, help_text='Enter the date of acquire')
    working = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    in_maintenance = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    out_of_order = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    created = models.DateTimeField(auto_now_add=True, null=True)
    last_modified = models.DateTimeField(auto_now=True, null=True)
    extra_value = JSONField(blank=True, null=True, default=dict)
    def __str__(self):
        return "{}-{}".format(self.name, self.model)

class Floor(models.Model):
    floor = models.PositiveSmallIntegerField(help_text='Enter the floor number', unique=True, validators=[MinValueValidator(0)])
    def __str__(self):
        return str(self.floor)

class Room(models.Model):
    room_no = models.PositiveSmallIntegerField(unique=True, help_text='Enter the room number',validators=[MinValueValidator(0)])
    room_name = models.CharField(max_length=50, default='Generic',
                                 help_text='Enter the name of the room', unique=True)
    floor = models.ForeignKey(
        'Floor', help_text='In which floor is this room?', on_delete=models.CASCADE)
    def __str__(self):
        return "{}:{}".format(self.room_no, self.room_name)

class SubItem(models.Model):
    item = models.ForeignKey(Item,related_name='sub_items',on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=50, default='Generic',
                            help_text='Enter the name of the sub-item')
    model = models.CharField(max_length=50, default='Generic',
                             help_text='Enter the model of the sub-item', blank=True, null=True)
    cost_per_item = models.DecimalField(
        decimal_places=2, max_digits=10, null=True, help_text='Enter the cost per sub-item',blank=True,validators=[MinValueValidator(0)])
    working = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    in_maintenance = models.IntegerField(default=0,validators=[MinValueValidator(0)])
    out_of_order = models.IntegerField(default=0,validators=[MinValueValidator(0)])

    def __str__(self):
        return "{}-{}".format(self.name, self.model)