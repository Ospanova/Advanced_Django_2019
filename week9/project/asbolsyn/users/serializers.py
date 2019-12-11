from rest_framework import serializers
from django.db import transaction

import logging

from users.models import MainUser, Profile

logger = logging.getLogger(__name__)


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'image_url')


class MainUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    # profile = ProfileSerializer(read_only=True)
    profile = ProfileSerializer()
    role = serializers.IntegerField(read_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'phone', 'password', 'role', 'profile')

    def create(self, validated_data):
        logger.info("something normal")
        with transaction.atomic():
            profile_data = validated_data.pop('profile')
            user = MainUser.objects.create_user(**validated_data)
            Profile.objects.create(user=user, **profile_data)
            return user
