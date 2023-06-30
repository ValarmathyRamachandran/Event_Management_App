from django.db import models

class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField()
    time = models.CharField()
    location = models.CharField(max_length=255)
    online = models.BooleanField(default=False)

    def __str__(self):
        return self.title
