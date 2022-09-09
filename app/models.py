from django.db import models

# Create your models here.

class data(models.Model):
    full_name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    age = models.CharField(max_length=200)
    height = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)
    height_diff = models.IntegerField(default=0)
    weight_diff = models.IntegerField(default=0)
    attributes = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    video = models.CharField(max_length=200)
    foot = models.CharField(max_length=200)

class user_data(models.Model):
    age = models.CharField(max_length=200)
    male_height = models.IntegerField(default=0)
    male_weight = models.IntegerField(default=0)
    female_height = models.IntegerField(default=0)
    female_weight = models.IntegerField(default=0) 