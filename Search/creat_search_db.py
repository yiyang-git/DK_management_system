def creat_search():
    from Requirements.models import Require
    from Maintenance.models import Fault, RunRecord
    from Manufacturing.models import ManOuter, ManUnqual, ManReceive
    from Experiment.models import Test
    from Search.models import Search

    datalist_req = Require.objects.values(
        'ID',
        'customer',
        'product_type',
        'product_code',
        'place',
        'condition',
        'nandian',
        'attention'
    )
    datalist_rec = ManReceive.objects.values(
        'ID',
        'problem',
        'solution',
        'banzu',
        'diaodu',
        'yanshouren'
    )

    datalist_unq = ManUnqual.objects.values(
        'ID',
        'type',
        'problem',
        'pro_detail',
        'chuzhi',
        'result',
        'defect_text'
    )

    datalist_out = ManOuter.objects.values(
        'nid',
        'problem',
        'institution',
        'charger',
        'note'
    )

    datalist_run = RunRecord.objects.values(
        'nid',
        'equipment',
        'charger',
        "note"
    )

    datalist_fault = Fault.objects.values(
        'nid',
        'problem',
        'charger',
        'reportperson'
    )

    datalist_exp = Test.objects.values(
        'nid',
        'detail',
        'conclusion'
    )
    for item in datalist_req:
        record = Search(
            nid=item['ID'],
            classes='req',
            document=item['customer'] + item['product_type'] + item['product_code'] + item['place'] + item[
                'condition'] + item['nandian'] + item['attention'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_rec:
        record = Search(
            nid=item['ID'],
            classes='rec',
            document=item['problem'] + item['solution'] + item['banzu'] + item['diaodu'] + item['yanshouren'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_unq:
        record = Search(
            nid=item['ID'],
            classes='unq',
            document=item['problem'] + item['type'] + item['pro_detail'] + item['chuzhi'] + item['result'] + item[
                'defect_text'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_out:
        record = Search(
            nid=item['nid'],
            classes='out',
            document=item['problem'] + item['institution'] + item['charger'] + item['note'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_run:
        record = Search(
            nid=item['nid'],
            classes='run',
            document=item['equipment'] + item['charger'] + item['note'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_fault:
        record = Search(
            nid=item['nid'],
            classes='fault',
            document=item['problem'] + item['charger'] + item['reportperson'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_fault:
        record = Search(
            nid=item['nid'],
            classes='fault',
            document=item['problem'] + item['charger'] + item['reportperson'],
            global_similar_text='',
            similar=0
        )
        record.save()

    for item in datalist_exp:
        record = Search(
            nid=item['nid'],
            classes='exp',
            document=item['detail'] + item['conclusion'],
            global_similar_text='',
            similar=0
        )
        record.save()
