# from django.db import models

# # Create your models here.

# class Order(models.Model):
#     PAYMENT_STATUS_PENDING = 'P'
#     PAYMENT_STATUS_COMPLETE = 'C'
#     PAYMENT_STATUS_FAILD = 'F'
#     PAYMENT_STATUS_CHOICE = [
#         ('PAYMENT_STATUS_PENDING','P'),
#         ('PAYMENT_STATUS_COMPLETE','C'),
#         ('PAYMENT_STATUS_FAILD','F'),
#     ]
#     place_order = models.DateTimeField(auto_now_add=True,)
#     payment_status = models.CharField(
#         max_length=1, choices=PAYMENT_STATUS_CHOICE, default=PAYMENT_STATUS_PENDING
#     )


# class Product (models.Model):
   
#     sku = models.CharField(max_length=10,primary_key=True)
#     title = models.CharField(max_length=255)
#     describtion = models.TextField()
#     price = models.DecimalField(max_digits=10, decimal_places=True)
#     inventory = models.IntegerField()
#     last_update = models.DateTimeField(auto_now=True)




# class Customer(models.Model):
#     MEMBERSHIP_BRONZE = 'B'
#     MEMBERSHIP_SLIVER = 'S'
#     MEMBERSHIP_GOLD = 'G'
#     MEMBERSHIP_CHOICE = [
#         ('MEMBERSHIP_BRONZE','Bronze'),
#         ('MEMBERSHIP_SLIVER','Silver'),
#         ('MEMBERSHIP_GOLD','Gold'),
#     ]
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(unique=True)
#     brith_date = models.DateField(null=True)
#     membership = models.CharField(max_length=1,choices=MEMBERSHIP_CHOICE, default=MEMBERSHIP_BRONZE )

