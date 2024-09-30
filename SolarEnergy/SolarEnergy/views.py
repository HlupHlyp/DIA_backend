from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from SolarEnergy.models import item_model
import psycopg2

plant_reqs = {'plant_reqs':[
    {'plant_req_id':0,'plant_req_amount':5,'sets':[{'id':'battery_2', 'amount':'2'}, {'id':'solar_panel_2','amount':'3'}]},
    {'plant_req_id':1,'plant_req_amount':9,'sets':[{'id':'battery_1', 'amount':'4'}, {'id':'solar_panel_1','amount':'3'},
     {'id':'solar_panel_2','amount':'2'}]}
    ]}

def GetItem(request, id):
    items_list = item_model.objects.values()
    item = {}
    for element in items_list:
        if element['item_id'] == int(id): 
            element['specification'] = str(element['specification']).replace('!','\n')
            item = {'item': element}
    return render(request, 'item_page.html', item)

def GetPlantRequest(request, id):
    plant_req_list = plant_reqs['plant_reqs']
    plant_req = {}
    for element in plant_req_list:
        if int(element['plant_req_id']) == int(id):
            plant_req = element
            break
    items_list = items['items']
    data = {'data':{'items': items_list, 'plant_req':plant_req}}
    return render(request, 'plant_req_page.html', data)

def GetPlantItems(request):
    #conn = psycopg2.connect(dbname="solarenergy", host="127.0.0.1", user="student", password="root", port="5432")
    #cursor = conn.cursor()
    #cursor.execute('SELECT * FROM items')
    #rows = cursor.fetchall()
    #for table in rows:
    #    print(table)
    #conn.close()

    #print(item_model.objects.all())
    #print(temp_str)

    input_text = request.GET.get('text','')
    data = {}
    items_list = []
    sorted_list = []

    for item in item_model.objects.values():
        item['short_description'] = str(item['short_description']).replace('!','\n')
        items_list.append(item)

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

    