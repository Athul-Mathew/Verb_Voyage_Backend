# Generated by Django 4.2.4 on 2023-11-03 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0005_transaction_duration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscriptionplan',
            name='edit_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
