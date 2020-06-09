from django.db import models

# Create your models here.

class Chuck(models.Model):
    joke = models.CharField(max_length=250)
    categories = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
