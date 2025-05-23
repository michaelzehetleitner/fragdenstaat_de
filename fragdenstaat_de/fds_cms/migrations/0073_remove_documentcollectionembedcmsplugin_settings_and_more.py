# Generated by Django 4.2.16 on 2025-04-03 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("fds_cms", "0072_alter_datashowdatasettheme_banner_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="documentcollectionembedcmsplugin",
            name="settings",
        ),
        migrations.AddField(
            model_name="documentcollectionembedcmsplugin",
            name="deep_urls",
            field=models.BooleanField(
                blank=True,
                default=False,
                help_text="The embed will use deep URLs to link to the document pages and directories. Only enable this when no other embeds are on the same page.",
            ),
        ),
    ]
