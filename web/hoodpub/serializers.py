from rest_framework import serializers
from django.contrib.auth.models import User
from threadedcomments.models import ThreadedComment
from .models import UserProfile


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ('id', 'profile_picture', 'user', 'sns_id',
                  'first_name', 'last_name', 'name')

class ThreadedCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThreadedComment
