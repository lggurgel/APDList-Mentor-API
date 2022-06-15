from django.contrib import admin

from api.models import Member, Mentor, MentorshipArea, BookingSchedule

admin.site.register(Member)
admin.site.register(Mentor)
admin.site.register(MentorshipArea)
admin.site.register(BookingSchedule)
