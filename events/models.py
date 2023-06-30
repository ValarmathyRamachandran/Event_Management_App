from datetime import time
from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    location = models.CharField(max_length=255)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.title
