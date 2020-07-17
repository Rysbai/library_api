from app.tests.base import AbstractModelSerializerTest
from app.models import Author
from app.serializers import AuthorSerializer
from app.tests.factories import AuthorFactory


class TestAuthorSerializer(AbstractModelSerializerTest):
    model = Author
    factory = AuthorFactory
    serializer_class = AuthorSerializer

    def generate_parsable_data(self) -> dict:
        author = AuthorFactory.build()

        return {
            "name": author.name,
            "surname": author.surname
        }
