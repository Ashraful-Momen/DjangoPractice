from django.db import models

from typing import Any
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.db.models import Count,Min,Max,Avg,Sum

from . import models


@admin.register(models.Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'unit_price', 'inventory_status', 'collections_title'] # show the title and unit_price in admin page, product has a link with collections table with collections column.
    list_editable = ['unit_price'] #now can edit -> 'unit_price' column.
    list_per_page = 10 #paginations .
    ordering = ['title', 'unit_price'] #accending order with titel and followed by unit_price.
    list_select_related = ['collections'] # Product Fk with Collections , collections form collections table in Product table


    def collections_title(self,product): #this product varible reffer to the Product Models.
        return product.collections.title 


    #return inventory coloumn in admin panel as string : 
    # if inventory is < 10 : show low or show 'high'

    @admin.display(ordering='inventory') # show admin panael inventory as accending order.
    def inventory_status(self, product): # this product varibale work with 'inventory_status' column.
        if product.inventory < 10:
            return 'Low'
        return 'Ok'
    

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'place_order', 'customers', 'payment_status']
    list_editable = ['payment_status']
    list_per_page = 10

    

    def place_order(self, order):
        return order.place_order

    def customers(self, order):
        return order.Customers


# @admin.register(models.Customers)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'membership','orders']
#     list_editable = ['membership']
#     list_per_page = 10
#     list_select_related = ['user']
#     ordering = ['user__first_name', 'user__last_name']

from django.contrib import admin
from .models import Customers, Order

# @admin.register(Customers)
# class CustomerAdmin(admin.ModelAdmin):
#     list_display = ['first_name', 'last_name', 'membership', 'display_orders']
#     list_editable = ['membership']
#     list_per_page = 10
    


#     """
#         In this case, obj will be an instance of the Customers model because we're working within the CustomerAdmin class.
#           This means obj will represent a specific customer.
#     """
#     def display_orders(self, obj):
#         orders = Order.objects.filter(Customers=obj)
#         return ', '.join([str(order.id) for order in orders])



#     display_orders.short_description = 'Orders' #admin panel name is Orders

@admin.register(models.Customers)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'get_order_count']
    list_editable = ['membership']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']

    def get_order_count(self, obj):
        return obj.order_set.count() #customer parent , order child fk with customer. so , customer get order_set as default relative name.
    get_order_count.admin_order_field = 'order_set_count'
    get_order_count.short_description = 'Order Count'



#insert custom table with annotate -------------------------------

@admin.register(models.Collections)
class CollectionsAdmin(admin.ModelAdmin):
    list_display = ['title', 'featured_product', 'product_count']
    list_editable = ['featured_product']

    def product_count(self, collections):
        return collections.product_count

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            product_count=Count('products') # this variable comes from Collections Models. if reserve error then change the Variable name
        )


# Register your models here.
# admin.site.register(models.Collections) or use => @admin.register(models.Collections)

