import datetime
import factory
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from app.models import Author, Book


class LibraryAPIModelFactory(factory.django.DjangoModelFactory):
    @classmethod
    def create_many(cls, count=4, **kwargs):
        return [cls(**kwargs) for _ in range(count)]


class UserFactory(LibraryAPIModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'example_username{0}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    email = factory.Sequence(lambda n: 'example{0}@email.com'.format(n))

    first_name = 'Example first name'
    last_name = 'Example last name'
    is_superuser = False
    is_staff = False
    is_active = True


@factory.django.mute_signals(post_save)
class AuthorFactory(LibraryAPIModelFactory):
    class Meta:
        model = Author

    name = 'test_name'
    surname = 'test_surname'


@factory.django.mute_signals(post_save)
class BookFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Book

    author = factory.SubFactory(AuthorFactory)
    name = 'Test Book Name'
