from django.db import models

# Create your models here.

class Category(models.Model):

    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category


class Azkar(models.Model):
    azkar = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    order = models.PositiveIntegerField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.azkar
