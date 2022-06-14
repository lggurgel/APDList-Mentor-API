from rest_framework.reverse import reverse
from rest_framework import status


def test_onboarding_mentor_view_set_not_authenticated(not_authenticated_user):
    url = reverse("onboarding-mentor")
    response = not_authenticated_user.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
