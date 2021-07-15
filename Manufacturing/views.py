from django.shortcuts import render, HttpResponse, redirect
from Manufacturing.models import ManReceive, ManUnqual


# Create your views here.
def receive(request):
    if request.method == 'GET':
        return render(request, 'receive.html')
    else:
        date = request.POST.get('date')
        worker = request.POST.get('worker')
        problem = request.POST.get('problem')
        solution = request.POST.get('solution')
        banzu = request.POST.get('banzu')
        diaodu = request.POST.get('diaodu')
        laiyuan = request.POST.get('laiyuan')
        yanshouren = request.POST.get('yanshouren')
        wancheng = request.POST.get('wancheng')
        print(date, worker, problem, solution, banzu, diaodu, laiyuan, yanshouren, wancheng)
        record = ManReceive(
            date=date,
            worker=worker,
            problem=problem,
            solution=solution,
            banzu=banzu,
            diaodu=diaodu,
            laiyuan=laiyuan,
            yanshouren=yanshouren,
            wancheng=wancheng,
        )
        record.save()
        return redirect('/Manufacturing/receive/')


def receive_table(request):
    datalist = ManReceive.objects.values(
        'date',
        'worker',
        'problem',
        'solution',
        'banzu',
        'diaodu',
        'laiyuan',
        'yanshouren',
        'wancheng',
    )
    return render(request, 'receive_tabel.html', {'data_list': datalist})


def unqual(request):
    return render(request, 'unqual.html')


def unqual_table(request):
    datalist = ManUnqual.objects.values(
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
    return render(request, 'unqual_tabel.html', {'data_list': datalist})
