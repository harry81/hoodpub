from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from social.apps.django_app.default.models import UserSocialAuth
from social.apps.django_app.default.admin import UserSocialAuthOption

from .models import UserProfile, Read


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'profile'
    fields = ['sns_id', 'name', 'link', 'gender']


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ReadAdmin(admin.ModelAdmin):
    def userprofile(self, obj):
        if obj.userprofile_set.all().exists():
            return obj.userprofile_set.all()[0]
        return ''

    list_display = ('book', 'userprofile', 'created_at')


admin.site.register(Read, ReadAdmin)


class CustomUserSocialAuthOption(UserSocialAuthOption):
    def uid_picture(self, instance):
        return '<a href="https://www.facebook.com/{0}" target="_new">\
        <img src="https://graph.facebook.com/{0}/picture/"></a>'.format(
            instance.uid)
    uid_picture.allow_tags = True

    list_display = ('id', 'uid_picture', 'user', 'provider', 'uid')

admin.site.unregister(UserSocialAuth)
admin.site.register(UserSocialAuth, CustomUserSocialAuthOption)
