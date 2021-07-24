from django.db import models


# Create your models here.
class ManReceive(models.Model):
    ID = models.IntegerField()
    date = models.CharField(max_length=16, null=True)
    worker = models.CharField(max_length=16, null=True)
    problem = models.TextField(null=True, default='')
    solution = models.TextField(null=True, default='')
    banzu = models.CharField(max_length=16, null=True)
    diaodu = models.CharField(max_length=16, null=True)
    laiyuan = models.CharField(max_length=16, null=True)
    yanshouren = models.CharField(max_length=16, null=True)
    wancheng = models.CharField(max_length=16, null=True)


class ManUnqual(models.Model):
    ID = models.IntegerField()
    date = models.CharField(max_length=16, null=True)
    inform = models.CharField(max_length=16, null=True)
    type = models.CharField(max_length=16, null=True)
    fac = models.CharField(max_length=16, null=True)
    found_date = models.CharField(max_length=16, null=True)
    creat_date = models.CharField(max_length=16, null=True)
    gongying = models.CharField(max_length=16, null=True)
    result = models.CharField(max_length=16, null=True)
    defect_text = models.CharField(max_length=16, null=True)
    problem = models.TextField(null=True, default='')
    pro_detail = models.TextField(null=True, default='')
    chuzhi = models.TextField(null=True, default='')


class ManOuter(models.Model):
    ID = models.IntegerField(null=True)
    nid = models.IntegerField()
    problem = models.TextField(null=True, default='')
    institution = models.CharField(max_length=16, null=True)
    charger = models.CharField(max_length=16, null=True)
    completion = models.CharField(max_length=16, null=True)
    note = models.TextField(null=True, default='')
