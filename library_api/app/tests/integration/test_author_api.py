import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from app.models import Author
from app.serializers import AuthorSerializer
from app.tests.factories import AuthorFactory


class AuthorTestHelperMixin:
    def get_serialized_author(self, author: Author):
        return AuthorSerializer(author).data

    def assert_equal_author_jsons(self, first: dict, second: dict):
        assert first['name'] == second['name']
        assert first['surname'] == second['surname']


class TestAuthorListAPI(AuthorTestHelperMixin):
    url = reverse('app:author_list_create')

    @pytest.mark.django_db
    def test_status_should_be_ok(self, client: Client):
        response = client.get(self.url)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_should_return_all_authors(self, client: Client):
        authors = AuthorFactory.create_many()

        response = client.get(self.url)
        body = response.json()

        for i in range(len(body)):
            self.assert_equal_author_jsons(body[i],
                                           self.get_serialized_author(authors[i]))


class TestAuthorCreateAPI(AuthorTestHelperMixin):
    url = reverse('app:author_list_create')

    @pytest.mark.django_db
    def test_should_return_unauthorized_if_credentials_incorrect(self, client: Client):
        data = self.get_serialized_author(AuthorFactory.build())

        response = client.post(self.url,
                               data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION='Token incorrect credentials')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_should_return_forbidden_if_user_is_not_staff(self, non_staff_user_token: str, client: Client):
        data = self.get_serialized_author(AuthorFactory.build())

        response = client.post(self.url,
                               data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {non_staff_user_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_should_create_author(self, staff_user_token: str, client: Client):
        data = self.get_serialized_author(AuthorFactory.build())

        response = client.post(self.url,
                               data=data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {staff_user_token}')
        body = response.json()

        Author.objects.get(id=body['id'])

    @pytest.mark.django_db
    def test_should_response_with_created_status_on_success(self, staff_user_token: str, client: Client):
        data = self.get_serialized_author(AuthorFactory.build())

        response = client.post(self.url,
                               data=data,
                               content_type='application/json',
                               HTTP_AUTHORIZATION=f'Token {staff_user_token}')

        assert response.status_code == status.HTTP_201_CREATED


class TestAuthorRetrieveAPI(AuthorTestHelperMixin):
    url_name = 'app:author_retrieve_update_delete'

    @pytest.mark.django_db
    def test_should_return_not_found_if_author_does_not_exist_with_given_pk(self, client: Client):
        does_not_exist_author_id = 12345678
        url = reverse(self.url_name, args=[does_not_exist_author_id])

        response = client.get(url)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_should_response_with_status_ok_on_success(self, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])

        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_should_retrieve_author(self, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])

        response = client.get(url)
        body = response.json()

        self.assert_equal_author_jsons(body,
                                       self.get_serialized_author(author))


class TestAuthorUpdateAPI(AuthorTestHelperMixin):
    url_name = 'app:author_retrieve_update_delete'

    @pytest.mark.django_db
    def test_should_return_unauthorized_if_credentials_is_incorrect(self, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])
        new_data = self.get_serialized_author(AuthorFactory.build())

        response = client.put(url,
                              new_data,
                              content_type='application/json',
                              HTTP_AUTHORIZATION='Token incorrect_credentials')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_should_return_forbidden_if_user_is_not_staff(self, non_staff_user_token: str, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])
        new_data = self.get_serialized_author(AuthorFactory.build())

        response = client.put(url,
                              new_data,
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Token {non_staff_user_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_should_return_not_found_if_author_does_not_exist_with_given_pk(self,
                                                                            staff_user_token: str,
                                                                            client: Client):
        does_not_exist_author_id = 12345678
        url = reverse(self.url_name, args=[does_not_exist_author_id])
        new_data = self.get_serialized_author(AuthorFactory.build())

        response = client.put(url,
                              new_data,
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Token {staff_user_token}')

        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_should_update_author(self, staff_user_token: str, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])
        new_data = self.get_serialized_author(AuthorFactory.build())

        response = client.put(url,
                              new_data,
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Token {staff_user_token}')
        body = response.json()

        Author.objects.get(id=body['id'], name=body['name'], surname=body['surname'])

    @pytest.mark.django_db
    def test_should_response_with_status_ok_on_success(self, staff_user_token: str, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])
        new_data = self.get_serialized_author(AuthorFactory.build())

        response = client.put(url,
                              new_data,
                              content_type='application/json',
                              HTTP_AUTHORIZATION=f'Token {staff_user_token}')

        assert response.status_code == status.HTTP_200_OK


class TestAuthorDeleteAPI(AuthorTestHelperMixin):
    url_name = 'app:author_retrieve_update_delete'

    @pytest.mark.django_db
    def test_should_return_unauthorized_if_credentials_is_incorrect(self, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])

        response = client.delete(url,
                                 HTTP_AUTHORIZATION='Token incorrect_credentials')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_should_return_forbidden_if_user_is_not_staff(self, non_staff_user_token: str, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])

        response = client.delete(url,
                                 HTTP_AUTHORIZATION=f'Token {non_staff_user_token}')

        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_should_delete_author_by_pk(self, staff_user_token: str, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])

        client.delete(url, HTTP_AUTHORIZATION=f'Token {staff_user_token}')

        with pytest.raises(Author.DoesNotExist):
            Author.objects.get(pk=author.pk)

    @pytest.mark.django_db
    def test_should_response_with_status_no_content(self, staff_user_token: str, client: Client):
        author = AuthorFactory()
        url = reverse(self.url_name, args=[author.pk])

        response = client.delete(url, HTTP_AUTHORIZATION=f'Token {staff_user_token}')

        assert response.status_code == status.HTTP_204_NO_CONTENT
