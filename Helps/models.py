from django.db import models


class Helps(models.Model):
    ID = models.IntegerField()
    nid = models.IntegerField()
    classes = models.CharField(max_length=16, null=True)
    problem = models.TextField(null=True, default='')
    answer = models.TextField(null=True, default='')
    completion = models.CharField(max_length=16, null=True)


class Suggest(models.Model):
    ID = models.IntegerField()
    nid = models.IntegerField()
    suggest = models.TextField(null=True, default='')
    completion = models.CharField(max_length=16, null=True)
