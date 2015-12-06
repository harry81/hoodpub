from rest_framework import serializers
from django.contrib.contenttypes.models import ContentType
from threadedcomments.models import ThreadedComment

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


class BookListSerializer(serializers.ModelSerializer):
    reads = ReadSerializer(many=True,
                           source='read_set',
                           read_only=True)

    is_read = serializers.SerializerMethodField('is_read_by_user')
    onesentense = serializers.SerializerMethodField()

    def is_read_by_user(self, obj):
        request = self.context.get('request', None)
        if request is None or request.user.is_anonymous():
            return False
        else:
            profile = request.user.userprofile_set.all()[0]
            if profile.read.filter(book__isbn=obj.isbn).exists():
                return True
        return False

    def get_onesentense(self, obj):
        comments = ThreadedComment.objects.values(
            'id', 'object_pk', 'user_name', 'user_url', 'user_id', 'comment').\
            filter(
                content_type=ContentType.objects.get(
                    app_label="book", model="book"),
            object_pk=obj.pk).order_by('-submit_date')[:5]

        return list(comments)

    class Meta:
        model = Book
        fields = ('isbn', 'reads', 'category', 'cover_s_url', 'author',
                  'link', 'cover_l_url', 'is_read', 'title', 'pub_nm',
                  'onesentense')
