from django.db import models
from django import forms


# Create your models here.


class Joke(models.Model):
    category = models.CharField(max_length=255)
    joke_type = models.CharField(max_length=50)  
    setup = models.TextField(null=True, blank=True)  
    delivery = models.TextField(null=True, blank=True)  
    joke_text = models.TextField(null=True, blank=True)  
    nsfw = models.BooleanField(default=False)
    political = models.BooleanField(default=False)
    sexist = models.BooleanField(default=False)
    safe = models.BooleanField(default=False)
    lang = models.CharField(max_length=10)




