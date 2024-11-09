from django.shortcuts import render
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
from SolarPlants.serializers import ItemSerializer, PlantSerializer, PlantChangeSerializer, Item2PlantSerializer, PlantStatusSerializer, UserSerializer
from SolarPlants.models import item_model, plant_model, item2plant_model, CustomUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from SolarPlants.minio import add_pic, del_pic
import datetime
from django.contrib.auth.models import User
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from SolarPlants.permissions import IsManager, IsAuthorised
from django.conf import settings
import redis, uuid

# Connect to our Redis instance
session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

def get_user(request):
    session_id = request.COOKIES['session_id']
    email = session_storage.get(session_id).decode('utf-8')
    return CustomUser.objects.filter(email=email).first()

class UserViewSet(ModelViewSet):
    """Класс, описывающий методы работы с пользователями
    Осуществляет связь с таблицей пользователей в базе данных
    """
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model_class = CustomUser

    def create(self, request):
        """
        Функция регистрации новых пользователей
        Если пользователя c указанным в request email ещё нет, в БД будет добавлен новый пользователь.
        """
        if self.model_class.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            self.model_class.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def method_permission_classes(classes):
    def decorator(func):
        def decorated_func(self, *args, **kwargs):
            self.permission_classes = classes        
            self.check_permissions(self.request)
            return func(self, *args, **kwargs)
        return decorated_func
    return decorator

