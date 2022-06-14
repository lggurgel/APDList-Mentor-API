from django.urls import path

from api.views import MentorViewSet, OnboardingMentorViewSet

urlpatterns = [
    path("mentor/list", MentorViewSet.as_view(), name="mentor-list"),
    path(
        "onboarding/mentor/",
        OnboardingMentorViewSet.as_view(),
        name="onboarding-mentor",
    ),
]
