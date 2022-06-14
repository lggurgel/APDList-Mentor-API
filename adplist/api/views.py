from django.contrib.auth import get_user_model
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.filters import MentorFilterSet
from api.models import Mentor, Member
from api.serializers import (
    MentorSerializer,
    MemberSerializer,
    ReadOnlyMemberSerializer,
    ReadOnlyMentorSerializer,
)


class MentorViewSet(ListAPIView):
    queryset = Mentor.objects.all()
    serializer_class = ReadOnlyMentorSerializer
    filterset_class = MentorFilterSet
    ordering = ("-created_at",)


class MemberViewSet(ListAPIView):
    queryset = Member.objects.all()
    serializer_class = ReadOnlyMemberSerializer
    ordering = ("-created_at",)


class OnboardingMentorViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class OnboardingMemberViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MemberSerializer
