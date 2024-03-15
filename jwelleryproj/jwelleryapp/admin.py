from django.contrib import admin
from .models import Jproduct
# Register your models here.


class ProductAdmin(admin.ModelAdmin):
   list_display=['id','name','price','cat','product_details','is_active']
   list_filter=['cat','is_active']

admin.site.register(Jproduct,ProductAdmin) 


