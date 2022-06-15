from typing import Any
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.filters import MentorFilterSet, MemberFilterSet
from api.models import Mentor, Member, User
from api.permissions import UpdatePermission
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
    filterset_class = MemberFilterSet
    ordering = ("-created_at",)


class UserDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = (UpdatePermission,)
    user = None

    def get_user(self, id):
        if not self.user:
            self.user = User.objects.get(id=id)
        return self.user

    def get_queryset(self):
        id = self.kwargs["pk"]

        if hasattr(self.get_user(id), "mentor"):
            return Mentor.objects.get(user_id=self.user.id)

        return Member.objects.get(user_id=id)

    def get_object(self):
        obj = self.get_queryset()
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        id = self.kwargs["pk"]

        if hasattr(self.get_user(id), "mentor"):
            return MentorSerializer

        return MemberSerializer


class OnboardingMentorViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class OnboardingMemberViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MemberSerializer
