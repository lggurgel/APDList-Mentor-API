from django_filters import rest_framework as filters

from api.models import Mentor, Member


class ChoiceInFilter(filters.BaseInFilter, filters.ChoiceFilter):
    pass


class MentorFilterSet(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id", help_text="Filter by mentor id")
    status = ChoiceInFilter(
        field_name="status",
        help_text="Filter by status",
        choices=Mentor.STATUS,
    )

    class Meta:
        model = Mentor
        fields = ["id", "status"]


class MemberFilterSet(filters.FilterSet):
    id = filters.UUIDFilter(field_name="id", help_text="Filter by member id")
    expertise = ChoiceInFilter(
        field_name="expertise",
        help_text="Filter by expertise",
        choices=Member.EXPERTISES,
        lookup_expr="contains",
    )

    class Meta:
        model = Member
        fields = ["id", "expertise"]
