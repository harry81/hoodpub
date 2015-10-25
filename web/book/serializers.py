from .models import Book
from rest_framework import serializers


class BookSerializer(serializers.ModelSerializer):
    total_read = serializers.IntegerField(
        source='read_set.count',
        read_only=True)

    class Meta:
        model = Book
