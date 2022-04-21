from datetime import datetime, timezone
from email.headerregistry import Address
from itertools import product
import numbers
from statistics import mode
from turtle import color, title
from django.db import models
from django.utils.timezone import now
from django.forms import CharField, EmailInput, FloatField, IntegerField


class products(models.Model):
    title=models.CharField(max_length=100)
    img = models.FileField(upload_to="products/", max_length=250, null=True, default=None)
    desc = models.TextField()
    productCategory = models.CharField(max_length=50)
    category = models.CharField(max_length=50)
    cost = models.FloatField()
    discount = models.IntegerField(default=0)


class customer(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=100)

    def isExists(email):
        exist=customer.objects.filter(email=email)
        if exist:
            return 'Email already exists'
        else:
            return ''


    @staticmethod
    def get_customer_by_email(email):
        try:
            return customer.objects.get(email=email)
        except:
            return False



class cart(models.Model):
    customer_id=models.ForeignKey(customer,on_delete=models.CASCADE)
    product_id=models.ForeignKey(products,on_delete=models.CASCADE,default=1)
    quantity = models.CharField(max_length=2,default=1)

status_choice=(
    ('pending','PENDING'),
    ('completed','COMPLETED')
)

class orders(models.Model):
    customer=models.ForeignKey(customer,on_delete=models.CASCADE,default=10)
    product=models.ForeignKey(products,on_delete=models.CASCADE,default=1)
    quantity = models.CharField(max_length=2,default=1)
    price = models.FloatField(default=0)
    date = models.DateTimeField(default=now)
    status =models.CharField(max_length=9,choices=status_choice,default='pending')
    address =models.CharField(max_length=100, blank=True, null=True)
