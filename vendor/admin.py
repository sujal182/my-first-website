from django.contrib import admin
from .models import *

# Register your models here.
class ven_(admin.ModelAdmin):
    list_display = ['id','name','email','mob','sell_type']
admin.site.register(ven_reg,ven_)