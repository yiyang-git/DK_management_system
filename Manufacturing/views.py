from django.shortcuts import render, HttpResponse, redirect
from Manufacturing.models import ManReceive, ManUnqual, ManOuter


# Create your views here.
def add_receive(request):
    if request.method == 'GET':
        ID_new = ManReceive.objects.count() + 1
        return render(request, 'add_receive.html', {'ID_new': ID_new})
    else:
        ID = int(request.POST.get('ID'))
        date = request.POST.get('date')
        worker = request.POST.get('worker')
        part = request.POST.get('part')
        problem = request.POST.get('problem')
        solution = request.POST.get('solution')
        banzu = request.POST.get('banzu')
        diaodu = request.POST.get('diaodu')
        laiyuan = request.POST.get('laiyuan')
        yanshouren = request.POST.get('yanshouren')
        wancheng = request.POST.get('wancheng')
        print(date, worker, problem, solution, banzu, diaodu, laiyuan, yanshouren, wancheng)
        record = ManReceive(
            ID=ID,
            date=date,
            worker=worker,
            part=part,
            problem=problem,
            solution=solution,
            banzu=banzu,
            diaodu=diaodu,
            laiyuan=laiyuan,
            yanshouren=yanshouren,
            wancheng=wancheng,
        )
        record.save()
        return redirect('/Manufacturing/receive_table/')


def receive_table(request):
    ID_count = ManReceive.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = ManReceive.objects.all()[j]
        ID_old = k.ID
        ManReceive.objects.filter(id=ID_old).update(ID=i)
    try:
        page = int(request.GET.get('page'))
        pageRange1, pageRange2 = (page - 1) * 11, (page - 1) * 11 + 10
    except:
        page = 1
        pageRange1, pageRange2 = (page - 1) * 11, (page - 1) * 11 + 10
    datalist = ManReceive.objects.values(
        'ID',
        'date',
        'worker',
        'part',
        'problem',
        'solution',
        'banzu',
        'diaodu',
        'laiyuan',
        'yanshouren',
        'wancheng',
    )
    return render(request, 'receive_table.html', {'data_list': datalist[pageRange1:pageRange2]})


