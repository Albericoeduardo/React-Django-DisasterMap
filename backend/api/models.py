from django.db import models

class Category(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

    def __str__(self):
        return f"{self.longitude} - {self.latitude}"

class Event(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    date = models.DateTimeField()
    country = models.CharField(max_length=255, null=True, blank=True)
    link = models.URLField(null=True, blank=True)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='events')
    sources = models.JSONField(null=True, blank=True)
    geometry = models.JSONField(null=True, blank=True)
    
    def __str__(self):
        return self.title