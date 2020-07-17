from app.models import Book
from app.serializers import BookSerializer
from app.tests.base import AbstractModelSerializerTest
from app.tests.factories import BookFactory, AuthorFactory


class TestBookSerializer(AbstractModelSerializerTest):
    model = Book
    factory = BookFactory
    serializer_class = BookSerializer

    def generate_parsable_data(self) -> dict:
        author = AuthorFactory()
        book = self.factory.build()

        return {
            'author': author.id,
            'name': book.name
        }
