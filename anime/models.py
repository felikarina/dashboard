from django.db import models
from django.utils import timezone

class Manga(models.Model):
    title2 = models.CharField(max_length=100)
    image_url2 = models.URLField()
    synopsis2 = models.CharField(max_length=400)
    
    def __str__(self):
        return self.title2
    
class Anime(models.Model):
    title = models.CharField(max_length=100)
    image_url = models.URLField()
    synopsis = models.CharField(max_length=400)
    
    def __str__(self):
        return self.title
    
class Visit(models.Model):
    counter = models.PositiveIntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Visit {self.pk}"