import pytest

from rest_framework.reverse import reverse
from rest_framework import status

from tests.api.factories import UserFactory, MentorFactory, MemberFactory

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


@pytest.mark.parametrize(
    "params, response_count",
    [
        ({"status": "APPROVED"}, 2),
        ({"status": "PENDING"}, 1),
        ({}, 3),
    ],
    ids=["Approved", "Pending", "Without params"],
)
def test_get_mentor_viewset_list_filtered_by_status(client_api, params, response_count):
    url = reverse("mentor-list")

    user_1 = UserFactory(username="User_1")
    user_2 = UserFactory(username="User_2")
    user_3 = UserFactory(username="User_3")

    MentorFactory(user=user_1)
    MentorFactory(user=user_2, status="APPROVED")
    MentorFactory(user=user_3, status="APPROVED")

    response = client_api.get(url, params)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == response_count


def test_mentor_viewset_list_filtered_by_invalid_status(client_api):
    url = reverse("mentor-list")
    response = client_api.get(url, {"status": "fake_status"})
    assert response.json() == {
        "status": [
            "Select a valid choice. fake_status is not one of the available choices."
        ]
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    "params, response_count",
    [
        ({"expertise": "UI_UX"}, 2),
        ({"expertise": "PRODUCT"}, 0),
        ({}, 3),
    ],
    ids=["UI_UX", "PRODUCT", "Without params"],
)
def test_get_member_viewset_list_filtered_by_expertise(
    client_api, params, response_count
):
    url = reverse("member-list")

    user_1 = UserFactory(username="User_1")
    user_2 = UserFactory(username="User_2")
    user_3 = UserFactory(username="User_3")

    MemberFactory(user=user_1)
    MemberFactory(user=user_2, expertise=["UI_UX"])
    MemberFactory(user=user_3, expertise=["UI_UX"])

    response = client_api.get(url, params)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == response_count


def test_member_viewset_list_filtered_by_invalid_expertise(client_api):
    url = reverse("member-list")
    response = client_api.get(url, {"expertise": "fake_expertise"})
    assert response.json() == {
        "expertise": [
            "Select a valid choice. fake_expertise is not one of the available choices."
        ]
    }
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_get_member_none(client_api):
    url = reverse("member-list")
    response = client_api.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"count": 0, "previous": None, "results": [], "next": None}


def test_get_member_all(client_api):
    url = reverse("member-list")

    user_1 = UserFactory(username="User_1")
    user_2 = UserFactory(username="User_2")
    user_3 = UserFactory(username="User_3")

    MemberFactory(user=user_1)
    MemberFactory(user=user_2)
    MemberFactory(user=user_3)

    response = client_api.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 3


@pytest.mark.parametrize(
    "endpoint", ["mentor-list", "member-list", "onboarding-mentor", "onboarding-member"]
)
def test_views_not_authenticated(not_authenticated_user, endpoint):
    url = reverse(endpoint)
    response = not_authenticated_user.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_member_onboarding_success(client_api, onboarding_member):
    onboarding_url = reverse("onboarding-member")

    client_api.post(onboarding_url, onboarding_member)

    member_url = reverse("member-list")

    response = client_api.get(member_url)

    assert response.status_code == status.HTTP_200_OK
    assert [field in response.json()["results"][0] for field in onboarding_member]


def test_mentor_onboarding_success(client_api, onboarding_mentor):
    onboarding_url = reverse("onboarding-mentor")

    client_api.post(onboarding_url, onboarding_mentor)

    mentor_url = reverse("mentor-list")

    response = client_api.get(mentor_url)

    assert response.status_code == status.HTTP_200_OK
    assert [field in response.json()["results"][0] for field in onboarding_mentor]


def test_member_update_other_profile_failure(client_member_api):
    user = UserFactory(username="user")
    MentorFactory(user=user)

    url = reverse("user-detail", kwargs={"pk": user.id})

    respose_get = client_member_api.get(url)
    response_patch = client_member_api.patch(url, {"title": "Mid Level"})

    assert respose_get.status_code == status.HTTP_200_OK
    assert response_patch.status_code == status.HTTP_403_FORBIDDEN
    assert response_patch.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_mentor_update_other_profile_failure(client_mentor_api):
    user = UserFactory(username="user")
    MemberFactory(user=user)

    url = reverse("user-detail", kwargs={"pk": user.id})

    respose_get = client_mentor_api.get(url)
    response_patch = client_mentor_api.patch(url, {"title": "Mid Level"})

    assert respose_get.status_code == status.HTTP_200_OK
    assert response_patch.status_code == status.HTTP_403_FORBIDDEN
    assert response_patch.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_mentor_approval_not_allowed(client_mentor_api):
    url = reverse("mentor-approve")

    response = client_mentor_api.get(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You do not have permission to perform this action."
    }


def test_mentor_approval_allowed(client_admin_api):
    url = reverse("mentor-approve")

    user_1 = UserFactory(username="User_1")
    user_2 = UserFactory(username="User_2")
    user_3 = UserFactory(username="User_3")

    MentorFactory(user=user_1, status="APPROVED")
    MentorFactory(user=user_2)
    MentorFactory(user=user_3)

    response = client_admin_api.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["count"] == 2


def test_mentor_approval_success(client_admin_api):
    url = reverse("mentor-approve")

    user_1 = UserFactory(username="User_1")
    user_2 = UserFactory(username="User_2")
    user_3 = UserFactory(username="User_3")

    MentorFactory(user=user_1, status="APPROVED")

    mentors_pending = [MentorFactory(user=user_2), MentorFactory(user=user_3)]

    response = client_admin_api.post(
        url, {"ids": [str(mentor.user.id) for mentor in mentors_pending]}
    )

    response_get = client_admin_api.get(url)

    assert response_get.status_code == status.HTTP_200_OK
    assert response_get.json()["count"] == 0

    assert response.status_code == status.HTTP_200_OK
    assert [mentor.status == "APPROVED" for mentor in mentors_pending]


def test_mentor_approval_bad_request(client_admin_api):
    url = reverse("mentor-approve")

    response = client_admin_api.post(url, {"ids": ["fake_UUID"]})

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json() == {"ids": {"0": ["Must be a valid UUID."]}}


def test_book_schedule_as_member_fail(client_member_api, booking_datetime):
    url = reverse("mentor-booking-create")

    response = client_member_api.post(url, booking_datetime)

    assert response.status_code == status.HTTP_403_FORBIDDEN
    assert response.json() == {
        "detail": "You do not have permission to perform this action."
    }
