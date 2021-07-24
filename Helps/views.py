from django.shortcuts import render, redirect
from Helps.models import Helps, Suggest
from tool11 import settings


# Create your views here.


def add_help(request):
    if request.method == 'GET':
        ID_count = Helps.objects.count() + 1
        return render(request, 'add_help.html', {'ID_new': ID_count})
    else:
        nid = int(request.POST.get('ID'))
        classes = request.POST.get('classes')
        problem = request.POST.get('problem')
        completion = request.POST.get('completion')

        record = Helps(
            ID=nid,
            nid=nid,
            classes=classes,
            problem=problem,
            completion=completion
        )
        record.save()
        return redirect('/Helps/help_table/')


def help_table(request):
    ID_count = Helps.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = Helps.objects.all()[j]
        ID_old = k.nid
        Helps.objects.filter(nid=ID_old).update(nid=i)
    datalist = Helps.objects.values(
        'ID',
        'nid',
        'classes',
        'problem',
        'answer',
        'completion',
    )
    return render(request, 'help_table.html', {'data_list': datalist})


def complete_help(request):
    ID = request.GET.get('ID')
    completion = '已解决'
    Helps.objects.filter(nid=ID).update(
        completion=completion
    )
    return redirect('/Helps/help_table/')


def add_suggest(request):
    if request.method == 'GET':
        ID_count = Suggest.objects.count() + 1
        return render(request, 'add_suggest.html', {'ID_new': ID_count})
    else:
        nid = int(request.POST.get('ID'))
        suggest = request.POST.get('suggest')
        completion = request.POST.get('completion')

        record = Suggest(
            ID=nid,
            nid=nid,
            suggest=suggest,
            completion=completion
        )
        record.save()
        return redirect('/Helps/suggest_table/')


def suggest_table(request):
    ID_count = Suggest.objects.count()
    for i in range(1, ID_count + 1):
        j = i - 1
        k = Suggest.objects.all()[j]
        ID_old = k.nid
        Suggest.objects.filter(nid=ID_old).update(nid=i)
    datalist = Suggest.objects.values(
        'ID',
        'nid',
        'suggest',
        'completion'
    )
    return render(request, 'suggest_table.html', {'data_list': datalist})


def complete_suggest(request):
    ID = request.GET.get('ID')
    completion = '已采纳'
    Suggest.objects.filter(nid=ID).update(
        completion=completion
    )
    return redirect('/Helps/suggest_table/')


def documentations(request):
    if request.method == "GET":
        picDict = {}
        picDict['requirement'] = "/static/img/requirement.png"
        picDict['manufacturing'] = "/static/img/manufacturing.png"
        picDict['maintenance'] = "/static/img/maintenance.png"
        picDict['experience'] = "/static/img/experience.png"
        picDict['knowledge'] = "/static/img/knowledge.png"
        return render(request, 'documentations.html', {"picDict": picDict})
