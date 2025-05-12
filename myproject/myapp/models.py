from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    copies_available = models.IntegerField()
    isbn_number = models.CharField(max_length=13, unique=True)

    def __str__(self):
        return self.title
    
class BorrowTransaction(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='borrowed')

    def __str__(self):
        return f"{self.user} - {self.book.title} ({self.status})"