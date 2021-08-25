from django.db import models


# Create your models here.
class Knowledge(models.Model):
    classes = models.CharField(max_length=64, null=True)
    process = models.CharField(max_length=64, null=True)
    relation = models.CharField(max_length=64, null=True)
    standard = models.CharField(max_length=64, null=True)
