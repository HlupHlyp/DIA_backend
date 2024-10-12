from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from SolarPlants.serializers import ItemSerializer, PlantSerializer, Item2PlantSerializer
from SolarPlants.models import item_model, plant_model, item2plant_model
from rest_framework.views import APIView
from rest_framework.decorators import api_view

class ItemList(APIView):
    model_class = item_model
    serializer_class = ItemSerializer

    # Возвращает список акций
    def get(self, request, format=None):
        items = self.model_class.objects.all()
        serializer = self.serializer_class(items, many=True)
        return Response(serializer.data)

    # Добавляет новую акцию
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(APIView):
    model_class = item_model
    serializer_class = ItemSerializer

    # Возвращает информацию об акции
    def get(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        serializer = self.serializer_class(item)
        return Response(serializer.data)

    # Обновляет информацию об акции (для модератора)
    def put(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Удаляет информацию об акции
    def delete(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Обновляет информацию об акции (для пользователя)    
@api_view(['Put'])
def put(self, request, item_id, format=None):
    item = get_object_or_404(self.model_class, item_id=item_id)
    serializer = self.serializer_class(item, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)