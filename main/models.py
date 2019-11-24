from django.db import models
from django.contrib.postgres.fields import ArrayField
from uuid import uuid4



class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    vector = ArrayField(models.FloatField(), blank=True, null=True)


    def __str__(self):
        return self.last_name
