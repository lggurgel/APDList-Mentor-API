from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_member"),
    ]

    operations = [
        migrations.CreateModel(
            name="BookingSchedule",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ("datetime", models.DateTimeField()),
                (
                    "member",
                    models.OneToOneField(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="booking_schedule",
                        to="api.member",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="mentor",
            name="booking",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="mentor",
                to="api.bookingschedule",
            ),
        ),
    ]
