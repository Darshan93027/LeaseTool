from django.urls import path
from .views import *

custom_tool_view = CustomToolCreateView.as_view({'post': 'create'})#


urlpatterns = [
  
    path('tools/<int:user_id>/all/', ToolListView.as_view(), name='all-user-tools'),
    path('tools/<int:user_id>/custom/', custom_tool_view, name='add-custom-tool'),
    path('tools/<int:user_id>/check-tool/', CheckToolAvailability.as_view(), name='check-tool'),
    path('tools/<int:user_id>/update/<str:tool_code>/', ToolUpdateView.as_view(), name='update-tool'),
    path('tools/<int:user_id>/delete/<str:tool_code>/', ToolDeleteView.as_view(), name='delete-tool'),
    path('tools/<int:user_id>/filter/', ToolFilteredListView.as_view(), name='filter-tools'),
    path('tools/<int:user_id>/borrowed/', BorrowedToolView.as_view(), name='tool-availability'),
]
