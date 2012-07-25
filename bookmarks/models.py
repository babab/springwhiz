from django.db import models
from django.contrib.auth.models import User

class Bookmark(models.Model):
    user = models.ForeignKey(User, unique=True)
    label = models.CharField(max_length=60)
    url = models.URLField()
