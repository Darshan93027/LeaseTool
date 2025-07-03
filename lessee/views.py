from django.shortcuts import render
from tool.models import Tool
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import LesseeDetail
from .serializers import LesseeDetailSerializer
from django.shortcuts import get_object_or_404
from datetime import date
from datetime import timedelta
from .helpers import calculate_price , update_lessee_overdue_and_price

  

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import LesseeDetailSerializer

class LesseeDetailAPIView(APIView):
    def post(self, request):
        # Deserialize the incoming request data
        serializer = LesseeDetailSerializer(data=request.data)
        
        if serializer.is_valid():
            # Save and get the instance
            lessee = serializer.save()
            lessee_id = lessee.id  # Get the Lessee ID
            lessee_code = lessee.lessee_code  # Get the Lessee Code

            return Response({
                "message": "Lessee details saved successfully.",
                "data": serializer.data,
                "Lessee_id": lessee_id,
                "Lessee_code": lessee_code
            }, status=status.HTTP_201_CREATED)
        
        # Return validation errors if any
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, lessee_id):
        lessee = get_object_or_404(LesseeDetail, pk=lessee_id)
        serializer = LesseeDetailSerializer(lessee, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Lessee details updated successfully (PUT).",
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404
from .models import LesseeDetail
from .serializers import LesseeDetailSerializer
from .helpers import calculate_price  # the helper you defined
from django.forms.models import model_to_dict



                

class GetLesseedatails(APIView):
    def get(self, request, pk=None):
        if pk:
            lessee = get_object_or_404(LesseeDetail, pk=pk)
            price_data = update_lessee_overdue_and_price(lessee)

            serializer = LesseeDetailSerializer(lessee)
            return Response({
                "data": serializer.data,
                "pricing_info": price_data
            }, status=status.HTTP_200_OK)
        else:
            all_lessees = LesseeDetail.objects.all()
            data_list = []

            for lessee in all_lessees:
                price_data = update_lessee_overdue_and_price(lessee)

                # serializer की जगह model_to_dict यूज़ कर रहे हैं
                lessee_dict = model_to_dict(lessee)
                lessee_dict["pricing_info"] = price_data

                data_list.append(lessee_dict)

            return Response({"data": data_list}, status=status.HTTP_200_OK)

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
       
        
        
        
        
        
        
        
        
        
from django.forms.models import model_to_dict

class LesseeByToolCodeView(APIView):
    def get(self, request, tool_code):
        lessee = LesseeDetail.objects.filter(tool_code=tool_code, tool_status='Ongoing').first()
        if lessee:
            update_lessee_overdue_and_price(lessee)

            # सभी fields को dictionary में convert करें
            lessee_dict = model_to_dict(lessee)

            # अगर आपको किसी ForeignKey या DateTime को string में भेजना हो, तो यहां handle करें
            # उदाहरण:
            # lessee_dict["some_foreign_key_field"] = str(lessee.some_foreign_key_field)

            return Response(lessee_dict)

        return Response({"message": "No ongoing borrowing found for this tool code."}, status=404)




class DueTodayView(APIView):
    def get(self, request):
        today = date.today()
        due_today = LesseeDetail.objects.filter(return_date=today, tool_status='Ongoing')
        serializer = LesseeDetailSerializer(due_today, many=True)
        return Response(serializer.data)
    


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from django.shortcuts import get_object_or_404

class ReturnToolView(APIView):
    def post(self, request):
        tool_code = request.data.get('tool_code')
        lessee_code = request.data.get('lessee_code')
        condition = request.data.get('condition')

        # Validate input
        if not all([tool_code, lessee_code, condition]):
            return Response({"error": "Missing required fields."}, status=status.HTTP_400_BAD_REQUEST)

        print(tool_code, lessee_code, condition)

        # Fetch the lessee entry
        lessee = LesseeDetail.objects.filter(
            lessee_code=lessee_code
        ).first()
        print(lessee)

        if not lessee:
            return Response({"error": "Lessee record not found or already returned."}, status=status.HTTP_404_NOT_FOUND)

        # Update overdue + pricing
        update_lessee_overdue_and_price(lessee)

        # Update lessee return info
        lessee.tool_status = 'Returned'
        lessee.return_date = timezone.now()
        lessee.doc_status = 'Returned'
        lessee.security_amount_status = 'Returned'
        lessee.remarks = f"Condition: {condition}, Security Refunded: True, ID Proof: Returned"
        lessee.save()

        # Update tool quantity
        
        try:
            tool = Tool.objects.get(tool_code=tool_code)
            print(f"tool is {tool}")
        except Tool.DoesNotExist:
            return Response({"error": "Tool not found."}, status=status.HTTP_404_NOT_FOUND)

        if tool.borrowed_quantity > 0:
            tool.borrowed_quantity -= 1
            tool.quantity += 1
            tool.save()

        return Response({"message": "Tool returned successfully."}, status=status.HTTP_200_OK)
