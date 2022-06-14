from django.urls import path

from api.views import OnboardingMentorViewSet

urlpatterns = [
    path(
        "onboarding/mentor/",
        OnboardingMentorViewSet.as_view(),
        name="onboarding-mentor",
    ),
]
