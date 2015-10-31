from rest_framework import serializers
from .models import Book
from hoodpub.models import Read, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('sns_id', 'first_name', 'last_name', 'name')


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

    is_read = serializers.SerializerMethodField('is_read_by_user')

    def is_read_by_user(self, obj):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous():
            return False
        else:
            profile = request.user.userprofile_set.all()[0]
            if profile.read.filter(book__isbn=obj.isbn).exists():
                return True
        return False

    class Meta:
        model = Book
