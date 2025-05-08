from django.db import models

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    copies_available = models.IntegerField()
    isbn_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title