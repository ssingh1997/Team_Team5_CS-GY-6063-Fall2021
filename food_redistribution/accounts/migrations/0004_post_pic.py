# Generated by Django 3.2.7 on 2021-10-31 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_auto_20211027_0029"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="pic",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
