from django.db import models
from django.conf import settings
from django.contrib import admin
from uuid import uuid4
from django.core.validators import MinValueValidator

# Collection model
class Collection(models.Model):
    title = models.CharField(max_length=255)
    # product = models.ForeignKey('Product', on_delete=models.PROTECT, related_name='collections')
    feature_product = models.ForeignKey('Product', on_delete=models.SET_NULL,null=True, related_name='+')
    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

# Product model
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True,blank=True)
    description = models.TextField(blank=True)
    unit_price = models.DecimalField(max_digits=6,decimal_places=2,validators=[MinValueValidator(1)],default=175.65)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE, related_name='products',null=True)
    promotions = models.ManyToManyField('Promotion', related_name='+')

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title
        
# Reviews model 
class Review(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)

# Promotion model
class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()

# Customer model
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_SILVER, 'Silver'),
        (MEMBERSHIP_GOLD, 'Gold')
    ]
    
    phone = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=2, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    # A customer can place many orders
    orders = models.ManyToManyField('Order', related_name='customers')
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.first_name},{self.user.last_name}'

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
    
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ['user__first_name','user__last_name']
        

# Order model
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAILED, 'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # An order can have many order items
    order_items = models.ManyToManyField('OrderItem', related_name='order_items_set')
    customer = models.ForeignKey('Customer', on_delete= models.CASCADE,related_name='customer_orders',default=3)

    class Meta:
        permissions = [
            ('cancel_order','Can cancel Order')
        ]

# Cart model
class Cart(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    order_item = models.ForeignKey('OrderItem', on_delete=models.CASCADE,null=True,blank=True, related_name='carts')

# CartItem model
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE,default=2)
    quantity = models.PositiveSmallIntegerField()

    # class Meta:
    #     unique_together = [['cart','product']]

# OrderItem model
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT,related_name='orderitems')
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,default=150.06)

# Address model
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip_addr = models.CharField(max_length=255, default='kavali')
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, related_name='addresses')
