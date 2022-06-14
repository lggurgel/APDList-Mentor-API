from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.filters import MentorFilterSet
from api.models import Mentor
from api.serializers import MentorSerializer


class MentorViewSet(ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
    filterset_class = MentorFilterSet
    ordering = ("-updated_at",)


class OnboardingMentorViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer
