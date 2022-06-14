import pytest
from datetime import datetime, timedelta

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from tests.api.factories import UserFactory, MentorshipAreaFactory


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


@pytest.fixture
def onboarding_member(authenticated_user):
    return {
        "user": authenticated_user.id,
        "latitude": -15.7792,
        "longitude": -47.9341,
        "employer": "Sr Company",
        "title": "Jr Developer",
        "expertise": ["UI_UX", "PRODUCT"],
    }


@pytest.fixture
def onboarding_mentor(authenticated_user):

    mentorships = [
        MentorshipAreaFactory(title="Career Advice"),
        MentorshipAreaFactory(title="Portfolio Review"),
        MentorshipAreaFactory(title="Interview Techniques"),
    ]

    availability = [
        str(datetime.now() + timedelta(days=days)) for days in range(1, 12, 4)
    ]

    return {
        "user": authenticated_user.id,
        "latitude": -15.7792,
        "longitude": -47.9341,
        "employer": "Sr Company",
        "title": "Sr Developer",
        "expertise": ["AI"],
        "mentorship": [mentorship.id for mentorship in mentorships],
        "availability": availability,
        "status": "PENDING",
    }
