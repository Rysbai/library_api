from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser

from app.models import Author, Book
from app.serializers import AuthorSerializer, BookSerializer


class AuthorListCreateAPIView(ListCreateAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]

        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]


class AuthorRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = AuthorSerializer
    queryset = Author.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]

        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]


class BookListCreateAPIView(ListCreateAPIView):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]

        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]


class BookRetrieveUpdateDeleteAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.request.method == 'GET':
            permission_classes = [AllowAny, ]

        else:
            permission_classes = [IsAuthenticated, IsAdminUser]

        return [permission() for permission in permission_classes]

