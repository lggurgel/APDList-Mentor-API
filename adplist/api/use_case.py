import uuid
from typing import List, Union

from api.models import Mentor


class MentorApproval:
    def __init__(self, ids: List[Union[uuid.uuid4, str]]) -> None:
        self.ids = ids

    def execute(self) -> None:
        mentors_to_approval = Mentor.objects.filter(user__id__in=self.ids)

        for mentor in mentors_to_approval:
            mentor.status = "APPROVED"
            mentor.save(update_fields=["status"])


class BookScheduleAssociation:
    def __init__(self) -> None:
        pass

    def execute(self) -> None:
        pass
