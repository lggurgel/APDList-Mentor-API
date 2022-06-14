from django.urls import path

from api.views import (
    MentorViewSet,
    MemberViewSet,
    OnboardingMentorViewSet,
    OnboardingMemberViewSet,
)

urlpatterns = [
    path("mentor/list", MentorViewSet.as_view(), name="mentor-list"),
    path("member/list", MemberViewSet.as_view(), name="member-list"),
    path(
        "onboarding/mentor/",
        OnboardingMentorViewSet.as_view(),
        name="onboarding-mentor",
    ),
    path(
        "onboarding/member/",
        OnboardingMemberViewSet.as_view(),
        name="onboarding-member",
    ),
]
