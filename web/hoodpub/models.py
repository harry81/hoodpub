from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.db import models
from book.models import Book
from .utils import facebook_set_profile


class Read(models.Model):
    book = models.ForeignKey(Book)
    created_at = models.DateTimeField(default=datetime.now, blank=True)

    def __unicode__(self):
        return u'%s %s' % (
            self.book.title, self.book.isbn)


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    read = models.ManyToManyField(Read)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
    sns_id = models.CharField(max_length=256, blank=True)
    facebook_access_token = models.CharField(max_length=256, blank=True)
    birthday = models.DateField(default=datetime.now, blank=True)
    email = models.CharField(max_length=64, blank=True)
    first_name = models.CharField(max_length=32, blank=True)
    gender = models.CharField(max_length=8, blank=True)
    last_name = models.CharField(max_length=32, blank=True)
    link = models.CharField(max_length=128, blank=True)
    locale = models.CharField(max_length=128, blank=True)
    name = models.CharField(max_length=32, blank=True)
    timezone = models.IntegerField(blank=True, default=0)
    updated_at = models.DateTimeField(default=datetime.now, blank=True)
    verified = models.NullBooleanField(blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

    def set_facebook_profile(self, request, *args, **kwargs):
        facebook_set_profile(request, *args, **kwargs)

    def set_read(self, request, *args, **kwargs):
        isbn = isbn=request.data['isbn']
        if not self.read.filter(book__isbn=isbn).exists():
            book = Book.objects.get(isbn=isbn)
            self.read.add(Read.objects.create(book=book))
            return {
                'success' : True,
                'book' : book.isbn
            }
        else:
            return {'success': False }


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
