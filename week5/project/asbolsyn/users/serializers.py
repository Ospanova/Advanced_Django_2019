from rest_framework import serializers
from django.db import transaction

from users.models import MainUser, Profile


class ProfileSerializer(serializers.ModelSerializer):
    image_url = serializers.CharField(read_only=True)
    image = serializers.FileField(read_only=True)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'image_url', 'image')

    def create(self, validated_data):
        print(validated_data.user)


class MainUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # profile = ProfileSerializer(read_only=True)
    # profile = ProfileSerializer()
    profile = serializers.JSONField()
    role = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'phone', 'password', 'role', 'profile')

    def create(self, validated_data):
        print(self.data.image)
        with transaction.atomic():
            profile_data = validated_data.pop('profile')
            user = MainUser.objects.create_user(**validated_data)
            Profile.objects.create(user=user, **profile_data)
            return user
