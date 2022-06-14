import pytest

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.api.factories import UserFactory


@pytest.fixture
def not_authenticated_user():
    return APIClient()


@pytest.fixture
def authenticated_user():
    return UserFactory()


@pytest.fixture
def client_api(authenticated_user):
    client = APIClient()
    token = Token.objects.create(user=authenticated_user)
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client
