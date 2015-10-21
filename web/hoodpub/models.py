from datetime import datetime
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)


class Book(models.Model):
    category = models.CharField(max_length=168)
    sale_yn = models.CharField(max_length=16)
    barcode = models.CharField(max_length=168)
    isbn = models.CharField(max_length=168)
    isbn13 = models.CharField(max_length=168)
    cover_s_url = models.CharField(max_length=512)
    author = models.CharField(max_length=168)
    author_t = models.CharField(max_length=168)
    sale_price = models.CharField(max_length=168)
    title = models.CharField(max_length=168)
    translator = models.CharField(max_length=168)
    link = models.CharField(max_length=168)
    etc_author = models.CharField(max_length=128)
    pub_nm = models.CharField(max_length=128)
    list_price = models.CharField(max_length=168)
    ebook_barcode = models.CharField(max_length=168)
    cover_l_url = models.CharField(max_length=512)
    pub_date = models.DateTimeField(default=datetime.now, blank=True)
    status_des = models.CharField(max_length=168)
    description = models.TextField()

    def __unicode__(self):
        return u'%d %s' % (self.pk, self.title)
