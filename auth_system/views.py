from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import  ShopDetailSerializer ,UserSerializer
from django.contrib.auth.models import User
from .utils import send_OTP
from django.core.cache import cache
from django.contrib.auth import authenticate


class Signup(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            email = validated_data['email']
            first_name = validated_data.get('first_name', '')

            # Cache validated signup data
            cache.set(f"signup_data_{email}", validated_data, timeout=300)

            # Send OTP
            sent = send_OTP(email, first_name)
            if sent:
                return Response({
                    "message": "OTP sent to your email.",
                    "email": email
                }, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Failed to send OTP."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OTPVerify(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({"message": "Email and OTP are required."}, status=status.HTTP_400_BAD_REQUEST)

        cached_otp = cache.get(f"otp_{email}")
        if not cached_otp:
            return Response({"message": "OTP expired or not found."}, status=status.HTTP_400_BAD_REQUEST)

        if str(cached_otp) != str(otp):
            return Response({"message": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)

        # OTP valid
        cache.delete(f"otp_{email}")
        signup_data = cache.get(f"signup_data_{email}")
        if not signup_data:
            return Response({"message": "Signup data expired. Please sign up again."}, status=status.HTTP_400_BAD_REQUEST)

        # Create user
        try:
            serializer = UserSerializer(data=signup_data)
            if serializer.is_valid():
                serializer.save()
                cache.delete(f"signup_data_{email}")
        
                user = User.objects.filter(email=email).first()
                if user:
                     return Response({
                    "message": "User registered successfully.",
                    "User_id": user.id
                }, status=status.HTTP_201_CREATED)
                else:
                    return Response({
                    "message": "User saved but not found in database."
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e), "msg": "here is error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


 
class ShopDetail(APIView):
    def post(self, request):
        user_id = request.data.get("user") 

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User is not valid"}, status=status.HTTP_400_BAD_REQUEST)

        # Build new request data with a proper user reference
        data = request.data.copy()
        data["user"] = user.id  # Must be explicitly present

        # Serialize and save
        serializer = ShopDetailSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Shop details added successfully"}, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class Login(APIView):
    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        # Get user by email first
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

        # Authenticate using username (which is email in our case)
        user = authenticate(username=user_obj.username, password=password)

        if user is not None:
            return Response({"message": "User found, login successful."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
