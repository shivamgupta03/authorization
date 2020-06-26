# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Credential(models.Model):
    state_token = models.CharField(max_length=512)
    access_token = models.CharField(max_length=512)
    refresh_token = models.CharField(max_length=512)
    expires = models.DateTimeField(null=True)
    authorization_code = models.CharField(max_length=30)

class GoogleUser(models.Model):
    credential = models.ForeignKey(Credential)
