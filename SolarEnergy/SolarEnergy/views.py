from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from SolarEnergy.models import item_model, plant_model, item2plant_model
import psycopg2
from django.db.models import Max

plant_reqs = {'plant_reqs':[
    {'plant_req_id':0,'plant_req_amount':5,'sets':[{'id':'battery_2', 'amount':'2'}, {'id':'solar_panel_2','amount':'3'}]},
    {'plant_req_id':1,'plant_req_amount':9,'sets':[{'id':'battery_1', 'amount':'4'}, {'id':'solar_panel_1','amount':'3'},
     {'id':'solar_panel_2','amount':'2'}]}
    ]}

def GetItems():
    items = []
    for item in item_model.objects.values():
        item['short_description'] = str(item['short_description']).replace('!','\n')
        item['specification'] = str(item['specification']).replace('!','\n')
        items.append(item)
    return items   

def GetItem(request, id):
    items_list = item_model.objects.values()
    item = {}
    for element in items_list:
        if element['item_id'] == int(id): 
            element['specification'] = str(element['specification']).replace('!','\n')
            item = {'item': element}
    return render(request, 'item_page.html', item)

def GetPlantRequest(request, login = 'andrew'):
    plant = {}
    plants_list = plant_model.objects.values()
    item2plant_list = item2plant_model.objects.values()
    plant_items = []
    temp_plant = {}
    for plant in plants_list:
        if plant['creator_login'] == login and plant['plant_status'] == 'draft':
            temp_plant = plant
            for item in item2plant_list:
                if item['plant_id'] == plant['plant_id']:
                    plant_items.append(item)
            break
    data = {'data':{'items': GetItems(), 'plant_req':plant_items, 'plant':temp_plant}}
    return render(request, 'plant_req_page.html', data)

def GetPlantItems(request):
    input_text = request.GET.get('text','')
    data = {}
    items_list = GetItems()
    sorted_list = []

    if not input_text:
        data = {'data':{'items':items_list,'searchText':input_text}}
    else:
        for item in items_list:
            f = False
            if input_text in item['item_name'] or input_text in item['long_description']: f = True
            if f == False:
                for sign in item['short_description']:
                    if input_text in sign:
                        f = True
                        break
            if f == False:
                for sign in item['specification']:
                    if input_text in sign:
                        f = True
                        break
            if f: sorted_list.append(item)
        data = {'data':{'items':sorted_list,'searchText':input_text}}
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
    
def DelPlant(request, login='andrew'):
    print("!")
    return GetPlantItems(request)
     #conn = psycopg2.connect(dbname="solarenergy", host="127.0.0.1", user="student", password="root", port="5432")
    #cursor = conn.cursor()
    #cursor.execute('SELECT * FROM items')
    #rows = cursor.fetchall()
    #for table in rows:
    #    print(table)
    #conn.close()

    #print(item_model.objects.all())
    #print(temp_str)