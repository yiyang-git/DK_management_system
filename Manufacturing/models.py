from django.db import models


# Create your models here.
class ManReceive(models.Model):
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
    date = models.CharField(max_length=32, null=True)
    inform = models.CharField(max_length=32, null=True)
    type = models.CharField(max_length=32, null=True)
    fac = models.CharField(max_length=32, null=True)
    found_date = models.CharField(max_length=32, null=True)
    creat_date = models.CharField(max_length=32, null=True)
    chuzhi = models.CharField(max_length=32, null=True)
    gongying = models.CharField(max_length=32, null=True)
    result = models.CharField(max_length=32, null=True)
    defect_text = models.CharField(max_length=32, null=True)
    problem = models.TextField(null=True, default='')
    pro_detail = models.TextField(null=True, default='')
    chuzhi = models.TextField(null=True, default='')
