from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings  # Import settings to use the custom user model

class ShopDetail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shop_name = models.CharField(max_length=100)
    address = models.TextField()
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=50)
    phone = models.CharField(max_length=10, unique=True)
    
    class Meta:
        db_table = 'ShopDetail'

    def __str__(self):
        return self.shop_name
    
