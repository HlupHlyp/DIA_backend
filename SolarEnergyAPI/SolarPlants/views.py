from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from SolarPlants.serializers import ItemSerializer, PlantSerializer, PlantChangeSerializer, Item2PlantSerializer, PlantFormingSerializer, PlantFinishingSerializer, UserSerializer
from SolarPlants.models import item_model, plant_model, item2plant_model, AuthUser
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from SolarPlants.minio import add_pic, del_pic

def user():
    try:
        user1 = AuthUser.objects.get(id=1)
    except:
        user1 = AuthUser(id=1, first_name="Иван", last_name="Иванов", password=1234, username="user1")
        user1.save()
    return user1

class ItemList(APIView):
    model_class = item_model
    serializer_class = ItemSerializer

    # Возвращает список акций
    def get(self, request, format=None, creator_login = "andrew"):
        plant_id = 0
        amount = 0
        search_request = request.GET.get('search_request','')
        print(search_request)
        items = (item_model.objects.filter(item_name__icontains=search_request, item_status = 'active') 
        or item_model.objects.filter(long_description__icontains=search_request, item_status = 'active') 
        or item_model.objects.filter(short_description__icontains=search_request, item_status = 'active'))
        serializer = self.serializer_class(items, many=True)
        plants = plant_model.objects.filter(creator_login = creator_login, plant_status = "draft").values()
        for plant in plants:
            print('!')
            plant_id = plant['plant_id']
        items2plant = item2plant_model.objects.filter(plant_id = plant_id).values()
        for item2plant in items2plant:
            amount+=item2plant['amount']
        print(plant_id)
        print(amount)
        plant_amount = 0
        data = {'items':serializer.data, 'plant_id':plant_id, 'amount':amount}
        return Response(data)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
            user1 = user()
            item.user = user1
            item.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Добавляет новую акцию

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
        del_pic(item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def post(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            pic = request.FILES.get("pic")
            pic_result = add_pic(item, pic)
            # Если в результате вызова add_pic результат - ошибка, возвращаем его.
            if 'error' in pic_result.data:    
                return pic_result
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersList(APIView):
    model_class = AuthUser
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = self.model_class.objects.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)

class item2plant(APIView):
    model_class = item2plant_model
    serializer_class = Item2PlantSerializer

    def delete(self, request, format=None):
        item_id = request.POST['item_id']
        plant_id = request.POST['plant_id']
        if self.model_class.objects.filter(item_id = item_id, plant_id = plant_id):
            self.model_class.objects.filter(item_id = item_id, plant_id = plant_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, format=None):
        item_id = request.POST['item_id']
        plant_id = request.POST['plant_id']
        amount = request.POST['amount']
        item2plant = get_object_or_404(self.model_class, item_id=item_id, plant_id=plant_id)
        item2plant.amount = amount
        serializer = self.serializer_class(item2plant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantDetail(APIView):
    model_class = plant_model
    serializer_class = PlantSerializer
    partial_serializer_class = PlantChangeSerializer

    def get(self, request, plant_id, format=None):
        item_ids = []
        items = []
        plant = get_object_or_404(self.model_class, plant_id=plant_id)
        items2plant = item2plant_model.objects.filter(plant_id = plant_id).values()
        for item in items2plant:
            item_ids.append(item['item_id'])
        for id in item_ids:
            items.append(item_model.objects.filter(item_id = id).values())
        serializer = self.serializer_class(plant)
        data = {"plant":serializer.data, "item2plant": items2plant, "items": items}
        return Response(data)

    def put(self, request, plant_id, format=None):
        plant = get_object_or_404(self.model_class, plant_id=plant_id)

        serializer = self.partial_serializer_class(plant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def plant_forming(self, request, plant_id, format=None):
    plant = get_object_or_404(self.model_class, plant_id = plant_id)
    if request.POST.get('generation'): 
        plant.generation = request.POST['generation']
    serializer = PlantFormingSerializer(plant, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

   