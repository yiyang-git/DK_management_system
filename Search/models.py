from django.db import models

# Create your models here.
class Search(models.Model):
    # id = models.IntegerField()
    nid = models.IntegerField()
    classes = models.CharField(max_length=16, null=True)
    document = models.CharField(max_length=512, null=True)
    global_similar_text = models.CharField(max_length=16, null=True)
    similar = models.IntegerField(null=True)
