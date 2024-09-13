from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

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
def GetOrder(request, id):
    return render(request, 'order.html', {'data' : {
        'current_date': date.today(),
        'id': id
    }})

def GetProducts(request):
    return render(request, 'products.html', {'data' : {
        'current_date': date.today(),
        'products': [
            {'title': 'ПАНЕЛЬ СОЛНЕЧНАЯ 285 ВТ 24 В ПОЛИ', 
            'img': 'https://static.tildacdn.com/stor3233-3066-4138-b131-313435613565/42677272.gif',
            'model':'General Energo',
            'power': 210, 
            'structure':'Поликристаллические', 
            'category':'Grade A', 
            'type':'solar_panel', 
            'cost': 10500
            },
            {'title': 'СЕТЕВОЙ ИНВЕРТОР KSTAR BLUE-G 3000S', 
            'img': 'https://optim.tildacdn.com/stor3033-3638-4337-b035-616665363734/-/resize/400x/-/format/webp/85787059.png',
            'power': 3000, 
            'num_phases':'1-фаза', 
            'type':'invertor',
            'cost': 49000
            },
            {'title': '', 
            'img': '',
            'model': '', 
            'capacity':'', 
            'voltage':'',
            'type':'invertor',
            'cost': 49000
            },
            {'title': 'КОНТРОЛЛЕР ЗАРЯДА ШИМ', 
            'img': '',
            'bms_type': 'ШИМ', 
            'current':'', 
            'voltage':'',
            'type':'invertor',
            'cost': 49000
            },
        ]
    }})