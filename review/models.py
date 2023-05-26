from django.db import models
# from user.models import User 

# Create your models here.
class Alcohol_Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=40)
    content = models.TextField()
    # image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)
    

class Brewery_Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=40)
    content = models.TextField()
    # image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)
    

class Event_Review(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    # title = models.CharField(max_length=40)
    content = models.TextField()
    # image = models.ImageField(blank=True, upload_to='%Y/%m/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.content)