# Generated by Django 5.0.7 on 2024-09-13 16:12

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("election", "0002_auca_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="candidate",
            name="email",
            field=models.EmailField(
                default=datetime.datetime(
                    2024, 9, 13, 16, 12, 32, 560865, tzinfo=datetime.timezone.utc
                ),
                max_length=254,
                unique=True,
            ),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name="candidate",
            unique_together={("email", "election")},
        ),
        migrations.AlterUniqueTogether(
            name="vote",
            unique_together={("voter_email", "election")},
        ),
    ]
