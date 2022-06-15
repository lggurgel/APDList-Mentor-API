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
from api.models import Mentor, Member, User, BookingSchedule
from api.permissions import UpdatePermission, IsMentorPermission
from api.serializers import (
    MentorSerializer,
    MemberSerializer,
    ReadOnlyMemberSerializer,
    ReadOnlyMentorSerializer,
    MentorApproveSerializer,
    BookingScheduleRegisterSerializer,
)
from api.use_case import MentorApproval, BookScheduleAssociation


class MentorViewSet(ListAPIView):
    """API endpoint that allows mentors to be listed."""

    queryset = Mentor.objects.all()
    serializer_class = ReadOnlyMentorSerializer
    filterset_class = MentorFilterSet
    ordering = ("-created_at",)


class MemberViewSet(ListAPIView):
    """API endpoint that allows members to be listed."""

    queryset = Member.objects.all()
    serializer_class = ReadOnlyMemberSerializer
    filterset_class = MemberFilterSet
    ordering = ("-created_at",)


class UserDetailAPIView(RetrieveUpdateAPIView):
    """API endpoint that allows users to be viewed or edited."""

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
    """API endpoint that allows users to be registered as Mentor."""

    queryset = Mentor.objects.all()
    serializer_class = MentorSerializer


class OnboardingMemberViewSet(CreateAPIView):
    """API endpoint that allows users to be registered as Member."""

    queryset = Mentor.objects.all()
    serializer_class = MemberSerializer


class MentorApproveViewSet(ListCreateAPIView):
    """API endpoint that allows Administrators approve PENDING Mentors."""

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


class BokkingScheduleMentorCreateViewSet(CreateAPIView):
    """API endpoint that allows mentor to register their own availabilities for mentorship."""

    queryset = BookingSchedule.objects.all()
    serializer_class = BookingScheduleRegisterSerializer
    permission_classes = (IsMentorPermission,)

    def post(self, request, *args, **kwargs):

        obj = self.get_queryset()
        self.check_object_permissions(self.request, obj)

        try:
            serializer = self.get_serializer(data=request.data)

            if serializer.is_valid():
                uc = BookScheduleAssociation()
                uc.execute()

                return Response(serializer.data, HTTP_200_OK)

        except Exception as e:
            return Response(
                "Booking Scheduler Association Failed: {}".format(e),
                HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return Response(serializer.errors, HTTP_400_BAD_REQUEST)
