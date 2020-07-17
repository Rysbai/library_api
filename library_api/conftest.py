import pytest
from rest_framework.authtoken.models import Token

from app.tests.factories import UserFactory


@pytest.fixture(scope='function')
def non_staff_user_token():
    user = UserFactory(is_staff=False)
    token, _ = Token.objects.get_or_create(user=user)

    return token


@pytest.fixture(scope='function')
def staff_user_token():
    user = UserFactory(is_staff=True)
    token, _ = Token.objects.get_or_create(user=user)

    return token
