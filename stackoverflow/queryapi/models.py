from django.db import models
from django.db.models import JSONField


# Create your models here.
class Question(models.Model):
    querystring = models.CharField(max_length=300)
    data = JSONField()

    def __str__(self):
        return self.querystring