from django.db import models
from django.contrib.auth.models import User


class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userdata')
    address = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} Data"
    

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    rating = models.DecimalField(max_digits=3, decimal_places=2, blank=True, null=True)
    product_image = models.ImageField(upload_to='dishes/', blank=True, null=True)


    def __str__(self):
        return self.name
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    menu_item = models.ForeignKey(MenuItem, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10, unique=True)
    order_type = models.CharField(max_length=20, choices=[('online', 'Online'), ('cod', 'Cash on Delivery')])
    created_at = models.DateTimeField(auto_now_add=True)
    # You can add more fields as needed

    def __str__(self):
        return f"Order {self.order_number} by {self.user.username}"