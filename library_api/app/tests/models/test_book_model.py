from app.models import Book
from app.tests.base import AbstractModelTest, AbstractModelManagerTest
from app.tests.factories import BookFactory, AuthorFactory


class TestBookModel(AbstractModelTest):
    model = Book
    factory = BookFactory

    def get_test_unsaved_instance(self):
        author = AuthorFactory()
        return self.factory.build(author=author)

    def test_str_method(self):
        book = self.factory.build()

        assert book.__str__() == book.name


class TestBookModelManager(AbstractModelManagerTest):
    model = Book
    factory = BookFactory

    def generate_model_kwargs(self) -> dict:
        author = AuthorFactory()
        book = self.factory.build()

        return {
            "author_id": author.id,
            "name": book.name
        }
