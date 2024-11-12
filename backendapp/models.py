from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.core.exceptions import ValidationError
from django.utils import timezone
from .manager import UserManager
from django.contrib.auth.models import User


# Abstract base model to handle timestamps
class DateTimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True


# Category model to group products
class Category(DateTimeModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Brand model to represent different brands
class Brand(DateTimeModel):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


# Product model representing fashion items
class Product(DateTimeModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    def __str__(self):
        return self.name


# Custom user model for customers
class Customer(DateTimeModel):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.email


#For Cart
class Cart(DateTimeModel):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    total = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Cart: {self.id}"


#For CartProduct
class CartProduct(DateTimeModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rate = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return f"Cart: {self.cart.id} CartProduct: {self.id}"


ORDER_STATUS = (
    ('Order Received', 'Order Received'),
    ('Order Processing', 'Order Processing'),
    ('On the way', 'On the way'),
    ('Order Completed', 'Order Completed'),
    ('Order Canceled', 'Order Canceled'),
)

PAYMENT_METHOD = (
    ("Cash On Delivery", "Cash On Delivery"),
    ("Khalti", "Khalti"),
)

#For Order
class Order(DateTimeModel):
    cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    ordered_by = models.CharField(max_length=300)
    shipping_address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    order_status = models.CharField(max_length=50, choices=ORDER_STATUS)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default="Cash On Delivery")
    payment_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"Order: {self.id}"


# Review model to allow customers to review products
class Review(DateTimeModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='reviews')
    timestamp = models.DateTimeField(default=timezone.now)  # Store time of comment
    comment = models.TextField(blank=True, null=True)
    likes = models.PositiveIntegerField(default=0)  # Count likes


    def __str__(self):
        return f"Review for {self.product.name} by {self.customer.email}"



#For Inquery
class Inquiry(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Inquiry from {self.name}"
    

    
#For Profile
class Profile(models.Model):
    image = models.ImageField(upload_to='profile', blank=True,null=True)
    name = models.CharField(max_length=100)
    dob = models.DateField()
    qualification = models.CharField(max_length=200,blank=True,null=True)
    post = models.CharField(max_length=100,)

