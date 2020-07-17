import pytest

from app.tests.base import AbstractModelTest, AbstractModelManagerTest
from app.models import Author
from app.tests.factories import AuthorFactory


class TestAuthorModel(AbstractModelTest):
    model = Author
    factory = AuthorFactory

    def test_str_method(self):
        author = self.factory.build()
        assert author.__str__() == f'{author.name} {author.surname}'


class TestAuthorModelManager(AbstractModelManagerTest):
    model = Author
    factory = AuthorFactory

    def generate_model_kwargs(self) -> dict:
        author = self.factory.build()
        return {
            "name": author.name,
            "surname": author.surname
        }
