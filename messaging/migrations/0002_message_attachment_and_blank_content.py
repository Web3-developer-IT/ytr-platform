# Generated manually for attachment uploads

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("messaging", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="content",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="message",
            name="attachment",
            field=models.FileField(
                blank=True,
                help_text="Optional image or short video shared in the thread.",
                null=True,
                upload_to="messaging/attachments/",
            ),
        ),
    ]
