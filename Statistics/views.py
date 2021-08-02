from django.shortcuts import render
from Requirements.models import Require
from Maintenance.models import Fault, RunRecord
from Manufacturing.models import ManOuter, ManUnqual, ManReceive
from Experiment.models import Test
import datetime


# Create your views here.

def statistics_req(request):
    if request.method == "GET":
        if request.GET.get("begin_date") is not None:
            begin_date = request.GET.get("begin_date")
            end_date = request.GET.get("end_date")
        else:
            begin_date = Require.objects.order_by("date")[0].date  # 拿到最早的日期
            end_date = str(datetime.datetime.now())[:10]  # 拿到现在的日期
        date = {'begin_date': begin_date, 'end_date': end_date}

        datalist = Require.objects.filter(date__range=(begin_date, end_date)).values(
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
                      {"date": date, "customers_data": customers_data, "product_data": product_data,
                       "yearsNum": yearsNum})


def get_data(list):
    dict = {}
    data = []
    for i in list:
        if i not in dict.keys():
            dict[i] = 1
        else:
            dict[i] += 1
    for key in dict.keys():
        dataDict = {}
        dataDict["value"] = dict[key]
        dataDict["name"] = key
        data.append(dataDict)
    return data


def statistics_man(request):
    if request.method == "GET":
        if request.GET.get("begin_date") is not None:
            begin_date = request.GET.get("begin_date")
            end_date = request.GET.get("end_date")
        else:
            begin_date = ManReceive.objects.order_by("date")[0].date  # 拿到最早的日期
            end_date = str(datetime.datetime.now())[:10]  # 拿到现在的日期
        if request.GET.get("begin_date2") is not None:
            begin_date2 = request.GET.get("begin_date2")
            end_date2 = request.GET.get("end_date2")
        else:
            begin_date2 = ManUnqual.objects.order_by("date")[0].date  # 拿到最早的日期
            end_date2 = str(datetime.datetime.now())[:10]  # 拿到现在的日期
        if request.GET.get("begin_date3") is not None:
            begin_date3 = request.GET.get("begin_date3")
            end_date3 = request.GET.get("end_date3")
        else:
            begin_date3 = ManOuter.objects.order_by("date")[0].date  # 拿到最早的日期
            end_date3 = str(datetime.datetime.now())[:10]  # 拿到现在的日期
        date = {'begin_date': begin_date, 'end_date': end_date}
        date2 = {'begin_date2': begin_date2, 'end_date2': end_date2}
        date3 = {'begin_date3': begin_date3, 'end_date3': end_date3}
        datalist_rec = ManReceive.objects.filter(date__range=(begin_date, end_date)).values(
            'date',
            'part',
            'worker',
            'problem',
            'solution',
            'banzu',
            'diaodu',
            'laiyuan',
            'yanshouren',
            'wancheng',
        )
        datalist_unq = ManUnqual.objects.filter(date__range=(begin_date2, end_date2)).values(
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
        data_list = ManReceive.objects.filter(date__range=(begin_date, end_date), wancheng='未完成').values(
            'ID',
            'date',
            'part',
            'worker',
            'problem',
            'solution',
            'banzu',
            'diaodu',
            'laiyuan',
            'yanshouren',
            'wancheng',
        )
        datalist_out = ManOuter.objects.filter(date__range=(begin_date3, end_date3)).values(
            'nid',
            'date',
            'problem',
            'institution',
            'charger',
            'completion',
            'note'
        )
        parts = []
        teams = []
        completions = []
        types = []
        handles = []
        years = []
        yearsNum = [0, 0, 0, 0, 0, 0, 0, 0]
        institutions = []
        completions_out = []
        for item in datalist_rec:
            parts.append(item["part"])
            teams.append(item["banzu"])
            completions.append(item["wancheng"])

        for item in datalist_unq:
            types.append(item["type"])
            handles.append(item["chuzhi"])
            years.append(eval(item["date"][:4]))

        for item in datalist_out:
            institutions.append(item["institution"])
            completions_out.append(item["completion"])

        type_data = get_data(types)
        part_data = get_data(parts)
        team_data = get_data(teams)
        handle_data = get_data(handles)
        institution_data = get_data(institutions)
        completions_out_data = get_data(completions_out)
        for y in years:
            yearsNum[y - 2014] += 1
        num_not = 0
        num_done = 0
        for c in completions:
            if c == '已完成':
                num_done += 1
            else:
                num_not -= 1

        return render(request, 'statistics_man.html',
                      {
                          "date": date,
                          "date2": date2,
                          "date3": date3,
                          "part_data": part_data, "team_data": team_data, "num_done": num_done, "num_not": num_not,
                          "data_list": data_list,
                          "type_data": type_data, "handle_data": handle_data, "yearsNum": yearsNum,
                          "institution_data": institution_data, "completions_out_data": completions_out_data
                      })


def statistics_mtn(request):
    if request.method == "GET":
        if request.GET.get("begin_date") is not None:
            begin_date = request.GET.get("begin_date")
            end_date = request.GET.get("end_date")
        else:
            begin_date = ManReceive.objects.order_by("date")[0].date  # 拿到最早的日期
            end_date = str(datetime.datetime.now())[:10]  # 拿到现在的日期
        date = {'begin_date': begin_date, 'end_date': end_date}

        if request.GET.get("record_year") is not None:
            record_year = request.GET.get("record_year")[:4]
        else:
            record_year = str(datetime.datetime.now())[:4]  # 拿到现在的年
        datalist_runrecord = RunRecord.objects.filter(
            date__range=(record_year + '-01-01', record_year + '-12-30')).values(
            'date',
            'circuit',
            'screw',
            'deformation',
            "work",
            "all")
        datalist_fault = Fault.objects.filter(date__range=(begin_date, end_date)).values(
            'ID',
            'nid',
            'date',
            'problem',
            'charger',
            'reportperson',
            'completion',
            'risk_level'
        )
        data_runrecord = []
        for item in datalist_runrecord:
            if item['circuit'] == item['screw'] == item['deformation'] == item['work'] == item['all'] == '是':
                status = 2
            elif item['work'] == '是':
                status = 1
            else:
                status = 0
            data_runrecord.append([item['date'], status])
        chargers = []
        completions = []
        risks = []
        for item in datalist_fault:
            chargers.append(item["charger"])
            risks.append(item["risk_level"])
            completions.append(item["completion"])
        charger_data = get_data(chargers)
        risk_data = get_data(risks)

        num_not = 0
        num_done = 0
        for c in completions:
            if c == '已解决':
                num_done += 1
            else:
                num_not -= 1

        return render(request, 'statistics_mtn.html',
                      {
                          "date": date,
                          "record_year_title": record_year,
                          "record_year": record_year + "-01-01",
                          "data_runrecord": data_runrecord,
                          "charger_data": charger_data,
                          "risk_data": risk_data,
                          "num_done": num_done,
                          "num_not": num_not
                      })


def statistics_exp(request):
    if request.GET.get("begin_date") is not None:
        begin_date = request.GET.get("begin_date")
        end_date = request.GET.get("end_date")
    else:
        begin_date = Test.objects.order_by("date")[0].date  # 拿到最早的日期
        end_date = str(datetime.datetime.now())[:10]  # 拿到现在的日期
    date = {'begin_date': begin_date, 'end_date': end_date}

    datalist = Test.objects.filter(date__range=(begin_date, end_date)).values(
        'ID',
        'nid',
        'date',
        'equipment',
        'charger',
        'detail',
        'conclusion'
    )
    chargers = []
    years = []
    yearsNum = [0, 0, 0, 0, 0, 0, 0, 0]
    for item in datalist:
        chargers.append(item["charger"])
        years.append(eval(item["date"][0:4]))
    charger_data = get_data(chargers)
    for y in years:
        yearsNum[y - 2014] += 1
    return render(request, 'statistics_exp.html',
                  {
                      "date": date,
                      "charger_data": charger_data,
                      "yearsNum": yearsNum
                  })


def statistics_custom(request):
    if request.method == "GET":
        if request.GET.get("begin_date") is not None:
            begin_date = request.GET.get("begin_date")
            end_date = request.GET.get("end_date")
        else:
            begin_date = '2010-01-01'  # 拿到最早的日期
            end_date = str(datetime.datetime.now())[:10]  # 拿到现在的日期
        date = {'begin_date': begin_date, 'end_date': end_date}
        datalist_req = Require.objects.filter(date__range=(begin_date, end_date)).values(
            'customer',
            'product_type',
            'place'
        )
        datalist_rec = ManReceive.objects.filter(date__range=(begin_date, end_date)).values(
            'part',
            'banzu'
        )
        datalist_unq = ManUnqual.objects.filter(date__range=(begin_date, end_date)).values(
            'type',
            'chuzhi'
        )
        datalist_out = ManOuter.objects.filter(date__range=(begin_date, end_date)).values(
            'institution'
        )
        datalist_fault = Fault.objects.filter(date__range=(begin_date, end_date)).values(
            'charger',
        )
        datalist_exp = Test.objects.filter(date__range=(begin_date, end_date)).values(
            'charger',
        )
        datalistDict = {
            'datalist_req': datalist_req,
            'datalist_rec': datalist_rec,
            'datalist_unq': datalist_unq,
            'datalist_out': datalist_out,
            'datalist_fault': datalist_fault,
            'datalist_exp': datalist_exp,
        }
        table_names = [
            '需求数据-客户',
            '需求数据-产品类别',
            '需求数据-交货地点',
            '验收数据-验收问题部件',
            '验收数据-验收班组',
            '不合格单-不合格类型',
            '不合格单-处置方式',
            '外协问题-外部负责机构',
            '故障数据-故障负责人',
            '试验数据-负责人'
        ]
        datalist_names = [['req', 'customer'],
                          ['req', 'product_type'],
                          ['req', 'place'],
                          ['rec', 'part'],
                          ['rec', 'banzu'],
                          ['unq', 'type'],
                          ['unq', 'chuzhi'],
                          ['out', 'institution'],
                          ['fault', 'charger'],
                          ['exp', 'charger']
                          ]
        data = []
        table_titles = []
        subtexts = []
        for i in range(6):
            table_titles.append(request.GET.get("table" + str(i)))
        for table in table_titles:
            if table == "暂无":
                data.append([])
                subtexts.append('暂无')
            else:
                for j in range(10):
                    if table == table_names[j]:
                        datalist_name = "datalist_" + datalist_names[j][0]
                        column_name = datalist_names[j][1]
                        subtexts.append(table_names[j])
                        list = []
                        for item in datalistDict[datalist_name]:
                            list.append(item[column_name])
                        data.append(get_data(list))
                    else:
                        continue

        return render(request, 'statistics_custom.html',
                      {
                          "date": date,
                          "dataList": data,
                          "subtexts": subtexts
                      })
