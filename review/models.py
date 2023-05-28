from django.db import models
from user.models import User
from alchol.models import Alchol
from brewery.models import Brewery
from information.models import Event

class Alcohol_Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    alchol = models.ForeignKey(Alchol, on_delete=models.CASCADE, related_name='alchol_review')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.content)
    
class Brewery_Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    brewery = models.ForeignKey(Brewery, on_delete=models.CASCADE, related_name='brewery_review')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)
    
class Event_Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    information = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='event_review')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)