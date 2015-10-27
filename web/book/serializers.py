from rest_framework import serializers
from .models import Book
from hoodpub.models import Read, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('sns_id', )


class ReadSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(
        many=True,
        source='userprofile_set',
        read_only=True)

    class Meta:
        model = Read
        fields = ('user', )


class BookSerializer(serializers.ModelSerializer):
    reads = ReadSerializer(many=True,
                           source='read_set',
                           read_only=True)
    total_read = serializers.IntegerField(
        source='read_set.count',
        read_only=True)

    class Meta:
        model = Book
