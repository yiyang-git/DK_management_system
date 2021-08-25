import jieba
from django.shortcuts import render
from Requirements.models import Require
from Maintenance.models import Fault, RunRecord
from Manufacturing.models import ManOuter, ManUnqual, ManReceive
from Experiment.models import Test
from Search.models import Search
from django.db.models import Q

from gensim import corpora, models, similarities
import datetime


def search(request):
    if request.method == "GET":
        search_way = 'None'
        return render(request, 'search.html', {'search_way': search_way})
    elif request.method == "POST":
        key_word = request.POST.get('key_word')
        key_word_exact = request.POST.get('key_word_exact')
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
        if key_word != None and key_word != '':
            search_way = 'fuzzy'
            text_base = []
            cases = Search.objects.all()
            for a in cases:
                text_base.append(str(a.document))

            # 1.提取实例库中物料类型属性的全部数据构成text_base，将text_base中的每条数据进行分词得到words_base
            words_base = [[i for i in jieba.lcut(item)] for item in text_base]
            # 2.生成词典
            dictionary = corpora.Dictionary(words_base)
            # 3.通过doc2bow稀疏向量生成语料库
            corpus = [dictionary.doc2bow(item) for item in words_base]
            # 4.获得语料库的TFIDF、LSI模型
            tfidf = models.TfidfModel(corpus)
            lsi = models.LsiModel(corpus)
            # 5.通过token2id得到特征数（字典里面的键的个数）
            num_features = len(dictionary.token2id.keys())
            # 6.通过TFIDF、LSI模型将语料库的词转化为该模型下的向量
            vec_corpus_tfidf = tfidf[corpus]
            vec_corpus_lsi = lsi[corpus]
            # 7.构建每个文档对每个特征词的相似度，通过计算欧式距离（也可选择其他方法），获得稀疏矩阵相似度，建立一个索引
            similar_matrix_index_tfidf = similarities.MatrixSimilarity(vec_corpus_tfidf,
                                                                       num_features=num_features)  # 欧氏距离相似度
            similar_matrix_index_lsi = similarities.MatrixSimilarity(vec_corpus_lsi, num_features=num_features)  # 余弦相似度
            # 8.对待搜索文本进行分词
            search_words = [word for word in jieba.cut(key_word)]
            # 9.通过TFIDF、LSI模型获得新的稀疏向量
            vec_bow = dictionary.doc2bow(search_words)
            vec_tfidf = tfidf[vec_bow]  # 通过tfidf模型将新词转化为该模型下的向量
            vec_lsi = lsi[vec_bow]
            # 10.到构建的相似度矩阵中，通过索引找到和语料库中相同向量的词的tfidf相似度、lsi相似度
            similar_tfidf = similar_matrix_index_tfidf[vec_tfidf]
            similar_lsi = similar_matrix_index_lsi[vec_lsi]
            for i in range(len(similar_lsi)):
                if similar_lsi[i] < 0:
                    similar_lsi[i] = 0
            # 11.综合相似度
            w1 = 0.5
            w2 = 0.5
            amplification = 8  # 放大系数
            global_similar_text = w1 * similar_tfidf + w2 * similar_lsi
            global_similar_text = 1 - (global_similar_text - 1) ** amplification  # 放大函数

            num = 0
            for i in cases:
                i.global_similar_text = round(100 * global_similar_text[num], 2)  # 圆整
                i.save()
                num = num + 1
            datalist_req = []
            datalist_rec = []
            datalist_unq = []
            datalist_out = []
            datalist_run = []
            datalist_fault = []
            datalist_exp = []
            search_datalist = Search.objects.filter(global_similar_text__gt=0).values('nid', 'classes')
            for item in search_datalist:
                if item['classes'] == 'req':
                    datalist_req.append(Require.objects.filter(id=item['nid']).values('ID',
                                                                                      'customer',
                                                                                      'product_type',
                                                                                      'product_code',
                                                                                      'place',
                                                                                      'condition',
                                                                                      'nandian',
                                                                                      'attention'))
                elif item['classes'] == 'rec':
                    datalist_rec.append(ManReceive.objects.filter(id=item['nid']).values('ID',
                                                                                         'problem',
                                                                                         'solution',
                                                                                         'banzu',
                                                                                         'diaodu',
                                                                                         'yanshouren'
                                                                                         ))
                elif item['classes'] == 'unq':
                    datalist_unq.append(ManUnqual.objects.filter(id=item['nid']).values('ID',
                                                                                        'type',
                                                                                        'problem',
                                                                                        'pro_detail',
                                                                                        'chuzhi',
                                                                                        'result',
                                                                                        'defect_text'
                                                                                        ))
                elif item['classes'] == 'out':
                    datalist_out.append(ManOuter.objects.filter(nid=item['nid']).values('ID',
                                                                                        'problem',
                                                                                        'institution',
                                                                                        'charger',
                                                                                        'note'
                                                                                        ))
                elif item['classes'] == 'run':
                    datalist_run.append(RunRecord.objects.filter(nid=item['nid']).values('ID',
                                                                                         'equipment',
                                                                                         'charger',
                                                                                         "note"
                                                                                         ))
                elif item['classes'] == 'fault':
                    datalist_fault.append(Fault.objects.filter(nid=item['nid']).values('ID',
                                                                                       'problem',
                                                                                       'charger',
                                                                                       'reportperson'
                                                                                       ))
                elif item['classes'] == 'exp':
                    datalist_exp.append(Test.objects.filter(nid=item['nid']).values('ID',
                                                                                    'detail',
                                                                                    'conclusion'
                                                                                    ))
            data_list["req"] = datalist_req
            data_list["rec"] = datalist_rec
            data_list["unq"] = datalist_unq
            data_list["out"] = datalist_out
            data_list["run"] = datalist_run
            data_list["fault"] = datalist_fault
            data_list["exp"] = datalist_exp

        elif key_word == None and key_word_exact != None and key_word_exact != '':
            search_way = 'exact'
            if date != '全部数据':
                now = datetime.datetime.now()
                if date == '本周内':
                    days = 7
                elif date == '本月内':
                    days = 31
                else:
                    days = 365
                delta = datetime.timedelta(days=days)
                n_days = now - delta
                begin_date = n_days.strftime('%Y-%m-%d')
                end_date = str(datetime.datetime.now())[:10]
            else:
                begin_date = '2014-01-01'  # 拿到最早的日期
                end_date = str(datetime.datetime.now())[:10]  # 拿到现在的日期

            if charger == '暂无':
                datalist_req = Require.objects.filter(
                    Q(customer__contains=key_word_exact) |
                    Q(product_type__contains=key_word_exact) |
                    Q(product_code__contains=key_word_exact) |
                    Q(place__contains=key_word_exact) |
                    Q(condition__contains=key_word_exact) |
                    Q(nandian__contains=key_word_exact) |
                    Q(attention__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
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
                    Q(yanshouren__contains=key_word_exact) |
                    Q(part__contains=key_word_exact) |
                    Q(problem__contains=key_word_exact) |
                    Q(solution__contains=key_word_exact) |
                    Q(banzu__contains=key_word_exact) |
                    Q(diaodu__contains=key_word_exact) |
                    Q(laiyuan__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
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
                    Q(inform__contains=key_word_exact) |
                    Q(type__contains=key_word_exact) |
                    Q(result__contains=key_word_exact) |
                    Q(pro_detail__contains=key_word_exact) |
                    Q(chuzhi__contains=key_word_exact) |
                    Q(defect_text__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
                    'ID',
                    'date',
                    'inform',
                    'type',
                    'fac',
                    'problem',
                    'pro_detail',
                    'chuzhi',
                    'gongying',
                    'result',
                    'defect_text',
                )

                datalist_out = ManOuter.objects.filter(

                    Q(problem__contains=key_word_exact) |
                    Q(institution__contains=key_word_exact) |
                    Q(charger__contains=key_word_exact) |
                    Q(note__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
                    'nid',
                    'date',
                    'problem',
                    'institution',
                    'charger',
                    'completion',
                    'note'
                )

                datalist_run = RunRecord.objects.filter(

                    Q(charger__contains=key_word_exact) |
                    Q(equipment__contains=key_word_exact) |
                    Q(circuit__contains=key_word_exact) |
                    Q(screw__contains=key_word_exact) |
                    Q(deformation__contains=key_word_exact) |
                    Q(note__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
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

                    Q(problem__contains=key_word_exact) |
                    Q(charger__contains=key_word_exact) |
                    Q(reportperson__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
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

                    Q(charger__contains=key_word_exact) |
                    Q(equipment__contains=key_word_exact) |
                    Q(detail__contains=key_word_exact) |
                    Q(conclusion__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
                    'ID',
                    'nid',
                    'date',
                    'equipment',
                    'charger',
                    'detail',
                    'conclusion'
                )
            else:
                datalist_req = Require.objects.filter(
                    Q(customer__contains=key_word_exact) |
                    Q(product_type__contains=key_word_exact) |
                    Q(product_code__contains=key_word_exact) |
                    Q(place__contains=key_word_exact) |
                    Q(condition__contains=key_word_exact) |
                    Q(nandian__contains=key_word_exact) |
                    Q(attention__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
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
                    Q(yanshouren__contains=key_word_exact) |
                    Q(part__contains=key_word_exact) |
                    Q(problem__contains=key_word_exact) |
                    Q(solution__contains=key_word_exact) |
                    Q(banzu__contains=charger) |
                    Q(diaodu__contains=charger) |
                    Q(laiyuan__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
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
                    Q(inform__contains=key_word_exact) |
                    Q(type__contains=key_word_exact) |
                    Q(result__contains=key_word_exact) |
                    Q(pro_detail__contains=key_word_exact) |
                    Q(chuzhi__contains=key_word_exact) |
                    Q(defect_text__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).values(
                    'ID',
                    'date',
                    'inform',
                    'type',
                    'fac',
                    'problem',
                    'pro_detail',
                    'chuzhi',
                    'gongying',
                    'result',
                    'defect_text',
                )

                datalist_out = ManOuter.objects.filter(
                    Q(problem__contains=key_word_exact) |
                    Q(institution__contains=key_word_exact) |
                    Q(note__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).filter(charger=charger).values(
                    'nid',
                    'date',
                    'problem',
                    'institution',
                    'charger',
                    'completion',
                    'note'
                )

                datalist_run = RunRecord.objects.filter(
                    Q(equipment__contains=key_word_exact) |
                    Q(circuit__contains=key_word_exact) |
                    Q(screw__contains=key_word_exact) |
                    Q(deformation__contains=key_word_exact) |
                    Q(note__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).filter(charger=charger).values(
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
                    Q(problem__contains=key_word_exact) |
                    Q(reportperson__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).filter(charger=charger).values(
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

                    Q(equipment__contains=key_word_exact) |
                    Q(detail__contains=key_word_exact) |
                    Q(conclusion__contains=key_word_exact)
                ).filter(date__range=(begin_date, end_date)).filter(charger=charger).values(
                    'ID',
                    'nid',
                    'date',
                    'equipment',
                    'charger',
                    'detail',
                    'conclusion'
                )

            if req == '1':
                data_list["req"] = datalist_req
            if man == '1':
                data_list["rec"] = datalist_rec
                data_list["unq"] = datalist_unq
                data_list["out"] = datalist_out
            if mtn == '1':
                data_list["run"] = datalist_run
                data_list["fault"] = datalist_fault
            if exp == '1':
                data_list["exp"] = datalist_exp
        else:
            search_way = 'None'
        return render(request, 'search.html', {"data_list": data_list, 'search_way': search_way})
