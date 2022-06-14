from django_filters import rest_framework as filters

from api.models import Mentor


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
