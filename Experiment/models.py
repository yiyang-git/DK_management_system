from django.db import models


# Create your models here.
class Test(models.Model):
    ID = models.IntegerField()
    nid = models.IntegerField()
    date = models.CharField(max_length=16, null=True)
    equipment = models.CharField(max_length=16, null=True)
    charger = models.CharField(max_length=16, null=True)
    detail = models.TextField(null=True, default='')
    conclusion = models.TextField(null=True, default='')
