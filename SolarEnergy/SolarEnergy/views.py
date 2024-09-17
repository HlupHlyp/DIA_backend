from django.http import HttpResponse
from django.shortcuts import render
from datetime import date

products = {'products':[
        {'id':'solar_panel_1',
        'title': 'ПАНЕЛЬ СОЛНЕЧНАЯ 285 ВТ 24 В ПОЛИ', 
        'img': 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL3NvbGFyLW'
        'VuZXJneS9zb2xhcl9wYW5lbF8xLmdpZj9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUVMMDZ'
        'IUzlYMlpKTkRVTFZBSVUxJTJGMjAyNDA5MTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOTE3V'
        'DIwMTY0MVomWC1BbXotRXhwaXJlcz00MzE5OSZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ0k2SWt'
        'wWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSkZUREEyU0ZNNVdESmFTazVFVlV4V1FVbFZNU0lzSW1WNGNDSTZNVGN5TmpZME5UazFOU3dpY'
        '0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5BakFyLWlKYm5JYjJFVFBCcWxRMnNqZXhGSnpYMG1zZm11dEw0aVdNVHFlSkxrNDFrVU9'
        'vQmlfbEVGYmhvWTdib2J3ZHJ0dXhlSlA1RkVYYTZvRlFYQSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklkPTNkMmEzOTk1L'
        'WIzYjQtNDhiZS05NzVhLTZiMDI2NTg1ZDZhYSZYLUFtei1TaWduYXR1cmU9MGE2NzI3NGEwMjUwNTI0ODAxNTg5MDlhMGJhZTk5ZGRhYz'
        'JkODM1MjNhMDM3ZTlmNmFhNGFkZDkzN2RlZDBiYQ',
        'short_description':['General Energo', 'Мощность 210Вт', 'Поликристаллические,Grade A'],
        'long_description':'Солнечная панель представляет собой устройство, которое преобразует солнечный свет'
        'в электрическую энергию, используя для этого множество объединённых в общую цепь фотоэлементов.'
        'Поликристаллические солнечные батареи – это разновидность солнечных панелей, которые производятся из'
        ' поликристаллов кремния. Поликристалический кремний специально производят для фотоэлементов солнечных '
        'батарей. Больше нигде он не используется. Поликристаллические солнечные панели, внешне отличаются от'
        ' других видов солнечных панелей, так как поликремний имеет неравномерный цвет с синеватым отливом.',
        'specification': ['Тип: Поликристаллические', 'Мощность, ВТ: 285', 
        'Максимальный ток, А: 9.02','Габариты, мм: 1640х992х35', 'ДхШхВ: 1640х2х35 мм', 'Вес: 19г',
         'ДхШхВ: 485х172х242 мм'],
        'type':'solar_panel', 
        'cost': 10500
        },
        {'id':'battery_1',
        'title': 'ГЕЛЕВЫЙ АККУМУЛЯТОР GENERAL ENERGO 150-12', 
        'img': 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL3NvbGFy'
        'LWVuZXJneS9iYXR0ZXJ5XzEucG5nP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9'
        'RUwwNkhTOVgyWkpORFVMVkFJVTElMkYyMDI0MDkxNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURh'
        'dGU9MjAyNDA5MTdUMjAyNTAyWiZYLUFtei1FeHBpcmVzPTQzMTk5JlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKS'
        'VV6VXhNaUlzSW5SNWNDSTZJa3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKRlREQTJTRk01V0RKYVNrNUVWVXhXUVVsVk1TSXNJ'
        'bVY0Y0NJNk1UY3lOalkwTlRrMU5Td2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5LkFqQXItaUpibkliMkVUUEJxbFEyc2pl'
        'eEZKelgwbXNmbXV0TDRpV01UcWVKTGs0MWtVT29CaV9sRUZiaG9ZN2JvYndkcnR1eGVKUDVGRVhhNm9GUVhBJlgtQW16LVNpZ25'
        'lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9MmM4MDNlOTQtNDJkZC00OWY4LTgzNjUtNWVjY2ZiNmU0YzY1JlgtQW16LVNpZ25hdHV'
        'yZT01MmQzMDE5NTUyZGQ2ODhlYjc5NDUxNjk5OTNjOTkwNTkzNzU0NmY4ZmZmNmZhMjk5ZmRiZDBkOTE3NGIyOGY0',
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
        'img': 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL3NvbGFyLWVuZX'
        'JneS9zb2xhcl9wYW5lbF8yLmpwZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUVMMDZI'
        'UzlYMlpKTkRVTFZBSVUxJTJGMjAyNDA5MTclMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjQwOT'
        'E3VDIwMjgxMlomWC1BbXotRXhwaXJlcz00MzIwMCZYLUFtei1TZWN1cml0eS1Ub2tlbj1leUpoYkdjaU9pSklVelV4TWlJc0luUjVjQ'
        '0k2SWtwWFZDSjkuZXlKaFkyTmxjM05MWlhraU9pSkZUREEyU0ZNNVdESmFTazVFVlV4V1FVbFZNU0lzSW1WNGNDSTZNVGN5TmpZME5U'
        'azFOU3dpY0dGeVpXNTBJam9pYldsdWFXOWhaRzFwYmlKOS5BakFyLWlKYm5JYjJFVFBCcWxRMnNqZXhGSnpYMG1zZm11dEw0aVdNVHFl'
        'SkxrNDFrVU9vQmlfbEVGYmhvWTdib2J3ZHJ0dXhlSlA1RkVYYTZvRlFYQSZYLUFtei1TaWduZWRIZWFkZXJzPWhvc3QmdmVyc2lvbklk'
        'PWE1MGJhYTBhLWY3ZDctNDExYy04Yzk0LTA0NWU3MTdmNjZmYSZYLUFtei1TaWduYXR1cmU9YmI0MTlkOGE1MjI4ZDcwZTBiOTlmODNi'
        'ZGU0ZGNkZjg1NjM5OWZkNzExZjIxNjk3ODMwNDU0OGJjZTczNDlmYw',
        'short_description':['LUXEN 450-144M', 'Мощность 450Вт', 'Монокремний, Grade A+'],
        'long_description':'Солнечная панель представляет собой устройство, которое преобразует солнечный свет'
        ' в электрическую энергию, используя для этого множество объединённых в общую цепь фотоэлементов.'
        'Монокристаллические солнечные панели - это категория фотоэлектрических устройств, которые используются'
        ' для преобразования солнечного излучения в электрическую энергию. Они изготавливаются из одного'
        ' кристалла кремния, что делает их наиболее эффективными среди всех типов солнечных панелей.',
        'specification': ['Тип: Монокристаллические', 'Мощность, ВТ: 450', 
        'Максимальный ток, А: 10.87','Габариты, мм: 2095х1039х35'],
        'type':'solar_panel', 
        'cost': 17400
        },
        {'id':'battery_2',
        'title': 'КАРБОНОВЫЙ АККУМУЛЯТОР 100-12', 
        'img': 'http://127.0.0.1:9001/api/v1/download-shared-object/aHR0cDovLzEyNy4wLjAuMTo5MDAwL3NvbGFyLWVuZX'
        'JneS9iYXR0ZXJ5XzIuanBnP1gtQW16LUFsZ29yaXRobT1BV1M0LUhNQUMtU0hBMjU2JlgtQW16LUNyZWRlbnRpYWw9RUwwNkhTOVgy'
        'WkpORFVMVkFJVTElMkYyMDI0MDkxNyUyRnVzLWVhc3QtMSUyRnMzJTJGYXdzNF9yZXF1ZXN0JlgtQW16LURhdGU9MjAyNDA5MTdUMj'
        'AyNzIyWiZYLUFtei1FeHBpcmVzPTQzMTk5JlgtQW16LVNlY3VyaXR5LVRva2VuPWV5SmhiR2NpT2lKSVV6VXhNaUlzSW5SNWNDSTZJa'
        '3BYVkNKOS5leUpoWTJObGMzTkxaWGtpT2lKRlREQTJTRk01V0RKYVNrNUVWVXhXUVVsVk1TSXNJbVY0Y0NJNk1UY3lOalkwTlRrMU5Td'
        '2ljR0Z5Wlc1MElqb2liV2x1YVc5aFpHMXBiaUo5LkFqQXItaUpibkliMkVUUEJxbFEyc2pleEZKelgwbXNmbXV0TDRpV01UcWVKTGs0M'
        'WtVT29CaV9sRUZiaG9ZN2JvYndkcnR1eGVKUDVGRVhhNm9GUVhBJlgtQW16LVNpZ25lZEhlYWRlcnM9aG9zdCZ2ZXJzaW9uSWQ9NWM4N'
        'GZiMzUtM2MxNC00ZDYxLWE2NGEtNDQ5ZTcyNTdhNGFiJlgtQW16LVNpZ25hdHVyZT01NWQ3MmE2NjEzZDgxMjJhMWM2NjNkNmQxYWNiY'
        'mVmYmI3NTQ2NGYxNTRkMTJhZmM3ZTRiZDgwMWM1NDA0MjA0',
        'short_description':['Карбоновый AGM аккумулятор GENERAL ENERGO CB100-12',
        'Емкость 100 а.ч.',
        'Напряжение 12 В.',
        'Текущую стоимость и наличие - уточняйте'],
        'long_description':'Карбоновый AGM аккумулятор GENERAL ENERGO СВ100-12 изготовлен с добавлением углерода,'
        ' который позволяет увеличивать размер пор отрицательных пластин, позволяя кислоте проходить через них и '
        'диспергироваться в свинцовой пасте.'
        ' Данный эффект поможет улучшить прием заряда в условиях высоких токов и повысить производительность'
        ' PSoC аккумулятора. Таким образом, карбоновый AGM аккумулятор серии CB работает эффективнее при'
        ' частичном заряде, дает больше циклов и более высокую эффективность Замена активного материала'
        ' отрицательной пластины на свинцово-углеродный композит потенциально снижает сульфатацию и улучшает'
        ' прием заряда отрицательной пластины.'
        'Расчетный срок службы карбонового аккумулятора составляет 20 лет.',
        'specification': ['Тип: Карбоновые', 'Производитель: GENERAL ENERGO', 'Ёмкость АКБ, Ah: 100',
        'Напряжение АКБ, Вольт: 12'],
        'type':'battery',
        'cost': 27700
        }
    ]}

card = {'card':[{'id':'battery_2'}]}

def GetProduct(request, id):
    prod_list = products['products']
    product = {}
    for element in prod_list:
        if element['id'] == id: product = {'product': element}
    return render(request, 'product_page.html', product)

def GetCard(request, id=1):
    return render(request, 'card_page.html', products)

def GetProducts(request):
    input_text = request.GET.get('text','')
    prod_list = products['products']
    sorted_list = []
    data = {}
    if not input_text:
        data = {'data':{'products':products['products'],'searchText':input_text}}
    else:
        for product in prod_list:
            f = False
            if input_text in product['title'] or input_text in product['long_description']: f = True
            if f == False:
                for sign in product['short_description']:
                    if input_text in sign:
                        f = True
                        break
            if f == False:
                for sign in product['specification']:
                    if input_text in sign:
                        f = True
                        break
            if f: sorted_list.append(product)
        data = {'data':{'products':sorted_list,'searchText':input_text}}
    return render(request, 'products.html', data)

    