from django.shortcuts import render, HttpResponse, redirect
from Maintenance.models import RunRecord, Fault


# Create your views here.
def add_runRecord(request):
    if request.method == 'GET':
        ID_new = RunRecord.objects.count() + 1
        return render(request, 'add_runrecord.html', {'ID_new': ID_new})
    else:
        nid = int(request.POST.get('ID'))
        date = request.POST.get('date')
        equipment = request.POST.get('equipment')
        charger = request.POST.get('charger')
        circuit = request.POST.get('circuit')
        screw = request.POST.get('screw')
        deformation = request.POST.get('deformation')
        work = request.POST.get('work')
        all = request.POST.get('all')
        note = request.POST.get('note')
        record = RunRecord(
            ID=nid,
            nid=nid,
            date=date,
            equipment=equipment,
            charger=charger,
            circuit=circuit,
            screw=screw,
            deformation=deformation,
            work=work,
            all=all,
            note=note,
        )
        record.save()
        return redirect('/Maintenance/runRecord_table/')


def runRecord_table(request):
    ID_count = RunRecord.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = RunRecord.objects.all()[j]
        ID_old = k.nid
        RunRecord.objects.filter(nid=ID_old).update(nid=i)
        RunRecord.objects.filter(nid=ID_old).update(id=i)
    datalist = RunRecord.objects.values(
        'nid',
        'date',
        'equipment',
        'charger',
        'circuit',
        'screw',
        'deformation',
        "work",
        "all",
        "note"
    )
    return render(request, 'runrecord_table.html', {'data_list': datalist})


def edit_runRecord(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = RunRecord.objects.get(nid=ID)
        return render(request, 'edit_runrecord.html', {'item': item})
    else:
        RunRecord.objects.filter(nid=ID).update(
            id=int(request.POST.get('ID')),
            nid=int(request.POST.get('ID')),
            date=request.POST.get('date'),
            equipment=request.POST.get('equipment'),
            charger=request.POST.get('charger'),
            circuit=request.POST.get('circuit'),
            screw=request.POST.get('screw'),
            deformation=request.POST.get('deformation'),
            work=request.POST.get('work'),
            all=request.POST.get('all'),
            note=request.POST.get('note')
        )
        return redirect('/Maintenance/runRecord_table')


def delete_runRecord(request):
    ID = request.GET.get('ID')
    RunRecord.objects.filter(nid=ID).delete()
    return redirect('/Maintenance/runRecord_table/')


def add_fault(request):
    if request.method == 'GET':
        ID_count = Fault.objects.count() + 1
        return render(request, 'add_fault.html', {'ID_new': ID_count})
    else:
        nid = int(request.POST.get('ID'))
        date = request.POST.get('date')
        problem = request.POST.get('problem')
        charger = request.POST.get('charger')
        reportperson = request.POST.get('reportperson')
        completion = request.POST.get('completion')
        risk_level = request.POST.get('risk_level')

        record = Fault(
            ID=nid,
            nid=nid,
            date=date,
            problem=problem,
            charger=charger,
            reportperson=reportperson,
            completion=completion,
            risk_level=risk_level
        )
        record.save()
        return redirect('/Maintenance/fault_table/')


def fault_table(request):
    ID_count = Fault.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = Fault.objects.all()[j]
        ID_old = k.nid
        Fault.objects.filter(nid=ID_old).update(nid=i)
    datalist = Fault.objects.values(
        'ID',
        'nid',
        'date',
        'problem',
        'charger',
        'reportperson',
        'completion',
        'risk_level'
    )
    return render(request, 'fault_table.html', {'data_list': datalist})


def edit_fault(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = Fault.objects.get(nid=ID)
        return render(request, 'edit_fault.html', {'item': item})
    else:
        Fault.objects.filter(nid=ID).update(
            id=int(request.POST.get('ID')),
            nid=int(request.POST.get('ID')),
            date=request.POST.get('date'),
            problem=request.POST.get('problem'),
            charger=request.POST.get('charger'),
            reportperson=request.POST.get('reportperson'),
            completion=request.POST.get('completion'),
            risk_level=request.POST.get('risk_level')
        )
        return redirect('/Maintenance/fault_table/')


def delete_fault(request):
    ID = request.GET.get('ID')
    Fault.objects.filter(nid=ID).delete()
    return redirect('/Maintenance/fault_table/')
