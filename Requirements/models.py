from django.db import models


# Create your models here.
class Require(models.Model):
    customer = models.CharField(max_length=32, null=True)
    product_type = models.CharField(max_length=32, null=True)
    product_code = models.CharField(max_length=32, null=True)
    date = models.CharField(max_length=32, null=True)
    place = models.CharField(max_length=32, null=True)
    condition = models.TextField(null=True, default='')
    nandian = models.TextField(null=True, default='')
    attention = models.TextField(null=True, default='')
    inputfile = models.CharField(max_length=32, null=True)
