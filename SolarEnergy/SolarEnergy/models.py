from django.db import models
import uuid

class item_model(models.Model):
    item_id = models.AutoField(primary_key=True)
    item_status = models.CharField(max_length=20)
    item_name = models.CharField(max_length=200)
    img_link = models.CharField(max_length=200)
    short_description = models.CharField(max_length=255)
    long_description = models.CharField(max_length=1000)
    specification = models.CharField(max_length=400)
    item_cost = models.IntegerField()
    item_type = models.CharField(max_length=10)
    item_voltage = models.DecimalField(decimal_places=2, max_digits=10)
    item_capacity = models.DecimalField(decimal_places=2, max_digits=10)
    item_power = models.DecimalField(decimal_places=2, max_digits=10)

    class Meta:
        managed = False
        db_table = 'items'
class plant_model(models.Model):
    plant_id = models.AutoField(primary_key=True)
    plant_status = models.CharField(max_length = 50)
    creation_date = models.DateTimeField()
    forming_date = models.DateTimeField()
    finishing_date = models.DateTimeField()
    creator_login = models.CharField(max_length=50)
    moderator_login = models.CharField(max_length=50)
    generation = models.DecimalField(decimal_places=2, max_digits=10)
    saving = models.DecimalField(decimal_places=2, max_digits=10)
    latitude = models.DecimalField(decimal_places=5, max_digits=8)
    fio = models.CharField(max_length=255)
    class Meta:
        managed = False
        db_table = 'plants'

class item2plant_model(models.Model):
    relate_id = models.AutoField(primary_key=True)
    item_id = models.IntegerField()
    plant_id = models.IntegerField()
    amount = models.IntegerField()
    class Meta:
        managed = False
        db_table = 'item2plant'
        constraints = [
            models.UniqueConstraint(fields=['item_id', 'plant_id'], name='unique item in plant')
        ]
