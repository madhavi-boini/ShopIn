from pyexpat import model
from django.contrib import admin
from .models import customer,cart,orders,products

class Cart(admin.ModelAdmin):
    list_display=('get_customer','get_product','quantity')

    def get_customer(self,obj):
        return obj.customer_id.firstname
    def get_product(self ,obj):
        return obj.product_id.category+"  -  "+obj.product_id.productCategory

class Customer(admin.ModelAdmin):
    list_display=('get_customer','email')

    def get_customer(self,obj):
        return obj.firstname+" "+obj.lastname


class Product(admin.ModelAdmin):
    list_display=('title','get_category')

    def get_category(self,obj):
        return obj.category+"  -  "+obj.productCategory


admin.site.register(customer,Customer)
admin.site.register(cart,Cart) 
admin.site.register(products,Product)
admin.site.register(orders)
