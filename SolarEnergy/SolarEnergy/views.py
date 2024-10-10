from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from SolarEnergy.models import item_model, plant_model, item2plant_model
import psycopg2
from django.db.models import Max

def AddLineChanges(items):
    for item in items:
        item['short_description'] = item['short_description'].replace('!', '\n')
        item['specification'] = item['specification'].replace('!', '\n')
    return items

def GetItem(request, id):
    item = item_model.objects.filter(item_id = id).values()
    return render(request, 'item_page.html', item)

def GetPlantRequest(request, id):
    plant_items = []
    plant = plant_model.objects.get(creator_login = login, plant_status = 'draft')
    temp_plant = plant_model.objects.filter(creator_login = login, plant_status = 'draft').values()
    item2plant_list = item2plant_model.objects.filter(plant_id = plant.plant_id).values()
    for item2plant in item2plant_list:
        plant_items.append(item2plant)
    data = {'data':{'items': AddLineChanges(item_model.objects.values()), 'plant_req':plant_items, 'plant':temp_plant}}
    return render(request, 'plant_req_page.html', data)

def GetPlantItems(request):
    search_request = request.GET.get('search_request','')
    sorted_list= [] 
    for item in ((item_model.objects.filter(item_name__icontains=search_request) or item_model.objects.filter(long_description__icontains=search_request) 
    or item_model.objects.filter(short_description__icontains=search_request)) and item_model.objects.filter(item_status = 'active')).values():
        sorted_list.append(item)
    data = {'data':{'items':AddLineChanges(sorted_list),'searchText':search_request}}
    return render(request, 'plant_items_page.html', data)

def Add2Plant(request, login='andrew'):
    temp_item_id = request.POST['item_id']
    temp_plant_id = 0
    for plant in plant_model.objects.values():
        if plant['creator_login'] == login and plant['plant_status'] == 'draft':
            temp_plant_id = int(plant['plant_id'])
            break
    records = item2plant_model.objects.filter(item_id = temp_item_id, plant_id = temp_plant_id).values()
    if not records:
        max_id = item2plant_model.objects.aggregate(Max('relate_id'))
        item2plant = item2plant_model(item_id=temp_item_id, plant_id = temp_plant_id, amount = 1, 
        relate_id = max_id['relate_id__max'] + 1)
        item2plant.save()
    else:
        item2plant = item2plant_model.objects.get(item_id = temp_item_id, plant_id = temp_plant_id)
        item2plant.amount = item2plant.amount+1
        item2plant.save()
    return GetPlantItems(request)
    
def DelPlant(request, login, plant_id):
    print("!")
    #print[creator_login]
    #conn = psycopg2.connect(dbname="solarenergy", host="127.0.0.1", user="student", password="root", port="5432")
    #cursor = conn.cursor()
    return GetPlantItems(request)
    #cursor.execute('SELECT * FROM items')
    #rows = cursor.fetchall()
    #for table in rows:
    #    print(table)
    #conn.close()

    #print(item_model.objects.all())
    #print(temp_str)