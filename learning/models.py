from django.db import models

# Create your models here.


class Movies(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField('description')
    rating = models.IntegerField(default=0)
    producer = models.CharField(max_length=100)
    public_id = models.CharField(max_length=300)

    def __str__(self):
        return self.title
