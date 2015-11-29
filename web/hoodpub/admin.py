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
    fields = ['sns_id', 'name', 'link', 'gender',
              'facebook_access_token']


class UserAdmin(UserAdmin):
    inlines = (UserProfileInline, )
    ordering = ('-date_joined',)
    search_fields = ['username', ]

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class ReadAdmin(admin.ModelAdmin):
    raw_id_fields = ('book',)

    def userprofile(self, obj):
        if obj.userprofile_set.all().exists():
            return obj.userprofile_set.all()[0]
        return ''

    list_display = ('book', 'userprofile', 'created_at')
    search_fields = ['book__title', 'userprofile__user__username']

    def update_description(self, request, queryset):
        for ele in queryset:
            ele.book.get_description()
    update_description.short_description = "Update the descriptioin"\
                                           " of each book"

    actions = ['update_description']

admin.site.register(Read, ReadAdmin)


class CustomUserSocialAuthOption(UserSocialAuthOption):
    def uid_picture(self, instance):
        return '<a href="https://www.facebook.com/{0}" target="_new">\
        <img src="https://graph.facebook.com/{0}/picture/"></a>'\
        .format(instance.uid)
    uid_picture.allow_tags = True

    def url_facebook_get(self, instance):
        return "curl https://graph.facebook.com/me/hoodpub:read?access_token=%s"\
               "&method=GET | python -m json.tool" %\
               instance.access_token

    def url_facebook_post(self, instance):
        return "curl https://graph.facebook.com/me/hoodpub:read?access_token=%s" \
               "&method=POST&book=%s" % (
                   instance.access_token,
                   'https://www.hoodpub.com/book/8954608647/')

    list_display = ('id', 'uid_picture', 'user', 'provider', 'uid',)
    readonly_fields = ('url_facebook_get', 'url_facebook_post')

admin.site.unregister(UserSocialAuth)
admin.site.register(UserSocialAuth, CustomUserSocialAuthOption)
