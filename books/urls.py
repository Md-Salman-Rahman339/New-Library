from django.urls import path
from .views import book_view, DetailsPost, BorrowBookView, return_book

urlpatterns = [
    path('book/', book_view, name='book_list'),
    path('category/<slug:category_slug>/', book_view, name='category_wise_post'),
    path('details/<int:pk>/', DetailsPost.as_view(), name="details_view"),
    path('borrow_book/<int:book_id>/', BorrowBookView.as_view(), name='borrow_book'),
    path('return_book/<int:book_id>/', return_book, name='return_book'), 
]
