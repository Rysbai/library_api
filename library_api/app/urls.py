from django.urls import path

from app.views import AuthorListCreateAPIView, AuthorRetrieveUpdateDeleteAPIView, BookListCreateAPIView, \
    BookRetrieveUpdateDeleteAPIView

app_name = 'app'

urlpatterns = [
    path('authors', AuthorListCreateAPIView.as_view(), name='author_list_create'),
    path('authors/<int:pk>', AuthorRetrieveUpdateDeleteAPIView.as_view(), name='author_retrieve_update_delete'),
    path('books', BookListCreateAPIView.as_view(), name='book_list_create'),
    path('books/<int:pk>', BookRetrieveUpdateDeleteAPIView.as_view(), name='book_retrieve_update_delete')
]
