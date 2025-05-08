from django.urls import path
from . import views

urlpatterns = [
    path('books/', views.BookViewSet.as_view({
        'get': 'list',
        'post': 'create',
        }), name='book-list'),
    path('books/<int:pk>/', views.BookViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
        }), name='book-list-id'),
]