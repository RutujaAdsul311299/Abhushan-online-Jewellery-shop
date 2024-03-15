from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Jproduct(models.Model):
    CAT = ((1, 'Braslets'), (2, 'Rings'), (3, 'Earrings'))
    name = models.CharField(max_length=50, verbose_name="Product Name")
    price = models.IntegerField()
    cat = models.IntegerField(verbose_name="Category", choices=CAT)
    product_details = models.CharField(max_length=500, verbose_name="Product Details")
    is_active = models.BooleanField(default=True, verbose_name="Available")
    p_img = models.ImageField(upload_to='uploads/')



class Order(models.Model):
    orderid=models.CharField(max_length=50)
    userid=models.ForeignKey('auth.User',on_delete=models.CASCADE,db_column='userid')
    # trackingid=models.CharField(max_length=50,blank=True,null=True)
    address=models.CharField(max_length=80, blank=False, null=False)
    # paymentlink=models.CharField(max_length=50,blank=True,null=True)
    paymentstatus=models.CharField(max_length=50,blank=True,null=True)
    order_date=models.DateTimeField(blank=False, null=False, default=datetime.now)
    amt=models.IntegerField(default=0)
    
   

# define user cart model
class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # foreign key to user table                                                                                       
    product = models.ForeignKey(Jproduct, on_delete=models.CASCADE, verbose_name="Product")  # foreign key to product table
    quantity = models.IntegerField(default=1)
    total = models.IntegerField(default=0)
    order=models.ForeignKey(Order,on_delete=models.CASCADE,db_column='orderid',null=True,blank=True)


    
# generate an address model
class Address(models.Model):
    # first_name = models.CharField(max_length=50, blank=False, null=False)
    # last_name = models.CharField(max_length=50, blank=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # foreign key to user table
    address = models.CharField(max_length=80, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)