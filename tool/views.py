# Django & DRF imports
from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.generics import UpdateAPIView, DestroyAPIView, ListAPIView

# Model and Serializer imports
from .models import Tool
from .serializers import ToolSerializer

# Django DB imports
from django.db.models import F

# Date/time utilities
from datetime import datetime, timedelta, date


# View to list all tools of a specific user
class ToolListView(APIView):
    def get(self, request, user_id):
        tools = Tool.objects.filter(user_id=user_id)
        serializer = ToolSerializer(tools, many=True)
        return Response(serializer.data)


# ViewSet for creating and updating custom tools
class CustomToolCreateView(viewsets.ViewSet):
    def create(self, request, user_id):
        # Supports both single and multiple tool creation
        serializer = ToolSerializer(data=request.data, many=isinstance(request.data, list))
        if serializer.is_valid():
            serializer.save(user_id=user_id)  # Save with user ID
            return Response({"message": "Tool(s) added successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, user_id, pk):
        # Update a specific tool by tool_id and user_id
        tool = get_object_or_404(Tool, tool_id=pk, user_id=user_id)
        serializer = ToolSerializer(tool, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tool updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Check if a tool is available based on its tool_code and user_id
class CheckToolAvailability(APIView):
    def post(self, request, user_id):
        tool_code = request.data.get('tool_code')

        if not tool_code:
            return Response({"message": "tool_code is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tool = Tool.objects.get(tool_code=tool_code, user_id=user_id)
            if tool.quantity >= 1:
                return Response({
                    "tool_code": tool_code,
                    "available": True,
                    "message": "Tool is available.",
                    "remaining_tool": tool.quantity
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "tool_code": tool_code,
                    "available": False,
                    "message": "Tool is not available.",
                    "quantity": tool.quantity
                }, status=status.HTTP_200_OK)
        except Tool.DoesNotExist:
            return Response({
                "tool_code": tool_code,
                "available": False,
                "message": "Invalid tool code."
            }, status=status.HTTP_404_NOT_FOUND)


# Update tool data partially by tool_code and user_id
class ToolUpdateView(APIView):
    def put(self, request, user_id, tool_code):
        tool = get_object_or_404(Tool, tool_code=tool_code, user_id=user_id)
        serializer = ToolSerializer(tool, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Tool updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete a tool based on tool_code and user_id
class ToolDeleteView(APIView):
    def delete(self, request, user_id, tool_code):
        tool = get_object_or_404(Tool, tool_code=tool_code, user_id=user_id)
        tool.delete()
        return Response({"message": "Tool deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# View to filter tools based on availability status (borrowed/available/all)
class ToolFilteredListView(APIView):
    def get(self, request, user_id):
        status_filter = request.query_params.get('status')

        if status_filter == 'borrowed':
            tools = Tool.objects.filter(borrowed_quantity__gt=0, user_id=user_id)
        elif status_filter == 'available':
            tools = Tool.objects.filter(quantity__gt=F('borrowed_quantity'), user_id=user_id)
        else:
            tools = Tool.objects.filter(user_id=user_id)

        serializer = ToolSerializer(tools, many=True)
        return Response(serializer.data)


# View to get all tools currently borrowed by a user
class BorrowedToolView(APIView):
    def get(self, request, user_id):
        borrowed_tools = Tool.objects.filter(user_id=user_id, borrowed_quantity__gt=0)
        serializer = ToolSerializer(borrowed_tools, many=True)
        return Response(serializer.data)
