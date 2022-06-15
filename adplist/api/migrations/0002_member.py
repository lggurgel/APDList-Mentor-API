from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Member",
            fields=[
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("latitude", models.FloatField()),
                ("longitude", models.FloatField()),
                ("employer", models.CharField(max_length=100)),
                ("title", models.CharField(max_length=100)),
                (
                    "expertise",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(
                            choices=[
                                ("UI_UX", "UI/UX Design"),
                                ("PRODUCT", "Product Design"),
                                ("AI", "AI Design"),
                            ],
                            max_length=50,
                        ),
                        size=None,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
