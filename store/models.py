from django.db import models
from uuid import uuid4 #for generate cart unique number.

#import for users links with profile: 
from django.conf import settings
#improt admin for display first_name, last_name as ordering : 
from django.contrib import admin

# Create your models here.


class Promotions(models.Model):
    describtion = models.CharField(max_length=255)
    discount = models.FloatField()


class Collections(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey('Products',on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title 
    
    class Meta:
        ordering = ['title']

    


class Products (models.Model):
    slug = models.SlugField()
    sku = models.CharField(max_length=10)
    title = models.CharField(max_length=255)
    describtion = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) 
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collections,on_delete=models.PROTECT,related_name='products') # if want to delete Collections , Before must be delete Products .
    promotions = models.ManyToManyField(Promotions)

    def __str__(self) -> str:
        return self.title
    
    class Meta: 
        ordering = ['title']



class ProductImage(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE,related_name='product')
    image = models.ImageField(upload_to='store/images') #in medial folder -> media/store/img/= here store the img.



class Customers(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        ('MEMBERSHIP_BRONZE', 'Bronze'),
        ('MEMBERSHIP_SILVER', 'Silver'),
        ('MEMBERSHIP_GOLD', 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=17, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def get_order_count(self):
        return self.order_set.count()

    class Meta:
        ordering = ['user__first_name', 'user__last_name']


        #custom model permission: 
        permissions = [('view_history', 'Can view history')]
        #then run >>> python manage.py makemigrations, migrate...


class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILD = 'F'
    PAYMENT_STATUS_CHOICE = [
        ('PAYMENT_STATUS_PENDING','P'),
        ('PAYMENT_STATUS_COMPLETE','C'),
        ('PAYMENT_STATUS_FAILD','F'),
    ]
    place_order = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
    max_length=23, choices=PAYMENT_STATUS_CHOICE, default=PAYMENT_STATUS_PENDING
    )

    customers = models.ForeignKey(Customers, on_delete=models.PROTECT) #if accidently delete the Customers , we don't delete the order .

    class Meta: 
        permissions=[
            ('cancel_order', 'Can cancel Order')
        ]


class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT, related_name='items')
    product = models.ForeignKey(Products,on_delete=models.PROTECT, related_name='orderItems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    street = models.CharField(max_length=255)  # Corrected max_length
    city = models.CharField(max_length=255)  
    

    #one to one relationship
    Customers = models.OneToOneField(Customers,on_delete=models.CASCADE, primary_key=True ) 

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE, related_name='items') #
    product = models.ForeignKey(Products,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    unique_together = [['cart','products']] #for unique generated....



class Review(models.Model):
    product = models.ForeignKey(Products,on_delete=models.CASCADE, related_name='review')
    name = models.CharField(max_length=255)
    describtion = models.TextField()
    date = models.DateField(auto_now_add=True)