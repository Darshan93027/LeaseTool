from django.urls import path 
from .views import *
urlpatterns = [
    path('lessee/', GetLesseedatails.as_view()),
    path('lessee/<int:pk>/', GetLesseedatails.as_view()),
    path('lessee/search-by-tool/<str:tool_code>/', LesseeByToolCodeView.as_view()),
    path('lessee/due-today/', DueTodayView.as_view()),
    path('lessee/return-tool/', ReturnToolView.as_view()),
    path('lessee/add/',LesseeDetailAPIView.as_view()),
]