class ItemList(APIView):
    model_class = item_model
    serializer_class = ItemSerializer
    def get(self, request, format=None, creator_login = "andrew"):
        plant_id = 0
        amount = 0
        search_request = request.GET.get('search_request','')
        items = (item_model.objects.filter(item_name__icontains=search_request, item_status = 'active') 
        or item_model.objects.filter(long_description__icontains=search_request, item_status = 'active') 
        or item_model.objects.filter(short_description__icontains=search_request, item_status = 'active'))
        serializer = self.serializer_class(items, many=True)
        plants = plant_model.objects.filter(creator_login = creator_login, plant_status = "draft").values()
        print('!')
        if not plants:
            data = {'items':serializer.data, 'plant_id':None, 'amount':None}
        else:
            for plant in plants:
                plant_id = plant['plant_id']
            items2plant = item2plant_model.objects.filter(plant_id = plant_id).values()
            for item2plant in items2plant:
                amount+=item2plant['amount']
            data = {'items':serializer.data, 'plant_id':plant_id, 'amount':amount} 
        return Response(data)
    
    @method_permission_classes((IsManager,))
    @swagger_auto_schema(request_body=ItemSerializer)
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            item = serializer.save()
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
    
    @swagger_auto_schema(request_body=ItemSerializer)
    @method_permission_classes((IsManager,))
    def put(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @method_permission_classes((IsManager,))
    def delete(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        del_pic(item_id)
        item.item_status = "deleted"
        item.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @method_permission_classes((IsManager,))
    def post(self, request, item_id, format=None):
        item = get_object_or_404(self.model_class, item_id=item_id)
        serializer = self.serializer_class(item, data=request.data, partial=True)
        if serializer.is_valid():
            pic = request.FILES.get("pic")
            pic_result = add_pic(item, pic)
            if 'error' in pic_result.data:    
                return pic_result
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class item2plant(APIView):
    model_class = item2plant_model
    serializer_class = Item2PlantSerializer

    @method_permission_classes((IsAuthorised,)) #✔
    def delete(self, request, format=None):
        item_id = request.POST['item_id']
        plant_id = request.POST['plant_id']
        plant = get_object_or_404(plant_model,plant_id=plant_id)
        if plant.creator != get_user(request):
            return Response("This plant doesn't belong to you", status=status.HTTP_400_BAD_REQUEST)
        if plant.plant_status != 'draft':
            return Response("Status of this plant isn't draft", status=status.HTTP_400_BAD_REQUEST)
        if self.model_class.objects.filter(item_id = item_id, plant_id = plant_id):
            self.model_class.objects.filter(item_id = item_id, plant_id = plant_id).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
    @method_permission_classes((IsAuthorised,)) #✔
    def put(self, request, format=None):
        item_id = request.POST['item_id']
        plant_id = request.POST['plant_id']
        amount = request.POST['amount']
        plant = get_object_or_404(plant_model,plant_id=plant_id)
        if plant.creator != get_user(request):
            return Response("This plant doesn't belong to you", status=status.HTTP_400_BAD_REQUEST)
        if plant.plant_status != 'draft':
            return Response("Status of this plant isn't draft", status=status.HTTP_400_BAD_REQUEST)
        item2plant = get_object_or_404(self.model_class, item_id=item_id, plant_id=plant_id)
        item2plant.amount = amount
        serializer = self.serializer_class(item2plant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlantList(APIView):
    model_class = plant_model
    serializer_class = PlantSerializer

    @method_permission_classes((IsAuthorised,)) #✔
    def get(self, request, format=None):
        plants = []
        req_plant_status = request.POST.get("plant_status")
        status_f = False
        bottom_date = request.POST.get("bottom_date")
        bottom_f = False
        top_date = request.POST.get("top_date")
        top_f = False
        if req_plant_status:
            status_f = True
            if not req_plant_status in ['rejected', 'completed', 'formed']:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        if top_date:
            top_f = True
        else: 
            top_date = datetime.datetime.now()
        if bottom_date:
            top_f = True
        else:
            bottom_date = "2000-01-01"
        if status_f:
            plants = (plant_model.objects.filter(plant_status = req_plant_status) 
            & plant_model.objects.filter(forming_date__range=[bottom_date, top_date]) & plant_model.objects.filter(creator=get_user(request)))
        else:
            plants = ((plant_model.objects.filter(plant_status = "completed") | plant_model.objects.filter(plant_status = "formed") 
            | plant_model.objects.filter(plant_status = "rejected")) & plant_model.objects.filter(forming_date__range=[bottom_date, top_date]) 
            & plant_model.objects.filter(creator=get_user(request)))
            plants = plant_model.objects.filter(forming_date__range=[bottom_date, top_date])
        if not plants:
            return Response(None)
        else:
            serializer = self.serializer_class(plants, many=True)
            return Response(serializer.data)

class PlantDetail(APIView):
    model_class = plant_model
    serializer_class = PlantSerializer
    partial_serializer_class = PlantChangeSerializer

    @method_permission_classes((IsAuthorised,)) #✔
    def get(self, request, plant_id, format=None):
        plant = plant_model.objects.get(plant_id = plant_id) 
        if plant.creator != get_user(request) or not get_user(request).is_staff: 
            return Response("This plant doesn't available for you", status=status.HTTP_400_BAD_REQUEST)
        items = []
        items2plant = item2plant_model.objects.filter(plant_id = plant_id).values()
        for item2plant in items2plant:
            item = item_model.objects.get(item_id = int(item2plant['item_id']))
            items.append({'item_name':item.item_name, 'img_link':item.img_link, 'amount':item2plant["amount"], 
                          'item_cost':item.item_cost,'sum_cost':item.item_cost*item2plant["amount"]})
        data = {"plant":self.serializer_class(plant).data, "items":items}
        return Response(data)

    @method_permission_classes((IsAuthorised,)) #✔
    def put(self, request, plant_id, format=None):
        plant = get_object_or_404(self.model_class, plant_id=plant_id)
        if plant.creator != get_user(request) or not get_user(request).is_staff: 
            return Response("This plant doesn't available for you", status=status.HTTP_400_BAD_REQUEST)
        serializer = self.partial_serializer_class(plant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @method_permission_classes((IsAuthorised,)) #✔
    def delete(self, request, plant_id, format=None):
        plant = get_object_or_404(plant_model, plant_id = plant_id)
        if plant.creator != get_user(request): 
            return Response("This plant doesn't available for you", status=status.HTTP_400_BAD_REQUEST)
        plant.plant_status = "deleted"
        plant.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

permission_classes([IsAuthorised]) #✔
@api_view(['Put'])
def plant_forming(request, plant_id, format=None):
    plant = get_object_or_404(plant_model, plant_id = plant_id)
    if plant.creator != get_user(request): 
        return Response("This plant doesn't available for you", status=status.HTTP_400_BAD_REQUEST)
    plant.plant_status = "formed"
    plant.forming_date = datetime.datetime.now()
    plant.save()
    return Response(status=status.HTTP_206_PARTIAL_CONTENT)

permission_classes([IsManager]) #✔
@api_view(['Put'])
def plant_finishing(request, plant_id, format=None):
    plant_status = request.POST.get("plant_status")
    if plant_status in ["rejected", "completed"]:
        plant = get_object_or_404(plant_model, plant_id = plant_id)
        serializer = PlantStatusSerializer(plant, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(finishing_date = datetime.datetime.now())
            return Response(status=status.HTTP_206_PARTIAL_CONTENT)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)

@permission_classes([IsAuthorised])
@api_view(['Post'])
def add2plant(request, item_id, format=None):
    plant = None
    f = False
    if not plant_model.objects.filter(creator = get_user(request), plant_status = 'draft').values(): f = True  
    if f:
        if not plant_model.objects.filter(creator = get_user(request), plant_status = 'draft').values():
            plant = plant_model.objects.create(creator = get_user(request))
            plant.save()
        else:
            plant = plant_model.objects.get(creator = get_user(request), plant_status = 'draft')
        plant_id = plant.plant_id

    get_object_or_404(item_model, item_id=item_id)

    if not item2plant_model.objects.filter(item_id = item_id, plant_id = plant_id):
        item2plant = item2plant_model(item_id = item_id, plant_id = plant_id, amount = 1)
        item2plant.save()
    else:
        item2plant = item2plant_model.objects.get(item_id = item_id, plant_id = plant_id)
        item2plant.amount = item2plant.amount+1
        item2plant.save()
    if plant_id != request.POST.get('plant_id'):
        return Response(status=status.HTTP_201_CREATED, data = {'plant_id':plant_id})

@api_view(['Post'])
def user_login(request):
    return Response('login',status=status.HTTP_200_OK)

@api_view(['Post'])
def user_logout(request):
    return Response('logout',status=status.HTTP_200_OK)
    
@api_view(['Post'])    
@permission_classes([AllowAny])
@csrf_exempt
def login_user(request):
    username = request.POST["email"] 
    password = request.POST["password"]
    user = authenticate(request, email=username, password=password)
    if user is not None:
        random_key = str(uuid.uuid4())
        session_storage.set(random_key, username)

        response = HttpResponse("{'status': 'ok'}")
        print(random_key)
        response.set_cookie("session_id", random_key)

        return response
    else:
        return HttpResponse("{'status': 'error', 'error': 'login failed'}")
    
@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([AllowAny])
@authentication_classes([])
@csrf_exempt
def create_user(request):
        if CustomUser.objects.filter(email=request.data['email']).exists():
            return Response({'status': 'Exist'}, status=400)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            print(serializer.data)
            CustomUser.objects.create_user(email=serializer.data['email'],
                                     password=serializer.data['password'],
                                     is_superuser=serializer.data['is_superuser'],
                                     is_staff=serializer.data['is_staff'])
            return Response({'status': 'Success'}, status=200)
        return Response({'status': 'Error', 'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#@swagger_auto_schema(method='post', request_body=UserSerializer)
@api_view(['Post'])
@permission_classes([IsAuthorised])
@authentication_classes([])
def logout_user(request):
    session_id = request.COOKIES["session_id"]
    print(session_id)
    if session_storage.exists(session_id):
        session_storage.delete(session_id)
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response.delete_cookie("session_id")
        return Response(status=status.HTTP_204_NO_CONTENT)

    return Response(status=status.HTTP_403_FORBIDDEN)

@api_view(['Post'])
@method_permission_classes([AllowAny])
#@swagger_auto_schema(request_body=ItemSerializer)
def add_item(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        item = serializer.save()
        item.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

