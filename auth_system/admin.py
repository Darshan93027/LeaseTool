from django.contrib import admin
from .models import ShopDetail
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin

@admin.register(ShopDetail)
class ShopDetailAdmin(admin.ModelAdmin):
    list_display = ('id' ,'shop_name', 'user', 'phone', 'pincode', 'state')
    search_fields = ('shop_name', 'user__email', 'phone', 'pincode', 'state')
   
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'first_name', 'last_name', 'is_staff')