def edit_receive(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = ManReceive.objects.get(id=ID)
        return render(request, 'edit_receive.html', {'item': item})
    else:
        ManReceive.objects.filter(id=ID).update(
            ID=request.POST.get('ID'),
            date=request.POST.get('date'),
            worker=request.POST.get('worker'),
            part=request.POST.get('part'),
            problem=request.POST.get('problem'),
            solution=request.POST.get('solution'),
            banzu=request.POST.get('banzu'),
            diaodu=request.POST.get('diaodu'),
            laiyuan=request.POST.get('laiyuan'),
            yanshouren=request.POST.get('yanshouren'),
            wancheng=request.POST.get('wancheng')
        )
        return redirect('/Manufacturing/receive_table/')


def delete_receive(request):
    ID = request.GET.get('ID')
    ManReceive.objects.filter(id=ID).delete()
    return redirect('/Manufacturing/receive_table/')


def add_unqual(request):
    if request.method == 'GET':
        ID_count = ManUnqual.objects.count() + 1
        # ID_new = ManUnqual.objects.values('id')
        # print(ID_new)
        # print(ManUnqual.objects.values('id'))
        return render(request, 'add_unqual.html', {'ID_new': ID_count})
    else:
        ID = int(request.POST.get('ID'))
        date = request.POST.get('date')
        inform = request.POST.get('inform')
        type = request.POST.get('type')
        fac = request.POST.get('fac')
        found_date = request.POST.get('found_date')
        creat_date = request.POST.get('creat_date')
        chuzhi = request.POST.get('chuzhi')
        gongying = request.POST.get('gongying')
        result = request.POST.get('result')
        defect_text = request.POST.get('defect_text')
        problem = request.POST.get('problem')
        pro_detail = request.POST.get('pro_detail')

        record = ManUnqual(
            ID=ID,
            date=date,
            inform=inform,
            type=type,
            fac=fac,
            found_date=found_date,
            creat_date=creat_date,
            chuzhi=chuzhi,
            gongying=gongying,
            result=result,
            defect_text=defect_text,
            problem=problem,
            pro_detail=pro_detail
        )
        record.save()
        return redirect('/Manufacturing/unqual_table/')


def unqual_table(request):
    ID_count = ManUnqual.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = ManUnqual.objects.all()[j]
        ID_old = k.ID
        ManUnqual.objects.filter(id=ID_old).update(ID=i)
    try:
        page = int(request.GET.get('page'))
        pageRange1, pageRange2 = (page - 1) * 11, (page - 1) * 11 + 10
    except:
        page = 1
        pageRange1, pageRange2 = (page - 1) * 11, (page - 1) * 11 + 10
    datalist = ManUnqual.objects.values(
        'ID',
        'date',
        'inform',
        'type',
        'fac',
        'found_date',
        'creat_date',
        'problem',
        'pro_detail',
        'chuzhi',
        'gongying',
        'result',
        'defect_text',
    )
    return render(request, 'unqual_table.html', {'data_list': datalist[pageRange1:pageRange2]})


def edit_unqual(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = ManUnqual.objects.get(id=ID)
        return render(request, 'edit_unqual.html', {'item': item})
    else:
        ManUnqual.objects.filter(id=ID).update(
            ID=request.POST.get('ID'),
            date=request.POST.get('date'),
            inform=request.POST.get('inform'),
            type=request.POST.get('type'),
            fac=request.POST.get('fac'),
            found_date=request.POST.get('found_date'),
            creat_date=request.POST.get('creat_date'),
            chuzhi=request.POST.get('chuzhi'),
            gongying=request.POST.get('gongying'),
            result=request.POST.get('result'),
            defect_text=request.POST.get('defect_text'),
            problem=request.POST.get('problem'),
            pro_detail=request.POST.get('pro_detail')
        )
        return redirect('/Manufacturing/unqual_table/')


def delete_unqual(request):
    ID = request.GET.get('ID')
    ManUnqual.objects.filter(id=ID).delete()
    return redirect('/Manufacturing/unqual_table/')


def outer_table(request):
    ID_count = ManOuter.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = ManOuter.objects.all()[j]
        ID_old = k.nid
        ManOuter.objects.filter(nid=ID_old).update(nid=i)
    try:
        page = int(request.GET.get('page'))
        pageRange1, pageRange2 = (page - 1) * 11, (page - 1) * 11 + 10
    except:
        page = 1
        pageRange1, pageRange2 = (page - 1) * 11, (page - 1) * 11 + 10
    datalist = ManOuter.objects.values(
        'nid',
        'date',
        'problem',
        'institution',
        'charger',
        'completion',
        'note'
    )
    return render(request, 'outer_table.html', {'data_list': datalist[pageRange1:pageRange2]})


def add_outer(request):
    if request.method == 'GET':
        ID_count = ManOuter.objects.count() + 1
        return render(request, 'add_outer.html', {'ID_new': ID_count})
    else:
        nid = int(request.POST.get('ID'))
        date = request.POST.get('date')
        problem = request.POST.get('problem')
        institution = request.POST.get('institution')
        charger = request.POST.get('charger')
        completion = request.POST.get('completion')
        note = request.POST.get('note')

        record = ManOuter(
            ID=nid,
            nid=nid,
            date=date,
            problem=problem,
            institution=institution,
            charger=charger,
            completion=completion,
            note=note
        )
        record.save()
        return redirect('/Manufacturing/outer_table/')


def edit_outer(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = ManOuter.objects.get(nid=ID)
        return render(request, 'edit_outer.html', {'item': item})
    else:
        ManOuter.objects.filter(nid=ID).update(
            nid=request.POST.get('ID'),
            date=request.POST.get('date'),
            problem=request.POST.get('problem'),
            institution=request.POST.get('institution'),
            charger=request.POST.get('charger'),
            completion=request.POST.get('completion'),
            note=request.POST.get('note')
        )
        return redirect('/Manufacturing/outer_table/')


def delete_outer(request):
    ID = request.GET.get('ID')
    ManOuter.objects.filter(nid=ID).delete()
    return redirect('/Manufacturing/outer_table/')
