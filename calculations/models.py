from django.contrib.postgres.fields import ArrayField
from django.db import models

class Calculations(models.Model):
    numbers      = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    calculations = ArrayField(models.IntegerField(null=True, blank=True), null=True, blank=True)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)
