from django.urls import path
from . import views

urlpatterns = [
    # Book ViewSet (still uses .as_view since it's a ViewSet)
    path('books/', views.BookViewSet.as_view({
        'get': 'list',
        'post': 'create',
    }), name='book-list'),

    path('books/<int:pk>/', views.BookViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    }), name='book-detail'),

    # Borrow/Return/Transactions using function-based views
    path('borrow/', views.borrow_book, name='borrow-book'),
    path('return/<int:borrow_id>/', views.return_book, name='return-book'),
    path('transactions/', views.transaction_list, name='transaction-list'),
]
