from django.db import models

# Create your models here.


# ------------------ PRODUCT ------------------
class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    stock = models.IntegerField()

    def __str__(self):
        return self.name


# ------------------ CART ------------------
class Cart(models.Model):
    user = models.CharField(max_length=100)

    def __str__(self):
        return self.user


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"


# ------------------ ORDER ------------------
class Order(models.Model):
    STATUS_CHOICES = [
        ('CREATED', 'Created'),
        ('PENDING', 'Pending Payment'),
        ('PAID', 'Paid'),
        ('FAILED', 'Failed'),
        ('CANCELLED', 'Cancelled'),
    ]

    user = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='CREATED')
    total = models.FloatField(default=0)

    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"
