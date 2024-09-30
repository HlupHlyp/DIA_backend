from django.http import HttpResponse
from django.shortcuts import render
from datetime import date
from SolarEnergy.models import item_model
import psycopg2

items = {'items':[
        {'id':'solar_panel_1',
        'title': 'ПАНЕЛЬ СОЛНЕЧНАЯ 285 ВТ 24 В ПОЛИ', 
        'img': 'http://127.0.0.1:9000/solar-energy/solar_panel_1.gif',
        'short_description':'General Energo\n Мощность 210Вт\n Поликристаллические, Grade A',
        'long_description':'Солнечная панель представляет собой устройство, которое преобразует солнечный свет'
        'в электрическую энергию, используя для этого множество объединённых в общую цепь фотоэлементов.'
        'Поликристаллические солнечные батареи – это разновидность солнечных панелей, которые производятся из'
        ' поликристаллов кремния. Поликристалический кремний специально производят для фотоэлементов солнечных '
        'батарей. Больше нигде он не используется. Поликристаллические солнечные панели, внешне отличаются от'
        ' других видов солнечных панелей, так как поликремний имеет неравномерный цвет с синеватым отливом.',
        'specification': 'Тип: Поликристаллические \nМощность, ВТ: 285 \nМаксимальный ток, А: 9.02 \n'
        'Габариты, мм: 1640х992х35 \nДхШхВ: 1640х2х35 мм \nВес: 19г \nДхШхВ: 485х172х242 мм',
        'type':'solar_panel', 
        'cost': 10500
        },
        {'id':'solar_panel_2',
        'title': 'СОЛНЕЧНАЯ ПАНЕЛЬ LUXEN 450-144M', 
        'img': 'http://127.0.0.1:9000/solar-energy/solar_panel_2.jpg',
        'short_description': 'LUXEN 450-144M\n' 'Мощность 450Вт\n' 'Монокремний, Grade A+\n',
        'long_description':'Солнечная панель представляет собой устройство, которое преобразует солнечный свет'
        ' в электрическую энергию, используя для этого множество объединённых в общую цепь фотоэлементов.'
        'Монокристаллические солнечные панели - это категория фотоэлектрических устройств, которые используются'
        ' для преобразования солнечного излучения в электрическую энергию. Они изготавливаются из одного'
        ' кристалла кремния, что делает их наиболее эффективными среди всех типов солнечных панелей.',
        'specification': 'Тип: Монокристаллические \nМощность, ВТ: 450 \n'
        'Максимальный ток, А: 10.87 \nГабариты, мм: 2095х1039х35',
        'type':'solar_panel', 
        'cost': 17400
        },
        {'id':'solar_panel_3',
        'title': 'СОЛНЕЧНАЯ ПАНЕЛЬ 370 Вт 24 В', 
        'img': 'http://127.0.0.1:9000/solar-energy/solar_panel_4.jpg',
        'short_description': 'SRP-370-BMB-HV\n' 'Мощность 370Вт\n' 'Монокристаллические, PERC Mono\n',
        'long_description':'Солнечная панель представляет собой устройство, которое преобразует солнечный свет'
        ' в электрическую энергию, используя для этого множество объединённых в общую цепь фотоэлементов.'
        'Монокристаллические солнечные панели - это категория фотоэлектрических устройств, которые используются'
        ' для преобразования солнечного излучения в электрическую энергию. Они изготавливаются из одного кристалла'
        ' кремния, что делает их наиболее эффективными среди всех типов солнечных панелей.',
        'specification': 'Тип: Монокристаллические \nМощность, ВТ: 370 \n'
        'Максимальный ток, А: 10.70 \nГабариты, мм: 1755х1038х35',
        'type':'solar_panel', 
        'cost': 17850
        },
        {'id':'solar_panel_4',
        'title': 'СОЛНЕЧНАЯ ПАНЕЛЬ GE410-144M', 
        'img': 'http://127.0.0.1:9000/solar-energy/solar_panel_3.jpg',
        'short_description':'GE410-144M\n Мощность 410Вт\n Монокремний, Grade A+',
        'long_description':'Солнечная панель представляет собой устройство, которое преобразует солнечный свет в'
        ' электрическую энергию, используя для этого множество объединённых в общую цепь фотоэлементов.'
        'Монокристаллические солнечные панели - это категория фотоэлектрических устройств, которые используются '
        'для преобразования солнечного излучения в электрическую энергию. Они изготавливаются из одного кристалла'
        ' кремния, что делает их наиболее эффективными среди всех типов солнечных панелей.',
        'specification': 'Тип: Монокристаллические \nМощность, ВТ: 410 \nМаксимальный ток, А: 10.12 \n'
        'Габариты, мм: 2008х1002х35',
        'type':'solar_panel', 
        'cost': 18400
        },
        {'id':'battery_1',
        'title': 'ГЕЛЕВЫЙ АККУМУЛЯТОР GENERAL ENERGO 150-12', 
        'img': 'http://127.0.0.1:9000/solar-energy/battery_1.png',
        'short_description':'Свинцово-кислотные аккумуляторы GENRAL ENERGO серии NCPG\n'
        'Емкость 150 а.ч\n'
        'Напряжение 12 В.\n'
        'Текущую стоимость и наличие - уточняйте.\n',
        'long_description':'Свинцово-кислотные аккумуляторы GENERAL ENERGO серии NPCG'
         'изготовлены по технологии GEL. В качестве электролита используется загущенная серная кислота в виде' 
         'геля, что обеспечивает устойчивость аккумуляторов GENERAL ENERGO серии NPCG к глубоким разрядам и'
         ' широкий диапазон рабочих температур.',
        'specification': 'Тип: Гелевый \nПроизводитель: GENERAL ENERGO \n'
        'Ёмкость АКБ, Ah: 150 \nНапряжение АКБ, Вольт: 12 \n'
         'ДхШхВ: 485х172х242 мм\n',
        'type':'battery',
        'cost': 34400
        },
        {'id':'battery_2',
        'title': 'КАРБОНОВЫЙ АККУМУЛЯТОР 100-12', 
        'img': 'http://127.0.0.1:9000/solar-energy/battery_2.jpg',
        'short_description':'Карбоновый AGM аккумулятор GENERAL ENERGO CB100-12\n'
        'Емкость 100 а.ч.\n'
        'Напряжение 12 В.\n'
        'Текущую стоимость и наличие - уточняйте',
        'long_description':'Карбоновый AGM аккумулятор GENERAL ENERGO СВ100-12 изготовлен с добавлением углерода,'
        ' который позволяет увеличивать размер пор отрицательных пластин, позволяя кислоте проходить через них и '
        'диспергироваться в свинцовой пасте.'
        ' Данный эффект поможет улучшить прием заряда в условиях высоких токов и повысить производительность'
        ' PSoC аккумулятора. Таким образом, карбоновый AGM аккумулятор серии CB работает эффективнее при'
        ' частичном заряде, дает больше циклов и более высокую эффективность Замена активного материала'
        ' отрицательной пластины на свинцово-углеродный композит потенциально снижает сульфатацию и улучшает'
        ' прием заряда отрицательной пластины.'
        'Расчетный срок службы карбонового аккумулятора составляет 20 лет.',
        'specification': 'Тип: Карбоновые \nПроизводитель: GENERAL ENERGO \nЁмкость АКБ, Ah: 100'
        '\nНапряжение АКБ, Вольт: 12',
        'type':'battery',
        'cost': 27700
        },
        {'id':'battery_3',
        'title': 'КАРБОНОВЫЙ AGM АККУМУЛЯТОР GENERAL ENERGO CB200-12', 
        'img': 'http://127.0.0.1:9000/solar-energy/battery_3.jpg',
        'short_description':'Карбоновый AGM аккумулятор GENERAL ENERGO CB 200-12\n'
        'Емкость 200 а.ч\n'
        'Напряжение 12 В.\n'
        'Текущую стоимость и наличие - уточняйте.\n',
        'long_description':'Карбоновый AGM аккумулятор GENERAL ENERGO СВ200-12 изготовлен с добавлением углерода,'
        ' который позволяет увеличивать размер пор отрицательных пластин, позволяя кислоте проходить через них и '
        'диспергироваться в свинцовой пасте.'  
        'Данный эффект поможет улучшить прием заряда в условиях высоких токов и повысить производительность PSoC'
        ' аккумулятора. Таким образом, карбоновый AGM аккумулятор серии CB работает эффективнее при частичном заряде,'
        ' дает больше циклов и более высокую эффективность Замена активного материала отрицательной пластины на'
        ' свинцово-углеродный композит потенциально снижает сульфатацию и улучшает прием заряда отрицательной пластины.'
        'Расчетный срок службы карбонового аккумулятора составляет 20 лет.',
        'specification': 'Тип: Гелевый \nПроизводитель: GENERAL ENERGO \n'
        'Ёмкость АКБ, Ah: 200 \nНапряжение АКБ, Вольт: 12 \n'
         'ДхШхВ: 485х172х242 мм\n',
        'type':'battery',
        'cost': 56000
        },
        {'id':'battery_4',
        'title': 'КАРБОНОВЫЙ АККУМУЛЯТОР VECTOR VPBC 12-100', 
        'img': 'http://127.0.0.1:9000/solar-energy/battery_4.png',
        'short_description':'Карбоновый AGM аккумулятор GENERAL ENERGO CB100-12\n'
        'Емкость 100 а.ч.\n'
        'Напряжение 12 В.\n'
        'Текущую стоимость и наличие - уточняйте',
        'long_description':'Аккумуляторные батареи VEKTOR ENERGY серии CARBON (VPbC) изготовлены по технологии'
        ' PURE GEL с использованием PVC сепаратора. Все пластины изготовлены по технологии DEEP CYCLE + CARBON'
        ' (Super Lead-Carbon Batteries). За счет карбонизации как отрицательной, так и положительной пластин, '
        'аккумуляторы данной серии имеют высочайшую цикличность, сравнимую с литий-ионными аккумуляторами.'
        ' Имеют отличные эксплуатационные характеристики в режиме частичного заряда, а также возможность'
        ' ускоренного заряда токами до 0,5С.'
        'Расчетный срок службы карбонового аккумулятора составляет 20 лет.',
        'specification': 'Тип: Карбоновые \nПроизводитель: GENERAL ENERGO \nЁмкость АКБ, Ah: 100'
        '\nНапряжение АКБ, Вольт: 12',
        'type':'battery',
        'cost': 27700
        }
    ]}

plant_reqs = {'plant_reqs':[
    {'plant_req_id':0,'plant_req_amount':5,'sets':[{'id':'battery_2', 'amount':'2'}, {'id':'solar_panel_2','amount':'3'}]},
    {'plant_req_id':1,'plant_req_amount':9,'sets':[{'id':'battery_1', 'amount':'4'}, {'id':'solar_panel_1','amount':'3'},
     {'id':'solar_panel_2','amount':'2'}]}
    ]}

def GetItem(request, id):
    items_list = items['items']
    item = {}
    for element in items_list:
        if element['id'] == id: item = {'item': element}
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
    temp_list = []
    for item in item_model.objects.values():
        item['short_description'] = str(item['short_description']).replace('!','\n')
        temp_list.append(item)

    input_text = request.GET.get('text','')
    items_list = items['items']
    sorted_list = []
    data = {}
    if not input_text:
        data = {'data':{'items':temp_list,'searchText':input_text}}
    else:
        for item in items_list:
            f = False
            if input_text in item['title'] or input_text in item['long_description']: f = True
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

    