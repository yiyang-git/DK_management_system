from django.shortcuts import render
from Requirements.models import Require
from Maintenance.models import Fault, RunRecord
from Manufacturing.models import ManOuter, ManUnqual, ManReceive
from Experiment.models import Test
from django.db.models import Q
import datetime


def search(request):
    if request.method == "GET":
        return render(request, 'search.html')
    elif request.method == "POST":
        key_word = request.POST.get('key_word')
        key_word_all = request.POST.get('key_word_all')
        key_word_full = request.POST.get('key_word_full')
        key_word_any = request.POST.get('key_word_any')
        req = request.POST.get('req')
        man = request.POST.get('man')
        mtn = request.POST.get('mtn')
        exp = request.POST.get('exp')
        date = request.POST.get('date')
        charger = request.POST.get('charger')
        data_list = {
            "req": '',
            "rec": '',
            "unq": '',
            "out": '',
            "run": '',
            "fault": '',
            "exp": '',
        }
        if key_word is not None:
            datalist_req = Require.objects.filter(
                Q(customer__contains=key_word) |
                Q(product_type__contains=key_word) |
                Q(product_code__contains=key_word) |
                Q(place__contains=key_word) |
                Q(condition__contains=key_word) |
                Q(nandian__contains=key_word) |
                Q(attention__contains=key_word)
            ).values(
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
            datalist_rec = ManReceive.objects.filter(
                Q(yanshouren__contains=key_word) |
                Q(part__contains=key_word) |
                Q(problem__contains=key_word) |
                Q(solution__contains=key_word) |
                Q(banzu__contains=key_word) |
                Q(diaodu__contains=key_word) |
                Q(laiyuan__contains=key_word)
            ).values(
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

            datalist_unq = ManUnqual.objects.filter(
                Q(inform__contains=key_word) |
                Q(type__contains=key_word) |
                Q(result__contains=key_word) |
                Q(pro_detail__contains=key_word) |
                Q(chuzhi__contains=key_word) |
                Q(defect_text__contains=key_word)
            ).values(
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

            datalist_out = ManOuter.objects.filter(
                Q(problem__contains=key_word) |
                Q(institution__contains=key_word) |
                Q(charger__contains=key_word) |
                Q(note__contains=key_word)
            ).values(
                'nid',
                'date',
                'problem',
                'institution',
                'charger',
                'completion',
                'note'
            )

            datalist_run = RunRecord.objects.filter(
                Q(charger__contains=key_word) |
                Q(equipment__contains=key_word) |
                Q(circuit__contains=key_word) |
                Q(screw__contains=key_word) |
                Q(deformation__contains=key_word) |
                Q(note__contains=key_word)
            ).values(
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

            datalist_fault = Fault.objects.filter(
                Q(problem__contains=key_word) |
                Q(charger__contains=key_word) |
                Q(reportperson__contains=key_word)
            ).values(
                'ID',
                'nid',
                'date',
                'problem',
                'charger',
                'reportperson',
                'completion',
                'risk_level'
            )

            datalist_exp = Test.objects.filter(
                Q(charger__contains=key_word) |
                Q(equipment__contains=key_word) |
                Q(detail__contains=key_word) |
                Q(conclusion__contains=key_word)
            ).values(
                'ID',
                'nid',
                'date',
                'equipment',
                'charger',
                'detail',
                'conclusion',

            )

            data_list["req"] = datalist_req
            data_list["rec"] = datalist_rec
            data_list["unq"] = datalist_unq
            data_list["out"] = datalist_out
            data_list["run"] = datalist_run
            data_list["fault"] = datalist_fault
            data_list["exp"] = datalist_exp

        # elif key_word_all is not None:

        return render(request, 'search.html', {"data_list": data_list})
