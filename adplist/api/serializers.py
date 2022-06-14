from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

from api.models import Mentor


class MentorSerializer(ModelSerializer):
    class Meta:
        model = Mentor
        fields = "__all__"
