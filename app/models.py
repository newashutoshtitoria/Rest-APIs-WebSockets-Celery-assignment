from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='image/%Y/%m/%d/', max_length=300)
    like = models.ManyToManyField(User, related_name='likes', blank=True)

    def __str__(self):
        return self.name
