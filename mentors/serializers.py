
from rest_framework import serializers
from .models import *

class MentorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = (
            'id',
            'name',
            # 'user',
            'email',
            'age',
            'qualifications',
            'education',
            'image',
            'phoneNumber',
            'is_active',
        )

class MentorApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = '__all__'


class PlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Playlist
        fields = ['id', 'title', 'premium', 'user']

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Video
        fields = '__all__'       
        