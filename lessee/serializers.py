from rest_framework import serializers
from .models import LesseeDetail
from tool.models import Tool
from datetime import date, datetime
from .helpers import calculate_price

\
class LesseeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = LesseeDetail
        fields = [
            'name', 'phone', 'email', 'address', 'tool_code', 'return_date', 
            'security_amount', 'id_document_type', 'id_document_number', 'remarks'
        ]
    
    def validate(self, data):
        # Validate return date (cannot be earlier than start date)
        start_date = date.today()
        if data.get('return_date') and data['return_date'] < start_date:
            raise serializers.ValidationError("Return date cannot be earlier than start date.")
        
        # Validate tool_code availability
        tool_code = data.get('tool_code')
        try:
            tool = Tool.objects.get(tool_code=tool_code)
        except Tool.DoesNotExist:
            raise serializers.ValidationError("Invalid tool code.")
        
        if tool.quantity < 1:
            raise serializers.ValidationError("Tool is not available. Quantity is zero.")
        
        return data

    def create(self, validated_data):
        tool_code = validated_data.get('tool_code')
        tool = Tool.objects.get(tool_code=tool_code)
        
        # Decrease borrowed quantity and quantity
        tool.borrowed_quantity += 1
        tool.quantity -= 1
        tool.save()

        # Set default values for missing fields
        validated_data['start_date'] = date.today()
        validated_data['security_amount_status'] = 'Not Returned'
        validated_data['tool_status'] = 'Ongoing'
        validated_data['is_overdue'] = False
        validated_data['doc_status'] = 'Not Returned'
        validated_data['remarks'] = None

        # Handle overdue logic and calculate total price
        return_date = validated_data.get('return_date')
        if return_date and return_date < datetime.now().date():
            validated_data['is_overdue'] = True
            validated_data['overdue_date'] = datetime.now()

        # Calculate the price using the updated calculate_price function
        price_data = calculate_price(tool, validated_data['start_date'], return_date, is_overdue=validated_data.get('is_overdue', False))

        # Update the validated data with the calculated price
        validated_data['price'] = price_data['base_price']
        validated_data['extra_charge'] = price_data['extra_charge']
        validated_data['total_price'] = price_data['total_price']

        # Create and return the instance
        return super().create(validated_data)