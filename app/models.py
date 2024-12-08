from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES = (
    ('Dhaka', 'Dhaka'),
    ('Chattogram', 'Chattogram'),
    ('Rajshahi', 'Rajshahi'),
    ('Khulna', 'Khulna'),
    ('Barishal', 'Barishal'),
    ('Sylhet', 'Sylhet'),
    ('Rangpur', 'Rangpur'),
    ('Mymensingh', 'Mymensingh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    village = models.CharField(max_length=200)
    city = models.CharField(max_length=100)  # Specify max_length for city
    state = models.CharField(choices=STATE_CHOICES, max_length=50)
    union = models.CharField(max_length=200, null=True, blank=True)
    mobile = models.CharField(max_length=15, unique=True, blank=False, null=False)


    def __str__(self):
        return str(self.id)





CATEGORY_CHOICES = (
    ('M', 'Mens'),
    ('L', 'Ladies'),
    ('TS', 'Men T-Shirt'),
    ('BW', 'Formal Shirt'),
    ('EL', 'Female Dress'),
    ('HM', 'Three Piece'),
    ('FT', 'Women Saree'),
    ('BK', 'Cosmetics'),
    ('FR', 'Personal Care'),
    ('BT', 'Beauty & Personal Care'),
    ('KD', 'Kids Wear'),
)





class Product(models.Model):
    title = models.CharField(max_length=200)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    brand = models.CharField(max_length=100)
    category = models.CharField(choices= CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)
    



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # ForeignKey to Product model
    quantity = models.PositiveIntegerField(default=1)  # Positive integer for quantity

    def __str__(self):
        return str(self.id)



    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price


STATUS_CHOICES = (
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On the Way', 'On the Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel'),
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)  # Assuming Customer model exists
    product = models.ForeignKey('Product', on_delete=models.CASCADE)  # Assuming Product model exists
    quantity = models.PositiveIntegerField(default=1)  # Auto increment is not suitable for quantity
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')





#pyment section 

from django.db import models

class Payment(models.Model):
    PAYMENT_CHOICES = [
        ('bkash', 'Bkash'),
        ('nagad', 'Nagad'),
        ('visa', 'Visa'),
    ]
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_CHOICES, default='bkash')
    customer_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    transaction_id = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.customer_name} - {self.payment_method}"
