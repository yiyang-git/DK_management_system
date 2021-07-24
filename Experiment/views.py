from django.shortcuts import render, HttpResponse, redirect
from Experiment.models import Test


def add_test(request):
    if request.method == 'GET':
        ID_count = Test.objects.count() + 1
        return render(request, 'add_test.html', {'ID_new': ID_count})
    else:
        nid = int(request.POST.get('ID'))
        date = request.POST.get('date')
        equipment = request.POST.get('equipment')
        charger = request.POST.get('charger')
        detail = request.POST.get('detail')
        conclusion = request.POST.get('conclusion')

        record = Test(
            ID=nid,
            nid=nid,
            date=date,
            equipment=equipment,
            charger=charger,
            detail=detail,
            conclusion=conclusion,

        )
        record.save()
        return redirect('/Experiment/test_table/')


def test_table(request):
    ID_count = Test.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = Test.objects.all()[j]
        ID_old = k.nid
        Test.objects.filter(nid=ID_old).update(nid=i)
    datalist = Test.objects.values(
        'ID',
        'nid',
        'date',
        'equipment',
        'charger',
        'detail',
        'conclusion',

    )
    return render(request, 'test_table.html', {'data_list': datalist})


def edit_test(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = Test.objects.get(nid=ID)
        return render(request, 'edit_test.html', {'item': item})
    else:
        Test.objects.filter(nid=ID).update(
            id=int(request.POST.get('ID')),
            nid=int(request.POST.get('ID')),
            date=request.POST.get('date'),
            equipment=request.POST.get('equipment'),
            charger=request.POST.get('charger'),
            detail=request.POST.get('detail'),
            conclusion=request.POST.get('conclusion')
        )
        return redirect('/Experiment/test_table/')


def delete_test(request):
    ID = request.GET.get('ID')
    Test.objects.filter(nid=ID).delete()
    return redirect('/Experiment/test_table/')
