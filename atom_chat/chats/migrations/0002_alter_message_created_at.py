# Generated by Django 5.1.2 on 2024-10-23 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("chats", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="message",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
