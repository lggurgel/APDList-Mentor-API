import pytest

from rest_framework.test import APIClient


@pytest.fixture
def not_authenticated_user():
    return APIClient()
