

from rest_framework import serializers
from .models import UserCollection

class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField(max_length=100)
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserCollection(
            name=validated_data['name'],
            email=validated_data['email']
        )
        user.password = validated_data['password']
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    # def validate(self, data):
    #     return data

class SearchHistorySerializer(serializers.Serializer):
    timestamp = serializers.DateTimeField()
    city = serializers.CharField()
    weather_details = serializers.CharField()