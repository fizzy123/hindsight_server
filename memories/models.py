from django.db import models
from django.utils import timezone

from users.models import HindsightUser

class Memory(models.Model):
    owner = models.ForeignKey(HindsightUser)
    image = models.ImageField(upload_to='memories')
    latitude = models.FloatField()
    longitude = models.FloatField()
    caption = models.TextField(blank=True, null=True)
    created = models.DateField(auto_now_add=True)
