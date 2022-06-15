from django.urls import path

from api.views import (
    MentorViewSet,
    MemberViewSet,
    UserDetailAPIView,
    OnboardingMentorViewSet,
    OnboardingMemberViewSet,
)

urlpatterns = [
    path("user/mentor/", MentorViewSet.as_view(), name="mentor-list"),
    path("user/member/", MemberViewSet.as_view(), name="member-list"),
    path("user/<uuid:pk>/", UserDetailAPIView.as_view(), name="user-detail"),
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
