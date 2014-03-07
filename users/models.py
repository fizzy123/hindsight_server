from django.db import models
from django.contrib.auth.models import User

class HindsightUser(models.Model):
    user = models.OneToOneField(User, primary_key= True)
    key = models.CharField(max_length=200, blank = True, null = True)
    follows = models.ManyToManyField("self", related_name="followers", related_query_name="follower", blank=True, null=True, symmetrical=False)
