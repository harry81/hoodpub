from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.db import models


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    profile_picture = models.ImageField(upload_to='thumbpath', blank=True)
    facebook_access_token = models.CharField(max_length=128)


    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

post_save.connect(create_user_profile, sender=User)
