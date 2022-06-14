import factory

from api.models import User, Mentor, Member, MentorshipArea


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    id = factory.Faker("uuid4")
    name = factory.Faker("name")


class MentorshipAreaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = MentorshipArea

    id = factory.Faker("uuid4")
    title = ""


class MentorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Mentor

    user = factory.SubFactory(UserFactory)
    latitude = -15.7792
    longitude = -47.9341
    employer = "Company"
    title = "Senior Developer"
    expertise = ["UI_UX", "PRODUCT"]
    mentorship = factory.RelatedFactoryList(MentorshipAreaFactory)
    status = "PENDING"


class MemberFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Member

    user = factory.SubFactory(UserFactory)
    latitude = -15.7792
    longitude = -47.9341
    employer = "Company"
    title = "Junior Developer"
    expertise = ["AI"]
