from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from api.models import Member, Mentor


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

    def get_location(self, obj):
        return {"latitude": obj.latitude, "longitude": obj.longitude}


class ReadOnlyMemberSerializer(BaseReadOnlyUserSerializer):
    class Meta:
        model = Member
        exclude = ("longitude", "latitude")


class ReadOnlyMentorSerializer(BaseReadOnlyUserSerializer):
    class Meta:
        model = Mentor
        exclude = ("longitude", "latitude")
