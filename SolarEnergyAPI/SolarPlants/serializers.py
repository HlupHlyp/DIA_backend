from SolarPlants.models import item_model,plant_model,item2plant_model, CustomUser
#from SolarPlants.models import AuthUser
from rest_framework import serializers
from collections import OrderedDict

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = item_model
        # Поля, которые мы сериализуем
        fields = ["item_id", "item_status", "item_name", "img_link", "short_description", "long_description", "specification", "item_cost", 
        "item_type", "item_voltage", "item_capacity", "item_power"]
        def get_fields(self):
            new_fields = OrderedDict()
            for name, field in super().get_fields().items():
                field.required = False
                new_fields[name] = field
            return new_fields 

class FullItemSerializer(serializers.ModelSerializer):

    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        # Модель, которую мы сериализуем
        model = item_model
        # Поля, которые мы сериализуем
        fields = ["item_id", "item_status", "item_name", "img_link", "short_description", "long_description", "specification", "item_cost", 
        "item_type", "item_voltage", "item_capacity", "item_power", "user_id"] 

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = plant_model
        # Поля, которые мы сериализуем  
        fields = ["plant_id", "plant_status", "creation_date", "forming_date", "finishing_date", "generation", "saving", "latitude", "fio", "creator", "moderator"]    

class PlantChangeSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = plant_model
        # Поля, которые мы сериализуем
        fields = ["generation", "saving", "latitude", "fio"] 

class PlantStatusSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = plant_model
        # Поля, которые мы сериализуем
        fields = ["plant_status"] 

class Item2PlantSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = item2plant_model
        # Поля, которые мы сериализуем
        fields = ["relate_id", "item_id", "plant_id", "amount"]

class UserSerializer(serializers.ModelSerializer):
    is_staff = serializers.BooleanField(default=False, required=False)
    is_superuser = serializers.BooleanField(default=False, required=False)
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'is_staff', 'is_superuser']