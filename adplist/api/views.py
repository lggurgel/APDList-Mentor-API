from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveUpdateAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import IsAdminUser, SAFE_METHODS
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_400_BAD_REQUEST,
)

from api.filters import MentorFilterSet, MemberFilterSet
from api.models import Mentor, Member, User
from api.permissions import UpdatePermission
from api.serializers import (
    MentorSerializer,
    MemberSerializer,
    ReadOnlyMemberSerializer,
    ReadOnlyMentorSerializer,
    MentorApproveSerializer,
)
from api.use_case import MentorApproval


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


class MentorApproveViewSet(ListCreateAPIView):
    STATUS = "PENDING"
    queryset = Mentor.objects.filter(status=STATUS)
    permission_classes = (IsAdminUser,)

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return MentorSerializer
        return MentorApproveSerializer

    def post(self, request, *args, **kwargs):

        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                uc = MentorApproval(serializer.data["ids"])
                uc.execute()

                return Response(serializer.data, HTTP_200_OK)

        except Exception as e:
            return Response(
                "Mentors approval error: {}".format(e),
                HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
