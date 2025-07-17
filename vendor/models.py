from django.db import models

# Create your models here.
TYPE_BUSINESS =[
    ("Pvt Ltd.","private limited"),
    ("Handmade Crafts","handmade crafts"),
    ("collabration","collb"),
]

class ven_reg(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    mob = models.CharField(max_length=10)
    add = models.TextField(default="")
    password = models.CharField(max_length=8)
    sell_type = models.CharField(max_length=50, choices=TYPE_BUSINESS)

    def __str__(self):
        return self.name