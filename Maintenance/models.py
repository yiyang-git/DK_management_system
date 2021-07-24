from django.db import models


# Create your models here.
class RunRecord(models.Model):
    ID = models.IntegerField(null=True)
    nid = models.IntegerField()
    date = models.CharField(max_length=16, null=True)
    equipment = models.CharField(max_length=16, null=True)
    charger = models.CharField(max_length=16, null=True)
    circuit = models.CharField(max_length=16, null=True)
    screw = models.CharField(max_length=16, null=True)
    deformation = models.CharField(max_length=16, null=True)
    work = models.CharField(max_length=16, null=True)
    all = models.CharField(max_length=16, null=True)
    note = models.TextField(null=True, default='')


class Fault(models.Model):
    ID = models.IntegerField(null=True)
    nid = models.IntegerField()
    date = models.CharField(max_length=16, null=True)
    problem = models.TextField(null=True, default='')
    charger = models.CharField(max_length=16, null=True)
    reportperson = models.CharField(max_length=16, null=True)
    completion = models.CharField(max_length=16, null=True)
    risk_level = models.CharField(max_length=16, null=True)
