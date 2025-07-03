from django.urls import path
from .views import Signup, ShopDetail , OTPVerify , Login

urlpatterns = [
    path('signup/', Signup.as_view(), name='signup'),
    path('shop-detail/', ShopDetail.as_view(), name='shop-detail'),
    path('OTPVerify/',OTPVerify.as_view(),name="OTPVerify"),
    path('login/',Login.as_view(),name="login"),
]
