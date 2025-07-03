from django.contrib.auth.models import User
from rest_framework import serializers
from .models import ShopDetail
from rest_framework import serializers
from .models import ShopDetail

from rest_framework import serializers
from .models import ShopDetail


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("Passwords do not match.")
        return data
    
    class Meta:
        model = User  # Automatically uses the custom user model
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['email'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user


class ShopDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopDetail
        fields = '__all__'

    def validate_phone(self, value):
        if len(value) != 10 or not value.isdigit():
            raise serializers.ValidationError("Phone must be 10 digits.")
        if ShopDetail.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Phone already exists.")
        return value    
