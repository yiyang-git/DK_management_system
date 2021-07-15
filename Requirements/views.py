from django.shortcuts import render, redirect, HttpResponse
from Requirements.models import Require


# Create your views here.

def add_req(request):
    if request.method == 'GET':
        return render(request, 'add_req.html')
    else:
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
        return redirect('/Requirements/add_req/')


def req_list(request):
    datalist = Require.objects.values(
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
    return render(request, 'req_list.html', {'data_list': datalist})
