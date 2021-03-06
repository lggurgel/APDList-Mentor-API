from typing import Union
from rest_framework.serializers import (
    ModelSerializer,
    SerializerMethodField,
    Serializer,
    ListField,
    UUIDField,
    DateTimeField,
)

from api.models import BookingSchedule, Member, Mentor


class MentorSerializer(ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"


class MemberSerializer(ModelSerializer):
    class Meta:
        model = Member
        fields = "__all__"


class BaseReadOnlyUserSerializer(ModelSerializer):
    location = SerializerMethodField(read_only=True)

    def get_location(self, obj: Union[Mentor, Member]):
        return obj.location


class ReadOnlyMemberSerializer(BaseReadOnlyUserSerializer):
    class Meta:
        model = Member
        exclude = ("longitude", "latitude")


class ReadOnlyMentorSerializer(BaseReadOnlyUserSerializer):
    class Meta:
        model = Mentor
        exclude = ("longitude", "latitude")


class MentorApproveSerializer(Serializer):
    ids = ListField(child=UUIDField())


class BookingScheduleRegisterSerializer(Serializer):
    datetimes = ListField(child=DateTimeField())
