# Generated by Django 4.2 on 2023-06-19 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="image",
            field=models.ImageField(null=True, upload_to="userImages/"),
        ),
    ]
