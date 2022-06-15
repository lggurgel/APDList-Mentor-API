from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from api.filters import MentorFilterSet
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
    ordering = ("-created_at",)


class UserDetailAPIView(RetrieveUpdateAPIView):
    permission_classes = (UpdatePermission,)

    def get_queryset(self):
        id = self.kwargs["pk"]
        user = User.objects.get(id=id)

        if hasattr(user, "mentor"):
            return Mentor.objects.get(user_id=id)

        return Member.objects.get(user_id=id)

    def get_object(self):
        obj = self.get_queryset()
        self.check_object_permissions(self.request, obj)

        return obj

    def get_serializer_class(self):
        user = self.request.user

        if hasattr(user, "mentor"):
            return MentorSerializer

        return MemberSerializer


class OnboardingMentorViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class OnboardingMemberViewSet(CreateAPIView):
    queryset = Mentor.objects.all()
    serializer_class = MemberSerializer
