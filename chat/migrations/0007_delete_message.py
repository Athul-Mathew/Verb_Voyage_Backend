# Generated by Django 4.2.4 on 2023-10-13 16:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_alter_message_options_remove_message_username_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]