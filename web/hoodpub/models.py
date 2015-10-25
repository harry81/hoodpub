from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.db import models
from book.models import Book


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
    facebook_access_token = models.CharField(max_length=256)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username

    def set_access_token(self, token):
        self.facebook_access_token = token
        self.save(update_fields=['facebook_access_token'])

    def set_read(self, request, *args, **kwargs):
        book = Book.objects.get(isbn=request.data['isbn'])
        read = Read.objects.create(user=self.user, book=book)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Read(models.Model):
    user = models.ForeignKey(User, unique=True)
    book = models.ForeignKey(Book, unique=True)

    class Meta:
        unique_together = ('user', 'book',)

