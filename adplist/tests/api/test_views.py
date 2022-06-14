import pytest

from rest_framework.reverse import reverse
from rest_framework import status

from tests.api.factories import UserFactory, MentorFactory

pytestmark = pytest.mark.django_db


def test_get_mentor_none(client_api):
    url = reverse("mentor-list")
    response = client_api.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"count": 0, "previous": None, "results": [], "next": None}


def test_get_mentor_all(client_api):
    url = reverse("mentor-list")

    user_1 = UserFactory(username="User_1")
    user_2 = UserFactory(username="User_2")
    user_3 = UserFactory(username="User_3")

    MentorFactory(user=user_1)
    MentorFactory(user=user_2)
    MentorFactory(user=user_3)

    response = client_api.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


def test_onboarding_mentor_view_set_not_authenticated(not_authenticated_user):
    url = reverse("onboarding-mentor")
    response = not_authenticated_user.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
