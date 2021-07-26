from django.shortcuts import render, redirect, HttpResponse
from Requirements.models import Require
from django.core import serializers


# Create your views here.

def add_req(request):
    if request.method == 'GET':
        ID_new = Require.objects.count() + 1
        return render(request, 'add_req.html', {'ID_new': ID_new})
    else:
        ID = int(request.POST.get('ID')),
        customer = request.POST.get('customer')
        product_type = request.POST.get('product_type')
        product_code = request.POST.get('product_code')
        date = request.POST.get('date')
        place = request.POST.get('place')
        condition = request.POST.get('condition')
        nandian = request.POST.get('nandian')
        attention = request.POST.get('attention')
        inputfile = request.POST.get('inputfile')
        print(customer, product_type, product_code, date, place, condition, nandian, attention, inputfile)
        record = Require(
            ID=ID[0],
            customer=customer,
            product_type=product_type,
            product_code=product_code,
            date=date,
            place=place,
            condition=condition,
            nandian=nandian,
            attention=attention,
            inputfile=inputfile,
        )
        record.save()
        return redirect('/Requirements/req_list/')


def req_list(request):
    ID_count = Require.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = Require.objects.all()[j]
        ID_old = k.ID
        Require.objects.filter(id=ID_old).update(ID=i)
    try:
        page = int(request.GET.get('page'))
        pageRange1, pageRange2 = (page - 1) * 6, (page - 1) * 6 + 5
    except:
        page = 1
        pageRange1, pageRange2 = (page - 1) * 6, (page - 1) * 6 + 5
    datalist = Require.objects.values(
        'ID',
        'customer',
        'product_type',
        'product_code',
        'date',
        'place',
        'condition',
        'nandian',
        'attention',
        'inputfile',
    )
    return render(request, 'req_list.html', {'data_list': datalist[pageRange1:pageRange2]})


def edit_req(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = Require.objects.get(id=ID)
        return render(request, 'edit_req.html', {'item': item})
    else:
        # customer = request.POST.get('customer')
        # product_type = request.POST.get('product_type')
        # product_code = request.POST.get('product_code')
        # date = request.POST.get('date')
        # place = request.POST.get('place')
        # condition = request.POST.get('condition')
        # nandian = request.POST.get('nandian')
        # attention = request.POST.get('attention')
        # inputfile = request.POST.get('inputfile')
        # print(customer, product_type, product_code, date, place, condition, nandian, attention, inputfile)
        Require.objects.filter(id=ID).update(
            ID=request.POST.get('ID'),
            customer=request.POST.get('customer'),
            product_type=request.POST.get('product_type'),
            product_code=request.POST.get('product_code'),
            date=request.POST.get('date'),
            place=request.POST.get('place'),
            condition=request.POST.get('condition'),
            nandian=request.POST.get('nandian'),
            attention=request.POST.get('attention'),
            inputfile=request.POST.get('inputfile')
        )
        return redirect('/Requirements/req_list/')


def delete_req(request):
    ID = request.GET.get('ID')
    Require.objects.filter(id=ID).delete()
    return redirect('/Requirements/req_list/')


def req_export(request):
    import tablib
    from tool11 import settings
    import os
    # json.text文件的格式： [{"model":...,"fields":{"..":"..",},{}]
    # 获取ｊｓｏｎ数据
    requireData = Require.objects.all()
    json_data = serializers.serialize('json', requireData)
    dictList = []
    for dict in eval(json_data):
        dictList.append(dict["fields"])
    header = tuple([i for i in dictList[0].keys()])
    # print('header',header)
    data = []
    # 循环里面的字典，将value作为数据写入进去
    for row in dictList:
        body = []
        for v in row.values():
            body.append(v)
        data.append(tuple(body))
        # print('data',data)
    data = tablib.Dataset(*data, headers=header)
    open(os.path.join(settings.BASE_DIR, 'static') + '/xlsx/Require_data.xlsx', 'wb').write(data.xlsx)
    file = open(os.path.join(settings.BASE_DIR, 'static') + '/xlsx/Require_data.xlsx', 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'  # 设置头信息，告诉浏览器这是个文件
    response['Content-Disposition'] = 'attachment;filename="Require_data.xlsx"'
    return response


def statistics_req(request):
    if request.method == "GET":
        datalist = Require.objects.values(
            'ID',
            'customer',
            'product_type',
            'product_code',
            'date',
            'place',
            'condition',
            'nandian',
            'attention',
            'inputfile',
        )
        customers = []
        customersDict = {}
        product_types = []
        product_typesDict = {}
        years = []
        yearsNum = [0, 0, 0, 0, 0, 0, 0, 0]
        for item in datalist:
            customers.append(item["customer"])
            product_types.append(item["product_type"])
            years.append(eval(item["date"][0:4]))
        for c in customers:
            if c not in customersDict.keys():
                customersDict[c] = 1
            else:
                customersDict[c] += 1
        for p in product_types:
            if p not in product_typesDict.keys():
                product_typesDict[p] = 1
            else:
                product_typesDict[p] += 1
        for y in years:
            yearsNum[y - 2014] += 1
        customers_data = []
        product_data = []
        for customer in customersDict.keys():
            dataDict = {}
            dataDict["value"] = customersDict[customer]
            dataDict["name"] = customer
            customers_data.append(dataDict)
        for product in product_typesDict.keys():
            dataDict = {}
            dataDict["value"] = product_typesDict[product]
            dataDict["name"] = product
            product_data.append(dataDict)
        return render(request, 'statistics_req.html',
                      {"customers_data": customers_data, "product_data": product_data, "yearsNum": yearsNum})
