from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.tokens import RefreshToken

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = '__all__'

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user
        

    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAccount
        fields = ['id', 'email', 'name', 'profile_image', 'is_active', 'is_staff', 'is_admin', 'is_online','is_premium']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['profile_image'] = instance.get_profile_image_url()  # Assuming you have a method to get the image URL
        return representation

    # def update(self, instance, validated_data):
    #     validated_data.pop('profile_image', None)  # Assuming you want to exclude profile_image from updates
    #     return super().update(instance, validated_data)