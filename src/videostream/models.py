from django.db import models

class Videostream(models.Model):
    title = models.CharField(max_length=100)