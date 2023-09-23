from django.db import models
from uuid import uuid4 #for generate cart unique number.

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
    sku = models.CharField(max_length=10,primary_key=True)
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




class Customers(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SLIVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICE = [
    ('MEMBERSHIP_BRONZE','Bronze'),
    ('MEMBERSHIP_SLIVER','Silver'),
    ('MEMBERSHIP_GOLD','Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    brith_date = models.DateField(null=True)
    membership = models.CharField(max_length=17, choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name }"


    class Meta:
        ordering = ['first_name', 'last_name']



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

    Customers = models.ForeignKey(Customers,on_delete=models.PROTECT) #if accidently delete the Customers , we don't delete the order .

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    Products = models.ForeignKey(Products,on_delete=models.PROTECT, related_name='orderItems')
    quentity = models.PositiveSmallIntegerField()
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