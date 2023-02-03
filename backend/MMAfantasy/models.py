from django.db import models



class fighter(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    record = models.CharField(max_length=100)
    weight_class = models.CharField(max_length=100)
