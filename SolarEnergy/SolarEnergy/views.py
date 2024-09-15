from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

products = {'products':[
        {'id':'solar_panel_1',
        'title': 'ПАНЕЛЬ СОЛНЕЧНАЯ 285 ВТ 24 В ПОЛИ', 
        'img': 'https://static.tildacdn.com/stor3233-3066-4138-b131-313435613565/42677272.gif',
        'short_description':['General Energo', 'Мощность 210Вт', 'Поликристаллические,Grade A'],
        'long_description':'',
        'type':'solar_panel', 
        'cost': 10500
        },
        {'id':'battery_1',
        'title': 'ГЕЛЕВЫЙ АККУМУЛЯТОР GENERAL ENERGO 150-12', 
        'img': 'https://optim.tildacdn.com/stor6132-3266-4261-b064-383038643537/-/format/webp/46392380.png',
        'short_description':['Свинцово-кислотные аккумуляторы GENRAL ENERGO серии NCPG',
        'Емкость 150 а.ч.',
        'Напряжение 12 В.'
        'Текущую стоимость и наличие - уточняйте.'],
        'long_description':'Свинцово-кислотные аккумуляторы GENERAL ENERGO серии NPCG'
         'изготовлены по технологии GEL. В качестве электролита используется загущенная серная кислота в виде' 
         'геля, что обеспечивает устойчивость аккумуляторов GENERAL ENERGO серии NPCG к глубоким разрядам и'
         ' широкий диапазон рабочих температур.',
        'specification': ['Тип: Гелевый', 'Производитель: GENERAL ENERGO', 'Ёмкость АКБ, Ah: 150','Напряжение АКБ, Вольт: 12',
         'ДхШхВ: 485х172х242 мм'],
        'type':'battery',
        'cost': 34400
        },
        {'id':'solar_panel_2',
        'title': 'СОЛНЕЧНАЯ ПАНЕЛЬ LUXEN 450-144M', 
        'img': 'https://optim.tildacdn.com/stor3364-6163-4138-b566-363731333861/-/resize/400x/-/format/webp/97770851.jpg',
        'short_description':['LUXEN 450-144M', 'Мощность 450Вт', 'Монокремний, Grade A+'],
        'long_description':'',
        'type':'solar_panel', 
        'cost': 17400
        },
        {'id':'battery_2',
        'title': 'КАРБОНОВЫЙ АККУМУЛЯТОР 100-12', 
        'img': 'https://optim.tildacdn.com/stor3632-6339-4235-a230-383533643566/-/resize/500x/-/format/webp/62062225.jpg',
        'short_description':['Карбоновый AGM аккумулятор GENERAL ENERGO CB100-12',
        'Емкость 100 а.ч.',
        'Напряжение 12 В.',
        'Текущую стоимость и наличие - уточняйте'],
        'long_description':'',
        'type':'battery',
        'cost': 27700
        }
    ]}

def hello(request):
    return render(request, 'index.html', {'data': {'current_date': date.today(), 'list': ['python', 'django', 'html']}})
def GetOrders(request):
    return render(request, 'orders.html', {'data' : {
        'current_date': date.today(),
        'orders': [
            {'title': 'Книга с картинками', 'id': 1, 'img': 'https://optim.tildacdn.com/stor3432-3135-4364-b065-353932633261/-/resize/400x/-/format/webp/96602545.jpg'},
            {'title': 'Бутылка с водой', 'id': 2, 'img': 'https://optim.tildacdn.com/stor3432-3135-4364-b065-353932633261/-/resize/400x/-/format/webp/96602545.jpg'},
            {'title': 'Коврик для мышки', 'id': 3, 'img': 'https://optim.tildacdn.com/stor3432-3135-4364-b065-353932633261/-/resize/400x/-/format/webp/96602545.jpg'},
        ]
    }})
def GetProduct(request, id):
    prod_list = products['products']
    product = {}
    for element in prod_list:
        if element['id'] == id: product = {'product': element}
    return render(request, 'product_page.html', product)

def GetProducts(request):
    return render(request, 'products.html', products)