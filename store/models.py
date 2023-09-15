from django.db import models

# Create your models here.


class Promotions(models.Model):
    describtion = models.CharField(max_length=255)
    discount = models.FloatField()


class Collections(models.Model):
    title = models.CharField(max_length=255)
    feature_product = models.ForeignKey('Product',on_delete=models.SET_NULL, null=True, related_name='+')


class Product (models.Model):
    slug = models.SlugField()
    sku = models.CharField(max_length=10,primary_key=True)
    title = models.CharField(max_length=255)
    describtion = models.TextField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2) 
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collections = models.ForeignKey(Collections,on_delete=models.PROTECT) # if want to delete Collections , Before must be delete Product .
    promotions = models.ManyToManyField(Promotions)


class Customer(models.Model):
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
    brith_date = models.DateField(null=True)
    membership = models.CharField(max_length=17, choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE)
    
    class Meta:
        db_table = 'store_customers' #table name of sqlite change to 'store_customers'
        indexes =[
            models.Index(fields=['first_name','last_name']) #
        ]


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

    customer = models.ForeignKey(Customer,on_delete=models.PROTECT) #if accidently delete the customer , we don't delete the order .

class OrderItems(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    product = models.ForeignKey(Product,on_delete=models.PROTECT)
    quentity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)

class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)

class Address(models.Model):
    street = models.CharField(max_length=255)  # Corrected max_length
    city = models.CharField(max_length=255)  
    

    #one to one relationship
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE, primary_key=True ) 

class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantitiy = models.PositiveSmallIntegerField()