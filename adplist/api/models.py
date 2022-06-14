import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(null=True, blank=True, max_length=100)


class MentorshipArea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=100)


class BaseUser(models.Model):

    EXPERTISES = (
        ("UI_UX", "UI/UX Design"),
        ("PRODUCT", "Product Design"),
        ("AI", "AI Design"),
    )

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    employer = title = models.CharField(max_length=100)
    title = title = models.CharField(max_length=100)
    expertise = ArrayField(models.CharField(max_length=50, choices=EXPERTISES))

    class Meta:
        abstract = True

    @property
    def location(self):
        return {"latitude": self.latitude, "longitude": self.longitude}


class Mentor(BaseUser):

    STATUS = (("PENDING", "Pending"), ("APPROVED", "Approved"))

    mentorship = models.ManyToManyField(MentorshipArea, related_name="mentorships")
    availability = ArrayField(models.DateTimeField(), blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="PENDING")
