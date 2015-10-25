from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.db import models
from book.models import Book
from .utils import facebook_set_profile


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
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
    updated_time = models.DateTimeField(default=datetime.now, blank=True)
    verified = models.NullBooleanField(blank=True)


    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username
    
    def set_facebook_profile(self, request, *args, **kwargs):
        facebook_set_profile(request, *args, **kwargs)

    def set_read(self, request, *args, **kwargs):
        book = Book.objects.get(isbn=request.data['isbn'])
        read = Read.objects.create(user=self.user, book=book)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Read(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)

    class Meta:
        unique_together = ('user', 'book',)

    def __unicode__(self):
        return u'%s %s %s' % (self.user.username, self.book.title, self.book.isbn)
