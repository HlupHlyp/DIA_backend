from SolarPlants.models import item_model,plant_model,item2plant_model
#from SolarPlants.models import AuthUser
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = item_model
        # Поля, которые мы сериализуем
        fields = ["item_id", "item_status", "item_name", "img_link", "short_description", "long_description", "specification", "item_cost", 
        "item_type", "item_voltage", "item_capacity", "item_power"]

class PlantSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = plant_model
        # Поля, которые мы сериализуем
        fields = ["plant_id", "plant_status", "creation_date", "forming_date", "finishing_date", "creator_login", "moderator_login", 
        "generation", "saving", "latitude", "fio"]    
class Item2PlantSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = item2plant_model
        # Поля, которые мы сериализуем
        fields = ["relate_id", "item_id", "plant_id", "amount"]