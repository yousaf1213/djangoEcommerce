from django.contrib import admin

from .models import Product,User,Order,Vendor,Product_holders_List

admin.site.register(Product)
admin.site.register(User)
admin.site.register(Order)
admin.site.register(Vendor)
admin.site.register(Product_holders_List)
