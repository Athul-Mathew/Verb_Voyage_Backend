# Generated by Django 4.2.4 on 2023-10-04 16:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mentors', '0006_remove_playlist_videos_alter_video_playlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='playlist',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='videos', to='mentors.playlist'),
        ),
    ]
