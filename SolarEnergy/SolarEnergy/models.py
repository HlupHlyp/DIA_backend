from django.db import models

class item_model(models.Model):
    item_id = models.IntegerField(primary_key=True)
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