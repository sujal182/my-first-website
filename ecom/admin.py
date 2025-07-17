from django.contrib import admin
from .models import *
# Register your models here.


class student_(admin.ModelAdmin):
    list_display = ['id','name','email']
admin.site.register(Student,student_)

class img_(admin.ModelAdmin):
    list_display = ['id','name','image']
admin.site.register(Img,img_)

class reg_(admin.ModelAdmin):
    list_display = ['id','name','email','mob','password','is_member']
admin.site.register(Registration,reg_)

class cat_(admin.ModelAdmin):
    list_display = ['id','name','image','discription']
admin.site.register(category,cat_)

class pro_(admin.ModelAdmin):
    list_display = ['id','name','image','discription','category','stock','vendor','price']
admin.site.register(Product,pro_)

class order_(admin.ModelAdmin):
    list_display = ['id','pro','user','qty','total_price','payment_type','payment_id','dt']
admin.site.register(Order,order_)
    
class cart_(admin.ModelAdmin):
    list_display = ['id','pro','user','qty','total_price','order_id']
admin.site.register(Cart,cart_)