from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils.timezone import now
from .models import Book, BorrowTransaction
from .serializers import BookSerializer, BorrowTransactionSerializer
from django.shortcuts import get_object_or_404

# Create your views here.
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def destroy(self, request, *args, **kwargs):
        book = self.get_object()
        active_borrowers = BorrowTransaction.objects.filter(book=book, status='borrowed').exists()
        
        if active_borrowers:
            return Response(
                {'error': f'Cannot delete "{book.title}" because it is still borrowed.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)

# View all Borrow Transactions
@api_view(['GET'])
def transaction_list(request):
    transactions = BorrowTransaction.objects.all().order_by('-borrow_date')
    serializer = BorrowTransactionSerializer(transactions, many=True)
    return Response(serializer.data)


# Borrow a Book
@api_view(['POST'])
def borrow_book(request):
    book_id = request.data.get('book_id')
    user = request.data.get('user')

    book = get_object_or_404(Book, id=book_id)

    if book.copies_available < 1:
        return Response({'error': 'No copies available'}, status=status.HTTP_400_BAD_REQUEST)

    book.copies_available -= 1
    book.save()

    transaction = BorrowTransaction.objects.create(book_id=book_id, user=user)
    serializer = BorrowTransactionSerializer(transaction)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


# Return a Book
@api_view(['POST'])
def return_book(request, borrow_id):
    try:
        transaction = BorrowTransaction.objects.get(id=borrow_id)
    except BorrowTransaction.DoesNotExist:
        return Response({'error': 'Transaction ID not found'}, status=status.HTTP_404_NOT_FOUND)

    if transaction.status == 'returned':
        return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

    # Process return
    transaction.status = 'returned'
    transaction.return_date = now()
    transaction.save()

    # Increment book copies
    book = transaction.book
    book.copies_available += 1
    book.save()

    serializer = BorrowTransactionSerializer(transaction)
    return Response(serializer.data)