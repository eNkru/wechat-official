from django.db import models


class Mode(models.Model):
    user = models.CharField(max_length=250)
    mode = models.CharField(max_length=50)
