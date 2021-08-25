from django.shortcuts import render, redirect
from Knowledge.models import Knowledge
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.db.models import Q
import csv, os, json, datetime


def csv_to_model(path, name):
    dict = {}
    save_dict = {}
    with open(path, "rt", encoding="utf-8") as f:
        reader = csv.reader(f)
        try:
            ids = Knowledge.objects.values('id')
            ids_list = []
            for i in ids:
                ids_list.append(i["id"])
            ids = ids_list[-1]
        except:
            ids = 0
        for row in reader:
            if row[0] != '':
                for i in row:
                    if i[-4:] == '设计任务' or i[-5:] == '设计任务书':
                        l1 = []
                        for j in i:
                            if j != '设':
                                l1.append(j)
                            else:
                                break
                        save_dict['type'] = ''.join(l1)
                    if i not in dict.keys():
                        dict[i] = 1
                    else:
                        dict[i] += 1
                ids += 1
                record = Knowledge(
                    classes=name,
                    process=row[0],
                    relation=row[1],
                    standard=row[2],
                    id=ids
                )
                record.save()
        dict = sorted(dict.items(), key=lambda x: x[1], reverse=False)
        print(dict)
        n = 0
        keyword_list = []
        for key, value in dict:
            if n <= 4:
                keyword_list.append(key)
                n += 1
            else:
                break

        save_dict['date'] = str(datetime.datetime.now())[:10]
        save_dict['name'] = name
        save_dict['keyword_list'] = keyword_list
        print(save_dict)
        with open('static/json/knowledge_save.txt', 'a') as f:
            f.write(str(save_dict) + '\n')
            f.close()


def knowledge_add(request):
    if request.method == 'GET':
        return render(request, 'knowledge_add.html')
    elif request.method == 'POST':
        csv_file = request.FILES.get('csv_file')
        path = settings.BASE_DIR + "/static/csv/" + csv_file.name
        save = default_storage.save(path, ContentFile(csv_file.read()))
        csv_to_model(path, name=csv_file.name)

        return redirect('/Knowledge/knowledge_show/')


def get_data(list):
    dict = {}
    for i in list:
        if i not in dict.keys():
            dict[i] = 1
        else:
            dict[i] += 1
    return dict


def knowledge_show(request):
    if request.method == 'GET':
        try:
            classes = request.GET.get('classes')
            datalist_knowledge = Knowledge.objects.filter(classes=classes).values('classes', "process", "standard",
                                                                                  "relation")
            datalist_knowledge_org = Knowledge.objects.values('classes')
        except:
            classes = 0
            datalist_knowledge_org = Knowledge.objects.values('classes')
            datalist_knowledge = datalist_knowledge_org

        classes = []
        processes = []
        standards = []
        relations = []
        for item in datalist_knowledge_org:
            classes.append(item["classes"])
        for item in datalist_knowledge:
            processes.append(item["process"])
            standards.append(item["standard"])
            relations.append(item["relation"])
        classes = get_data(classes).keys()
        names_org = get_data(processes + standards)
        names_org_keys = list(names_org.keys())
        for n in names_org.keys():
            if names_org[n] == 1:
                names_org[n] = 50
            elif names_org[n] >= 2 and names_org[n] <= 5:
                names_org[n] = 60
            elif names_org[n] >= 6 and names_org[n] <= 10:
                names_org[n] = 80
            else:
                names_org[n] = 100
        names = []
        for name in names_org_keys:
            if len(name) >= 7:
                names.append(name[0:6] + '...')
            else:
                names.append(name)
        plot = {}
        plot['name'] = names_org_keys
        plot['des'] = names
        symbolsize = []
        for sy in names_org_keys:
            symbolsize.append(names_org[sy])
        plot['symbolsize'] = symbolsize
        link = {}
        link['source'] = processes
        link['target'] = standards
        link['name'] = relations
        link['des'] = relations

        return render(request, 'knowledge_show.html',
                      {'classes': classes, 'len': len(names), 'link': link, 'plot': plot})


def knowledge_manage(request):
    if request.method == 'GET':
        ID_count = Knowledge.objects.count()
        for i in range(1, ID_count + 1):
            j = i - 1
            k = Knowledge.objects.all()[j]
            ID_old = k.id
            Knowledge.objects.filter(id=ID_old).update(id=i)

        datalist = Knowledge.objects.values('classes')
        classes_list = []
        for item in datalist:
            classes_list.append(item["classes"])
        classes_dict = get_data(classes_list)
        classes = list(classes_dict.keys())
        with open('static/json/knowledge_save.txt', 'r') as f:
            knowledge_list = []
            line = f.readline()

            while line:
                knowledge_list.append(eval(line))
                line = f.readline()

        return render(request, 'knowledge_manage.html', {'classes': classes, 'knowledge_list': knowledge_list})
    elif request.method == 'POST':
        type = request.POST.get('classes')
        keyword = request.POST.get('keyword')
        try:
            datalist = Knowledge.objects.filter(classes=type).filter(Q(process__contains=keyword) |
                                                                     Q(relation__contains=keyword) | Q(
                standard__contains=keyword)).values('process', 'relation', 'standard', 'id')
        except:
            datalist = Knowledge.objects.filter(classes=type).values('process', 'relation', 'standard', 'id')

        datalist_org = Knowledge.objects.values('classes')
        classes_list = []
        for item in datalist_org:
            classes_list.append(item["classes"])
        classes_dict = get_data(classes_list)
        classes = list(classes_dict.keys())
        with open('static/json/knowledge_save.txt', 'r') as f:
            knowledge_list = []
            line = f.readline()

            while line:
                knowledge_list.append(eval(line))
                line = f.readline()
        return render(request, 'knowledge_manage.html',
                      {'classes': classes, 'datalist': datalist, 'knowledge_list': knowledge_list})


def edit_knowledge(request):
    if request.method == 'GET' or request.GET:
        global ID
        ID = request.GET.get('ID')
        item = Knowledge.objects.get(id=ID)
        return render(request, 'edit_knowledge.html', {'item': item})
    else:
        id = request.POST.get('id')
        Knowledge.objects.filter(id=id).update(
            id=request.POST.get('id'),
            process=request.POST.get('process'),
            relation=request.POST.get('relation'),
            standard=request.POST.get('standard')
        )
        return redirect('/Knowledge/knowledge_manage/')


def delete_knowledge(request):
    ID = request.GET.get('ID')
    Knowledge.objects.filter(id=ID).delete()
    return redirect('/Knowledge/knowledge_manage/')


def delete_file(request):
    name = request.GET.get('name')
    Knowledge.objects.filter(classes=name).delete()
    return redirect('/Knowledge/knowledge_manage/')
