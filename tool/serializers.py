from rest_framework import serializers
from .models import  Tool
from rest_framework import serializers



class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'user_id', 'tool_name', 'tool_code', 'quantity', 'price', 'image', 'price_type']
      