from django.db import models
from vendor.models import ven_reg

# Create your models here.

class Student(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    


class Img(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='test_imgs')

    def __str__(self):
        return self.name
    

class Registration(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    mob = models.CharField(max_length=10)
    add = models.TextField(default="")
    password = models.CharField(max_length=255)
    is_member = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    

class category(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cat_img')
    discription = models.TextField()
    
    def __str__(self):
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='cat_img')
    discription = models.TextField()
    stock = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    vendor = models.ForeignKey(ven_reg,on_delete=models.CASCADE,null=True,blank=True )


    def __str__(self):
        return self.name
    


class Order(models.Model):
    user = models.ForeignKey(Registration,on_delete=models.CASCADE)
    pro = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    mob = models.CharField(max_length=15)
    add = models.TextField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pin = models.CharField(max_length=10,default="12")
    total_price = models.PositiveIntegerField()
    payment_type = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=100)
    dt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.user)
    


class Cart(models.Model):
    user = models.ForeignKey(Registration,on_delete=models.CASCADE)
    pro = models.ForeignKey(Product,on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    total_price = models.PositiveIntegerField()
    order_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.user)