from datetime import time
from django.db import models

from accounts.models import User


class Event(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField()
    end_time = models.TimeField(default=time(hour=0, minute=0, second=0))
    location = models.CharField(max_length=255)
    online = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    max_seats = models.PositiveIntegerField(default=10)

    def __str__(self):
        return self.title
    

class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    is_cancelled =models.BooleanField(default=False)
    booked_at = models.DateTimeField(auto_now_add=True)  


    def __str__(self):
        return f"{self.user.username}'s ticket for {self.event.title}"
    

