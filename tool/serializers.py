from rest_framework import serializers
from .models import PreDefineTools , Tool
from rest_framework import serializers

class PreDefineToolsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreDefineTools
        fields = ['id', 'tool_name', 'tool_code', 'image']


class AddPreDefinedToolSerializer(serializers.Serializer):
    user_id = serializers.CharField()
    tool_code = serializers.ListField(child=serializers.CharField(), allow_empty=False)
    quantity = serializers.ListField(child=serializers.IntegerField(), allow_empty=False)
    price = serializers.ListField(child=serializers.DecimalField(max_digits=10, decimal_places=2), allow_empty=False)
    
    def to_internal_value(self, data):
        # Auto-wrap single values in lists for tool_code, quantity, price
        for field in ['tool_code', 'quantity', 'price']:
            if field in data and not isinstance(data[field], list):
                data[field] = [data[field]]
        return super().to_internal_value(data)

    def validate(self, data):
        tool_codes = data.get('tool_code', [])
        quantities = data.get('quantity', [])
        prices = data.get('price', [])

        if not (len(tool_codes) == len(quantities) == len(prices)):
            raise serializers.ValidationError("tool_code, quantity, and price must all be of the same length.")

        return data
    


class ToolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tool
        fields = ['id', 'user_id', 'tool_name', 'tool_code', 'quantity', 'price', 'image', 'price_type']
      