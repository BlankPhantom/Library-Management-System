from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, BorrowTransaction

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class BorrowTransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    book = serializers.StringRelatedField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), source='user', write_only=True
    )
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(), source='book', write_only=True
    )

    class Meta:
        model = BorrowTransaction
        fields = ['id', 'user', 'user_id', 'book', 'book_id', 'borrow_date', 'return_date', 'status']
